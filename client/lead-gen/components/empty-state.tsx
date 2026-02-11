"use client";

import Link from "next/link";
import { ReactNode } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Inbox } from "lucide-react";
import { cn } from "@/lib/utils";

type EmptyStateProps = {
  title: string;
  description?: string;
  href?: string;
  buttonText?: string;
  icon?: ReactNode;
  className?: string;
  cardClassName?:string;
};

export function EmptyState({
  title,
  description,
  href,
  buttonText,
  icon,
  className,
  cardClassName
}: EmptyStateProps) {
  return (
    <div className={cn("h-[60vh] flex items-center justify-center",className) }>
      <Card className={cn("w-full h-full justify-center rounded-2xl border-dashed shadow-sm",cardClassName)}>
        <CardContent className="flex flex-col h items-center justify-center text-center py-14 px-6 space-y-4">

          <div className="p-4 rounded-full bg-muted">
            {icon ?? <Inbox className="h-8 w-8 text-muted-foreground" />}
          </div>

          <div>
            <h3 className="text-lg font-semibold">{title}</h3>
            {description && (
              <p className="text-sm text-muted-foreground mt-1">
                {description}
              </p>
            )}
          </div>

          {href && buttonText && (
            <Link href={href}>
              <Button size="sm">{buttonText}</Button>
            </Link>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
