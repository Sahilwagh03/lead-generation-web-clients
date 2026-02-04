"use client";

import { useQuery } from "@tanstack/react-query";
import { getBatches } from "@/services/lead-generation"; // your API function
import { GetBatchesResponse } from "@/types/leads";

/**
 * Custom hook to fetch scraping batches
 */
export const useBatches = () => {
  return useQuery<GetBatchesResponse>({
    queryKey: ["batches"],
    queryFn: () => getBatches(),
  });
};
