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
import { Lead } from "@/types/leads";
import { cn } from "@/lib/utils";

type Props = {
  data: Lead[];
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
  bio: "Bio",
  website: "Website",
  email: "Email",
  phone: "Phone",
  whatsapp: "WhatsApp",
  is_verified: "Verified",
  is_business: "Business",
  category: "Category",
  source_hashtag: "Hashtag",
  lead_type: "Lead Type",
  platform_detected: "Platform",
  website_phones: "Website Phones",
  tags: "Tags",
  pitch_angle: "Pitch Angle",
};

export default function LeadTable({ data }: Props) {
  if (!data?.length) return null;

  const visibleColumns = Object.keys(FIELD_LABELS).filter((key) =>
    data.some((row) => row[key as keyof Lead] !== undefined),
  ) as (keyof Lead)[];

  return (
    <div className="rounded-lg overflow-hidden border bg-background">
      <Table>
        <TableHeader>
          <TableRow>
            {visibleColumns.map((key) => (
              <TableHead key={key}>{FIELD_LABELS[key]}</TableHead>
            ))}
          </TableRow>
        </TableHeader>

        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
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
