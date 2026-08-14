"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { generateSalesPitch } from "@/lib/api";
import { Loader2, Copy, Check, Briefcase, Target, Send } from "lucide-react";

interface Props {
  companyName: string;
  initialPitch?: string;
}

export function SalesPitchViewer({ companyName, initialPitch }: Props) {
  const [prospectUrl, setProspectUrl] = useState("");
  const [pitchContent, setPitchContent] = useState(initialPitch || "");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async () => {
    if (!prospectUrl.trim() && !pitchContent) return;
    setLoading(true);
    try {
      const res = await generateSalesPitch({
        company_name: companyName,
        prospect_url: prospectUrl.trim() || "Target Prospect",
      });
      setPitchContent(res.sales_pitch_content || "");
    } catch (err) {
      console.error("Failed to generate sales pitch:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(pitchContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg border p-5 bg-white dark:bg-gray-900 shadow-sm space-y-4">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <Target className="w-5 h-5 text-emerald-600" />
          Sales Pitch & Prospecting Studio
        </h2>
        <p className="text-xs text-gray-500">
          Enter a target prospect company's URL to perform dual-company research and generate a custom sales outreach kit.
        </p>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={prospectUrl}
            onChange={(e) => setProspectUrl(e.target.value)}
            placeholder="Target Prospect URL (e.g., https://acme.com or Acme Inc)"
            className="flex-1 rounded border p-2 text-sm dark:bg-gray-800 dark:border-gray-700"
            onKeyDown={(e) => {
              if (e.key === "Enter" && prospectUrl.trim()) {
                handleGenerate();
              }
            }}
          />
          <button
            onClick={handleGenerate}
            disabled={loading || (!prospectUrl.trim() && !pitchContent)}
            className="flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-md font-medium text-sm transition-colors disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Briefcase className="w-4 h-4" />}
            Generate Sales Kit
          </button>
        </div>
      </div>

      {pitchContent ? (
        <div className="rounded-lg border p-5 bg-white dark:bg-gray-900 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b pb-3">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              Sales Outreach & Objection Kit
            </h3>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-xs border px-3 py-1 rounded hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? "Copied!" : "Copy Sales Kit"}
            </button>
          </div>

          <article className="prose prose-neutral max-w-none dark:prose-invert text-sm bg-gray-50 dark:bg-gray-950 p-4 rounded border">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {pitchContent}
            </ReactMarkdown>
          </article>
        </div>
      ) : (
        <div className="text-center py-12 border rounded-lg bg-gray-50 dark:bg-gray-950">
          <Briefcase className="w-10 h-10 text-gray-400 mx-auto mb-2" />
          <h3 className="font-semibold text-gray-700 dark:text-gray-300">No Sales Pitch Generated Yet</h3>
          <p className="text-xs text-gray-500 mt-1 max-w-md mx-auto">
            Enter a target prospect URL above to generate cold email sequences, LinkedIn outreach messages, and sales objection battlecards.
          </p>
        </div>
      )}
    </div>
  );
}
