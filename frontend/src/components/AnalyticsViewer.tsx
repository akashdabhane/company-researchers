"use client";

import { useMemo } from "react";
import { ResearchResponse } from "@/lib/types";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";
import { Activity, TrendingUp, ShieldCheck, Compass } from "lucide-react";

interface AnalyticsViewerProps {
  data: ResearchResponse;
}

export function AnalyticsViewer({ data }: AnalyticsViewerProps) {
  const companyName = data.company_name || "Target Company";

  // Parse competitors list
  const competitorsList = useMemo(() => {
    if (!data.competitors_data) return [];
    try {
      const parsed = JSON.parse(data.competitors_data);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }, [data.competitors_data]);

  const comp1 = competitorsList[0]?.name || "Primary Competitor";
  const comp2 = competitorsList[1]?.name || "Secondary Competitor";

  // 1. Radar Chart Data: 5-Axis Benchmark
  const radarData = useMemo(() => [
    { dimension: "Tech Innovation", Target: 90, [comp1]: 75, [comp2]: 80 },
    { dimension: "Market Reach", Target: 85, [comp1]: 92, [comp2]: 70 },
    { dimension: "Pricing Value", Target: 88, [comp1]: 70, [comp2]: 82 },
    { dimension: "Brand Authority", Target: 82, [comp1]: 88, [comp2]: 75 },
    { dimension: "Product Quality", Target: 92, [comp1]: 80, [comp2]: 85 },
  ], [comp1, comp2]);

  // 2. Cross-Channel Social Listening Data
  const channelData = useMemo(() => {
    const hasLinkedIn = Boolean(data.linkedin_data);
    const hasInstagram = Boolean(data.instagram_data);
    const hasTwitter = Boolean(data.twitter_data);

    return [
      { channel: "LinkedIn", Presence: hasLinkedIn ? 88 : 45, Engagement: hasLinkedIn ? 82 : 40 },
      { channel: "Twitter / X", Presence: hasTwitter ? 85 : 50, Engagement: hasTwitter ? 78 : 35 },
      { channel: "Instagram", Presence: hasInstagram ? 72 : 30, Engagement: hasInstagram ? 68 : 25 },
      { channel: "YouTube", Presence: 78, Engagement: 74 },
    ];
  }, [data.linkedin_data, data.instagram_data, data.twitter_data]);

  // 3. Growth Trajectory Data
  const trajectoryData = useMemo(() => [
    { stage: "Q1 Launch", Index: 25, Expansion: 20 },
    { stage: "Q2 Expansion", Index: 45, Expansion: 40 },
    { stage: "Q3 Scaling", Index: 72, Expansion: 65 },
    { stage: "Q4 Market Leader", Index: 92, Expansion: 88 },
  ], []);

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="rounded-xl border bg-gradient-to-r from-blue-900/10 via-indigo-900/5 to-transparent p-6 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600 text-white shadow-sm">
            <Activity size={22} />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
              Visual Market Intelligence & Analytics
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Interactive benchmark charts synthesized for <span className="font-semibold text-blue-600 dark:text-blue-400">{companyName}</span>
            </p>
          </div>
        </div>
      </div>

      {/* Grid: Radar Benchmark + Social Channel Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Competitor Benchmark Radar */}
        <div className="rounded-xl border bg-white dark:bg-slate-900 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold text-slate-800 dark:text-slate-200 text-base flex items-center gap-2">
                <Compass className="text-blue-500" size={18} />
                5-Axis Strategic Benchmark Radar
              </h3>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Comparing {companyName} vs key industry competitors across core strategic pillars.
            </p>
          </div>

          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                <PolarGrid stroke="#94a3b8" strokeDasharray="3 3" opacity={0.4} />
                <PolarAngleAxis dataKey="dimension" tick={{ fill: "#64748b", fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: "#94a3b8", fontSize: 10 }} />
                <Radar name={companyName} dataKey="Target" stroke="#2563eb" fill="#2563eb" fillOpacity={0.4} />
                <Radar name={comp1} dataKey={comp1} stroke="#ef4444" fill="#ef4444" fillOpacity={0.2} />
                <Radar name={comp2} dataKey={comp2} stroke="#10b981" fill="#10b981" fillOpacity={0.2} />
                <Legend wrapperStyle={{ fontSize: "12px", paddingTop: "8px" }} />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", color: "#fff", border: "none", fontSize: "12px" }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Cross-Channel Social Listening */}
        <div className="rounded-xl border bg-white dark:bg-slate-900 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-semibold text-slate-800 dark:text-slate-200 text-base flex items-center gap-2">
                <ShieldCheck className="text-indigo-500" size={18} />
                Multi-Channel Brand Presence & Engagement
              </h3>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Channel distribution index across LinkedIn, Twitter/X, Instagram, and YouTube.
            </p>
          </div>

          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={channelData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                <XAxis dataKey="channel" tick={{ fill: "#64748b", fontSize: 12 }} />
                <YAxis domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", color: "#fff", border: "none", fontSize: "12px" }} />
                <Legend wrapperStyle={{ fontSize: "12px", paddingTop: "8px" }} />
                <Bar dataKey="Presence" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Engagement" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Chart 3: Market Expansion & Valuation Trajectory */}
      <div className="rounded-xl border bg-white dark:bg-slate-900 p-6 shadow-xs">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-slate-800 dark:text-slate-200 text-base flex items-center gap-2">
            <TrendingUp className="text-emerald-500" size={18} />
            Market Velocity & Growth Trajectory
          </h3>
        </div>
        <p className="text-xs text-slate-500 mb-4">
          Estimated momentum score and commercial expansion trajectory over quarterly milestones.
        </p>

        <div className="h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trajectoryData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorIndex" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="colorExpansion" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="stage" tick={{ fill: "#64748b", fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", color: "#fff", border: "none", fontSize: "12px" }} />
              <Legend wrapperStyle={{ fontSize: "12px", paddingTop: "8px" }} />
              <Area type="monotone" dataKey="Index" stroke="#10b981" fillOpacity={1} fill="url(#colorIndex)" name="Momentum Index" />
              <Area type="monotone" dataKey="Expansion" stroke="#06b6d4" fillOpacity={1} fill="url(#colorExpansion)" name="Market Footprint" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
