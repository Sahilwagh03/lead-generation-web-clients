"use client";

import { Button } from "@/components/ui/button";
import { useLogout } from "@/hooks/useLogout";
import { LogOut } from "lucide-react";

export function LogoutButton() {
  const { logout } = useLogout();

  return (
    <Button
      variant="outline"
      onClick={logout}
      className="gap-2 cursor-pointer border-red-200 text-red-600 hover:text-red-500"
    >
      <LogOut className="size-4" />
      LogOut
    </Button>
  );
}
