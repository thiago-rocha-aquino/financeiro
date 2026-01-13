import api from "./api";
import type { Category } from "@/types";

interface CreateCategoryData {
  name: string;
  color?: string;
  icon?: string;
}

export async function getCategories(): Promise<Category[]> {
  const response = await api.get<Category[]>("/categories");
  return response.data;
}

export async function createCategory(
  data: CreateCategoryData
): Promise<Category> {
  const response = await api.post<Category>("/categories", data);
  return response.data;
}

export async function updateCategory(
  id: string,
  data: Partial<CreateCategoryData>
): Promise<Category> {
  const response = await api.patch<Category>(`/categories/${id}`, data);
  return response.data;
}

export async function deleteCategory(id: string): Promise<void> {
  await api.delete(`/categories/${id}`);
}
