"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import {
  LogOut,
  User,
  MapPin,
  Briefcase,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Languages,
  ArrowRight,
  ExternalLink,
  Edit3,
  Loader2,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <ProtectedRoute requireCompletedProfile={false}>
      <DashboardContent />
    </ProtectedRoute>
  );
}

function DashboardContent() {
  const router = useRouter();
  const { user, userProfile, logout } = useAuth();
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
      router.push("/login");
    } catch (err) {
      console.error("Logout error:", err);
      setLoggingOut(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FBF9F2]">
      
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-ivory-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            
            {/* Brand */}
            <Link href="/" className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-forest-900 text-ivory-50 flex items-center justify-center font-bold text-lg shadow-sm">
                🌾
              </div>
              <span className="font-extrabold text-lg tracking-tight text-forest-950 font-sans">
                RuralBiz <span className="text-forest-700 font-semibold">Navigator</span>
              </span>
            </Link>

            {/* User Session & Logout */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex flex-col text-right">
                <span className="text-xs font-bold text-charcoal-900">
                  {userProfile?.fullName || user?.displayName || "Entrepreneur"}
                </span>
                <span className="text-[11px] text-charcoal-500 font-mono">
                  {user?.email}
                </span>
              </div>

              <button
                onClick={handleLogout}
                disabled={loggingOut}
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl border border-ivory-300 bg-ivory-50 hover:bg-ivory-100 text-charcoal-700 hover:text-red-700 text-xs font-semibold transition-all disabled:opacity-50"
                aria-label="Sign Out"
              >
                {loggingOut ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <LogOut className="w-3.5 h-3.5" />
                )}
                <span>Sign Out</span>
              </button>
            </div>

          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
        
        {/* Verification Banner */}
        <div className="bg-gradient-to-r from-forest-950 via-forest-900 to-forest-800 text-white rounded-3xl p-6 sm:p-8 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-forest-800/80 border border-forest-700 text-forest-200 text-xs font-semibold">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Authenticated Session Active &bull; Firebase Modular SDK</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome, {userProfile?.fullName || user?.displayName || "Rural Entrepreneur"}!
            </h1>
            <p className="text-xs sm:text-sm text-forest-100/80 max-w-xl">
              Your authentication session is verified and persists across page reloads. All routes are secured.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/complete-profile"
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white border border-white/20 text-xs font-bold transition-all"
            >
              <Edit3 className="w-3.5 h-3.5" />
              <span>Edit Profile</span>
            </Link>

            <Link
              href="http://localhost:8501"
              target="_blank"
              className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-forest-950 text-xs font-bold shadow-md transition-all"
            >
              <span>Open Streamlit Engine</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* Entrepreneur Profile Summary Card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1: Identity & Credentials */}
          <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-extrabold uppercase tracking-wider text-forest-900">
                Auth Identity
              </span>
              <span className="px-2 py-0.5 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-800 text-[10px] font-bold">
                VERIFIED
              </span>
            </div>
            <div className="space-y-2 text-xs">
              <div>
                <span className="text-charcoal-500 block">UID</span>
                <span className="font-mono text-charcoal-900 break-all">{user?.uid}</span>
              </div>
              <div>
                <span className="text-charcoal-500 block">Email</span>
                <span className="font-medium text-charcoal-900">{user?.email || "N/A"}</span>
              </div>
              <div>
                <span className="text-charcoal-500 block">Provider</span>
                <span className="font-medium text-charcoal-900">
                  {user?.providerData?.[0]?.providerId || "password"}
                </span>
              </div>
            </div>
          </div>

          {/* Card 2: Locality & Language */}
          <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-extrabold uppercase tracking-wider text-forest-900">
                Locality Catchment
              </span>
              <MapPin className="w-4 h-4 text-forest-700" />
            </div>
            <div className="space-y-2 text-xs">
              <div>
                <span className="text-charcoal-500 block">State &amp; District</span>
                <span className="font-bold text-charcoal-900">
                  {userProfile?.state ? `${userProfile.district}, ${userProfile.state}` : "Profile Pending"}
                </span>
              </div>
              <div>
                <span className="text-charcoal-500 block">Village / Locality</span>
                <span className="font-medium text-charcoal-900">
                  {userProfile?.village || "Not specified yet"}
                </span>
              </div>
              <div>
                <span className="text-charcoal-500 block">Preferred Advisory Language</span>
                <span className="font-medium text-forest-800 uppercase">
                  {userProfile?.preferredLanguage || "en"}
                </span>
              </div>
            </div>
          </div>

          {/* Card 3: Enterprise Focus */}
          <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-extrabold uppercase tracking-wider text-forest-900">
                Target Business
              </span>
              <Briefcase className="w-4 h-4 text-forest-700" />
            </div>
            <div className="space-y-2 text-xs">
              <div>
                <span className="text-charcoal-500 block">Trade Sector</span>
                <span className="font-bold text-charcoal-900">
                  {userProfile?.businessCategory || "Food Processing & Milling"}
                </span>
              </div>
              <div>
                <span className="text-charcoal-500 block">Stage</span>
                <span className="font-medium text-charcoal-900">
                  {userProfile?.businessStage === "existing_business"
                    ? "Existing Business Expansion"
                    : "New Business Plan"}
                </span>
              </div>
              <div>
                <span className="text-charcoal-500 block">Profile Status</span>
                <span className="font-semibold text-forest-700">
                  {userProfile?.profileCompleted ? "Complete & Saved" : "Basic / Incomplete"}
                </span>
              </div>
            </div>
          </div>

        </div>

        {/* Phase 3 Ready Notice */}
        <div className="p-6 rounded-2xl bg-white border border-ivory-300 shadow-subtle text-xs text-charcoal-600 space-y-2">
          <div className="flex items-center gap-2 font-bold text-forest-950 text-sm">
            <CheckCircle2 className="w-4 h-4 text-forest-700" />
            <span>Authentication Architecture Verification Complete</span>
          </div>
          <p>
            Phase 3 Authentication covers modular Firebase login, registration, Google OAuth, password reset, session persistence, protected route redirection, logout, and post-registration rural entrepreneur profiles.
          </p>
        </div>

      </main>

    </div>
  );
}

