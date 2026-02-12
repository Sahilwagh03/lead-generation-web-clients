import { useMutation } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { generateLeads } from "@/services/lead-generation";
import {
  GenerateLeadsRequest,
  GenerateLeadsResponse,
} from "@/types/leads";
import { useRouter } from "next/navigation";

export const useGenerateLeads = () => {
  const router = useRouter()
  const mutation = useMutation<
    GenerateLeadsResponse,
    AxiosError,
    GenerateLeadsRequest
  >({
    mutationFn: generateLeads,

    onSuccess: (data) => {
      toast.success("Leads generated");
      setTimeout(()=>{
        router.push("/dashboard");
      },100)
    },

    onError: (error) => {
      toast.error("Generation failed", {
        description:
          error.message ??
          "Something went wrong",
      });
    },
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
