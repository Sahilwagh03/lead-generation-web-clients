"use client";

import { capitalizeWords } from "@/lib/batch-status";
import { updateLeadStatus } from "@/services/lead-generation";
import { Lead } from "@/types/leads";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

export default function useUpdateLeadStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateLeadStatus,

    onSuccess: (updatedLead: Lead) => {
      toast.success(`Lead status updated successfully to ${capitalizeWords(updatedLead.status ?? "")}`);
      queryClient.invalidateQueries({ queryKey: ["leads"] });
    },
  });
}
