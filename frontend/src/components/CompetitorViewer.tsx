"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Competitor {
  name: string;
  website?: string;
  type?: string;
  description?: string;
  pricing?: string;
  key_advantage?: string;
}

interface Props {
  competitorsData?: string;
  competitorMatrix?: string;
}

export function CompetitorViewer({ competitorsData, competitorMatrix }: Props) {
  let competitors: Competitor[] = [];
  if (competitorsData) {
    try {
      competitors = JSON.parse(competitorsData);
    } catch {
      competitors = [];
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">Identified Competitors</h2>
        {competitors.length === 0 ? (
          <p className="text-gray-500">No competitor structured cards available.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {competitors.map((comp, idx) => (
              <div key={idx} className="rounded-lg border p-4 shadow-sm bg-white dark:bg-gray-900 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-lg">{comp.name}</h3>
                    {comp.type && (
                      <span className={`text-xs px-2 py-0.5 rounded font-medium ${comp.type.toLowerCase() === 'direct' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                        {comp.type}
                      </span>
                    )}
                  </div>
                  {comp.description && (
                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">{comp.description}</p>
                  )}
                </div>

                <div className="space-y-1 text-xs border-t pt-3 mt-2 text-gray-500">
                  {comp.pricing && <div><span className="font-medium text-gray-700 dark:text-gray-200">Pricing:</span> {comp.pricing}</div>}
                  {comp.key_advantage && <div><span className="font-medium text-gray-700 dark:text-gray-200">Advantage:</span> {comp.key_advantage}</div>}
                  {comp.website && comp.website !== "N/A" && (
                    <div className="pt-1">
                      <a href={comp.website.startsWith("http") ? comp.website : `https://${comp.website}`} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline flex items-center gap-1">
                        Visit Website &rarr;
                      </a>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {competitorMatrix && (
        <div className="border-t pt-6">
          <h2 className="text-2xl font-bold mb-4">Competitive Battlecard & SWOT Matrix</h2>
          <article className="prose prose-neutral max-w-none dark:prose-invert">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {competitorMatrix}
            </ReactMarkdown>
          </article>
        </div>
      )}
    </div>
  );
}
