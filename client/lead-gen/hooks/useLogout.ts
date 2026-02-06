"use client";

import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
import { useCookies } from "@/hooks/useCookies";
import { useAuth } from "@/context/auth-context";

export const useLogout = () => {
  const router = useRouter();
  const queryClient = useQueryClient();

  const { removeCookie } = useCookies();
  const { setUser } = useAuth();

  const logout = () => {

    removeCookie("token");
    removeCookie("user");

    // ✅ clear user context
    setUser(null);

    queryClient.clear();

    router.replace("/login");
  };

  return { logout };
};
