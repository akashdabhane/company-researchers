"use client";

import { useState } from "react";
import { CompanyForm } from "@/components/CompanyForm";
import { ReportTabs } from "@/components/ReportTabs";
import { useCompanyResearch } from "@/hooks/useCompanyResearch";
import { Loader2 } from "lucide-react";

export default function HomePage() {
  const [result, setResult] = useState<any>(null);

  const mutation = useCompanyResearch();

  const handleSubmit = async (values: {
    company_name: string;
    website_url: string;
  }) => {
    const data = await mutation.mutateAsync(values);

    setResult(data);
  };

  return (
    <main className="container mx-auto py-10">
      <div className="mx-auto max-w-5xl space-y-8">
        <h1 className="text-4xl font-bold">
          AI Company Research Agent
        </h1>

        <CompanyForm
          onSubmit={handleSubmit}
        />

        {mutation.isPending && (
          <div className="flex items-center gap-2">
            <Loader2 className="animate-spin" />
            Analyzing company...
          </div>
        )}

        {result && (
          <ReportTabs data={result} />
        )}
      </div>
    </main>
  );
}