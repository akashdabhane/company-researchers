"use client";

import { useState, useEffect, useRef } from "react";
import { Volume2, VolumeX, Play, Pause, Square, FastForward } from "lucide-react";
import { toast } from "sonner";

interface AudioBriefingPlayerProps {
  companyName: string;
  reportContent: string;
}

export function AudioBriefingPlayer({ companyName, reportContent }: AudioBriefingPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [rate, setRate] = useState<number>(1);
  const [isSupported, setIsSupported] = useState<boolean>(true);

  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  useEffect(() => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      setIsSupported(false);
    }
  }, []);

  // Clean raw markdown to clean readable text for speech engine
  const cleanTextForSpeech = (text: string): string => {
    if (!text) return "";
    return text
      .replace(/#+/g, "") // remove headings
      .replace(/\*\*|__/g, "") // remove bold
      .replace(/\*|_/g, "") // remove italics
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1") // remove links
      .replace(/`{1,3}[^`]*`{1,3}/g, "") // remove code blocks
      .replace(/>+/g, "") // remove blockquotes
      .replace(/-{3,}/g, "") // remove horizontal rules
      .replace(/[*+-]\s+/g, "") // remove list bullets
      .trim();
  };

  const handlePlay = () => {
    if (!isSupported) {
      toast.error("Text-to-Speech audio briefings are not supported in this browser.");
      return;
    }

    if (isPaused) {
      window.speechSynthesis.resume();
      setIsPlaying(true);
      setIsPaused(false);
      return;
    }

    window.speechSynthesis.cancel(); // Stop any active speech

    const readableText = cleanTextForSpeech(reportContent);
    if (!readableText) {
      toast.error("No text available for audio briefing.");
      return;
    }

    const scriptText = `Executive Audio Intelligence Briefing for ${companyName}. ${readableText}`;
    const utterance = new SpeechSynthesisUtterance(scriptText);
    utterance.rate = rate;
    utterance.pitch = 1.0;

    utterance.onend = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    utterance.onerror = (e) => {
      console.error("Speech Synthesis Error:", e);
      setIsPlaying(false);
      setIsPaused(false);
    };

    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
    setIsPaused(false);
    toast.success(`Playing AI Audio Briefing for ${companyName}`);
  };

  const handlePause = () => {
    if (isPlaying && !isPaused) {
      window.speechSynthesis.pause();
      setIsPlaying(false);
      setIsPaused(true);
    }
  };

  const handleStop = () => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlaying(false);
    setIsPaused(false);
  };

  const toggleRate = () => {
    const rates = [1, 1.25, 1.5, 2];
    const nextIndex = (rates.indexOf(rate) + 1) % rates.length;
    const nextRate = rates[nextIndex];
    setRate(nextRate);

    if (utteranceRef.current && isPlaying) {
      // Re-trigger speech at new speed
      handleStop();
      setTimeout(handlePlay, 100);
    }
  };

  if (!isSupported) return null;

  return (
    <div className="flex items-center gap-2 rounded-lg border bg-white dark:bg-slate-900 px-3 py-1.5 shadow-xs">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 pr-2 border-r border-slate-200 dark:border-slate-800">
        <Volume2 className="text-blue-600 animate-pulse" size={16} />
        <span className="hidden sm:inline">Audio Briefing</span>
      </div>

      {!isPlaying ? (
        <button
          onClick={handlePlay}
          className="flex items-center gap-1 rounded bg-blue-600 px-2.5 py-1 text-xs font-medium text-white hover:bg-blue-700 transition"
        >
          <Play size={13} className="fill-white" />
          <span>{isPaused ? "Resume" : "Play Briefing"}</span>
        </button>
      ) : (
        <button
          onClick={handlePause}
          className="flex items-center gap-1 rounded bg-amber-600 px-2.5 py-1 text-xs font-medium text-white hover:bg-amber-700 transition"
        >
          <Pause size={13} className="fill-white" />
          <span>Pause</span>
        </button>
      )}

      {(isPlaying || isPaused) && (
        <button
          onClick={handleStop}
          className="p-1 rounded text-slate-500 hover:text-red-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          title="Stop Audio"
        >
          <Square size={13} className="fill-current" />
        </button>
      )}

      <button
        onClick={toggleRate}
        className="flex items-center gap-0.5 text-xs font-mono font-medium px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 transition"
        title="Playback Speed"
      >
        <FastForward size={11} />
        <span>{rate}x</span>
      </button>
    </div>
  );
}
