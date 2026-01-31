"use client";

import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import Link from "next/link";

import { useLeads } from "@/hooks/useLeads";
import LeadTable from "@/components/dashboard/lead-table";
import { useState } from "react";
import { SectionHeader } from "@/components/dashboard/section-header";

const DashboardPage = () => {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useLeads({
    page,
    pageSize: 20,
  });

  return (
    <div className="min-h-screen flex flex-col gap-4">
      <div className="mb-2 flex lg:items-center flex-col lg:flex-row justify-between gap-2">
        <SectionHeader
          title="Welcome to Dashboard"
          description="Convert leads in real-time with our comprehensive dashboard."
        />

        <Link href="/dashboard/lead-generation">
          <Button className="cursor-pointer">
            New Lead
            <Plus />
          </Button>
        </Link>
      </div>

      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-semibold">Leads</h2>
        {isLoading && <p className="text-sm text-gray-500">Loading leads...</p>}

        {data && (
          <LeadTable
            data={data.leads}
            pagination={data.pagination}
            onPageChange={setPage}
          />
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
