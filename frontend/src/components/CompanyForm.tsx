"use client";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const schema = z.object({
  company_name: z.string().min(2),
  website_url: z.string().url(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  onSubmit: (data: FormData) => void;
}

export function CompanyForm({ onSubmit }: Props) {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form
      onSubmit={form.handleSubmit(onSubmit)}
      className="space-y-4"
    >
      <input
        {...form.register("company_name")}
        placeholder="Company Name"
        className="w-full rounded border p-3"
      />

      <input
        {...form.register("website_url")}
        placeholder="Website URL"
        className="w-full rounded border p-3"
      />

      <button
        type="submit"
        className="rounded bg-black px-4 py-2 text-white"
      >
        Analyze Company
      </button>
    </form>
  );
}