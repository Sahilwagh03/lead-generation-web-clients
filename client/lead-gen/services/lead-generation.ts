import { api } from "@/lib/api";
import { GenerateLeadsRequest, GenerateLeadsResponse, GetLeadsResponse } from "@/types/leads";

export const generateLeads = async (
  payload: GenerateLeadsRequest,
): Promise<GenerateLeadsResponse> => {
  const { data } = await api.post<GenerateLeadsResponse>(
    "leads/generate-leads",
    payload,
  );

  return data;
};

export const getLeads = async (
  page: number,
  pageSize: number,
): Promise<GetLeadsResponse> => {
  const { data } = await api.get<GetLeadsResponse>(`leads/get-leads`, {
    params: {
      page,
      page_size: pageSize,
    },
  });
  return data;
};
