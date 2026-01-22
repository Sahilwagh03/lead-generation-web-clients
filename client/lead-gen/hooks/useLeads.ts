"use client";

import { useQuery } from "@tanstack/react-query";
import { getLeads } from '@/services/lead-generation'
import { Lead } from "@/types/leads";

interface UseLeadsParams {
  limit?: number;
  offset?: number;
}

export const useLeads = ({
  limit = 50,
  offset = 0,
}: UseLeadsParams = {}) => {
  return useQuery<{leads:Lead[]}>({
    queryKey: ["leads", limit, offset],
    queryFn: () => getLeads(limit, offset),
  });
};
