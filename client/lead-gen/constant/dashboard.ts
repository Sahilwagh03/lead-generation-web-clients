import { BatchStatus } from "@/lib/batch-status";
import { LeadStatus } from "@/types/leads";
import { LayoutDashboard, Target, Bell } from "lucide-react";

export const SidebarData = [
  { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
  { title: "Lead Generation", url: "/dashboard/lead-generation", icon: Target },
  { title: "Notifications", url: "/dashboard/notifications", icon: Bell },
];

export const VIEWABLE_STATUSES: BatchStatus[] = ["COMPLETED", "PROCESSED"];

export const BATCH_BUTTON_CONFIG: Record<
  string,
  { text: string; clickable: boolean }
> = {
  COMPLETED: { text: "Process", clickable: true },
  PROCESSED: { text: "Processed", clickable: false },
  PENDING: { text: "Process", clickable: false },
  FAILED: { text: "Process", clickable: false },
};

export const LEAD_STATUS_OPTIONS: LeadStatus[] = [
  "NEW",
  "CONTACTED",
  "REMINDER",
  "RETARGET",
  "INTERESTED",
  "NEGOTIATION",
  "ACCEPTED",
  "REJECTED",
  "INVALID",
  "BLOCKED",
];
