import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import Link from "next/link";

const Page = () => {
  return (
    <div className="min-h-screen flex flex-col gap-4">
      <div className="mb-2 flex lg:items-center flex-col lg:flex-row justify-between gap-2">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-gray-900 tracking-tight">
            Welcome to Dashboard
          </h1>
          <p className="lg:mt-2 text-md text-gray-600">
            Convert leads in real-time with our comprehensive dashboard.
          </p>
        </div>
        <div className="flex gap-4">
          <Link href="/dashboard/lead-generation">
            <Button className="cursor-pointer">
              New Lead
              <Plus />
            </Button>
          </Link>
        </div>
      </div>
      <div>
        <h2 className="text-xl font-semibold">Todays Leads</h2>
      </div>
    </div>
  );
};

export default Page;
