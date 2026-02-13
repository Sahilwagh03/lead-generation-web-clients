"use client";

import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useState } from "react";
import { LeadStatus } from "@/types/leads";
import { useLeads } from "@/hooks/useLeads";
import LeadTableSkeleton from "@/components/loading/lead-table-loading";
import LeadTable from "../lead-table";
import { getYesterdayRange } from "@/lib/common";

type TabConfig = {
  value: LeadStatus;
  label: string;
};

type Props = {
  tabs: TabConfig[];
};

export default function DynamicTabs({ tabs }: Props) {
  const [activeStatus, setActiveStatus] = useState<LeadStatus>(tabs[0].value);
  const [page, setPage] = useState(1);
  const { data, isLoading } = useLeads({
    page,
    pageSize: 20,
    status: activeStatus.toUpperCase(),
  });

  const handleTabChange = (value: string) => {
    setActiveStatus(value as LeadStatus);
    setPage(1);
  };

  return (
    <Tabs
      value={activeStatus}
      onValueChange={handleTabChange}
      className="w-full mt-4"
    >
      {/* Tabs Header */}
      <TabsList className="flex w-fit overflow-x-auto">
        {tabs.map((tab) => (
          <TabsTrigger key={tab.value} value={tab.value}>
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>

      {/* Tab Content */}
      {tabs.map((tab) => (
        <TabsContent key={tab.value} value={tab.value} className="pt-4">
          {isLoading ? (
            <LeadTableSkeleton />
          ) : (
            <LeadTable
              data={data?.leads || []}
              pagination={data?.pagination!}
              onPageChange={setPage}
            />
          )}
        </TabsContent>
      ))}
    </Tabs>
  );
}
