export type LeadTag =
  | "has_website"
  | "shopify"
  | "wix"
  | "webflow"
  | "framer"
  | "wordpress"
  | "custom_coded"
  | "custom_coded_or_unknown"
  | "high_intent"
  | "cost_cutting_pitch"
  | "has_contact"
  | "website_needed"
  | "warm_outreach"
  | "no_website"
  | "no_contact"
  | "needs_website"
  | "cold_outreach";

/**
 * Unique color per tag
 * (no duplicates for better visual scanning)
 */
export const getTagStyles = (tag: LeadTag | string) => {
  const styles: Record<LeadTag, string> = {
    // 🌐 Website/platform
    has_website: "bg-emerald-100 text-emerald-700 border-emerald-200",
    shopify: "bg-green-100 text-green-700 border-green-200",
    wix: "bg-orange-100 text-orange-700 border-orange-200",
    webflow: "bg-indigo-100 text-indigo-700 border-indigo-200",
    framer: "bg-pink-100 text-pink-700 border-pink-200",
    wordpress: "bg-sky-100 text-sky-700 border-sky-200",
    custom_coded: "bg-gray-200 text-gray-800 border-gray-300",
    custom_coded_or_unknown: "bg-zinc-200 text-zinc-800 border-zinc-300",

    // 🎯 Intent
    high_intent: "bg-purple-100 text-purple-700 border-purple-200",
    cost_cutting_pitch: "bg-fuchsia-100 text-fuchsia-700 border-fuchsia-200",

    // 📞 Contact
    has_contact: "bg-cyan-100 text-cyan-700 border-cyan-200",
    website_needed: "bg-amber-100 text-amber-700 border-amber-200",
    warm_outreach: "bg-lime-100 text-lime-700 border-lime-200",

    // ❄️ Cold
    no_website: "bg-red-100 text-red-700 border-red-200",
    no_contact: "bg-rose-100 text-rose-700 border-rose-200",
    needs_website: "bg-yellow-100 text-yellow-700 border-yellow-200",
    cold_outreach: "bg-slate-200 text-slate-800 border-slate-300",
  };

  return styles[tag as LeadTag] ??
    "bg-gray-100 text-gray-600 border-gray-200";
};

/**
 * Pretty label
 * no_website -> No Website
 */
export const formatTagLabel = (value: string) =>
  value
    .toLowerCase()
    .split("_")
    .map((w) => w[0].toUpperCase() + w.slice(1))
    .join(" ");
