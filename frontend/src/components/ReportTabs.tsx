"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ReportViewer } from "./ReportViewer";
import { CompetitorViewer } from "./CompetitorViewer";
import { PRStudioViewer } from "./PRStudioViewer";
import { SalesPitchViewer } from "./SalesPitchViewer";
import { ResearchResponse } from "@/lib/types";

export function ReportTabs({
  data,
}: {
  data: ResearchResponse;
}) {
  return (
    <Tabs defaultValue="report">
      <TabsList className="flex flex-wrap h-auto gap-1">
        <TabsTrigger value="report">
          Report
        </TabsTrigger>

        <TabsTrigger value="competitors">
          Competitors & Battlecard
        </TabsTrigger>

        <TabsTrigger value="pr_studio">
          PR & Social Studio
        </TabsTrigger>

        <TabsTrigger value="sales_pitch">
          Sales Pitch Studio
        </TabsTrigger>

        <TabsTrigger value="linkedin">
          LinkedIn
        </TabsTrigger>

        <TabsTrigger value="instagram">
          Instagram
        </TabsTrigger>

        <TabsTrigger value="twitter">
          Twitter / X
        </TabsTrigger>

        <TabsTrigger value="json">
          JSON
        </TabsTrigger>
      </TabsList>

      <TabsContent value="report">
        <ReportViewer report={data.report} />
      </TabsContent>

      <TabsContent value="competitors">
        <CompetitorViewer
          competitorsData={data.competitors_data}
          competitorMatrix={data.competitor_matrix}
        />
      </TabsContent>

      <TabsContent value="pr_studio">
        <PRStudioViewer
          companyName={data.company_name}
          initialContent={data.pr_content}
        />
      </TabsContent>

      <TabsContent value="sales_pitch">
        <SalesPitchViewer
          companyName={data.company_name}
          initialPitch={data.sales_pitch_content}
        />
      </TabsContent>

      <TabsContent value="linkedin">
        <div className="space-y-4 rounded-lg border p-4 bg-white dark:bg-gray-900">
          <h3 className="font-semibold text-lg">LinkedIn Intelligence</h3>
          {data.linkedin_data ? (
            <pre className="whitespace-pre-wrap text-xs font-mono overflow-auto max-h-[600px] bg-gray-50 dark:bg-gray-950 p-4 rounded border">
              {data.linkedin_data}
            </pre>
          ) : (
            <p className="text-sm text-gray-500">No LinkedIn data collected.</p>
          )}
        </div>
      </TabsContent>

      <TabsContent value="instagram">
        <div className="space-y-4 rounded-lg border p-4 bg-white dark:bg-gray-900">
          <h3 className="font-semibold text-lg">Instagram Brand Insights</h3>
          {data.instagram_data ? (
            <pre className="whitespace-pre-wrap text-xs font-mono overflow-auto max-h-[600px] bg-gray-50 dark:bg-gray-950 p-4 rounded border">
              {data.instagram_data}
            </pre>
          ) : (
            <p className="text-sm text-gray-500">No Instagram data collected.</p>
          )}
        </div>
      </TabsContent>

      <TabsContent value="twitter">
        <div className="space-y-4 rounded-lg border p-4 bg-white dark:bg-gray-900">
          <h3 className="font-semibold text-lg">Twitter / X Social Listening</h3>
          {data.twitter_data ? (
            <pre className="whitespace-pre-wrap text-xs font-mono overflow-auto max-h-[600px] bg-gray-50 dark:bg-gray-950 p-4 rounded border">
              {data.twitter_data}
            </pre>
          ) : (
            <p className="text-sm text-gray-500">No Twitter data collected.</p>
          )}
        </div>
      </TabsContent>

      <TabsContent value="json">
        <pre className="overflow-auto rounded border p-4 text-xs max-h-[600px]">
          {JSON.stringify(data, null, 2)}
        </pre>
      </TabsContent>
    </Tabs>
  );
}