"use client";

import { useQuery } from "@tanstack/react-query";
import {
  TrendingUp,
  TrendingDown,
  Wallet,
  ArrowLeftRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { OverviewChart } from "@/components/charts/overview-chart";
import { getTransactionSummary, getTransactions, getMonthlyData } from "@/services/transactions";
import { formatCurrency, formatDate } from "@/lib/utils";
import { cn } from "@/lib/utils";

export default function DashboardPage() {
  const { data: summary } = useQuery({
    queryKey: ["transactionSummary"],
    queryFn: () => getTransactionSummary(),
  });

  const { data: recentTransactions } = useQuery({
    queryKey: ["recentTransactions"],
    queryFn: () => getTransactions({ limit: 5 }),
  });

  const { data: monthlyData } = useQuery({
    queryKey: ["monthlyData"],
    queryFn: () => getMonthlyData(),
  });

  const stats = [
    {
      title: "Saldo Total",
      value: summary?.balance ?? 0,
      icon: Wallet,
      color: "text-foreground",
    },
    {
      title: "Receitas",
      value: summary?.total_income ?? 0,
      icon: TrendingUp,
      color: "text-green-500",
    },
    {
      title: "Despesas",
      value: summary?.total_expense ?? 0,
      icon: TrendingDown,
      color: "text-red-500",
    },
    {
      title: "Transações",
      value: summary?.transaction_count ?? 0,
      icon: ArrowLeftRight,
      color: "text-foreground",
      isCount: true,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Visão geral das suas finanças
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className={cn("h-4 w-4", stat.color)} />
            </CardHeader>
            <CardContent>
              <div className={cn("text-2xl font-bold", stat.color)}>
                {stat.isCount
                  ? stat.value
                  : formatCurrency(Number(stat.value))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <OverviewChart data={monthlyData ?? []} />

        <Card>
          <CardHeader>
            <CardTitle>Movimentações Recentes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentTransactions?.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  Nenhuma movimentação encontrada
                </p>
              ) : (
                recentTransactions?.map((transaction) => (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between"
                  >
                    <div className="space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {transaction.description}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {formatDate(transaction.date)}
                      </p>
                    </div>
                    <div
                      className={cn(
                        "text-sm font-medium",
                        transaction.type === "income"
                          ? "text-green-500"
                          : "text-red-500"
                      )}
                    >
                      {transaction.type === "income" ? "+" : "-"}
                      {formatCurrency(Number(transaction.amount))}
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
