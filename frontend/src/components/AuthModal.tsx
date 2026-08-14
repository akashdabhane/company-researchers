"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabaseClient";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Mail, Lock, CheckCircle2, AlertCircle, X, LogIn, UserPlus } from "lucide-react";
import { toast } from "sonner";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [verificationSent, setVerificationSent] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      if (mode === "signup") {
        const { data, error } = await supabase.auth.signUp({
          email,
          password,
        });

        if (error) throw error;

        setVerificationSent(true);
        toast.success("Registration successful! Check your inbox for the verification email.");
      } else {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (error) throw error;

        toast.success(`Welcome back, ${data.user?.email}!`);
        onClose();
      }
    } catch (err: any) {
      console.error("Auth error:", err);
      setErrorMsg(err.message || "An authentication error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4">
      <div className="relative w-full max-w-md rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-2xl space-y-6 animate-in fade-in zoom-in duration-200">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
        >
          <X size={20} />
        </button>

        {/* Header */}
        <div className="text-center space-y-1">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
            {mode === "signin" ? "Sign In to Lantern" : "Create an Account"}
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            {mode === "signin"
              ? "Access your saved company research sessions & chats"
              : "Register to save & segregate your company research history"}
          </p>
        </div>

        {/* Verification Sent Banner */}
        {verificationSent ? (
          <div className="rounded-xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 p-4 space-y-2 text-center">
            <CheckCircle2 className="mx-auto text-emerald-600 dark:text-emerald-400" size={32} />
            <h3 className="font-semibold text-sm text-emerald-900 dark:text-emerald-200">
              Verification Email Sent!
            </h3>
            <p className="text-xs text-emerald-700 dark:text-emerald-400">
              We sent a verification link to <span className="font-medium">{email}</span>. Please click the link in your inbox to verify your email, then return here to sign in.
            </p>
            <Button
              onClick={() => {
                setVerificationSent(false);
                setMode("signin");
              }}
              variant="outline"
              className="mt-2 text-xs border-emerald-300 text-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-900"
            >
              Back to Sign In
            </Button>
          </div>
        ) : (
          <>
            {/* Mode Switch Tabs */}
            <div className="grid grid-cols-2 rounded-xl bg-slate-100 dark:bg-slate-800 p-1 text-xs font-semibold text-slate-600 dark:text-slate-300">
              <button
                type="button"
                onClick={() => {
                  setMode("signin");
                  setErrorMsg(null);
                }}
                className={`py-2 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
                  mode === "signin"
                    ? "bg-white dark:bg-slate-900 text-blue-600 dark:text-white shadow-xs"
                    : "hover:text-slate-900 dark:hover:text-white"
                }`}
              >
                <LogIn size={14} />
                Sign In
              </button>
              <button
                type="button"
                onClick={() => {
                  setMode("signup");
                  setErrorMsg(null);
                }}
                className={`py-2 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
                  mode === "signup"
                    ? "bg-white dark:bg-slate-900 text-blue-600 dark:text-white shadow-xs"
                    : "hover:text-slate-900 dark:hover:text-white"
                }`}
              >
                <UserPlus size={14} />
                Register
              </button>
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="flex items-center gap-2 rounded-lg bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 p-3 text-xs text-red-700 dark:text-red-300">
                <AlertCircle size={16} className="shrink-0 text-red-500" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <label htmlFor="email" className="text-xs font-medium text-slate-700 dark:text-slate-300">
                  Email Address
                </label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3 top-3 text-slate-400" />
                  <Input
                    id="email"
                    type="email"
                    required
                    placeholder="you@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label htmlFor="password" className="text-xs font-medium text-slate-700 dark:text-slate-300">
                  Password
                </label>
                <div className="relative">
                  <Lock size={16} className="absolute left-3 top-3 text-slate-400" />
                  <Input
                    id="password"
                    type="password"
                    required
                    minLength={6}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2.5 rounded-xl transition-all shadow-sm"
              >
                {loading ? (
                  <Loader2 className="animate-spin" size={16} />
                ) : mode === "signin" ? (
                  "Sign In"
                ) : (
                  "Create Account"
                )}
              </Button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
