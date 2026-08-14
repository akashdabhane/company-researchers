"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  report: string;
}

export function ReportViewer({ report }: Props) {
  return (
    <article className="prose prose-neutral max-w-none dark:prose-invert">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {report}
      </ReactMarkdown>
    </article>
  );
}