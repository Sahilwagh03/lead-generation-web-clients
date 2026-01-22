"use client";

import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import Link from "next/link";

import { useLeads } from "@/hooks/useLeads";
import LeadTable from "@/components/dashboard/lead-table";

const Page = () => {
  const { data, isLoading } = useLeads({
    limit: 50,
    offset: 0,
  });

  return (
    <div className="min-h-screen flex flex-col gap-4">
      {/* Header */}
      <div className="mb-2 flex lg:items-center flex-col lg:flex-row justify-between gap-2">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-gray-900 tracking-tight">
            Welcome to Dashboard
          </h1>
          <p className="lg:mt-2 text-md text-gray-600">
            Convert leads in real-time with our comprehensive dashboard.
          </p>
        </div>

        <Link href="/dashboard/lead-generation">
          <Button className="cursor-pointer">
            New Lead
            <Plus />
          </Button>
        </Link>
      </div>

      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-semibold">Leads</h2>
        {isLoading && (
          <p className="text-sm text-gray-500">Loading leads...</p>
        )}

        {data?.leads && <LeadTable data={data.leads} />}
      </div>
    </div>
  );
};

export default Page;
