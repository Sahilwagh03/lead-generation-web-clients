import { BATCH_BUTTON_CONFIG } from "@/constant/dashboard";
import { LeadStatus } from "@/types/leads";

export function getProcessButtonConfig(status: string, isLoading: boolean) {
  const config = BATCH_BUTTON_CONFIG[status] ?? { text: "Process", clickable: false };
  return {
    text: isLoading ? "Processing..." : config.text,
    disabled: !config.clickable || isLoading,
  };
}

export const leadStatusMeta: Record<
  LeadStatus,
  { label: string; color: string }
> = {
  NEW: {
    label: "New",
    color: "bg-blue-100 text-blue-800 border-blue-200",
  },

  CONTACTED: {
    label: "Contacted",
    color: "bg-indigo-100 text-indigo-800 border-indigo-200",
  },

  REMINDER: {
    label: "Reminder",
    color: "bg-amber-100 text-amber-800 border-amber-200",
  },

  RETARGET: {
    label: "Retarget",
    color: "bg-purple-100 text-purple-800 border-purple-200",
  },

  INTERESTED: {
    label: "Interested",
    color: "bg-green-100 text-green-800 border-green-200",
  },

  MEETING:{
    label:"Meeting",
    color: "bg-cyan-100 text-cyan-800 border-cyan-200",
  },

  NEGOTIATION: {
    label: "Negotiation",
    color: "bg-orange-100 text-orange-800 border-orange-200",
  },

  ACCEPTED: {
    label: "Accepted",
    color: "bg-emerald-100 text-emerald-800 border-emerald-200",
  },

  REJECTED: {
    label: "Rejected",
    color: "bg-red-100 text-red-800 border-red-200",
  },

  INVALID: {
    label: "Invalid",
    color: "bg-gray-100 text-gray-700 border-gray-200",
  },

  BLOCKED: {
    label: "Blocked",
    color: "bg-zinc-800 text-white border-zinc-900",
  },
};