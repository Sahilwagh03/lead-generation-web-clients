"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useLeads } from "@/hooks/useLeads";
import LeadTable from "./lead-table";
import { BatchStatus } from "@/lib/batch-status";
import { VIEWABLE_STATUSES } from "@/constant/dashboard";
import LeadTableSkeleton from "../loading/lead-table-loading";

type Props = {
  batchId: number;
  batchStatus: BatchStatus;
};

export default function LeadTableDialog({ batchId, batchStatus }: Props) {
  const [open, setOpen] = useState(false);
  const [page, setPage] = useState(1);

  const { data, isLoading } = useLeads({
    batchId: batchId,
    page,
    pageSize: 5,
    enabled: open,
  });

  const leads = data?.leads ?? [];
  const pagination = data?.pagination;

  const isDisable = !VIEWABLE_STATUSES.includes(batchStatus);

  return (
    <Dialog
      open={open}
      onOpenChange={(value: boolean) => {
        setOpen(value);
        if (!value) setPage(1);
      }}
    >
      <DialogTrigger asChild>
        <Button
          size="sm"
          variant="outline"
          disabled={isDisable}
          className="cursor-pointer disabled:pointer-events-auto disabled:cursor-not-allowed"
        >
          View
        </Button>
      </DialogTrigger>

      <DialogContent className="p-4 max-w-[95vw]! max-h-[95vh] flex flex-col overflow-hidden">
        <DialogHeader className="px-1">
          <DialogTitle>Batch {batchId} Leads</DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-auto">
          {isLoading && (
            <LeadTableSkeleton/>
          )}

          {!isLoading && pagination && (
            <div className="relative">
              <LeadTable
                data={leads}
                pagination={pagination}
                onPageChange={(p) => setPage(p)}
              />
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
