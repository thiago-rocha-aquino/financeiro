export interface User {
  id: string;
  email: string;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Category {
  id: string;
  name: string;
  color: string;
  icon: string;
  user_id: string;
  created_at: string;
  updated_at?: string;
}

export type TransactionType = "income" | "expense";

export interface Transaction {
  id: string;
  description: string;
  amount: number;
  type: TransactionType;
  category_id?: string;
  user_id: string;
  date: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Budget {
  id: string;
  user_id: string;
  category_id: string;
  amount: number;
  month: number;
  year: number;
  created_at: string;
  updated_at?: string;
  spent?: number;
  remaining?: number;
  percentage_used?: number;
}

export interface TransactionSummary {
  total_income: number;
  total_expense: number;
  balance: number;
  transaction_count: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  name: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}
