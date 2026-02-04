"use client";

import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useBatches } from "@/hooks/useGetBatches";
import { BatchCard } from "./batch-card";

export default function BatchesList() {
  const { data, isLoading } = useBatches();

if (isLoading) {
  return (
    <div className="flex flex-col gap-3">
      {Array.from({ length: 6 }).map((_, i) => (
        <Card
          key={i}
          className="w-full px-5 py-4 rounded-xl shadow-xs"
        >
          <div className="flex items-center justify-between gap-4">

            {/* Left */}
            <div className="flex flex-col gap-2 w-28">
              <Skeleton className="h-4 w-20" />
              <Skeleton className="h-3 w-24" />
            </div>

            {/* Middle (hashtag) */}
            <div className="flex flex-col gap-2 flex-1 px-6">
              <Skeleton className="h-3 w-20" />
              <Skeleton className="h-4 w-40" />
            </div>

            {/* Leads */}
            <Skeleton className="h-4 w-16" />

            {/* Status badge */}
            <Skeleton className="h-6 w-20 rounded-full" />
          </div>
        </Card>
      ))}
    </div>
  );
}


  if (!data?.batches?.length) {
    return (
      <Card className="h-[70vh] shadow-none flex items-center justify-center p-6 text-center text-muted-foreground">
        No batches found
      </Card>
    );
  }


  return (
    <div className="flex flex-col gap-3">
      {data.batches.map((batch) => (
        <BatchCard key={batch.id} batch={batch} />
      ))}
    </div>
  );
}
