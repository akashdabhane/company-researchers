"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { supabase } from "@/lib/supabaseClient";
import { useAuth } from "@/providers/auth-provider";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Mail, Lock, CheckCircle2, AlertCircle, Building2 } from "lucide-react";
import { toast } from "sonner";

export default function RegisterPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [verificationSent, setVerificationSent] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // If already authenticated, redirect to home
  useEffect(() => {
    if (!authLoading && user) {
      router.replace("/");
    }
  }, [user, authLoading, router]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
      });

      if (error) throw error;

      setVerificationSent(true);
      toast.success("Registration successful! Check your inbox for verification.");
    } catch (err: any) {
      console.error("Register error:", err);
      setErrorMsg(err.message || "Could not register account.");
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-slate-50 dark:bg-slate-950">
        <Loader2 className="animate-spin text-blue-600" size={36} />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen w-full flex-col bg-slate-50 dark:bg-slate-950 font-sans antialiased">
      {/* Top Header */}
      <header className="flex h-16 items-center justify-between px-6 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <div className="flex items-center gap-2">
          <Building2 className="text-blue-600 dark:text-blue-400" size={24} />
          <span className="font-bold text-lg text-slate-900 dark:text-slate-100">
            Lantern AI
          </span>
        </div>
        <ThemeToggle />
      </header>

      {/* Main Register Card */}
      <main className="flex flex-1 items-center justify-center p-4">
        <div className="w-full max-w-md space-y-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 shadow-xl">
          <div className="space-y-2 text-center">
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
              Create Your Account
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Sign up to save & segregate your company research sessions.
            </p>
          </div>

          {verificationSent ? (
            <div className="rounded-xl bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 p-5 space-y-3 text-center">
              <CheckCircle2 className="mx-auto text-emerald-600 dark:text-emerald-400" size={36} />
              <h3 className="font-semibold text-sm text-emerald-900 dark:text-emerald-200">
                Verification Email Sent!
              </h3>
              <p className="text-xs text-emerald-700 dark:text-emerald-400 leading-relaxed">
                We sent a verification link to <span className="font-medium">{email}</span>. Please open your email inbox, click the verification link, and then sign in.
              </p>
              <Button
                onClick={() => router.push("/login")}
                className="w-full mt-2 bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs"
              >
                Proceed to Sign In
              </Button>
            </div>
          ) : (
            <>
              {errorMsg && (
                <div className="flex items-center gap-2 rounded-xl bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 p-3 text-xs text-red-700 dark:text-red-300">
                  <AlertCircle size={16} className="shrink-0 text-red-500" />
                  <span>{errorMsg}</span>
                </div>
              )}

              <form onSubmit={handleRegister} className="space-y-4">
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
                  {loading ? <Loader2 className="animate-spin" size={16} /> : "Create Account"}
                </Button>
              </form>

              <div className="text-center text-xs text-slate-500 dark:text-slate-400">
                Already have an account?{" "}
                <Link
                  href="/login"
                  className="font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                >
                  Sign in here
                </Link>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
