import { SectionHeader } from "@/components/dashboard/section-header"; 

const ProcessLeadsPage = () => {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Lead Workflow"
        description="Review, qualify, and move leads through your sales process."
      />
      <div>
        <h2 className="text-2xl font-semibold">Process Leads</h2>
      </div>
    </div>
  );
};

export default ProcessLeadsPage;
