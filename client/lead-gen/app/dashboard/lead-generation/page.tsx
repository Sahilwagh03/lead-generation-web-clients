"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Loader2, Hash } from "lucide-react";
import { useGenerateLeads } from "@/hooks/use-generate-leads";
import LeadTable from "@/components/dashboard/lead-table";

const LeadGeneration = () => {
  const [hashtags, setHashtags] = useState("");
  const [maxProfiles, setMaxProfiles] = useState("50");

  const { generate, data, loading, error, success } = useGenerateLeads();

  const handleScrape = () => {
    if (!hashtags.trim()) return;

    generate({
      hashtags: hashtags
        .split(",")
        .map((h) => h.trim())
        .filter(Boolean),
      max_profiles: Number(maxProfiles) || 10,
    });
  };

  return (
    <div className="min-h-screen flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl lg:text-3xl font-bold tracking-tight">
          Hashtag Lead Finder
        </h1>
        <p className="text-muted-foreground max-w-xl">
          Turn Instagram hashtags into qualified business leads in minutes.
        </p>
      </div>

      <Card className="rounded-lg py-4 gap-4">
        <CardHeader className="px-4">
          <CardTitle className="flex items-center gap-2">
            <Hash className="h-5 w-5" />
            Scrape Leads
          </CardTitle>
          <CardDescription>
            Enter hashtags and limit how many profiles you want to scrape.
          </CardDescription>
        </CardHeader>

        <Separator />

        <CardContent className="space-y-6 px-4">
          <div className="space-y-2">
            <Label htmlFor="hashtags">Hashtags</Label>
            <Input
              id="hashtags"
              placeholder="interiordesign, homedecor, furniture"
              value={hashtags}
              onChange={(e) => setHashtags(e.target.value)}
            />
            <p className="text-sm text-muted-foreground">
              Separate multiple hashtags using commas.
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="maxProfiles">Max Profiles</Label>
            <Input
              id="maxProfiles"
              type="number"
              min={1}
              max={1000}
              value={maxProfiles}
              onChange={(e) => setMaxProfiles(e.target.value)}
            />
            <p className="text-sm text-muted-foreground">
              Recommended: 50–200 for best performance.
            </p>
          </div>

          {error && (
            <p className="text-sm text-red-600">{"Failed to scrape leads"}</p>
          )}

          {success && data && (
            <p className="text-sm text-green-600">
              ✅ {data.leads_count} leads scraped successfully
            </p>
          )}

          <Button
            className="w-full"
            size="lg"
            onClick={handleScrape}
            disabled={loading || !hashtags.trim()}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Scraping Leads...
              </>
            ) : (
              "Start Scraping"
            )}
          </Button>
        </CardContent>
      </Card>
      {data?.leads && data.leads.length > 0 && (
        <LeadTable data={data?.leads || []} />
      )}
    </div>
  );
};

export default LeadGeneration;
