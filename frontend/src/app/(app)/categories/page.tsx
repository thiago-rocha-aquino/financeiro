"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  getCategories,
  createCategory,
  deleteCategory,
} from "@/services/categories";

const categorySchema = z.object({
  name: z.string().min(1, "Nome é obrigatório"),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/, "Cor inválida"),
});

type CategoryFormData = z.infer<typeof categorySchema>;

export default function CategoriesPage() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const queryClient = useQueryClient();

  const { data: categories, isLoading: isLoadingCategories } = useQuery({
    queryKey: ["categories"],
    queryFn: getCategories,
  });

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors },
  } = useForm<CategoryFormData>({
    resolver: zodResolver(categorySchema),
    defaultValues: {
      color: "#6366f1",
    },
  });

  const colorValue = watch("color");

  const createMutation = useMutation({
    mutationFn: createCategory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categories"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCategory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categories"] });
    },
  });

  const handleFormSubmit = async (data: CategoryFormData) => {
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
    if (confirm("Tem certeza que deseja excluir esta categoria?")) {
      await deleteMutation.mutateAsync(id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Categorias</h2>
          <p className="text-muted-foreground">
            Organize suas transações por categorias
          </p>
        </div>
        <Button onClick={() => setIsFormOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Nova Categoria
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoadingCategories ? (
          <div className="col-span-full flex justify-center py-8">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          </div>
        ) : categories?.length === 0 ? (
          <Card className="col-span-full">
            <CardContent className="py-8 text-center text-muted-foreground">
              Nenhuma categoria encontrada. Clique em &quot;Nova Categoria&quot; para
              começar.
            </CardContent>
          </Card>
        ) : (
          categories?.map((category) => (
            <Card key={category.id}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="flex items-center gap-3">
                  <div
                    className="h-4 w-4 rounded-full"
                    style={{ backgroundColor: category.color }}
                  />
                  <CardTitle className="text-base font-medium">
                    {category.name}
                  </CardTitle>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => handleDelete(category.id)}
                >
                  <Trash2 className="h-4 w-4 text-destructive" />
                </Button>
              </CardHeader>
            </Card>
          ))
        )}
      </div>

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Nova Categoria</DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Nome</Label>
              <Input
                id="name"
                {...register("name")}
                placeholder="Ex: Alimentação"
              />
              {errors.name && (
                <p className="text-sm text-destructive">{errors.name.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="color">Cor</Label>
              <div className="flex gap-2">
                <input
                  type="color"
                  value={colorValue || "#6366f1"}
                  onChange={(e) => setValue("color", e.target.value)}
                  className="w-16 h-10 p-1 rounded border border-input bg-background cursor-pointer"
                />
                <Input
                  {...register("color")}
                  placeholder="#6366f1"
                  className="flex-1"
                />
              </div>
              {errors.color && (
                <p className="text-sm text-destructive">{errors.color.message}</p>
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
