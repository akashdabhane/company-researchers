import axios from "axios";
import { ResearchResponse } from "./types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000",
});

export const researchCompany = async (
  company_name: string,
  website_url: string
): Promise<ResearchResponse> => {
  const { data } = await api.post("/api/research", {
    company_name,
    website_url,
  });

  return data;
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