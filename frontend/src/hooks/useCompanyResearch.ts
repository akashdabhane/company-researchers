"use client";

import { useMutation } from "@tanstack/react-query";
import { researchCompany } from "@/lib/api";

export const useCompanyResearch = () => {
  return useMutation({
    mutationFn: ({
      company_name,
      website_url,
    }: {
      company_name: string;
      website_url: string;
    }) => researchCompany(company_name, website_url),
  });
};