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