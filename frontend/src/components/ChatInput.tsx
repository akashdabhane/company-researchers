"use client";

import { useState, useRef, KeyboardEvent } from "react";
import { Send, Sparkles, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

const SUGGESTIONS = [
  "Who are our top competitors and matrix?",
  "Draft a PR announcement for LinkedIn",
  "Summarize key business risks from news",
  "Generate a sales pitch for a target prospect",
];

export function ChatInput({ onSendMessage, isLoading, disabled }: ChatInputProps) {
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (!text.trim() || isLoading || disabled) return;
    onSendMessage(text.trim());
    setText("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        160
      )}px`;
    }
  };

  return (
    <div className="fixed bottom-0 right-0 left-0 lg:left-72 z-10 bg-gradient-to-t from-white via-white/95 to-transparent dark:from-slate-950 dark:via-slate-950/95 p-4">
      <div className="mx-auto max-w-4xl space-y-3">
        {/* Suggestion Pills */}
        {!disabled && (
          <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
            <span className="flex items-center gap-1 text-xs font-semibold text-slate-400 shrink-0">
              <Sparkles size={12} className="text-amber-500" />
              Suggested:
            </span>
            {SUGGESTIONS.map((suggestion, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setText(suggestion);
                  textareaRef.current?.focus();
                }}
                className="shrink-0 rounded-full border border-slate-200 bg-white/80 dark:bg-slate-900/80 dark:border-slate-800 px-3 py-1 text-xs text-slate-600 dark:text-slate-300 hover:bg-blue-50 dark:hover:bg-slate-800 hover:text-blue-600 dark:hover:text-blue-400 transition-colors shadow-2xs"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        {/* Input Box */}
        <div className="relative flex items-center rounded-2xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-2.5 shadow-md focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            onInput={handleInput}
            disabled={isLoading || disabled}
            placeholder={
              disabled
                ? "Start a company research session first..."
                : "Ask a follow-up question, request PR copy, or query competitor data..."
            }
            rows={1}
            className="w-full resize-none bg-transparent text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-hidden disabled:opacity-50"
          />

          <Button
            onClick={handleSend}
            disabled={!text.trim() || isLoading || disabled}
            size="icon"
            className="ml-2 h-9 w-9 shrink-0 rounded-xl bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-40 transition-all"
          >
            {isLoading ? (
              <Loader2 className="animate-spin" size={16} />
            ) : (
              <Send size={16} />
            )}
          </Button>
        </div>

        <p className="text-center text-[10px] text-slate-400">
          AI Company Intelligence provides insights derived from public domain data & active scrapers.
        </p>
      </div>
    </div>
  );
}
