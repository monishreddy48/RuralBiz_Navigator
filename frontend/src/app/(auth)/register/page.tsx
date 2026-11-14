"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { AuthCard } from "@/components/auth/AuthCard";
import { getFriendlyAuthErrorMessage } from "@/lib/auth-errors";
import { User, Mail, Lock, Eye, EyeOff, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const { user, registerWithEmail, loginWithGoogle, firebaseConfigured } = useAuth();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [submitting, setSubmitting] = useState(false);
  const [googleSubmitting, setGoogleSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // If already logged in, redirect to complete-profile or dashboard
  useEffect(() => {
    if (user) {
      router.push("/complete-profile");
    }
  }, [user, router]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!fullName.trim()) {
      setErrorMessage("Please enter your full name.");
      return;
    }

    if (!email.trim()) {
      setErrorMessage("Please enter a valid email address.");
      return;
    }

    if (password.length < 6) {
      setErrorMessage("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match. Please re-enter your password.");
      return;
    }

    setSubmitting(true);
    try {
      await registerWithEmail(email, password, fullName);
      router.push("/complete-profile");
    } catch (err: any) {
      const code = err?.code || (err?.message === "auth/missing-credentials" ? "auth/missing-credentials" : "auth/unknown");
      setErrorMessage(getFriendlyAuthErrorMessage(code));
    } finally {
      setSubmitting(false);
    }
  };

  const handleGoogleSignup = async () => {
    setErrorMessage(null);
    setGoogleSubmitting(true);
    try {
      await loginWithGoogle();
      router.push("/complete-profile");
    } catch (err: any) {
      const code = err?.code || (err?.message === "auth/missing-credentials" ? "auth/missing-credentials" : "auth/unknown");
      setErrorMessage(getFriendlyAuthErrorMessage(code));
    } finally {
      setGoogleSubmitting(false);
    }
  };

  return (
    <AuthCard
      title="Create Your Account"
      subtitle="Join thousands of rural entrepreneurs and MSMEs making informed, data-backed business decisions."
      footerText="Already have an account?"
      footerLinkText="Sign in instead"
      footerLinkHref="/login"
    >
      {/* Error Alert Box */}
      {errorMessage && (
        <div className="mb-6 p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-900 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
          <div className="flex-1 font-medium">{errorMessage}</div>
        </div>
      )}

      {/* Google Sign-Up Button */}
      <button
        type="button"
        onClick={handleGoogleSignup}
        disabled={googleSubmitting || submitting || !firebaseConfigured}
        className="w-full flex items-center justify-center gap-3 py-3 px-4 border border-ivory-300 rounded-xl bg-white hover:bg-ivory-100 text-charcoal-800 text-sm font-semibold shadow-subtle hover:border-forest-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {googleSubmitting ? (
          <Loader2 className="w-4 h-4 animate-spin text-forest-800" />
        ) : (
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
            />
          </svg>
        )}
        <span>Sign up with Google</span>
      </button>

      {/* Divider */}
      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-ivory-200" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-white px-3 text-charcoal-500 font-medium tracking-wider">
            or register with email
          </span>
        </div>
      </div>

      {/* Registration Form */}
      <form onSubmit={handleRegister} className="space-y-4">
        {/* Full Name */}
        <div>
          <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
            Full Name
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-charcoal-400">
              <User className="w-4 h-4" />
            </div>
            <input
              type="text"
              required
              autoComplete="name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="e.g., Rajesh Kumar / Sunita Patel"
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 focus:border-transparent transition-all"
            />
          </div>
        </div>

        {/* Email Address */}
        <div>
          <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
            Email Address
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

        {/* Password */}
        <div>
          <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
            Password (Min 6 Characters)
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-charcoal-400">
              <Lock className="w-4 h-4" />
            </div>
            <input
              type={showPassword ? "text" : "password"}
              required
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a strong password"
              className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 focus:border-transparent transition-all"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-charcoal-400 hover:text-charcoal-700"
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Confirm Password */}
        <div>
          <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
            Confirm Password
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-charcoal-400">
              <Lock className="w-4 h-4" />
            </div>
            <input
              type={showPassword ? "text" : "password"}
              required
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 focus:border-transparent transition-all"
            />
          </div>
        </div>

        {/* Minimal Consent note */}
        <p className="text-[11px] text-charcoal-500 leading-normal pt-1">
          By registering, you agree to RuralBiz Navigator&apos;s decision-support terms. We keep your business numbers and personal plans strictly confidential.
        </p>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={submitting || googleSubmitting || !firebaseConfigured}
          className="w-full mt-2 py-3 px-4 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {submitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Creating your account...</span>
            </>
          ) : (
            <span>Create Account &amp; Continue</span>
          )}
        </button>
      </form>
    </AuthCard>
  );
}

