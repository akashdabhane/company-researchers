"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { generatePR, refinePR } from "@/lib/api";
import { Loader2, Copy, Check, Sparkles, Send } from "lucide-react";

interface Props {
  companyName: string;
  initialContent?: string;
}

const PLATFORMS = ["LinkedIn", "Twitter / X", "Instagram", "Press Release"];
const THEMES = [
  "Product Launch & Major Announcement",
  "Thought Leadership & Industry Vision",
  "Founder Story & Company Mission",
  "Customer Success & Milestone Celebration",
];

export function PRStudioViewer({ companyName, initialContent }: Props) {
  const [platform, setPlatform] = useState("LinkedIn");
  const [theme, setTheme] = useState(THEMES[0]);
  const [feedback, setFeedback] = useState("");
  const [content, setContent] = useState(initialContent || "");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async (customFeedback?: string) => {
    setLoading(true);
    try {
      if (content && customFeedback) {
        const res = await refinePR({
          company_name: companyName,
          platform,
          narrative_theme: theme,
          human_feedback: customFeedback,
          current_content: content,
        });
        setContent(res.pr_content || "");
      } else {
        const res = await generatePR({
          company_name: companyName,
          platform,
          narrative_theme: theme,
          human_feedback: customFeedback || feedback,
        });
        setContent(res.pr_content || "");
      }
    } catch (err) {
        console.error("Failed to generate/refine PR:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg border p-5 bg-white dark:bg-gray-900 shadow-sm space-y-4">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-blue-600" />
          AI PR & Social Studio
        </h2>

        {/* Platform Selection */}
        <div>
          <label className="text-xs font-semibold text-gray-500 uppercase block mb-2">Target Platform</label>
          <div className="flex flex-wrap gap-2">
            {PLATFORMS.map((p) => (
              <button
                key={p}
                onClick={() => setPlatform(p)}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  platform === p
                    ? "bg-black text-white dark:bg-white dark:text-black"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300"
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Narrative Theme Selection */}
        <div>
          <label className="text-xs font-semibold text-gray-500 uppercase block mb-2">Narrative Angle / Theme</label>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="w-full rounded border p-2 text-sm bg-white dark:bg-gray-800 dark:border-gray-700"
          >
            {THEMES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        {/* Generate / Action Button */}
        <button
          onClick={() => handleGenerate()}
          disabled={loading}
          className="flex items-center justify-center gap-2 w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-md font-medium text-sm transition-colors"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
          Generate {platform} Post
        </button>
      </div>

      {/* Draft & Human-in-the-Loop Steering Section */}
      {content && (
        <div className="rounded-lg border p-5 bg-white dark:bg-gray-900 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b pb-3">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              Generated Copy <span className="text-xs font-normal text-gray-500">({platform} • {theme})</span>
            </h3>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-xs border px-3 py-1 rounded hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? "Copied!" : "Copy Post"}
            </button>
          </div>

          <article className="prose prose-neutral max-w-none dark:prose-invert text-sm bg-gray-50 dark:bg-gray-950 p-4 rounded border">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {content}
            </ReactMarkdown>
          </article>

          {/* Human in the Loop Input Control */}
          <div className="border-t pt-4 space-y-2">
            <label className="text-xs font-semibold text-gray-500 uppercase block">
              Human-in-the-Loop Steering / Narrative Feedback
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="e.g. Make it more casual, add a call to action link, or focus on our 10x speed boost..."
                className="flex-1 rounded border p-2 text-sm dark:bg-gray-800 dark:border-gray-700"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && feedback.trim()) {
                    handleGenerate(feedback);
                  }
                }}
              />
              <button
                onClick={() => feedback.trim() && handleGenerate(feedback)}
                disabled={loading || !feedback.trim()}
                className="flex items-center gap-1.5 bg-black text-white dark:bg-white dark:text-black px-4 py-2 rounded text-sm font-medium disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                Refine Post
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
