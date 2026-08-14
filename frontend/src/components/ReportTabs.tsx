"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ReportViewer } from "./ReportViewer";
import { CompetitorViewer } from "./CompetitorViewer";
import { PRStudioViewer } from "./PRStudioViewer";
import { SalesPitchViewer } from "./SalesPitchViewer";
import { AnalyticsViewer } from "./AnalyticsViewer";
import { AudioBriefingPlayer } from "./AudioBriefingPlayer";
import { PDFExportButton } from "./PDFExportButton";
import { ReportFeedbackModal } from "./ReportFeedbackModal";
import { EcosystemGraph } from "./EcosystemGraph";
import { ShareReportModal } from "./ShareReportModal";
import { ResearchResponse } from "@/lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function ReportTabs({
  data,
}: {
  data: ResearchResponse;
}) {
  return (
    <div className="space-y-4">
      {/* Top Action Bar for PDF Export, Audio Briefing, Share & Feedback */}
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border bg-slate-50 dark:bg-slate-900/60 p-3">
        <AudioBriefingPlayer
          companyName={data.company_name}
          reportContent={data.report || ""}
        />

        <div className="flex items-center gap-2">
          <ReportFeedbackModal companyName={data.company_name} />
          <ShareReportModal data={data} />
          <PDFExportButton data={data} />
        </div>
      </div>

      <Tabs defaultValue="report">
        <TabsList className="flex flex-wrap h-auto gap-1">
        <TabsTrigger value="report">
          Report
        </TabsTrigger>

        <TabsTrigger value="analytics">
          Analytics & Visuals
        </TabsTrigger>

        <TabsTrigger value="ecosystem">
          Ecosystem Map
        </TabsTrigger>

        <TabsTrigger value="competitors">
          Competitors & Battlecard
        </TabsTrigger>

        <TabsTrigger value="location">
          Location & Footprint
        </TabsTrigger>

        <TabsTrigger value="tech_stack">
          Tech Stack Audit
        </TabsTrigger>

        <TabsTrigger value="financial">
          Financials & Valuation
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

      <TabsContent value="analytics">
        <AnalyticsViewer data={data} />
      </TabsContent>

      <TabsContent value="ecosystem">
        <EcosystemGraph data={data} />
      </TabsContent>

      <TabsContent value="competitors">
        <CompetitorViewer
          competitorsData={data.competitors_data}
          competitorMatrix={data.competitor_matrix}
        />
      </TabsContent>

      <TabsContent value="location">
        <div className="space-y-4 rounded-lg border p-6 bg-white dark:bg-slate-900 shadow-xs">
          {data.location_data ? (
            <article className="prose prose-slate dark:prose-invert max-w-none text-sm leading-relaxed">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.location_data}
              </ReactMarkdown>
            </article>
          ) : (
            <p className="text-sm text-slate-500">No corporate location footprint data collected.</p>
          )}
        </div>
      </TabsContent>

      <TabsContent value="tech_stack">
        <div className="space-y-4 rounded-lg border p-6 bg-white dark:bg-slate-900 shadow-xs">
          {data.tech_stack_data ? (
            <article className="prose prose-slate dark:prose-invert max-w-none text-sm leading-relaxed">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.tech_stack_data}
              </ReactMarkdown>
            </article>
          ) : (
            <p className="text-sm text-slate-500">No technology stack audit data collected.</p>
          )}
        </div>
      </TabsContent>

      <TabsContent value="financial">
        <div className="space-y-4 rounded-lg border p-6 bg-white dark:bg-slate-900 shadow-xs">
          {data.financial_data ? (
            <article className="prose prose-slate dark:prose-invert max-w-none text-sm leading-relaxed">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.financial_data}
              </ReactMarkdown>
            </article>
          ) : (
            <p className="text-sm text-slate-500">No financial or market valuation data collected.</p>
          )}
        </div>
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
    </div>
  );
}