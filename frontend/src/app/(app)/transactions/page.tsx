"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { TrendingUp, TrendingDown, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TransactionForm } from "@/components/forms/transaction-form";
import {
  getTransactions,
  createTransaction,
  deleteTransaction,
} from "@/services/transactions";
import { getCategories } from "@/services/categories";
import { formatCurrency, formatDate } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { TransactionType } from "@/types";

export default function TransactionsPage() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [formType, setFormType] = useState<TransactionType>("income");
  const queryClient = useQueryClient();

  const { data: transactions, isLoading } = useQuery({
    queryKey: ["transactions"],
    queryFn: () => getTransactions(),
  });

  const { data: categories } = useQuery({
    queryKey: ["categories"],
    queryFn: getCategories,
  });

  const invalidateAllTransactionQueries = () => {
    queryClient.invalidateQueries({ queryKey: ["transactions"] });
    queryClient.invalidateQueries({ queryKey: ["transactionSummary"] });
    queryClient.invalidateQueries({ queryKey: ["recentTransactions"] });
    queryClient.invalidateQueries({ queryKey: ["monthlyData"] });
  };

  const createMutation = useMutation({
    mutationFn: createTransaction,
    onSuccess: invalidateAllTransactionQueries,
  });

  const deleteMutation = useMutation({
    mutationFn: deleteTransaction,
    onSuccess: invalidateAllTransactionQueries,
  });

  const handleOpenForm = (type: TransactionType) => {
    setFormType(type);
    setIsFormOpen(true);
  };

  const handleSubmit = async (data: any) => {
    await createMutation.mutateAsync(data);
  };

  const handleDelete = async (id: string) => {
    if (confirm("Tem certeza que deseja excluir esta transação?")) {
      await deleteMutation.mutateAsync(id);
    }
  };

  const getCategoryName = (categoryId?: string) => {
    if (!categoryId || !categories) return "Sem categoria";
    const category = categories.find((c) => c.id === categoryId);
    return category?.name ?? "Sem categoria";
  };

  const incomeTransactions = transactions?.filter((t) => t.type === "income") ?? [];
  const expenseTransactions = transactions?.filter((t) => t.type === "expense") ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Movimentações</h2>
        <p className="text-muted-foreground">
          Registre suas entradas e saídas de dinheiro
        </p>
      </div>

      {/* Botões de Ação */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card
          className="cursor-pointer border-green-500/20 hover:border-green-500/50 transition-colors"
          onClick={() => handleOpenForm("income")}
        >
          <CardContent className="flex items-center gap-4 p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-500/10">
              <TrendingUp className="h-6 w-6 text-green-500" />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Adicionar Entrada</h3>
              <p className="text-sm text-muted-foreground">
                Salário, freelance, vendas, etc.
              </p>
            </div>
          </CardContent>
        </Card>

        <Card
          className="cursor-pointer border-red-500/20 hover:border-red-500/50 transition-colors"
          onClick={() => handleOpenForm("expense")}
        >
          <CardContent className="flex items-center gap-4 p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-500/10">
              <TrendingDown className="h-6 w-6 text-red-500" />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Adicionar Saída</h3>
              <p className="text-sm text-muted-foreground">
                Contas, compras, despesas, etc.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Transações */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Entradas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-500">
              <TrendingUp className="h-5 w-5" />
              Entradas
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="h-6 w-6 animate-spin rounded-full border-2 border-green-500 border-t-transparent" />
              </div>
            ) : incomeTransactions.length === 0 ? (
              <p className="text-center text-muted-foreground py-4 text-sm">
                Nenhuma entrada registrada
              </p>
            ) : (
              <div className="space-y-3">
                {incomeTransactions.map((transaction) => (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between rounded-lg border border-green-500/20 p-3"
                  >
                    <div className="space-y-0.5">
                      <p className="font-medium text-sm">{transaction.description}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatDate(transaction.date)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-500 font-semibold">
                        +{formatCurrency(Number(transaction.amount))}
                      </span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() => handleDelete(transaction.id)}
                      >
                        <Trash2 className="h-4 w-4 text-muted-foreground hover:text-destructive" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Saídas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-500">
              <TrendingDown className="h-5 w-5" />
              Saídas
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center py-8">
                <div className="h-6 w-6 animate-spin rounded-full border-2 border-red-500 border-t-transparent" />
              </div>
            ) : expenseTransactions.length === 0 ? (
              <p className="text-center text-muted-foreground py-4 text-sm">
                Nenhuma saída registrada
              </p>
            ) : (
              <div className="space-y-3">
                {expenseTransactions.map((transaction) => (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between rounded-lg border border-red-500/20 p-3"
                  >
                    <div className="space-y-0.5">
                      <p className="font-medium text-sm">{transaction.description}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatDate(transaction.date)} • {getCategoryName(transaction.category_id)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-red-500 font-semibold">
                        -{formatCurrency(Number(transaction.amount))}
                      </span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() => handleDelete(transaction.id)}
                      >
                        <Trash2 className="h-4 w-4 text-muted-foreground hover:text-destructive" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <TransactionForm
        open={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onSubmit={handleSubmit}
        categories={categories ?? []}
        defaultValues={{ type: formType }}
      />
    </div>
  );
}
