"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useAssessment } from "@/context/AssessmentContext";
import {
  Sparkles,
  MapPin,
  Briefcase,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  BarChart3,
  Lightbulb,
  CreditCard,
  TrendingDown,
  Building2,
  Bot,
  FileSpreadsheet,
  ArrowRight,
  Play,
  RotateCcw,
  Trash2,
  ExternalLink,
  ChevronRight,
  Loader2,
} from "lucide-react";

export default function DashboardOverviewPage() {
  const router = useRouter();
  const { user, userProfile } = useAuth();
  const {
    params,
    results,
    loading,
    hasRunAssessment,
    loadDemoCase,
    savedAssessments,
    deleteSavedAssessment,
  } = useAssessment();

  const [loadingCase, setLoadingCase] = useState<number | null>(null);

  const handleRunDemo = async (caseId: 1 | 2 | 3) => {
    setLoadingCase(caseId);
    try {
      await loadDemoCase(caseId);
      router.push("/dashboard/feasibility");
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingCase(null);
    }
  };

  // Calculate profile completion percentage
  let profilePercent = 25; // Registered
  if (userProfile?.fullName) profilePercent += 15;
  if (userProfile?.state && userProfile?.district) profilePercent += 20;
  if (userProfile?.village) profilePercent += 20;
  if (userProfile?.businessCategory) profilePercent += 20;

  const isProfileComplete = userProfile?.profileCompleted || profilePercent >= 90;

  const services = [
    {
      title: "Business Feasibility",
      desc: "Deterministic 0–100 viability score, 6-factor weightings, and objective 4-quadrant SWOT.",
      href: "/dashboard/feasibility",
      icon: BarChart3,
      tag: "Intelligence",
      status: results.feasibility ? `Score: ${results.feasibility.composite_score}/100` : "Ready to evaluate",
    },
    {
      title: "Hyperlocal Market Analysis",
      desc: "5 km walk-in & 10 km weekly haat catchment mapping, competitor entities and demand gaps.",
      href: "/dashboard/market",
      icon: MapPin,
      tag: "GIS Catchment",
      status: results.catchment ? `${results.catchment.competitor_count} competitors mapped` : "Ready to map",
    },
    {
      title: "Financial Planning & EMI",
      desc: "Reducing-balance debt amortization, 60-month schedules, break-even unit volumes & DSCR.",
      href: "/dashboard/financial",
      icon: CreditCard,
      tag: "Debt Math",
      status: results.finance ? `EMI: ₹${Math.round(results.finance.monthly_emi)}/mo` : "Ready to calculate",
    },
    {
      title: "What-If Stress Simulator",
      desc: "Simulate rural demand contractions, inflation, and rate shocks to verify enterprise survival.",
      href: "/dashboard/simulator",
      icon: TrendingDown,
      tag: "Risk Modeling",
      status: results.stress ? results.stress.survival_status : "Ready to simulate",
    },
    {
      title: "Government Scheme Navigator",
      desc: "Rule-based matching against verified programs (PMEGP 25%–35% subsidy, MUDRA, PMFME).",
      href: "/dashboard/schemes",
      icon: Building2,
      tag: "Subsidies",
      status: results.schemes ? `${results.schemes.length} schemes matched` : "Ready to match",
    },
    {
      title: "Business Alternatives",
      desc: "Compare and rank all 10 rural micro-enterprise trades matched to your exact available savings.",
      href: "/dashboard/alternatives",
      icon: Lightbulb,
      tag: "Comparison",
      status: results.alternatives ? "10 trades ranked" : "Ready to rank",
    },
    {
      title: "AI Business Advisor",
      desc: "Explainable multilingual guidance powered by Gemini in English, Hindi, Telugu, and Kannada.",
      href: "/dashboard/assistant",
      icon: Bot,
      tag: "Multilingual AI",
      status: "Online & Grounded",
    },
    {
      title: "DPR Report Generator",
      desc: "Download an institutional 20-section Detailed Project Report PDF for commercial bank appraisal.",
      href: "/dashboard/dpr",
      icon: FileSpreadsheet,
      tag: "Bank Appraisal",
      status: "PDF Generator Ready",
    },
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* 1. Personalized Welcome Header */}
      <div className="bg-gradient-to-r from-forest-950 via-forest-900 to-forest-800 text-white rounded-3xl p-6 sm:p-8 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden">
        <div className="space-y-2 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-forest-800/80 border border-forest-700 text-forest-200 text-xs font-semibold">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Authenticated Entrepreneur Cockpit</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome, {userProfile?.fullName || user?.displayName || "Entrepreneur"}!
          </h1>
          <p className="text-xs sm:text-sm text-forest-100/80 max-w-xl">
            Evaluate business opportunities, calculate true reducing-balance debt math, and generate bankable project proposals before committing capital.
          </p>
        </div>

        {/* Quick Primary Assessment Action */}
        <div className="flex flex-wrap items-center gap-3 relative z-10">
          <Link
            href="/dashboard/feasibility"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white hover:bg-ivory-100 text-forest-950 font-bold text-sm shadow-md transition-all active:scale-[0.98]"
          >
            <span>{hasRunAssessment ? "Continue Assessment" : "Start New Assessment"}</span>
            <ArrowRight className="w-4 h-4 text-forest-800" />
          </Link>
        </div>
      </div>

      {/* 2. Entrepreneur Profile & Location Status Widget */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Profile Completion Card */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-charcoal-400">
                Profile Status
              </span>
              <span
                className={`text-[10px] font-extrabold px-2 py-0.5 rounded-md ${
                  isProfileComplete
                    ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                    : "bg-amber-50 text-amber-800 border border-amber-200"
                }`}
              >
                {isProfileComplete ? "PROFILE COMPLETE" : `${profilePercent}% COMPLETED`}
              </span>
            </div>

            <h3 className="text-base font-bold text-charcoal-900 mb-1">
              {isProfileComplete ? "Verified Locality Details" : "Complete Locality Profile"}
            </h3>
            <p className="text-xs text-charcoal-600 mb-4">
              {isProfileComplete
                ? "Your rural catchment numbers and scheme matching are calibrated to your profile."
                : "Add your village, district, and enterprise stage for accurate catchment analysis."}
            </p>

            {/* Progress bar */}
            <div className="w-full bg-ivory-200 rounded-full h-2 mb-4 overflow-hidden">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${
                  isProfileComplete ? "bg-emerald-600" : "bg-amber-500"
                }`}
                style={{ width: `${profilePercent}%` }}
              />
            </div>
          </div>

          <Link
            href="/complete-profile"
            className="text-xs font-bold text-forest-800 hover:text-forest-950 flex items-center gap-1 transition-colors"
          >
            <span>{isProfileComplete ? "Edit Profile Settings" : "Finish Profile Setup"}</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Selected Village & Catchment */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-charcoal-400">
                Target Locality
              </span>
              <MapPin className="w-4 h-4 text-forest-700" />
            </div>

            <h3 className="text-base font-bold text-charcoal-900 mb-1">
              {userProfile?.village
                ? `${userProfile.village}, ${userProfile.district || ""}`
                : "Demo Village A (Agri Hub)"}
            </h3>
            <p className="text-xs text-charcoal-600">
              State: <strong className="text-charcoal-800">{userProfile?.state || "Punjab / Maharashtra"}</strong>
            </p>
            <div className="mt-3 text-[11px] text-charcoal-500 space-y-1">
              <p>&bull; 5 km Daily Walk-in Catchment radius</p>
              <p>&bull; 10 km Weekly Haat / Mandi radius</p>
            </div>
          </div>

          <Link
            href="/dashboard/market"
            className="text-xs font-bold text-forest-800 hover:text-forest-950 flex items-center gap-1 transition-colors mt-4"
          >
            <span>Inspect Hyperlocal GIS</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Selected Enterprise Sector */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-charcoal-400">
                Enterprise Sector
              </span>
              <Briefcase className="w-4 h-4 text-forest-700" />
            </div>

            <h3 className="text-base font-bold text-charcoal-900 mb-1">
              {params.category || userProfile?.businessCategory || "Food Processing"}
            </h3>
            <p className="text-xs text-charcoal-600">
              Lifecycle:{" "}
              <strong className="text-charcoal-800">
                {userProfile?.businessStage === "existing_business"
                  ? "Existing Business Expansion"
                  : "New Business Plan"}
              </strong>
            </p>
            <div className="mt-3 text-[11px] text-charcoal-500 space-y-1">
              <p>&bull; Target Capital: ₹{params.expected_investment.toLocaleString("en-IN")}</p>
              <p>&bull; Own Savings: ₹{params.own_capital.toLocaleString("en-IN")}</p>
            </div>
          </div>

          <Link
            href="/dashboard/financial"
            className="text-xs font-bold text-forest-800 hover:text-forest-950 flex items-center gap-1 transition-colors mt-4"
          >
            <span>Review Loan Structuring</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

      </div>

      {/* 3. Demo Case Loaders (For Quick Assessment & SIH Demonstration) */}
      <div className="p-6 rounded-2xl bg-white border border-ivory-300 shadow-subtle">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-950 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-forest-700" />
              <span>Instant Assessment Scenarios (1-Click Demonstration)</span>
            </h2>
            <p className="text-xs text-charcoal-600 mt-1">
              Test realistic rural MSME scenarios pre-configured with local unit economics, competitor mapping, and verified schemes.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Case 1 */}
          <button
            onClick={() => handleRunDemo(1)}
            disabled={loadingCase !== null}
            className="text-left p-4 rounded-xl border border-emerald-200 bg-emerald-50/50 hover:bg-emerald-50 hover:border-emerald-500 transition-all group flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                  VERDICT: GO
                </span>
                {loadingCase === 1 ? (
                  <Loader2 className="w-4 h-4 animate-spin text-emerald-700" />
                ) : (
                  <Play className="w-3.5 h-3.5 text-emerald-700 group-hover:translate-x-0.5 transition-transform" />
                )}
              </div>
              <h4 className="text-xs font-bold text-charcoal-900">Case 1: Flour Mill &amp; Agro-Unit</h4>
              <p className="text-[11px] text-charcoal-600 mt-1">
                ₹2.15L Outlay &bull; High unmet mandi demand &bull; PMEGP 35% subsidy match.
              </p>
            </div>
            <span className="text-[11px] font-bold text-emerald-800 mt-3 flex items-center gap-1">
              Load &amp; Evaluate &rarr;
            </span>
          </button>

          {/* Case 2 */}
          <button
            onClick={() => handleRunDemo(2)}
            disabled={loadingCase !== null}
            className="text-left p-4 rounded-xl border border-amber-200 bg-amber-50/50 hover:bg-amber-50 hover:border-amber-500 transition-all group flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800">
                  VERDICT: MODIFY
                </span>
                {loadingCase === 2 ? (
                  <Loader2 className="w-4 h-4 animate-spin text-amber-700" />
                ) : (
                  <Play className="w-3.5 h-3.5 text-amber-700 group-hover:translate-x-0.5 transition-transform" />
                )}
              </div>
              <h4 className="text-xs font-bold text-charcoal-900">Case 2: Rural Manufacturing Unit</h4>
              <p className="text-[11px] text-charcoal-600 mt-1">
                ₹3.20L Outlay &bull; Heavy machinery costs &bull; Requires working capital buffer.
              </p>
            </div>
            <span className="text-[11px] font-bold text-amber-800 mt-3 flex items-center gap-1">
              Load &amp; Evaluate &rarr;
            </span>
          </button>

          {/* Case 3 */}
          <button
            onClick={() => handleRunDemo(3)}
            disabled={loadingCase !== null}
            className="text-left p-4 rounded-xl border border-red-200 bg-red-50/50 hover:bg-red-50 hover:border-red-500 transition-all group flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-100 text-red-800">
                  VERDICT: AVOID
                </span>
                {loadingCase === 3 ? (
                  <Loader2 className="w-4 h-4 animate-spin text-red-700" />
                ) : (
                  <Play className="w-3.5 h-3.5 text-red-700 group-hover:translate-x-0.5 transition-transform" />
                )}
              </div>
              <h4 className="text-xs font-bold text-charcoal-900">Case 3: Saturated Kirana Store</h4>
              <p className="text-[11px] text-charcoal-600 mt-1">
                ₹1.90L Outlay &bull; 8 competitor entities in 1 km &bull; High debt insolvency risk.
              </p>
            </div>
            <span className="text-[11px] font-bold text-red-800 mt-3 flex items-center gap-1">
              Load &amp; Evaluate &rarr;
            </span>
          </button>
        </div>
      </div>

      {/* 4. Eight Core Decision-Support Services Grid */}
      <div>
        <div className="mb-4">
          <h2 className="text-base font-extrabold text-forest-950 tracking-tight">
            Decision-Support Intelligence Modules
          </h2>
          <p className="text-xs text-charcoal-600">
            Every module operates independently on your selected business parameters and local catchment benchmarks.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {services.map((svc, idx) => {
            const Icon = svc.icon;
            return (
              <Link
                key={idx}
                href={svc.href}
                className="bg-white rounded-2xl p-5 border border-ivory-300 shadow-subtle hover:shadow-card hover:border-forest-700 transition-all duration-200 flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-10 h-10 rounded-xl bg-forest-50 text-forest-900 flex items-center justify-center group-hover:bg-forest-900 group-hover:text-white transition-colors">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-[10px] font-bold uppercase tracking-wide text-forest-800 bg-forest-50 px-2 py-0.5 rounded-md">
                      {svc.tag}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-charcoal-900 group-hover:text-forest-950 transition-colors">
                    {svc.title}
                  </h3>
                  <p className="text-xs text-charcoal-600 mt-1.5 leading-relaxed">
                    {svc.desc}
                  </p>
                </div>

                <div className="mt-5 pt-3 border-t border-ivory-100 flex items-center justify-between text-xs font-semibold text-forest-800">
                  <span className="text-[11px] font-medium text-charcoal-500">{svc.status}</span>
                  <span className="flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                    Open &rarr;
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* 5. Recent Activity & Saved Reports (With Realistic Empty State) */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-950">
              Recent Activity &amp; Saved DPR Reports
            </h2>
            <p className="text-xs text-charcoal-600 mt-0.5">
              Access your previous business assessments, loan amortization schedules, and official project proposals.
            </p>
          </div>
          {savedAssessments.length > 0 && (
            <span className="text-xs font-semibold text-forest-800">
              {savedAssessments.length} Saved {savedAssessments.length === 1 ? "Report" : "Reports"}
            </span>
          )}
        </div>

        {savedAssessments.length === 0 ? (
          /* Realistic Empty State for New Users */
          <div className="py-12 px-4 text-center border-2 border-dashed border-ivory-300 rounded-2xl bg-ivory-50/50">
            <div className="w-12 h-12 rounded-full bg-forest-100 text-forest-800 flex items-center justify-center mx-auto mb-3">
              <FileSpreadsheet className="w-6 h-6 text-forest-700" />
            </div>
            <h3 className="text-sm font-bold text-charcoal-900 mb-1">
              No Business Assessments Saved Yet
            </h3>
            <p className="text-xs text-charcoal-600 max-w-md mx-auto mb-5 leading-relaxed">
              When you evaluate an enterprise idea, your complete 6-factor viability breakdown, loan amortization schedule, and bankable DPR proposal will appear here for 1-click retrieval.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3">
              <Link
                href="/dashboard/feasibility"
                className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-xs shadow-sm transition-all"
              >
                <span>Run First Feasibility Assessment</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
              <button
                onClick={() => handleRunDemo(1)}
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-ivory-300 bg-white hover:bg-ivory-100 text-charcoal-800 font-semibold text-xs transition-all"
              >
                <Play className="w-3.5 h-3.5 text-forest-800" />
                <span>Load Sample Flour Mill</span>
              </button>
            </div>
          </div>
        ) : (
          /* List of Saved Assessments */
          <div className="divide-y divide-ivory-200">
            {savedAssessments.map((item) => (
              <div
                key={item.id}
                className="py-3.5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-xs text-charcoal-900">{item.category}</span>
                    <span
                      className={`text-[10px] font-extrabold px-2 py-0.2 rounded ${
                        item.verdict === "GO"
                          ? "bg-emerald-100 text-emerald-800"
                          : item.verdict === "MODIFY"
                          ? "bg-amber-100 text-amber-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {item.verdict} &bull; {item.viabilityScore}/100
                    </span>
                  </div>
                  <div className="text-[11px] text-charcoal-500">
                    Locality: {item.villageName} &bull; Investment: ₹{item.params.expected_investment.toLocaleString("en-IN")} &bull; Saved on {item.date}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    href="/dashboard/feasibility"
                    className="px-3 py-1.5 rounded-lg border border-ivory-300 text-xs font-semibold text-charcoal-700 hover:bg-ivory-100 transition-colors"
                  >
                    View Feasibility
                  </Link>
                  <Link
                    href="/dashboard/dpr"
                    className="px-3 py-1.5 rounded-lg bg-forest-900 text-white text-xs font-bold hover:bg-forest-950 transition-colors"
                  >
                    Download DPR PDF
                  </Link>
                  <button
                    onClick={() => deleteSavedAssessment(item.id)}
                    className="p-1.5 text-charcoal-400 hover:text-red-600 rounded-lg transition-colors"
                    title="Delete assessment"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
