"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Trash2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getBudgets, createBudget, deleteBudget } from "@/services/budgets";
import { getCategories } from "@/services/categories";
import { formatCurrency, formatPercent } from "@/lib/utils";
import { cn } from "@/lib/utils";

const currentDate = new Date();
const currentMonth = currentDate.getMonth() + 1;
const currentYear = currentDate.getFullYear();

const budgetSchema = z.object({
  category_id: z.string().min(1, "Categoria é obrigatória"),
  amount: z.coerce.number().positive("Valor deve ser positivo"),
});

type BudgetFormData = z.infer<typeof budgetSchema>;

export default function BudgetsPage() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const queryClient = useQueryClient();

  const { data: budgets, isLoading: isLoadingBudgets } = useQuery({
    queryKey: ["budgets", currentMonth, currentYear],
    queryFn: () => getBudgets(currentMonth, currentYear),
  });

  const { data: categories } = useQuery({
    queryKey: ["categories"],
    queryFn: getCategories,
  });

  const {
    register,
    handleSubmit,
    setValue,
    reset,
    formState: { errors },
  } = useForm<BudgetFormData>({
    resolver: zodResolver(budgetSchema),
  });

  const createMutation = useMutation({
    mutationFn: (data: BudgetFormData) =>
      createBudget({
        ...data,
        month: currentMonth,
        year: currentYear,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["budgets"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteBudget,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["budgets"] });
    },
  });

  const handleFormSubmit = async (data: BudgetFormData) => {
    setIsLoading(true);
    try {
      await createMutation.mutateAsync(data);
      reset();
      setIsFormOpen(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("Tem certeza que deseja excluir este orçamento?")) {
      await deleteMutation.mutateAsync(id);
    }
  };

  const getCategoryName = (categoryId: string) => {
    if (!categories) return "Categoria";
    const category = categories.find((c) => c.id === categoryId);
    return category?.name ?? "Categoria";
  };

  const getCategoryColor = (categoryId: string) => {
    if (!categories) return "#6366f1";
    const category = categories.find((c) => c.id === categoryId);
    return category?.color ?? "#6366f1";
  };

  const monthNames = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Orçamentos</h2>
          <p className="text-muted-foreground">
            {monthNames[currentMonth - 1]} de {currentYear}
          </p>
        </div>
        <Button onClick={() => setIsFormOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Novo Orçamento
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {isLoadingBudgets ? (
          <div className="col-span-full flex justify-center py-8">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          </div>
        ) : budgets?.length === 0 ? (
          <Card className="col-span-full">
            <CardContent className="py-8 text-center text-muted-foreground">
              Nenhum orçamento encontrado. Clique em &quot;Novo Orçamento&quot; para
              começar.
            </CardContent>
          </Card>
        ) : (
          budgets?.map((budget) => {
            const percentUsed = budget.percentage_used ?? 0;
            const isExceeded = percentUsed > 100;

            return (
              <Card key={budget.id}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <div className="flex items-center gap-3">
                    <div
                      className="h-3 w-3 rounded-full"
                      style={{ backgroundColor: getCategoryColor(budget.category_id) }}
                    />
                    <CardTitle className="text-base font-medium">
                      {getCategoryName(budget.category_id)}
                    </CardTitle>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(budget.id)}
                  >
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">
                      Gasto: {formatCurrency(Number(budget.spent ?? 0))}
                    </span>
                    <span className="font-medium">
                      Limite: {formatCurrency(Number(budget.amount))}
                    </span>
                  </div>

                  <Progress
                    value={Math.min(percentUsed, 100)}
                    className={cn(
                      "h-2",
                      isExceeded && "[&>div]:bg-red-500"
                    )}
                  />

                  <div className="flex justify-between text-sm">
                    <span
                      className={cn(
                        isExceeded ? "text-red-500" : "text-muted-foreground"
                      )}
                    >
                      {formatPercent(percentUsed)} utilizado
                    </span>
                    <span
                      className={cn(
                        "font-medium",
                        isExceeded ? "text-red-500" : "text-green-500"
                      )}
                    >
                      {isExceeded
                        ? `Excedido em ${formatCurrency(Math.abs(Number(budget.remaining ?? 0)))}`
                        : `Restante: ${formatCurrency(Number(budget.remaining ?? 0))}`}
                    </span>
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Novo Orçamento</DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
            <div className="space-y-2">
              <Label>Categoria</Label>
              <Select onValueChange={(v) => setValue("category_id", v)}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione uma categoria" />
                </SelectTrigger>
                <SelectContent>
                  {categories?.map((category) => (
                    <SelectItem key={category.id} value={category.id}>
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.category_id && (
                <p className="text-sm text-destructive">
                  {errors.category_id.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="amount">Valor do Orçamento</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                {...register("amount")}
                placeholder="0,00"
              />
              {errors.amount && (
                <p className="text-sm text-destructive">{errors.amount.message}</p>
              )}
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsFormOpen(false)}
              >
                Cancelar
              </Button>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Salvando..." : "Salvar"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
