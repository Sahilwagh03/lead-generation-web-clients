"use client";

import { useQuery } from "@tanstack/react-query";
import { getLeads } from "@/services/lead-generation";
import { GetLeadsParams, GetLeadsResponse } from "@/types/leads";

interface UseLeadsParams extends GetLeadsParams {
  enabled?: boolean;
}

export const useLeads = ({
  enabled = true,
  ...params
}: UseLeadsParams = {}) => {
  return useQuery<GetLeadsResponse>({
    queryKey: ["leads", params],
    queryFn: () => getLeads(params),
    enabled,
    placeholderData: (prev) => prev,
  });
};
