import { ReactNode } from "react";
import { cn } from "@/lib/utils";

type SectionHeaderProps = {
  title: string;
  description?: string;
  /**
   * Optional right-side actions (buttons, filters, etc.)
   */
  children?: ReactNode;
  /**
   * Control description width if needed
   */
  maxWidth?: string;
};

export function SectionHeader({
  title,
  description,
  children,
  maxWidth = "max-w-xl",
}: SectionHeaderProps) {
  return (
    <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">

      <div className="flex flex-col gap-1">
        <h1 className="text-2xl lg:text-3xl font-bold text-gray-900 tracking-tight">
          {title}
        </h1>

        {description && (
          <p className={cn("text-md text-gray-600", maxWidth)}>{description}</p>
        )}
      </div>

      {children && <>{children}</>}
    </div>
  );
}
