"use client";

import { ChatSessionSummary } from "@/lib/types";
import { useAuth } from "@/providers/auth-provider";
import { useRouter } from "next/navigation";
import { PlusCircle, Trash2, Building2, ChevronLeft, ChevronRight, LogIn, LogOut, User as UserIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface SidebarProps {
  chats: ChatSessionSummary[];
  activeThreadId: string | null;
  onSelectChat: (threadId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (threadId: string, e: React.MouseEvent) => void;
}

export function Sidebar({
  chats,
  activeThreadId,
  onSelectChat,
  onNewChat,
  onDeleteChat,
}: SidebarProps) {
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);
  const { user, signOut } = useAuth();

  const handleSignOut = async () => {
    await signOut();
    router.replace("/login");
  };

  return (
    <aside
      className={`relative flex flex-col border-r border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-all duration-300 ${
        collapsed ? "w-16" : "w-72"
      } h-screen select-none shrink-0`}
    >
      {/* Collapse Toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-6 z-20 flex h-6 w-6 items-center justify-center rounded-full border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 shadow-md hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-slate-900 dark:hover:text-white transition-all"
        title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>

      {/* Header / New Chat */}
      <div className="p-3 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
        {collapsed ? (
          <Button
            onClick={onNewChat}
            variant="ghost"
            size="icon"
            className="w-full text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-800"
            title="New Research Chat"
          >
            <PlusCircle size={20} />
          </Button>
        ) : (
          <Button
            onClick={onNewChat}
            className="w-full justify-start gap-2 bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-xs transition-all"
          >
            <PlusCircle size={18} />
            <span>New Research</span>
          </Button>
        )}
      </div>

      {/* Chat History List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1 scrollbar-thin scrollbar-thumb-slate-300 dark:scrollbar-thumb-slate-700">
        {!collapsed && (
          <div className="px-2 py-1 text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 flex justify-between items-center">
            <span>Recent Research</span>
            {user && (
              <span className="text-[10px] lowercase text-blue-500 bg-blue-50 dark:bg-blue-950 px-1.5 py-0.5 rounded">
                synced
              </span>
            )}
          </div>
        )}

        {chats.length === 0 ? (
          !collapsed && (
            <div className="px-3 py-6 text-center text-xs text-slate-400 dark:text-slate-500">
              No previous research sessions.
            </div>
          )
        ) : (
          chats.map((chat) => {
            const isActive = activeThreadId === chat.thread_id;
            return (
              <div
                key={chat.thread_id}
                onClick={() => onSelectChat(chat.thread_id)}
                className={`group relative flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition-colors cursor-pointer ${
                  isActive
                    ? "bg-white dark:bg-slate-800 text-blue-600 dark:text-white font-semibold shadow-xs border border-slate-200 dark:border-slate-700"
                    : "text-slate-600 dark:text-slate-300 hover:bg-slate-200/70 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100"
                }`}
                title={chat.company_name}
              >
                <Building2 size={16} className={isActive ? "text-blue-600 dark:text-blue-400" : "text-slate-400"} />

                {!collapsed && (
                  <>
                    <span className="flex-1 truncate text-xs font-medium">
                      {chat.company_name}
                    </span>

                    <button
                      onClick={(e) => onDeleteChat(chat.thread_id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-red-500 transition-opacity"
                      title="Delete chat"
                    >
                      <Trash2 size={14} />
                    </button>
                  </>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* User Auth Section */}
      <div className="p-3 border-t border-slate-200 dark:border-slate-800">
        {user ? (
          collapsed ? (
            <Button
              onClick={handleSignOut}
              variant="ghost"
              size="icon"
              className="w-full text-slate-500 hover:text-red-500"
              title="Sign Out"
            >
              <LogOut size={18} />
            </Button>
          ) : (
            <div className="flex items-center justify-between gap-2 rounded-xl bg-white dark:bg-slate-800 p-2 border border-slate-200 dark:border-slate-700 shadow-2xs">
              <div className="flex items-center gap-2 overflow-hidden">
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300">
                  <UserIcon size={14} />
                </div>
                <span className="truncate text-xs font-medium text-slate-700 dark:text-slate-200">
                  {user.email}
                </span>
              </div>
              <button
                onClick={handleSignOut}
                className="p-1 text-slate-400 hover:text-red-500 transition-colors"
                title="Sign Out"
              >
                <LogOut size={14} />
              </button>
            </div>
          )
        ) : (
          collapsed ? (
            <Button
              onClick={() => router.push("/login")}
              variant="ghost"
              size="icon"
              className="w-full text-blue-600"
              title="Sign In"
            >
              <LogIn size={18} />
            </Button>
          ) : (
            <Button
              onClick={() => router.push("/login")}
              variant="outline"
              className="w-full justify-center gap-2 border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950 text-xs font-semibold"
            >
              <LogIn size={14} />
              <span>Sign In</span>
            </Button>
          )
        )}
      </div>
    </aside>
  );
}
