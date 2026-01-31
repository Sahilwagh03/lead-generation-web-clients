"use client";

import { useQuery } from "@tanstack/react-query";
import { getLeads } from "@/services/lead-generation";
import { GetLeadsResponse } from "@/types/leads";

interface UseLeadsParams {
  page?: number;
  pageSize?: number;
}

export const useLeads = ({
  page = 1,
  pageSize = 20,
}: UseLeadsParams = {}) => {
  return useQuery<GetLeadsResponse>({
    queryKey: ["leads", page, pageSize],
    queryFn: () => getLeads(page, pageSize),
    placeholderData: (previousData) => previousData,
  });
};