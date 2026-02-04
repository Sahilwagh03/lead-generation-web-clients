"use client";

import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import Link from "next/link";
import { SectionHeader } from "@/components/dashboard/section-header";
import BatchesList from "@/components/dashboard/batch-list";
import { useLeads } from "@/hooks/useLeads";
import LeadTable from "@/components/dashboard/lead-table";
import { useState } from "react";
import BatchesTable from "@/components/dashboard/batch-table";
import LeadTableSkeleton from "@/components/loading/lead-table-loading";

const DashboardPage = () => {
  const [page, setPage] = useState(1);
  const { data: leadsData, isLoading } = useLeads({
    page,
    pageSize: 10,
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
        <h2 className="text-2xl font-semibold">Batches</h2>
        <BatchesTable/>
      </div>

      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-semibold">All Leads</h2>
        {isLoading && <LeadTableSkeleton />}

        {leadsData && (
          <LeadTable
            data={leadsData.leads}
            pagination={leadsData.pagination}
            onPageChange={setPage}
          />
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
