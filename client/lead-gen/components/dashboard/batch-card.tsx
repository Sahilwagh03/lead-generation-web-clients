"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  BatchStatus,
  capitalizeWords,
  formatDateTime,
  getBatchStatusStyles,
} from "@/lib/batch-status";
import { Batch } from "@/types/leads";
import { cn } from "@/lib/utils";
import LeadTableDialog from "./lead-table-dialog";

interface BatchCardProps {
  batch: Batch;
  onView?: (batch: Batch) => void;
  onProcess?: (batch: Batch) => void;
}

export function BatchCard({ batch, onView, onProcess }: BatchCardProps) {
  return (
    <Card className="w-full px-4 py-4 rounded-xl shadow-xs cursor-pointer hover:shadow-sm transition-all bg-gradient-to-r from-background to-muted/30">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4 flex-wrap">
        <div className="flex flex-col min-w-30">
          <p className="font-semibold text-sm">Batch {batch.id}</p>
          <p className="text-xs text-muted-foreground">
            {formatDateTime(batch.created_at)}
          </p>
        </div>

        <div className="flex flex-col flex-1 text-sm px-0 sm:px-6 min-w-0">
          <p className="font-medium">Hashtag</p>
          <p className="truncate">#{batch.hashtag}</p>
        </div>

        <div className="flex gap-3 lg:gap-4">
          <div className="text-sm font-medium w-fit text-center sm:text-left">
            {batch.lead_count} leads
          </div>

          <Badge className={cn(getBatchStatusStyles(batch.status))}>
            {capitalizeWords(batch.status)}
          </Badge>
        </div>

        <div className="flex gap-3 lg:gap-4">
          <Button
            size="sm"
            className="cursor-pointer"
            onClick={() => onProcess?.(batch)}
          >
            Process
          </Button>
          
          <LeadTableDialog batchId={batch.id} batchStatus={batch.status}/>
        </div>
      </div>
    </Card>
  );
}
