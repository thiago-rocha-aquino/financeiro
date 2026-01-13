import api from "./api";
import type { AuthToken, LoginCredentials, RegisterData, User } from "@/types";

export async function login(credentials: LoginCredentials): Promise<AuthToken> {
  const formData = new URLSearchParams();
  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  const response = await api.post<AuthToken>("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return response.data;
}

export async function register(data: RegisterData): Promise<User> {
  const response = await api.post<User>("/auth/register", data);
  return response.data;
}

export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>("/users/me");
  return response.data;
}

export async function updateUser(data: { name?: string }): Promise<User> {
  const response = await api.patch<User>("/users/me", data);
  return response.data;
}
