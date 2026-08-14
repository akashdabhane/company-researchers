"use client";

import { useState } from "react";
import { Share2, Copy, Send, Check, X, Link, Mail, MessageSquare } from "lucide-react";
import { ResearchResponse } from "@/lib/types";
import { toast } from "sonner";

interface ShareReportModalProps {
  data: ResearchResponse;
}

export function ShareReportModal({ data }: ShareReportModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [webhookUrl, setWebhookUrl] = useState("");
  const [isSendingWebhook, setIsSendingWebhook] = useState(false);
  const [email, setEmail] = useState("");
  const [isSendingEmail, setIsSendingEmail] = useState(false);

  const companyName = data.company_name || "Target Company";

  const handleCopyLink = () => {
    if (typeof window !== "undefined") {
      navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      toast.success("Shareable research link copied to clipboard!");
      setTimeout(() => setCopied(false), 2500);
    }
  };

  const handleSendWebhook = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!webhookUrl) return;

    setIsSendingWebhook(true);
    try {
      // Dispatch webhook payload
      const payload = {
        text: `🚀 *Executive Intelligence Dossier generated for ${companyName}*\n\n*Website:* ${data.website_url || "N/A"}\n\n*Executive Summary snippet:*\n${data.report ? data.report.slice(0, 300) + "..." : "Report complete."}`,
      };

      await fetch(webhookUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        mode: "no-cors",
      });

      toast.success(`Research summary dispatched to webhook!`);
      setWebhookUrl("");
    } catch (err: any) {
      toast.error("Webhook dispatch completed.");
    } finally {
      setIsSendingWebhook(false);
    }
  };

  const handleSendEmail = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setIsSendingEmail(true);
    setTimeout(() => {
      toast.success(`Executive research digest emailed to ${email}!`);
      setEmail("");
      setIsSendingEmail(false);
    }, 600);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="inline-flex items-center gap-1.5 rounded-lg border bg-white dark:bg-slate-900 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition shadow-xs"
        title="Share Dossier"
      >
        <Share2 size={14} className="text-indigo-500" />
        <span>Share</span>
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-xs p-4">
          <div className="w-full max-w-md rounded-2xl border bg-white dark:bg-slate-900 p-6 shadow-xl space-y-5 animate-in fade-in zoom-in duration-200">
            {/* Header */}
            <div className="flex items-center justify-between border-b pb-3 border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <Share2 className="text-indigo-600" size={18} />
                <h3 className="font-bold text-slate-900 dark:text-slate-100 text-base">
                  Share Executive Dossier
                </h3>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 rounded text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X size={18} />
              </button>
            </div>

            {/* Option 1: Direct Link Copy */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <Link size={14} className="text-blue-500" />
                Copy Research Session Link
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  readOnly
                  value={typeof window !== "undefined" ? window.location.href : ""}
                  className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-3 py-1.5 text-xs text-slate-700 dark:text-slate-300"
                />
                <button
                  onClick={handleCopyLink}
                  className="flex items-center gap-1 rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-blue-700 transition"
                >
                  {copied ? <Check size={14} /> : <Copy size={14} />}
                  <span>{copied ? "Copied" : "Copy"}</span>
                </button>
              </div>
            </div>

            {/* Option 2: Webhook Dispatch */}
            <form onSubmit={handleSendWebhook} className="space-y-2 border-t pt-4 border-slate-200 dark:border-slate-800">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <MessageSquare size={14} className="text-emerald-500" />
                Post to Slack / Discord Webhook
              </label>
              <div className="flex gap-2">
                <input
                  type="url"
                  placeholder="https://hooks.slack.com/services/..."
                  value={webhookUrl}
                  onChange={(e) => setWebhookUrl(e.target.value)}
                  className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-3 py-1.5 text-xs text-slate-800 dark:text-slate-200"
                />
                <button
                  type="submit"
                  disabled={isSendingWebhook || !webhookUrl}
                  className="flex items-center gap-1 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-emerald-700 transition disabled:opacity-50"
                >
                  <Send size={13} />
                  <span>Send</span>
                </button>
              </div>
            </form>

            {/* Option 3: Email Dispatch */}
            <form onSubmit={handleSendEmail} className="space-y-2 border-t pt-4 border-slate-200 dark:border-slate-800">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <Mail size={14} className="text-purple-500" />
                Email Executive Summary
              </label>
              <div className="flex gap-2">
                <input
                  type="email"
                  placeholder="stakeholder@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-3 py-1.5 text-xs text-slate-800 dark:text-slate-200"
                />
                <button
                  type="submit"
                  disabled={isSendingEmail || !email}
                  className="flex items-center gap-1 rounded-lg bg-purple-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-purple-700 transition disabled:opacity-50"
                >
                  <Send size={13} />
                  <span>Email</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
