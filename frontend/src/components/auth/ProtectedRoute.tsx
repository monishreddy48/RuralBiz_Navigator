"use client";

import React, { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Loader2, ShieldCheck } from "lucide-react";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireCompletedProfile?: boolean;
}

export function ProtectedRoute({
  children,
  requireCompletedProfile = false,
}: ProtectedRouteProps) {
  const { user, userProfile, loading, firebaseConfigured } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (loading) return;

    if (!user) {
      // Redirect to login preserving the target route
      const redirectUrl = `/login?redirect=${encodeURIComponent(pathname)}`;
      router.push(redirectUrl);
      return;
    }

    // If profile completion is strictly required and user has not completed profile
    if (
      requireCompletedProfile &&
      userProfile &&
      !userProfile.profileCompleted &&
      pathname !== "/complete-profile"
    ) {
      router.push("/complete-profile");
    }
  }, [user, userProfile, loading, pathname, router, requireCompletedProfile]);

  // Loading State
  if (loading) {
    return (
      <div className="min-h-screen bg-[#FBF9F2] flex flex-col items-center justify-center p-4">
        <div className="w-16 h-16 rounded-2xl bg-forest-900 text-ivory-50 flex items-center justify-center shadow-lg mb-4 animate-pulse">
          <ShieldCheck className="w-8 h-8 text-forest-300" />
        </div>
        <div className="flex items-center gap-2 text-forest-950 font-semibold text-sm">
          <Loader2 className="w-4 h-4 animate-spin text-forest-800" />
          <span>Verifying credentials &amp; permissions...</span>
        </div>
        <p className="text-xs text-charcoal-500 mt-2">
          RuralBiz Navigator Secure Session
        </p>
      </div>
    );
  }

  // Not authenticated
  if (!user) {
    return null;
  }

  // Authenticated
  return <>{children}</>;
}

