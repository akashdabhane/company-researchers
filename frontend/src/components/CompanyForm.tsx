"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Search, Building2, Globe, Paperclip, FileCheck, X } from "lucide-react";

const schema = z.object({
  company_name: z.string().min(2, "Company name is required"),
  website_url: z.string().min(3, "Website URL is required"),
});

type FormData = z.infer<typeof schema>;

interface Props {
  onSubmit: (data: FormData) => void;
}

export function CompanyForm({ onSubmit }: Props) {
  const [attachedFile, setAttachedFile] = useState<File | null>(null);

  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      company_name: "",
      website_url: "",
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAttachedFile(e.target.files[0]);
    }
  };

  return (
    <form
      onSubmit={form.handleSubmit(onSubmit)}
      className="space-y-5"
    >
      <div className="space-y-4">
        {/* Company Name */}
        <div>
          <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5 flex items-center gap-1.5">
            <Building2 size={14} className="text-blue-600" />
            Target Company Name
          </label>
          <input
            {...form.register("company_name")}
            placeholder="e.g. Stripe, Acme Corp, 0101 Labs"
            className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-4 py-3 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:border-blue-600 focus:outline-hidden transition"
          />
          {form.formState.errors.company_name && (
            <span className="text-xs text-red-500 mt-1 block">
              {form.formState.errors.company_name.message}
            </span>
          )}
        </div>

        {/* Website URL */}
        <div>
          <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5 flex items-center gap-1.5">
            <Globe size={14} className="text-blue-600" />
            Official Website URL
          </label>
          <input
            {...form.register("website_url")}
            placeholder="https://example.com"
            className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-4 py-3 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:border-blue-600 focus:outline-hidden transition"
          />
          {form.formState.errors.website_url && (
            <span className="text-xs text-red-500 mt-1 block">
              {form.formState.errors.website_url.message}
            </span>
          )}
        </div>

        {/* Optional Pitch Deck Attachment Upload */}
        <div>
          <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Paperclip size={14} className="text-indigo-500" />
              Attach Investor Pitch Deck / Annual Report
            </span>
            <span className="text-[10px] text-slate-400 font-normal">Optional (PDF)</span>
          </label>

          {!attachedFile ? (
            <label className="flex items-center justify-center gap-2 rounded-xl border border-dashed border-slate-300 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-950/50 px-4 py-3 cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-900 transition">
              <Paperclip size={15} className="text-slate-400" />
              <span className="text-xs text-slate-500 font-medium">Click to upload pitch deck (PDF)</span>
              <input
                type="file"
                accept=".pdf,.pptx"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
          ) : (
            <div className="flex items-center justify-between rounded-xl border border-indigo-200 dark:border-indigo-900 bg-indigo-50/60 dark:bg-indigo-950/40 px-3.5 py-2.5 text-xs text-indigo-900 dark:text-indigo-200">
              <div className="flex items-center gap-2 overflow-hidden">
                <FileCheck size={16} className="text-indigo-600 shrink-0" />
                <span className="truncate font-medium">{attachedFile.name}</span>
                <span className="text-[10px] text-slate-400">({(attachedFile.size / 1024).toFixed(0)} KB)</span>
              </div>
              <button
                type="button"
                onClick={() => setAttachedFile(null)}
                className="p-1 text-slate-400 hover:text-red-500 transition"
              >
                <X size={14} />
              </button>
            </div>
          )}
        </div>
      </div>

      <button
        type="submit"
        className="w-full flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-blue-700 transition"
      >
        <Search size={16} />
        <span>Start Autonomous Company Research</span>
      </button>
    </form>
  );
}