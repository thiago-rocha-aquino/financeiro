"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";
import { useAuth } from "@/hooks/use-auth";
import { getCurrentUser } from "@/services/auth";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { token, setUser, logout } = useAuth();

  useEffect(() => {
    if (!token) {
      router.push("/auth");
      return;
    }

    getCurrentUser()
      .then(setUser)
      .catch(() => {
        logout();
        router.push("/auth");
      });
  }, [token, router, setUser, logout]);

  if (!token) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
