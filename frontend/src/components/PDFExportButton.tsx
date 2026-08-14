"use client";

import { useState } from "react";
import { Download, Loader2, FileText } from "lucide-react";
import { ResearchResponse } from "@/lib/types";
import { toast } from "sonner";
import jsPDF from "jspdf";

interface PDFExportButtonProps {
  data: ResearchResponse;
}

export function PDFExportButton({ data }: PDFExportButtonProps) {
  const [isExporting, setIsExporting] = useState(false);

  const handleExportPDF = async () => {
    setIsExporting(true);
    toast.info("Generating 1-Click Executive PDF Dossier...");

    try {
      const doc = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4",
      });

      const companyName = data.company_name || "Target Company";
      const websiteUrl = data.website_url || "N/A";
      const dateStr = new Date().toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });

      let yPos = 20;

      // Document Title Header
      doc.setFillColor(30, 58, 138); // Dark Navy Blue
      doc.rect(0, 0, 210, 35, "F");

      doc.setTextColor(255, 255, 255);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(20);
      doc.text("EXECUTIVE RESEARCH DOSSIER", 15, 16);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(10);
      doc.text(`Company: ${companyName} | Website: ${websiteUrl} | Date: ${dateStr}`, 15, 26);

      yPos = 45;
      doc.setTextColor(30, 41, 59);

      // Section Helper
      const addSection = (title: string, content?: string) => {
        if (!content) return;

        if (yPos > 250) {
          doc.addPage();
          yPos = 20;
        }

        // Section Heading
        doc.setFillColor(241, 245, 249);
        doc.rect(15, yPos, 180, 8, "F");

        doc.setFont("helvetica", "bold");
        doc.setFontSize(12);
        doc.setTextColor(30, 58, 138);
        doc.text(title.toUpperCase(), 18, yPos + 6);
        yPos += 14;

        // Section Body Text
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(51, 65, 85);

        const cleanText = content
          .replace(/#+/g, "")
          .replace(/\*\*|__/g, "")
          .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
          .trim();

        const splitLines = doc.splitTextToSize(cleanText, 175);
        for (const line of splitLines) {
          if (yPos > 270) {
            doc.addPage();
            yPos = 20;
          }
          doc.text(line, 18, yPos);
          yPos += 5;
        }
        yPos += 6;
      };

      // Add Sections
      addSection("1. Executive Research Report", data.report);
      addSection("2. Competitor Battlecard & SWOT Matrix", data.competitor_matrix);
      addSection("3. Corporate Location & Global Footprint", data.location_data);
      addSection("4. Technology Stack & Infrastructure Audit", data.tech_stack_data);
      addSection("5. Financials, Funding & Valuation", data.financial_data);
      addSection("6. PR Announcement Copy Draft", data.pr_content);
      addSection("7. Tailored Sales Pitch Strategy", data.sales_pitch_content);

      // Save PDF
      const sanitizedName = companyName.replace(/[^a-zA-Z0-9_-]/g, "_");
      doc.save(`Executive_Dossier_${sanitizedName}.pdf`);

      toast.success("Executive PDF Dossier downloaded successfully!");
    } catch (err: any) {
      console.error("PDF Export error:", err);
      toast.error("Failed to export PDF report.");
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <button
      onClick={handleExportPDF}
      disabled={isExporting}
      className="inline-flex items-center gap-1.5 rounded-lg border bg-white dark:bg-slate-900 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition shadow-xs disabled:opacity-50"
      title="Download 1-Click Executive PDF Report"
    >
      {isExporting ? (
        <Loader2 size={15} className="animate-spin text-blue-600" />
      ) : (
        <Download size={15} className="text-blue-600" />
      )}
      <span>Export PDF</span>
    </button>
  );
}
