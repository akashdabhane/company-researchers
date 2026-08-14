"use client";

import { useMemo, useState } from "react";
import { ResearchResponse } from "@/lib/types";
import { Network, Building, ShieldAlert, Cpu, Globe, Zap, CheckCircle2 } from "lucide-react";

interface EcosystemGraphProps {
  data: ResearchResponse;
}

export function EcosystemGraph({ data }: EcosystemGraphProps) {
  const companyName = data.company_name || "Target Company";
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  // Parse competitors list
  const competitorsList = useMemo(() => {
    if (!data.competitors_data) return ["Competitor A", "Competitor B"];
    try {
      const parsed = JSON.parse(data.competitors_data);
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed.map((c: any) => c.name || "Competitor");
      }
      return ["Competitor A", "Competitor B"];
    } catch {
      return ["Competitor A", "Competitor B"];
    }
  }, [data.competitors_data]);

  const nodes = useMemo(() => [
    { id: "hub", label: companyName, category: "Hub", color: "bg-blue-600 text-white border-blue-400", icon: Building, x: 250, y: 180, desc: "Central Target Enterprise Hub" },
    { id: "comp1", label: competitorsList[0] || "Primary Competitor", category: "Competitor", color: "bg-rose-500 text-white border-rose-300", icon: ShieldAlert, x: 70, y: 80, desc: "Direct Market Competitor" },
    { id: "comp2", label: competitorsList[1] || "Secondary Competitor", category: "Competitor", color: "bg-rose-500 text-white border-rose-300", icon: ShieldAlert, x: 430, y: 80, desc: "Secondary Industry Competitor" },
    { id: "tech", label: "Tech & Cloud Infra", category: "Infrastructure", color: "bg-indigo-600 text-white border-indigo-300", icon: Cpu, x: 80, y: 280, desc: "Detected Web Stack, Cloud Hosting & APIs" },
    { id: "geo", label: "Global Footprint", category: "Location", color: "bg-emerald-600 text-white border-emerald-300", icon: Globe, x: 420, y: 280, desc: "Corporate HQ & Regional Operating Hubs" },
    { id: "partner", label: "Strategic Partners", category: "Ecosystem", color: "bg-amber-600 text-white border-amber-300", icon: Zap, x: 250, y: 40, desc: "Vendor Integrations & Channel Distribution" },
  ], [companyName, competitorsList]);

  const selectedNodeInfo = useMemo(() => {
    return nodes.find((n) => n.id === selectedNode) || nodes[0];
  }, [selectedNode, nodes]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-xl border bg-white dark:bg-slate-900 p-6 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Network className="text-blue-600" size={22} />
            Enterprise Ecosystem & Market Topology Map
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Visual network diagram mapping enterprise relationships, competitors, infrastructure, and footprint.
          </p>
        </div>

        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1.5 font-medium text-slate-600 dark:text-slate-300">
            <span className="h-2.5 w-2.5 rounded-full bg-blue-600" /> Target Hub
          </span>
          <span className="flex items-center gap-1.5 font-medium text-slate-600 dark:text-slate-300">
            <span className="h-2.5 w-2.5 rounded-full bg-rose-500" /> Competitor
          </span>
          <span className="flex items-center gap-1.5 font-medium text-slate-600 dark:text-slate-300">
            <span className="h-2.5 w-2.5 rounded-full bg-indigo-600" /> Infrastructure
          </span>
          <span className="flex items-center gap-1.5 font-medium text-slate-600 dark:text-slate-300">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-600" /> Footprint
          </span>
        </div>
      </div>

      {/* SVG Interactive Topology Canvas */}
      <div className="relative rounded-xl border bg-slate-950 p-4 shadow-inner overflow-hidden min-h-[380px] flex items-center justify-center">
        <svg className="w-full h-[360px]" viewBox="0 0 500 360">
          {/* Connection Lines */}
          <g stroke="#334155" strokeWidth="2" strokeDasharray="4 4" opacity={0.6}>
            <line x1="250" y1="180" x2="70" y2="80" />
            <line x1="250" y1="180" x2="430" y2="80" />
            <line x1="250" y1="180" x2="80" y2="280" />
            <line x1="250" y1="180" x2="420" y2="280" />
            <line x1="250" y1="180" x2="250" y2="40" />
          </g>

          {/* Pulse Ripple Effect behind Hub */}
          <circle cx="250" cy="180" r="45" fill="#2563eb" opacity="0.15" className="animate-ping" />

          {/* Render Nodes */}
          {nodes.map((node) => {
            const isSelected = selectedNode === node.id || (selectedNode === null && node.id === "hub");
            return (
              <g
                key={node.id}
                transform={`translate(${node.x}, ${node.y})`}
                className="cursor-pointer group transition-all duration-300"
                onClick={() => setSelectedNode(node.id)}
              >
                <circle
                  r={node.id === "hub" ? 32 : 24}
                  className={`${node.color.split(" ")[0]} transition-transform duration-300 group-hover:scale-110 ${
                    isSelected ? "stroke-white stroke-3" : ""
                  }`}
                />
                <text
                  y={node.id === "hub" ? 44 : 36}
                  textAnchor="middle"
                  fill="#f8fafc"
                  fontSize={node.id === "hub" ? "12" : "10"}
                  fontWeight="600"
                  className="pointer-events-none select-none drop-shadow-md"
                >
                  {node.label.length > 18 ? `${node.label.slice(0, 16)}...` : node.label}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Selected Node Drawer Card */}
        <div className="absolute bottom-4 left-4 right-4 rounded-lg bg-slate-900/90 border border-slate-800 p-3 backdrop-blur-md flex items-center justify-between text-xs text-slate-200">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="text-blue-400 shrink-0" size={18} />
            <div>
              <span className="font-bold text-white block">{selectedNodeInfo.label}</span>
              <span className="text-slate-400">{selectedNodeInfo.desc}</span>
            </div>
          </div>
          <span className="px-2 py-0.5 rounded bg-blue-950 text-blue-300 font-semibold border border-blue-800 text-[10px]">
            {selectedNodeInfo.category}
          </span>
        </div>
      </div>
    </div>
  );
}
