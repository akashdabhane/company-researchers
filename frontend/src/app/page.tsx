"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Sidebar } from "@/components/Sidebar";
import { CompanyForm } from "@/components/CompanyForm";
import { ChatMessages } from "@/components/ChatMessages";
import { ChatInput } from "@/components/ChatInput";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useAuth } from "@/providers/auth-provider";
import {
  fetchChats,
  fetchChatById,
  researchCompany,
  sendChatMessage,
  deleteChatById,
} from "@/lib/api";
import { ChatSessionSummary, ChatSessionDetail } from "@/lib/types";
import { Loader2, Sparkles, Building2, ExternalLink } from "lucide-react";
import { toast } from "sonner";

export default function HomePage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();

  const [chats, setChats] = useState<ChatSessionSummary[]>([]);
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null);
  const [activeChatDetail, setActiveChatDetail] = useState<ChatSessionDetail | null>(null);

  const [isResearching, setIsResearching] = useState(false);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [isLoadingChat, setIsLoadingChat] = useState(false);

  // Route Protection Guard
  useEffect(() => {
    if (!authLoading && !user) {
      router.replace("/login");
    }
  }, [user, authLoading, router]);

  // Load/reload chat threads list whenever authenticated user changes
  useEffect(() => {
    if (user) {
      loadChatList();
      setActiveThreadId(null);
    }
  }, [user]);

  // Load active chat detail whenever activeThreadId changes
  useEffect(() => {
    if (activeThreadId) {
      loadChatDetail(activeThreadId);
    } else {
      setActiveChatDetail(null);
    }
  }, [activeThreadId]);

  const loadChatList = async () => {
    try {
      const data = await fetchChats();
      setChats(data);
    } catch (err) {
      console.error("Failed to load chat history:", err);
    }
  };

  const loadChatDetail = async (threadId: string) => {
    setIsLoadingChat(true);
    try {
      const detail = await fetchChatById(threadId);
      setActiveChatDetail(detail);
    } catch (err) {
      console.error("Failed to load chat detail:", err);
      toast.error("Failed to load chat thread");
    } finally {
      setIsLoadingChat(false);
    }
  };

  const handleStartNewResearch = async (values: {
    company_name: string;
    website_url: string;
  }) => {
    const newThreadId = crypto.randomUUID();
    setIsResearching(true);

    try {
      toast.info(`Starting research for ${values.company_name}...`);

      const researchRes = await researchCompany(
        values.company_name,
        values.website_url,
        newThreadId
      );

      toast.success("Research completed!");

      // Refresh chats list and set active thread
      await loadChatList();
      setActiveThreadId(newThreadId);
    } catch (err: any) {
      console.error("Research failed:", err);
      toast.error(err?.response?.data?.detail || "Research process failed. Please check inputs.");
    } finally {
      setIsResearching(false);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!activeThreadId) return;

    setIsSendingMessage(true);

    // Optimistically add user message to UI
    const tempUserMsg = {
      id: crypto.randomUUID(),
      role: "user" as const,
      type: "text" as const,
      content: text,
      timestamp: new Date().toISOString(),
    };

    if (activeChatDetail) {
      setActiveChatDetail({
        ...activeChatDetail,
        messages: [...activeChatDetail.messages, tempUserMsg],
      });
    }

    try {
      const res = await sendChatMessage(activeThreadId, text);

      // Replace with official server response
      if (activeChatDetail) {
        await loadChatDetail(activeThreadId);
      }
    } catch (err: any) {
      console.error("Failed to send message:", err);
      toast.error("Failed to generate AI response. Please try again.");
    } finally {
      setIsSendingMessage(false);
    }
  };

  const handleDeleteChat = async (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await deleteChatById(threadId);
      toast.success("Chat thread deleted");
      if (activeThreadId === threadId) {
        setActiveThreadId(null);
      }
      await loadChatList();
    } catch (err) {
      console.error("Failed to delete chat:", err);
      toast.error("Could not delete chat session");
    }
  };

  // Render Loading Screen while checking Auth Guard
  if (authLoading || !user) {
    return (
      <div className="flex h-screen w-full flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 space-y-3">
        <Loader2 className="animate-spin text-blue-600" size={38} />
        <p className="text-xs text-slate-500 font-medium">Verifying authentication session...</p>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-full bg-slate-50 dark:bg-slate-950 font-sans antialiased overflow-hidden">
      {/* ChatGPT Sidebar */}
      <Sidebar
        chats={chats}
        activeThreadId={activeThreadId}
        onSelectChat={(id) => setActiveThreadId(id)}
        onNewChat={() => setActiveThreadId(null)}
        onDeleteChat={handleDeleteChat}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Header Bar */}
        <header className="h-14 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 flex items-center justify-between shadow-2xs z-10 shrink-0">
          <div className="flex items-center gap-3">
            <Building2 className="text-blue-600 dark:text-blue-400" size={20} />
            <h1 className="font-semibold text-slate-800 dark:text-slate-100 text-sm md:text-base">
              {activeChatDetail
                ? activeChatDetail.company_name
                : "AI Company Research Agent"}
            </h1>
            {activeChatDetail?.website_url && (
              <a
                href={
                  activeChatDetail.website_url.startsWith("http")
                    ? activeChatDetail.website_url
                    : `https://${activeChatDetail.website_url}`
                }
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1 text-xs text-blue-500 hover:underline"
              >
                {activeChatDetail.website_url}
                <ExternalLink size={12} />
              </a>
            )}
          </div>

          <div className="flex items-center gap-2">
            <ThemeToggle />
          </div>
        </header>

        {/* Dynamic Content */}
        <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6">
          {!activeThreadId && !isResearching ? (
            /* Empty State / Initial Research Form */
            <div className="mx-auto max-w-3xl pt-10 pb-20 space-y-8">
              <div className="text-center space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 text-xs font-semibold">
                  <Sparkles size={14} />
                  <span>Autonomous Multi-Channel Business Intelligence</span>
                </div>
                <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
                  What company would you like to research today?
                </h2>
                <p className="text-slate-500 dark:text-slate-400 text-sm max-w-xl mx-auto">
                  Enter a target company name and official website URL. The AI agent will crawl website data, YouTube, press releases, social channels, and generate competitive battlecards & PR campaigns.
                </p>
              </div>

              <div className="rounded-2xl border bg-white dark:bg-slate-900 p-6 md:p-8 shadow-sm">
                <CompanyForm onSubmit={handleStartNewResearch} />
              </div>
            </div>
          ) : isResearching ? (
            /* Loading State during Graph Execution */
            <div className="flex flex-col items-center justify-center h-full space-y-4 text-center">
              <Loader2 className="animate-spin text-blue-600" size={44} />
              <div>
                <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100">
                  Conducting Multi-Channel Intelligence Gathering...
                </h3>
                <p className="text-sm text-slate-500 max-w-md mt-1">
                  Scraping website content, Wikipedia history, YouTube transcripts, news articles, and building competitive matrix.
                </p>
              </div>
            </div>
          ) : isLoadingChat ? (
            /* Loading State when loading existing thread */
            <div className="flex flex-col items-center justify-center h-full space-y-2">
              <Loader2 className="animate-spin text-blue-600" size={32} />
              <p className="text-sm text-slate-500">Loading conversation context...</p>
            </div>
          ) : activeChatDetail ? (
            /* Active Chat View */
            <div className="mx-auto max-w-4xl">
              <ChatMessages
                messages={activeChatDetail.messages}
                researchData={activeChatDetail.research_data}
              />
            </div>
          ) : null}
        </div>

        {/* Bottom Conversational Chat Bar */}
        {activeThreadId && activeChatDetail && (
          <ChatInput
            onSendMessage={handleSendMessage}
            isLoading={isSendingMessage}
          />
        )}
      </main>
    </div>
  );
}