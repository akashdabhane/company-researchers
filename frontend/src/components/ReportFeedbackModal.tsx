"use client";

import { useState } from "react";
import { ThumbsUp, ThumbsDown, MessageSquare, Check } from "lucide-react";
import { toast } from "sonner";

interface ReportFeedbackProps {
  companyName: string;
}

export function ReportFeedbackModal({ companyName }: ReportFeedbackProps) {
  const [rating, setRating] = useState<"up" | "down" | null>(null);
  const [showFeedbackInput, setShowFeedbackInput] = useState(false);
  const [feedbackText, setFeedbackText] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleRate = (type: "up" | "down") => {
    setRating(type);
    setShowFeedbackInput(true);
    if (type === "up") {
      toast.success("Thank you for the positive feedback!");
    } else {
      toast.info("Help us improve: What should be refined in this report?");
    }
  };

  const handleSubmitFeedback = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setShowFeedbackInput(false);
    toast.success(`Feedback saved for ${companyName} research report!`);
  };

  return (
    <div className="inline-flex items-center gap-1.5 rounded-lg border bg-white dark:bg-slate-900 px-3 py-1.5 shadow-xs">
      <span className="text-xs text-slate-500 font-medium hidden md:inline">Rate Report:</span>

      <button
        onClick={() => handleRate("up")}
        className={`p-1 rounded transition ${
          rating === "up"
            ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
            : "text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
        }`}
        title="Helpful Report"
      >
        <ThumbsUp size={14} className={rating === "up" ? "fill-current" : ""} />
      </button>

      <button
        onClick={() => handleRate("down")}
        className={`p-1 rounded transition ${
          rating === "down"
            ? "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300"
            : "text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
        }`}
        title="Needs Improvement"
      >
        <ThumbsDown size={14} className={rating === "down" ? "fill-current" : ""} />
      </button>

      {showFeedbackInput && !submitted && (
        <form onSubmit={handleSubmitFeedback} className="flex items-center gap-1.5 ml-1">
          <input
            type="text"
            placeholder="Add refinement note..."
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            className="h-7 w-36 sm:w-48 rounded border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-2 text-xs text-slate-800 dark:text-slate-200 focus:outline-hidden"
          />
          <button
            type="submit"
            className="flex h-7 w-7 items-center justify-center rounded bg-blue-600 text-white hover:bg-blue-700 transition"
          >
            <Check size={13} />
          </button>
        </form>
      )}

      {submitted && (
        <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium ml-1 flex items-center gap-1">
          <Check size={12} /> Feedback Saved
        </span>
      )}
    </div>
  );
}
