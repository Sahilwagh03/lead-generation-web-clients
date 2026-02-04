"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import LeadTableDialog from "./lead-table-dialog";

import { useBatches } from "@/hooks/useGetBatches";
import { useProcessLeads } from "@/hooks/useProcessLeads";
import {
  capitalizeWords,
  formatDateTime,
  getBatchStatusStyles,
} from "@/lib/batch-status";
import { cn } from "@/lib/utils";
import { getProcessButtonConfig } from "@/lib/common";

export default function BatchesTable() {
  const { data, isLoading } = useBatches();
  const { processAsync, loadingIds } = useProcessLeads();

  const handleProcess = async (batchId: number) => {
    await processAsync(String(batchId));
  };

  if (isLoading) {
    return (
      <div className="rounded-xl border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Batch</TableHead>
              <TableHead>Created</TableHead>
              <TableHead>Hashtag</TableHead>
              <TableHead>Leads</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {Array.from({ length: 6 }).map((_, i) => (
              <TableRow key={i}>
                {Array.from({ length: 6 }).map((_, j) => (
                  <TableCell key={j}>
                    <Skeleton className="h-4 w-full" />
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    );
  }

  if (!data?.batches?.length) {
    return (
      <div className="h-[60vh] flex items-center justify-center text-muted-foreground border rounded-xl">
        No batches found
      </div>
    );
  }

  return (
    <div className="rounded-xl border bg-background">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Batch</TableHead>
            <TableHead>Created</TableHead>
            <TableHead>Hashtag</TableHead>
            <TableHead>Leads</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {data.batches.map((batch) => {
            const isLoadingRow = loadingIds.has(String(batch.id));
            const { text: buttonText, disabled: isDisabled } =
              getProcessButtonConfig(batch.status, isLoadingRow);

            return (
              <TableRow key={batch.id}>
                <TableCell className="font-medium">#{batch.id}</TableCell>
                <TableCell>{formatDateTime(batch.created_at)}</TableCell>
                <TableCell className="max-w-50 truncate">
                  #{batch.hashtag}
                </TableCell>
                <TableCell>{batch.lead_count}</TableCell>
                <TableCell>
                  <Badge className={cn(getBatchStatusStyles(batch.status))}>
                    {capitalizeWords(batch.status)}
                  </Badge>
                </TableCell>

                <TableCell className="text-right flex gap-2 justify-end">
                  <Button
                    size="sm"
                    disabled={isDisabled}
                    onClick={() => handleProcess(batch.id)}
                    className="cursor-pointer"
                  >
                    {buttonText}
                  </Button>

                  <LeadTableDialog
                    batchId={batch.id}
                    batchStatus={batch.status}
                  />
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
