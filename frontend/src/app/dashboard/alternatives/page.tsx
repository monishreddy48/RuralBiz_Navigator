"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAssessment } from "@/context/AssessmentContext";
import { fetchRankedAlternatives } from "@/lib/api";
import {
  Lightbulb,
  CheckCircle2,
  TrendingUp,
  ArrowRight,
  ChevronRight,
  ShieldCheck,
  Check,
  Loader2,
} from "lucide-react";

export default function AlternativesPage() {
  const router = useRouter();
  const { params, updateParam, results, runFullAssessment } = useAssessment();

  const [alternatives, setAlternatives] = useState<any[]>(results.alternatives || []);
  const [loading, setLoading] = useState(false);
  const [adoptingId, setAdoptingId] = useState<string | null>(null);

  useEffect(() => {
    if (!alternatives || alternatives.length === 0) {
      setLoading(true);
      fetchRankedAlternatives(params.village_id, params.own_capital)
        .then(setAlternatives)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [params.village_id, params.own_capital]);

  const handleAdopt = async (alt: any) => {
    setAdoptingId(alt.business_id);
    updateParam("category", alt.category || alt.business_name);
    if (alt.typical_investment) {
      updateParam("expected_investment", Number(alt.typical_investment));
    }
    await runFullAssessment({
      ...params,
      category: alt.category || alt.business_name,
      expected_investment: alt.typical_investment || params.expected_investment,
    });
    setAdoptingId(null);
    router.push("/dashboard/feasibility");
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-ivory-200 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-forest-800 mb-1">
            <Lightbulb className="w-4 h-4 text-forest-700" />
            <span>Module 6 &bull; Capital-Matched Opportunity Ranking</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-950 tracking-tight">
            Business Alternatives Recommender
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Compare all 10 micro-enterprise sectors ranked for your village catchment and savings budget of ₹{params.own_capital.toLocaleString("en-IN")}.
          </p>
        </div>

        <Link
          href="/dashboard/assistant"
          className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white text-xs font-bold shadow-xs transition-all self-start sm:self-auto"
        >
          <span>Next: AI Assistant</span>
          <ChevronRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Alternatives Grid */}
      <div className="space-y-4">
        {loading ? (
          <div className="py-16 text-center">
            <Loader2 className="w-8 h-8 animate-spin text-forest-800 mx-auto mb-2" />
            <p className="text-xs text-charcoal-600 font-medium">Ranking 10 enterprise sectors...</p>
          </div>
        ) : alternatives.length === 0 ? (
          <div className="py-12 text-center bg-white rounded-2xl border border-ivory-300 text-xs text-charcoal-500">
            No alternatives returned from backend. Try refreshing.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {alternatives.map((alt: any, idx: number) => {
              const isSelected = params.category === alt.category || params.category === alt.business_name;
              const rank = alt.rank || idx + 1;
              const score = alt.viability_score || alt.composite_score || 75;

              return (
                <div
                  key={idx}
                  className={`bg-white rounded-2xl p-6 border shadow-subtle flex flex-col justify-between transition-all ${
                    isSelected
                      ? "border-forest-800 ring-2 ring-forest-800/10"
                      : "border-ivory-300 hover:border-forest-600"
                  }`}
                >
                  <div>
                    {/* Rank & Viability Badge */}
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className="w-6 h-6 rounded-full bg-forest-900 text-white font-bold text-xs flex items-center justify-center">
                          {rank}
                        </span>
                        <span className="text-[11px] font-bold uppercase tracking-wider text-charcoal-500">
                          {alt.category}
                        </span>
                      </div>
                      <span className="px-2.5 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-extrabold">
                        {score}/100 Viability
                      </span>
                    </div>

                    <h3 className="text-base font-bold text-forest-950 mb-1">
                      {alt.business_name}
                    </h3>
                    <p className="text-xs text-charcoal-600 leading-relaxed mb-4">
                      {alt.short_description || "High rural demand with low working capital risk."}
                    </p>

                    {/* Financial Estimates Grid */}
                    <div className="grid grid-cols-3 gap-2 p-3 bg-ivory-50 rounded-xl text-center mb-4 text-xs font-mono">
                      <div>
                        <span className="text-[10px] text-charcoal-500 font-sans block">OUTLAY</span>
                        <span className="font-bold text-charcoal-900">
                          ₹{alt.typical_investment ? (alt.typical_investment / 1000).toFixed(0) : "215"}k
                        </span>
                      </div>
                      <div>
                        <span className="text-[10px] text-charcoal-500 font-sans block">MONTHLY NET</span>
                        <span className="font-bold text-emerald-800">
                          ₹{alt.typical_monthly_profit ? (alt.typical_monthly_profit / 1000).toFixed(1) : "26"}k
                        </span>
                      </div>
                      <div>
                        <span className="text-[10px] text-charcoal-500 font-sans block">PAYBACK</span>
                        <span className="font-bold text-charcoal-900">
                          {alt.payback_months || 14} Mo.
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Adopt Button */}
                  <div className="pt-2">
                    {isSelected ? (
                      <div className="w-full py-2.5 rounded-xl bg-forest-100 text-forest-900 font-bold text-xs text-center flex items-center justify-center gap-1.5">
                        <Check className="w-4 h-4 text-forest-800" />
                        <span>Currently Active Assessment</span>
                      </div>
                    ) : (
                      <button
                        onClick={() => handleAdopt(alt)}
                        disabled={adoptingId !== null}
                        className="w-full py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-xs shadow-xs transition-all flex items-center justify-center gap-1.5 disabled:opacity-50"
                      >
                        {adoptingId === alt.business_id ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <>
                            <span>Select &amp; Evaluate This Sector</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

    </div>
  );
}

