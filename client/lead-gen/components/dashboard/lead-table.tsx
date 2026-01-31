"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Lead, PaginationMeta } from "@/types/leads";
import { cn } from "@/lib/utils";
import { Button } from "../ui/button";
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";
import TablePagination from "./TablePagination";

type Props = {
  data: Lead[];
  pagination: PaginationMeta;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (size: number) => void;
};

const WIDE_COLUMNS = ["bio", "pitch_angle"];

const FIELD_LABELS: Record<keyof Lead, string> = {
  username: "Username",
  full_name: "Full Name",
  profile_url: "Profile",
  scraped_at: "Scraped At",
  followers: "Followers",
  following: "Following",
  posts: "Posts",
  website: "Website",
  email: "Email",
  phone: "Phone",
  whatsapp: "WhatsApp",
  is_verified: "Verified",
  is_business: "Business",
  category: "Category",
  bio: "Bio",
  source_hashtag: "Hashtag",
  lead_type: "Lead Type",
  platform_detected: "Platform",
  website_phones: "Website Phones",
  tags: "Tags",
  pitch_angle: "Pitch Angle",
};

export default function LeadTable({ data, pagination, onPageChange }: Props) {
  if (!data?.length) return null;

  const visibleColumns = Object.keys(FIELD_LABELS).filter((key) =>
    data.some((row) => row[key as keyof Lead] !== undefined),
  ) as (keyof Lead)[];

  return (
    <div className="rounded-lg overflow-hidden border bg-background">
      {/* TABLE */}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-12 text-center">#</TableHead>
            {visibleColumns.map((key) => (
              <TableHead key={key}>{FIELD_LABELS[key]}</TableHead>
            ))}
          </TableRow>
        </TableHeader>

        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              <TableCell className="text-center text-muted-foreground">
                {(pagination.page - 1) * pagination.page_size + index + 1}
              </TableCell>

              {visibleColumns.map((key) => (
                <TableCell
                  key={key}
                  className={cn(
                    "align-top",
                    WIDE_COLUMNS.includes(key) && "max-w-65 truncate",
                  )}
                >
                  {renderCell(row[key])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <TablePagination pagination={pagination} onPageChange={onPageChange} />
    </div>
  );
}

function renderCell(value: any) {
  if (value === null || value === "") return "—";

  if (Array.isArray(value)) {
    return (
      <div className="flex flex-wrap gap-1">
        {value.map((item, i) => (
          <Badge key={i} variant="secondary">
            {item}
          </Badge>
        ))}
      </div>
    );
  }

  if (typeof value === "boolean") {
    return (
      <Badge variant={value ? "default" : "outline"}>
        {value ? "Yes" : "No"}
      </Badge>
    );
  }

  if (typeof value === "string" && value.startsWith("http")) {
    return (
      <a
        href={value}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 underline"
      >
        Visit
      </a>
    );
  }

  return value;
}
