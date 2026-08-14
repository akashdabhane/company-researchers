import axios from "axios";
import { ResearchResponse, ChatSessionSummary, ChatSessionDetail, ChatMessage } from "./types";
import { supabase } from "./supabaseClient";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

api.interceptors.request.use(async (config) => {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.user?.id) {
      config.headers["X-User-ID"] = session.user.id;
    } else {
      config.headers["X-User-ID"] = "anonymous";
    }
  } catch (err) {
    config.headers["X-User-ID"] = "anonymous";
  }
  return config;
});

export const researchCompany = async (
  company_name: string,
  website_url: string,
  thread_id?: string
): Promise<ResearchResponse> => {
  const { data } = await api.post("/api/research", {
    company_name,
    website_url,
    thread_id,
  });

  return data;
};

export const fetchChats = async (): Promise<ChatSessionSummary[]> => {
  const { data } = await api.get("/api/chats");
  return data;
};

export const fetchChatById = async (thread_id: string): Promise<ChatSessionDetail> => {
  const { data } = await api.get(`/api/chats/${thread_id}`);
  return data;
};

export const sendChatMessage = async (
  thread_id: string,
  message: string
): Promise<{ user_message: ChatMessage; assistant_message: ChatMessage }> => {
  const { data } = await api.post(`/api/chats/${thread_id}/message`, { message });
  return data;
};

export const deleteChatById = async (thread_id: string): Promise<void> => {
  await api.delete(`/api/chats/${thread_id}`);
};

export const generatePR = async (payload: {
  company_name: string;
  website_url?: string;
  platform: string;
  narrative_theme: string;
  human_feedback?: string;
}) => {
  const { data } = await api.post("/api/pr/generate", payload);
  return data;
};

export const refinePR = async (payload: {
  company_name: string;
  platform: string;
  narrative_theme: string;
  human_feedback: string;
  current_content?: string;
}) => {
  const { data } = await api.post("/api/pr/refine", payload);
  return data;
};

export const generateSalesPitch = async (payload: {
  company_name: string;
  website_url?: string;
  prospect_url: string;
  prospect_data?: string;
}) => {
  const { data } = await api.post("/api/pitch/generate", payload);
  return data;
};

const getUserId = async (): Promise<string> => {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    return session?.user?.id || "anonymous";
  } catch {
    return "anonymous";
  }
};

export const streamResearchCompany = async (
  company_name: string,
  website_url: string,
  thread_id?: string,
  onStatusUpdate?: (status: { node: string; message: string }) => void
): Promise<ResearchResponse> => {
  const userId = await getUserId();
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const response = await fetch(`${baseUrl}/api/research-stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": userId,
    },
    body: JSON.stringify({
      company_name,
      website_url,
      thread_id,
    }),
  });

  if (!response.ok) {
    throw new Error(`Research request failed: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error("No readable stream available");
  }

  const decoder = new TextDecoder();
  let buffer = "";
  let finalResult: ResearchResponse | null = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue;

      const dataStr = trimmed.replace(/^data:\s*/, "");
      if (dataStr === "[DONE]") break;

      try {
        const parsed = JSON.parse(dataStr);
        if (parsed.type === "status" && onStatusUpdate) {
          onStatusUpdate({ node: parsed.node, message: parsed.message });
        } else if (parsed.type === "complete") {
          finalResult = parsed.data;
        } else if (parsed.type === "error") {
          throw new Error(parsed.error || "Streaming error occurred");
        }
      } catch (e: any) {
        if (e.message && !e.message.includes("Unexpected token")) {
          console.warn("Error parsing stream chunk:", e);
        }
      }
    }
  }

  if (!finalResult) {
    throw new Error("Research stream ended without final report payload");
  }

  return finalResult;
};

export const streamChatMessage = async (
  thread_id: string,
  message: string,
  onToken: (token: string) => void
): Promise<{ user_message: ChatMessage; assistant_message: ChatMessage }> => {
  const userId = await getUserId();
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const response = await fetch(`${baseUrl}/api/chats/${thread_id}/message/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": userId,
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error(`Message stream request failed: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error("No readable stream available");
  }

  const decoder = new TextDecoder();
  let buffer = "";
  let userMsg: ChatMessage | null = null;
  let assistantMsg: ChatMessage | null = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue;

      const dataStr = trimmed.replace(/^data:\s*/, "");
      if (dataStr === "[DONE]") break;

      try {
        const parsed = JSON.parse(dataStr);
        if (parsed.type === "init") {
          userMsg = parsed.user_message;
        } else if (parsed.type === "token") {
          onToken(parsed.content);
        } else if (parsed.type === "complete") {
          assistantMsg = parsed.assistant_message;
        } else if (parsed.type === "error") {
          throw new Error(parsed.error || "Streaming error occurred");
        }
      } catch (e: any) {
        console.warn("Error parsing message stream chunk:", e);
      }
    }
  }

  return {
    user_message: userMsg!,
    assistant_message: assistantMsg!,
  };
};