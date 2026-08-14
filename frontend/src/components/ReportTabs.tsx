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

        <TabsTrigger value="website">
          Website
        </TabsTrigger>

        <TabsTrigger value="news">
          News
        </TabsTrigger>

        <TabsTrigger value="youtube">
          YouTube
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

      <TabsContent value="website">
        <pre className="whitespace-pre-wrap rounded border p-4 text-xs overflow-auto max-h-[600px]">
          {data.website_data?.website_content}
        </pre>
      </TabsContent>

      <TabsContent value="news">
        {!data.news_data?.articles || data.news_data.articles.length === 0 ? (
          <p className="text-gray-500">No news found.</p>
        ) : (
          <div className="space-y-4">
            {data.news_data.articles.map((article: any, idx: number) => (
              <div key={idx} className="border p-4 rounded bg-white dark:bg-gray-900">
                <a href={article.url} target="_blank" rel="noreferrer" className="font-semibold text-blue-600 hover:underline">
                  {article.title}
                </a>
                <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">{article.description}</p>
                <span className="text-xs text-gray-400 mt-2 block">{article.source?.name} • {new Date(article.publishedAt).toLocaleDateString()}</span>
              </div>
            ))}
          </div>
        )}
      </TabsContent>

      <TabsContent value="youtube">
        <div className="space-y-3">
          <p className="font-medium">
            Channel: {data.youtube_data?.channel?.title || "N/A"}
          </p>

          <p className="text-sm text-gray-600">
            Recent Videos: {data.youtube_data?.recent_videos?.length || 0}
          </p>
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