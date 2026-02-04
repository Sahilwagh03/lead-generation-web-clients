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
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

import { Lead, LeadStatus, PaginationMeta } from "@/types/leads";
import { cn } from "@/lib/utils";
import TablePagination from "./TablePagination";
import { getTagStyles, formatTagLabel } from "@/lib/lead-tags";
import { formatCount } from "@/lib/number-format";
import StatusSelect from "./StatusSelect";
import useUpdateLeadStatus from "@/hooks/useUpdateLeadStatus";

type Props = {
  data: Lead[];
  pagination: PaginationMeta;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (size: number) => void;
};

const WIDE_COLUMNS = ["bio", "pitch_angle"];

const FIELD_LABELS: Record<keyof Lead, string> = {
  id: "ID",
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
  batch_id: "Batch ID",
  status: "Status",
};

export default function LeadTable({ data, pagination, onPageChange }: Props) {

  const { mutate: updateStatus } = useUpdateLeadStatus();
  
  if (!data?.length) return null;

  const visibleColumns = Object.keys(FIELD_LABELS).filter((key) =>
    data.some((row) => row[key as keyof Lead] !== undefined),
  ) as (keyof Lead)[];

  const handleStatusChange = (leadId: number, status: LeadStatus) => {
    updateStatus({ id: leadId, status });
  };
  return (
    <div className="rounded-lg overflow-hidden border bg-background">
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
                    WIDE_COLUMNS.includes(key) && "max-w-65 truncate",
                  )}
                >
                  {key === "status" ? (
                    <StatusSelect
                      value={row.status as LeadStatus}
                      onChange={(s) => handleStatusChange(row.id, s)}
                    />
                  ) : (
                    renderCell(row[key])
                  )}
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
  if (
    value === null ||
    value === "" ||
    (Array.isArray(value) && value.length === 0)
  ) {
    return "—";
  }

  if (typeof value === "number") {
    return formatCount(value);
  }

  if (Array.isArray(value)) {
    const preview = value.slice(0, 3);
    const remaining = value.length - preview.length;

    return (
      <div className="flex items-center gap-1 max-w-60 overflow-hidden flex-wrap">
        {preview.map((item, i) => (
          <Badge key={i} className={getTagStyles(item)}>
            {formatTagLabel(item)}
          </Badge>
        ))}

        {remaining > 0 && (
          <Popover>
            <PopoverTrigger asChild>
              <button className="text-xs text-muted-foreground underline cursor-pointer">
                +{remaining}
              </button>
            </PopoverTrigger>

            <PopoverContent className="max-w-xs p-2 flex flex-wrap gap-2">
              {value.map((item, i) => (
                <Badge key={i} className={getTagStyles(item)}>
                  {formatTagLabel(item)}
                </Badge>
              ))}
            </PopoverContent>
          </Popover>
        )}
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

  if (
    typeof value === "string" &&
    (value.startsWith("http") ||
      value.startsWith("www") ||
      value.includes(".com"))
  ) {
    return (
      <a
        href={value.startsWith("http") ? value : `https://${value}`}
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
