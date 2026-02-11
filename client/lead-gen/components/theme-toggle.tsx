"use client";
 
import { useTheme } from "next-themes";
import { Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
 
export function ModeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
 
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;
 
  const toggleTheme = async (
    e: React.MouseEvent<HTMLButtonElement>
  ) => {
    const x = e.clientX;
    const y = e.clientY;
 
    // Set CSS variables for animation origin
    document.documentElement.style.setProperty("--x", `${x}px`);
    document.documentElement.style.setProperty("--y", `${y}px`);
 
    // Fallback for unsupported browsers
    if (!document.startViewTransition) {
      setTheme(theme === "light" ? "dark" : "light");
      return;
    }
 
    await document.startViewTransition(() => {
      setTheme(theme === "light" ? "dark" : "light");
    }).finished;
  };
 
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      className="relative cursor-pointer"
    >
      {theme === "light" ? (
        <Moon className="h-[1.2rem] w-[1.2rem]" />
      ) : (
        <Sun className="h-[1.2rem] w-[1.2rem]" />
      )}
    </Button>
  );
}