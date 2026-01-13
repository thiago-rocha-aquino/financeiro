import api from "./api";
import type { Transaction, TransactionSummary, TransactionType } from "@/types";

interface TransactionFilters {
  start_date?: string;
  end_date?: string;
  type?: TransactionType;
  category_id?: string;
  limit?: number;
  offset?: number;
}

interface CreateTransactionData {
  description: string;
  amount: number;
  type: TransactionType;
  category_id?: string;
  date?: string;
  notes?: string;
}

export async function getTransactions(
  filters?: TransactionFilters
): Promise<Transaction[]> {
  const response = await api.get<Transaction[]>("/transactions", {
    params: filters,
  });
  return response.data;
}

export async function getTransactionSummary(
  start_date?: string,
  end_date?: string
): Promise<TransactionSummary> {
  const response = await api.get<TransactionSummary>("/transactions/summary", {
    params: { start_date, end_date },
  });
  return response.data;
}

export async function createTransaction(
  data: CreateTransactionData
): Promise<Transaction> {
  const response = await api.post<Transaction>("/transactions", data);
  return response.data;
}

export async function updateTransaction(
  id: string,
  data: Partial<CreateTransactionData>
): Promise<Transaction> {
  const response = await api.patch<Transaction>(`/transactions/${id}`, data);
  return response.data;
}

export async function deleteTransaction(id: string): Promise<void> {
  await api.delete(`/transactions/${id}`);
}

export interface MonthlyData {
  name: string;
  receitas: number;
  despesas: number;
}

export async function getMonthlyData(year?: number): Promise<MonthlyData[]> {
  const response = await api.get<MonthlyData[]>("/transactions/monthly", {
    params: { year },
  });
  return response.data;
}
