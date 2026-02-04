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
        <h1 className="text-2xl font-semibold">
          {title}
        </h1>

        {description && (
          <p className={cn("text-sm text-muted-foreground", maxWidth)}>{description}</p>
        )}
      </div>

      {children && <>{children}</>}
    </div>
  );
}
