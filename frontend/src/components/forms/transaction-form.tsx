"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { TrendingUp, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import type { Category, TransactionType } from "@/types";

const transactionSchema = z.object({
  description: z.string().min(1, "Descrição é obrigatória"),
  amount: z.coerce.number().positive("Valor deve ser positivo"),
  type: z.enum(["income", "expense"]),
  category_id: z.string().optional(),
  date: z.string().optional(),
  notes: z.string().optional(),
});

type TransactionFormData = z.infer<typeof transactionSchema>;

interface TransactionFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: TransactionFormData) => Promise<void>;
  categories: Category[];
  defaultValues?: Partial<TransactionFormData>;
}

export function TransactionForm({
  open,
  onClose,
  onSubmit,
  categories,
  defaultValues,
}: TransactionFormProps) {
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors },
  } = useForm<TransactionFormData>({
    resolver: zodResolver(transactionSchema),
    defaultValues: {
      type: "expense",
      date: new Date().toISOString().split("T")[0],
      ...defaultValues,
    },
  });

  const type = watch("type");

  // Atualiza o tipo quando defaultValues mudar
  useEffect(() => {
    if (defaultValues?.type) {
      setValue("type", defaultValues.type);
    }
  }, [defaultValues?.type, setValue]);

  const handleFormSubmit = async (data: TransactionFormData) => {
    setIsLoading(true);
    try {
      await onSubmit(data);
      reset();
      onClose();
    } finally {
      setIsLoading(false);
    }
  };

  const isIncome = type === "income";

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {isIncome ? (
              <>
                <TrendingUp className="h-5 w-5 text-green-500" />
                <span>Nova Entrada</span>
              </>
            ) : (
              <>
                <TrendingDown className="h-5 w-5 text-red-500" />
                <span>Nova Saída</span>
              </>
            )}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="description">
              {isIncome ? "Origem do dinheiro" : "Descrição da despesa"}
            </Label>
            <Input
              id="description"
              {...register("description")}
              placeholder={isIncome ? "Ex: Salário, Freelance" : "Ex: Supermercado, Aluguel"}
            />
            {errors.description && (
              <p className="text-sm text-destructive">
                {errors.description.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="amount">Valor (R$)</Label>
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

          {/* Campo de tipo oculto, mas ainda no form */}
          <input type="hidden" {...register("type")} />

          {!isIncome && (
            <div className="space-y-2">
              <Label>Categoria</Label>
              <Select onValueChange={(v) => setValue("category_id", v)}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione uma categoria" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category.id} value={category.id}>
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="date">Data</Label>
            <Input id="date" type="date" {...register("date")} />
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Observações (opcional)</Label>
            <Input
              id="notes"
              {...register("notes")}
              placeholder="Anotações adicionais"
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={isLoading}
              className={isIncome ? "bg-green-600 hover:bg-green-700" : "bg-red-600 hover:bg-red-700"}
            >
              {isLoading ? "Salvando..." : isIncome ? "Adicionar Entrada" : "Adicionar Saída"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
