import { BatchStatus } from "@/lib/batch-status";

export interface Lead {
  id: number;
  batch_id?: number;
  username?: string;
  full_name?: string;
  profile_url?: string;
  scraped_at?: string;
  followers?: number;
  following?: number;
  posts?: number;
  bio?: string;
  website?: string;
  email?: string;
  phone?: string;
  whatsapp?: string;
  is_verified?: boolean;
  is_business?: boolean;
  category?: string;
  source_hashtag?: string;
  lead_type?: string;
  platform_detected?: string;
  website_phones?: string[];
  tags?: string[];
  pitch_angle?: string;
  status?: LeadStatus;
}

export interface GenerateLeadsRequest {
  hashtag: string;
  lead_count: number;
}

export interface GenerateLeadsResponse {
  status: "success";
  message: string;
  hashtag: string;
}

export interface GetLeadsResponse {
  leads: Lead[];
  pagination: PaginationMeta;
  filtered_by?: Record<string, any>;
}

export type PaginationMeta = {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
};

export interface Batch {
  id: number;
  hashtag: string;
  lead_count: number;
  status: BatchStatus;
  created_at: string;
}

export interface GetBatchesResponse {
  status: "success" | "error";
  batches: Batch[];
}

export interface GetLeadsParams {
  batchId?: number;
  page?: number;
  pageSize?: number;
  isVerified?: boolean;
  isBusiness?: boolean;
  search?: string;
  startDate?: string;
  endDate?: string;
  dateFilter?: string;
}

export type ProcessLeadsStats = {
  total: number;
  cost_reduction_clients: number;
  needs_website_clients: number;
  needs_website: number;
};

export type ProcessLeadsResponse = {
  status: "success" | "failed";
  processed_count: number;
  stats: ProcessLeadsStats;
};

export type LeadStatus =
  | "NEW"
  | "CONTACTED"
  | "REMINDER"
  | "RETARGET"
  | "INTERESTED"
  | "MEETING"
  | "NEGOTIATION"
  | "ACCEPTED"
  | "REJECTED"
  | "INVALID"
  | "BLOCKED";

export type UpdateLeadStatusPayload = {
  id: number;
  status: LeadStatus;
};
