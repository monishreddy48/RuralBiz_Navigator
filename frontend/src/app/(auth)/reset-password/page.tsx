"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { AuthCard } from "@/components/auth/AuthCard";
import { getFriendlyAuthErrorMessage } from "@/lib/auth-errors";
import { Lock, Eye, EyeOff, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";

export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <AuthCard
          title="Verifying Security Code"
          subtitle="Please wait while we verify your password reset link."
        >
          <div className="py-12 flex justify-center items-center">
            <Loader2 className="w-8 h-8 animate-spin text-forest-800" />
          </div>
        </AuthCard>
      }
    >
      <ResetPasswordForm />
    </Suspense>
  );
}

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const oobCode = searchParams.get("oobCode");

  const { verifyResetCode, confirmReset, firebaseConfigured } = useAuth();

  const [email, setEmail] = useState<string | null>(null);
  const [verifyingCode, setVerifyingCode] = useState(true);
  const [codeValid, setCodeValid] = useState(false);

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Verify the reset code when page loads
  useEffect(() => {
    if (!oobCode) {
      setVerifyingCode(false);
      setErrorMessage("No password reset code found in this link. Please request a new link.");
      return;
    }

    if (!firebaseConfigured) {
      setVerifyingCode(false);
      return;
    }

    const checkCode = async () => {
      try {
        const userEmail = await verifyResetCode(oobCode);
        setEmail(userEmail);
        setCodeValid(true);
      } catch (err: any) {
        const code = err?.code || (err?.message === "auth/missing-credentials" ? "auth/missing-credentials" : "auth/unknown");
        setErrorMessage(getFriendlyAuthErrorMessage(code));
        setCodeValid(false);
      } finally {
        setVerifyingCode(false);
      }
    };

    checkCode();
  }, [oobCode, verifyResetCode, firebaseConfigured]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!oobCode) {
      setErrorMessage("Missing reset authorization code.");
      return;
    }

    if (newPassword.length < 6) {
      setErrorMessage("Password must be at least 6 characters long.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setErrorMessage("Passwords do not match. Please verify.");
      return;
    }

    setSubmitting(true);
    try {
      await confirmReset(oobCode, newPassword);
      setSuccess(true);
    } catch (err: any) {
      const code = err?.code || (err?.message === "auth/missing-credentials" ? "auth/missing-credentials" : "auth/unknown");
      setErrorMessage(getFriendlyAuthErrorMessage(code));
    } finally {
      setSubmitting(false);
    }
  };

  if (verifyingCode) {
    return (
      <AuthCard
        title="Verifying Security Code"
        subtitle="Please wait while we verify your password reset link."
      >
        <div className="py-8 flex flex-col items-center justify-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-forest-800" />
          <p className="text-xs text-charcoal-600 font-medium">Validating reset token...</p>
        </div>
      </AuthCard>
    );
  }

  if (success) {
    return (
      <AuthCard
        title="Password Reset Complete"
        subtitle="Your password has been successfully updated. You can now sign in with your new password."
      >
        <div className="text-center space-y-4 py-2">
          <div className="w-12 h-12 rounded-full bg-forest-100 text-forest-800 flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-7 h-7 text-forest-700" />
          </div>
          <h3 className="text-lg font-bold text-forest-950">
            Account Secured
          </h3>
          <p className="text-xs text-charcoal-600 leading-relaxed max-w-xs mx-auto">
            Your login credentials have been securely updated.
          </p>
          <div className="pt-3">
            <Link
              href="/login"
              className="inline-flex items-center justify-center w-full py-3 px-4 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-sm shadow-md transition-all"
            >
              Sign In to Your Account
            </Link>
          </div>
        </div>
      </AuthCard>
    );
  }

  if (!codeValid && errorMessage) {
    return (
      <AuthCard
        title="Invalid or Expired Link"
        subtitle="This password reset link is invalid or has already expired."
        footerText="Need help?"
        footerLinkText="Request another reset link"
        footerLinkHref="/forgot-password"
      >
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-900 text-xs flex items-start gap-2.5 mb-4">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
          <div className="flex-1 font-medium">{errorMessage}</div>
        </div>
        <Link
          href="/forgot-password"
          className="inline-flex items-center justify-center w-full py-3 px-4 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-sm shadow-md transition-all"
        >
          Request New Reset Link
        </Link>
      </AuthCard>
    );
  }

  return (
    <AuthCard
      title="Create New Password"
      subtitle={
        email
          ? `Setting a new password for ${email}.`
          : "Choose a strong, memorable password for your account."
      }
      footerText="Remembered your password?"
      footerLinkText="Back to sign in"
      footerLinkHref="/login"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {errorMessage && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-900 text-xs flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
            <div className="flex-1 font-medium">{errorMessage}</div>
          </div>
        )}

        <div>
          <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
            New Password (Min 6 Characters)
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-charcoal-400">
              <Lock className="w-4 h-4" />
            </div>
            <input
              type={showPassword ? "text" : "password"}
              required
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter new password"
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

        <div>
          <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
            Confirm New Password
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-charcoal-400">
              <Lock className="w-4 h-4" />
            </div>
            <input
              type={showPassword ? "text" : "password"}
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
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
              <span>Updating password...</span>
            </>
          ) : (
            <span>Update Password &amp; Continue</span>
          )}
        </button>
      </form>
    </AuthCard>
  );
}

