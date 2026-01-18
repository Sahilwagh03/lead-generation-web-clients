import { useMutation } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { generateLeads } from "@/services/lead-generation";
import {
  GenerateLeadsRequest,
  GenerateLeadsResponse,
} from "@/types/leads";

export const useGenerateLeads = () => {
  const mutation = useMutation<
    GenerateLeadsResponse,
    AxiosError,
    GenerateLeadsRequest
  >({
    mutationFn: generateLeads,
  });

  return {
    generate: mutation.mutate,
    generateAsync: mutation.mutateAsync,

    data: mutation.data,

    loading: mutation.isPending,
    success: mutation.isSuccess,
    error: mutation.error,

    reset: mutation.reset,
  };
};
