"use client";

import { ChatMessage, ResearchResponse } from "@/lib/types";
import { ReportTabs } from "./ReportTabs";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Bot, User } from "lucide-react";

interface ChatMessagesProps {
  messages: ChatMessage[];
  researchData?: ResearchResponse;
}

export function ChatMessages({ messages, researchData }: ChatMessagesProps) {
  return (
    <div className="space-y-6 pb-24">
      {messages.map((msg) => {
        const isUser = msg.role === "user";

        if (msg.type === "research_report" && researchData) {
          return (
            <div key={msg.id} className="space-y-4">
              <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-blue-600 text-white shadow-sm">
                  <Bot size={16} />
                </div>
                <span>Executive Research Report</span>
              </div>

              <div className="rounded-xl border bg-white dark:bg-slate-950 p-4 shadow-sm">
                <ReportTabs data={researchData} />
              </div>
            </div>
          );
        }

        return (
          <div
            key={msg.id}
            className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
          >
            {!isUser && (
              <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-blue-600 text-white shadow-sm">
                <Bot size={18} />
              </div>
            )}

            <div
              className={`max-w-3xl rounded-2xl px-4 py-3 shadow-xs ${
                isUser
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 rounded-bl-none border border-slate-200 dark:border-slate-700"
              }`}
            >
              {isUser ? (
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
              ) : (
                <div className="prose prose-slate dark:prose-invert max-w-none text-sm leading-relaxed">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                </div>
              )}
            </div>

            {isUser && (
              <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-slate-700 text-white shadow-sm">
                <User size={18} />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
