import { api } from "@/lib/api";
import { GenerateLeadsRequest, GenerateLeadsResponse, GetBatchesResponse, GetLeadsParams, GetLeadsResponse, Lead, ProcessLeadsResponse, UpdateLeadStatusPayload } from "@/types/leads";

export const generateLeads = async (
  payload: GenerateLeadsRequest,
): Promise<GenerateLeadsResponse> => {
  const { data } = await api.post<GenerateLeadsResponse>(
    "leads/create-scraping-batch",
    payload,
  );

  return data;
};

export const getLeads = async (
  params: GetLeadsParams = {},
): Promise<GetLeadsResponse> => {
  const queryParams: Record<string, any> = {};

  // ✅ only append if exists
  if (params.page) queryParams.page = params.page;
  if (params.pageSize) queryParams.page_size = params.pageSize;

  if (params.batchId !== undefined) queryParams.batch_id = params.batchId;
  if (params.isVerified !== undefined)
    queryParams.is_verified = params.isVerified;
  if (params.isBusiness !== undefined)
    queryParams.is_business = params.isBusiness;

  if (params.search) queryParams.search = params.search;
  if (params.startDate) queryParams.start_date = params.startDate;
  if (params.endDate) queryParams.end_date = params.endDate;
  if (params.dateFilter) queryParams.date_filter = params.dateFilter;

  const { data } = await api.get<GetLeadsResponse>("leads/get-leads", {
    params: queryParams,
  });

  return data;
};

export const getBatches = async (): Promise<GetBatchesResponse> => {
  const { data } = await api.get<GetBatchesResponse>("/leads/get-batches");
  return data;
};

export const ProcessLeads = async (
  batchId: string,
): Promise<ProcessLeadsResponse> => {
  const { data } = await api.post(
    "/leads/process-leads?batch_id=" + batchId,
  );

  return data;
};

export const updateLeadStatus = async ({
  id,
  status,
}: UpdateLeadStatusPayload): Promise<Lead> => {
  const res = await api.patch(`/leads/${id}/status`, {
    status,
  });

  return res.data;
};