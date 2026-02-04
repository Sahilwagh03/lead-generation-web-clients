"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { LeadStatus } from "@/types/leads";
import { leadStatusMeta } from "@/lib/common";
import { LEAD_STATUS_OPTIONS } from "@/constant/dashboard";

type Props = {
  value: LeadStatus;
  onChange: (status: LeadStatus) => void;
};

export default function StatusSelect({ value, onChange }: Props) {
  return (
    <Select value={value} onValueChange={(v) => onChange(v as LeadStatus)}>
      <SelectTrigger className="w-31 h-8 px-2 border-0 bg-transparent">
        <SelectValue>
          <Badge className={leadStatusMeta[value].color}>
            {leadStatusMeta[value].label}
          </Badge>
        </SelectValue>
      </SelectTrigger>

      <SelectContent>
        {LEAD_STATUS_OPTIONS.map((status) => (
          <SelectItem key={status} value={status}>
            <Badge className={leadStatusMeta[status].color}>
              {leadStatusMeta[status].label}
            </Badge>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
