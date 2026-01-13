import api from "./api";
import type { Budget } from "@/types";

interface CreateBudgetData {
  category_id: string;
  amount: number;
  month: number;
  year: number;
}

export async function getBudgets(month: number, year: number): Promise<Budget[]> {
  const response = await api.get<Budget[]>("/budgets", {
    params: { month, year },
  });
  return response.data;
}

export async function createBudget(data: CreateBudgetData): Promise<Budget> {
  const response = await api.post<Budget>("/budgets", data);
  return response.data;
}

export async function updateBudget(
  id: string,
  data: { amount: number }
): Promise<Budget> {
  const response = await api.patch<Budget>(`/budgets/${id}`, data);
  return response.data;
}

export async function deleteBudget(id: string): Promise<void> {
  await api.delete(`/budgets/${id}`);
}
