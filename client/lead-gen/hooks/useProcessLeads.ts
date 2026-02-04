"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { ProcessLeads } from "@/services/lead-generation";
import { ProcessLeadsResponse } from "@/types/leads";
import { useState } from "react";

export const useProcessLeads = () => {
  const queryClient = useQueryClient();
  
  // ⭐ Track multiple processing batch IDs
  const [processingIds, setProcessingIds] = useState<Set<string>>(new Set());

  const mutation = useMutation<
    ProcessLeadsResponse,
    AxiosError,
    string // batchId
  >({
    mutationFn: async (batchId: string) => {
      setProcessingIds(prev => new Set(prev).add(batchId)); // add batchId
      try {
        return await ProcessLeads(batchId);
      } finally {
        setProcessingIds(prev => {
          const next = new Set(prev);
          next.delete(batchId); // remove after done
          return next;
        });
      }
    },

    onSuccess: (data, batchId) => {
      toast.success(`Batch ${batchId} processed`, {
        description: `${data.processed_count} leads processed`,
      });

      queryClient.invalidateQueries({ queryKey: ["batches"] });
      queryClient.invalidateQueries({ queryKey: ["leads", { batchId: Number(batchId) }] });
    },

    onError: (error) => {
      toast.error("Processing failed", {
        description: error.message ?? "Something went wrong",
      });
    },
  });

  return {
    process: mutation.mutate,
    processAsync: mutation.mutateAsync,
    loadingIds: processingIds,
    data: mutation.data,
    success: mutation.isSuccess,
    error: mutation.error,
    reset: mutation.reset,
  };
};
