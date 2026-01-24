import { api } from "@/lib/api";
import {
  GenerateLeadsRequest,
  GenerateLeadsResponse,
} from "@/types/leads";

export const generateLeads = async (
  payload: GenerateLeadsRequest
): Promise<GenerateLeadsResponse> => {
  const { data } = await api.post<GenerateLeadsResponse>(
    "leads/generate-leads",
    payload
  );

  return data;
};

export const getLeads = async (
  limit: number,
  offset: number
): Promise<GenerateLeadsResponse> => {
  const { data } = await api.get<GenerateLeadsResponse>(
    `leads/get-leads`,
    {
      params: { limit, offset },
    }
  );
  return data;
};