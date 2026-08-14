"use client";

import { useTheme } from "@/providers/theme-provider";
import { Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      className="h-9 w-9 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shadow-2xs"
      title={`Switch to ${theme === "light" ? "Dark" : "Light"} Mode`}
    >
      {theme === "light" ? (
        <Moon size={16} className="text-slate-700 transition-transform rotate-0 dark:-rotate-90" />
      ) : (
        <Sun size={16} className="text-amber-400 transition-transform rotate-0 dark:rotate-90" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
