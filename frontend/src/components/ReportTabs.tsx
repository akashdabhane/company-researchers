"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ReportViewer } from "./ReportViewer";
import { ResearchResponse } from "@/lib/types";

export function ReportTabs({
  data,
}: {
  data: ResearchResponse;
}) {
  return (
    <Tabs defaultValue="report">
      <TabsList>
        <TabsTrigger value="report">
          Report
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

      <TabsContent value="website">
        <pre className="whitespace-pre-wrap">
          {data.website_data.website_content}
        </pre>
      </TabsContent>

      <TabsContent value="news">
        {data.news_data.articles.length === 0 ? (
          <p>No news found.</p>
        ) : (
          <pre>
            {JSON.stringify(
              data.news_data.articles,
              null,
              2
            )}
          </pre>
        )}
      </TabsContent>

      <TabsContent value="youtube">
        <div className="space-y-3">
          <p>
            Channel:
            {data.youtube_data.channel?.title}
          </p>

          <p>
            Videos:
            {data.youtube_data.recent_videos.length}
          </p>
        </div>
      </TabsContent>

      <TabsContent value="json">
        <pre className="overflow-auto rounded border p-4">
          {JSON.stringify(data, null, 2)}
        </pre>
      </TabsContent>
    </Tabs>
  );
}