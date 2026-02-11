"use client";

import { Skeleton } from "@/components/ui/skeleton";

type Props = {
  count?: number;
};

export function NotificationsSkeleton({ count = 4 }: Props) {
  return (
    <div className="divide-y">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="flex items-start gap-4 p-4"
        >
          {/* Icon */}
          <Skeleton className="h-9 w-9 rounded-lg shrink-0" />

          {/* Content */}
          <div className="flex-1 space-y-2">
            {/* title + time */}
            <div className="flex items-center justify-between">
              <Skeleton className="h-4 w-40" />
              <Skeleton className="h-3 w-16" />
            </div>

            {/* message */}
            <Skeleton className="h-3 w-[85%]" />
            <Skeleton className="h-3 w-[60%]" />
          </div>
        </div>
      ))}
    </div>
  );
}
