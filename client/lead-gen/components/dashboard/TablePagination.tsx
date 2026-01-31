"use client";

import { Button } from "@/components/ui/button";
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";
import { PaginationMeta } from "@/types/leads";

type Props = {
  pagination: PaginationMeta;
  onPageChange: (page: number) => void;
};

export default function TablePagination({ pagination, onPageChange }: Props) {
  if (!pagination || pagination.total_pages <= 1) return null;

  return (
    <div className="flex items-center justify-between px-2 py-1 border-t">
      <p className="text-sm text-muted-foreground">
        Page {pagination.page} of {pagination.total_pages} · {pagination.total}{" "}
        leads
      </p>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="icon"
          className="shadow-none border-0"
          disabled={!pagination.has_prev}
          onClick={() => onPageChange(1)}
        >
          <ChevronsLeft className="h-4 w-4" />
        </Button>

        <Button
          variant="outline"
          size="icon"
          className="shadow-none border-0"
          disabled={!pagination.has_prev}
          onClick={() => onPageChange(pagination.page - 1)}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>

        <Button
          variant="outline"
          size="icon"
          className="shadow-none border-0"
          disabled={!pagination.has_next}
          onClick={() => onPageChange(pagination.page + 1)}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>

        <Button
          variant="outline"
          size="icon"
          className="shadow-none border-0"
          disabled={!pagination.has_next}
          onClick={() => onPageChange(pagination.total_pages)}
        >
          <ChevronsRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
