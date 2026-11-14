"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { AuthCard } from "@/components/auth/AuthCard";
import { getFriendlyAuthErrorMessage } from "@/lib/auth-errors";
import { Mail, Loader2, AlertCircle, CheckCircle2, ArrowLeft } from "lucide-react";

export default function ForgotPasswordPage() {
  const { sendResetEmail, firebaseConfigured } = useAuth();

  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!email.trim()) {
      setErrorMessage("Please enter the email address registered with your account.");
      return;
    }

    setSubmitting(true);
    try {
      await sendResetEmail(email);
      setSuccess(true);
    } catch (err: any) {
      const code = err?.code || (err?.message === "auth/missing-credentials" ? "auth/missing-credentials" : "auth/unknown");
      setErrorMessage(getFriendlyAuthErrorMessage(code));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthCard
      title="Reset Your Password"
      subtitle="Enter your registered email address and we'll send you a secure link to reset your account password."
      footerText="Remembered your password?"
      footerLinkText="Back to sign in"
      footerLinkHref="/login"
    >
      {success ? (
        <div className="text-center space-y-4 py-2">
          <div className="w-12 h-12 rounded-full bg-forest-100 text-forest-800 flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-7 h-7 text-forest-700" />
          </div>
          <h3 className="text-lg font-bold text-forest-950">
            Check Your Email
          </h3>
          <p className="text-xs text-charcoal-600 leading-relaxed max-w-xs mx-auto">
            We have sent password reset instructions to{" "}
            <strong className="text-charcoal-900">{email}</strong>.
          </p>
          <div className="p-3 bg-ivory-100 rounded-xl text-left text-xs text-charcoal-600 space-y-1">
            <p className="font-semibold text-charcoal-800">What to do next:</p>
            <p>&bull; Open your email inbox and click the reset link.</p>
            <p>&bull; If not received in 2 minutes, please check your Spam or Junk folder.</p>
          </div>
          <div className="pt-2">
            <button
              onClick={() => setSuccess(false)}
              className="text-xs font-bold text-forest-800 hover:text-forest-950 underline transition-colors"
            >
              Didn&apos;t receive it? Try another email
            </button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Error Alert */}
          {errorMessage && (
            <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-900 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
              <div className="flex-1 font-medium">{errorMessage}</div>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
              Registered Email Address
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-charcoal-400">
                <Mail className="w-4 h-4" />
              </div>
              <input
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="entrepreneur@domain.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 focus:border-transparent transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting || !firebaseConfigured}
            className="w-full mt-2 py-3 px-4 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Sending reset link...</span>
              </>
            ) : (
              <span>Send Password Reset Link</span>
            )}
          </button>
        </form>
      )}
    </AuthCard>
  );
}

