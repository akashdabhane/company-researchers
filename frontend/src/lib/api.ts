import axios from "axios";
import { ResearchResponse } from "./types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
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