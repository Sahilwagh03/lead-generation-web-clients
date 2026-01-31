export interface Lead {
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
}

export interface GenerateLeadsRequest {
  hashtag: string;
  max_profiles: number;
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
