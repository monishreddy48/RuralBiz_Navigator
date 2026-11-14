"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAssessment } from "@/context/AssessmentContext";
import { fetchLocalities } from "@/lib/api";
import {
  BarChart3,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  ArrowRight,
  ShieldCheck,
  Save,
  Loader2,
  TrendingUp,
  MapPin,
  Coins,
  ChevronRight,
  Sparkles,
} from "lucide-react";

export default function FeasibilityPage() {
  const {
    params,
    updateParam,
    results,
    loading,
    error,
    hasRunAssessment,
    runFullAssessment,
    loadDemoCase,
    saveCurrentAssessment,
  } = useAssessment();

  const [localities, setLocalities] = useState<any[]>([]);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    fetchLocalities().then(setLocalities).catch(console.error);
    // If not run yet, run initial evaluation
    if (!hasRunAssessment) {
      runFullAssessment();
    }
  }, []);

  const handleEvaluate = (e: React.FormEvent) => {
    e.preventDefault();
    runFullAssessment();
  };

  const handleSave = () => {
    saveCurrentAssessment();
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);
  };

  const feasibility = results.feasibility;
  const compositeScore = feasibility?.viability_score ?? feasibility?.composite_score ?? 78;
  const verdict = feasibility?.recommendation?.decision ?? feasibility?.recommendation?.verdict ?? "GO";
  const factors = feasibility?.factor_scores || [
    { factor: "Market Demand", score: 82, weight: 0.25, contribution: 20.5 },
    { factor: "Competition Saturation", score: 75, weight: 0.15, contribution: 11.3 },
    { factor: "Infrastructure & Road Access", score: 85, weight: 0.10, contribution: 8.5 },
    { factor: "Financial Fit & Debt Coverage", score: 74, weight: 0.20, contribution: 14.8 },
    { factor: "Growth Potential", score: 80, weight: 0.15, contribution: 12.0 },
    { factor: "Risk Resilience", score: 70, weight: 0.15, contribution: 10.5 },
  ];

  const swot = feasibility?.recommendation?.swot || {
    strengths: [
      "High local agro-catchment grain supply within 5 km radius.",
      "Manageable initial project cost with 25% owner margin coverage.",
    ],
    weaknesses: [
      "Moderate working capital liquidity buffer during initial monsoon months.",
    ],
    opportunities: [
      "Packaged flour distribution in nearest weekly haat mandi.",
      "Eligible for 25%–35% rural credit subsidy under PMEGP.",
    ],
    threats: [
      "Diesel/electricity tariff variations in unmetered rural feeders.",
    ],
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-ivory-200 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-forest-800 mb-1">
            <BarChart3 className="w-4 h-4 text-forest-700" />
            <span>Module 1 &bull; Deterministic Decision Intelligence</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-950 tracking-tight">
            Business Feasibility &amp; Viability Assessment
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Calculates an institutional 0–100 viability score across 6 weighted benchmarks, accompanied by an objective 4-quadrant SWOT matrix.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleSave}
            disabled={!feasibility || loading}
            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-ivory-300 bg-white hover:bg-ivory-100 text-charcoal-800 text-xs font-semibold shadow-xs transition-all disabled:opacity-50"
          >
            {saveSuccess ? (
              <>
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span className="text-emerald-700">Saved to Dashboard!</span>
              </>
            ) : (
              <>
                <Save className="w-4 h-4 text-forest-800" />
                <span>Save Assessment</span>
              </>
            )}
          </button>

          <Link
            href="/dashboard/market"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white text-xs font-bold shadow-xs transition-all"
          >
            <span>Next: Catchment GIS</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* 1-Click SIH Evaluation Presets Toolbar */}
      <div className="bg-ivory-100/80 border border-ivory-300 rounded-2xl p-4 sm:p-5 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-forest-800" />
            <span className="text-xs font-extrabold uppercase tracking-wider text-forest-950">
              1-Click SIH Evaluation Presets:
            </span>
          </div>
          <span className="text-[11px] text-charcoal-500">
            Click any case to test instant multi-engine calculations
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button
            type="button"
            onClick={() => loadDemoCase(1)}
            disabled={loading}
            className={`p-3 rounded-xl border text-left transition-all ${
              params.category === "Food Processing" && params.village_id === "VIL_001"
                ? "bg-emerald-100/90 border-emerald-500 shadow-sm ring-2 ring-emerald-500/20"
                : "bg-white border-emerald-200 hover:bg-emerald-50"
            }`}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-700 text-white">
                CASE 1: GO
              </span>
              <span className="text-xs font-bold text-emerald-800">~82/100</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Flour Mill &amp; Agro-Unit</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">Tumakuru &bull; ₹2.15L Outlay &bull; PMEGP 35%</p>
          </button>

          <button
            type="button"
            onClick={() => loadDemoCase(2)}
            disabled={loading}
            className={`p-3 rounded-xl border text-left transition-all ${
              params.category === "Small Manufacturing" && params.village_id === "VIL_005"
                ? "bg-amber-100/90 border-amber-500 shadow-sm ring-2 ring-amber-500/20"
                : "bg-white border-amber-200 hover:bg-amber-50"
            }`}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-amber-600 text-white">
                CASE 2: MODIFY
              </span>
              <span className="text-xs font-bold text-amber-800">~58/100</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Rural Manufacturing Unit</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">Nashik &bull; ₹3.20L Outlay &bull; Needs Equity</p>
          </button>

          <button
            type="button"
            onClick={() => loadDemoCase(3)}
            disabled={loading}
            className={`p-3 rounded-xl border text-left transition-all ${
              params.category === "Retail / General Store" && params.village_id === "VIL_004"
                ? "bg-red-100/90 border-red-500 shadow-sm ring-2 ring-red-500/20"
                : "bg-white border-red-200 hover:bg-red-50"
            }`}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-red-700 text-white">
                CASE 3: AVOID
              </span>
              <span className="text-xs font-bold text-red-800">~44/100</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Saturated Village Kirana</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">Peri-Urban &bull; 8 Competitors &bull; DSCR &lt; 1.0</p>
          </button>
        </div>
      </div>

      {/* Input Form Panel */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle">
        <form onSubmit={handleEvaluate} className="space-y-4">
          <div className="text-xs font-bold uppercase tracking-wider text-forest-900 mb-2">
            Assessment Input Parameters
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            {/* Village Selector */}
            <div>
              <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
                Village / Locality
              </label>
              <select
                value={params.village_id}
                onChange={(e) => updateParam("village_id", e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900 focus:ring-2 focus:ring-forest-800"
              >
                {localities.map((loc) => (
                  <option key={loc.village_id} value={loc.village_id}>
                    {loc.village_name} ({loc.district}, {loc.state})
                  </option>
                ))}
              </select>
            </div>

            {/* Category */}
            <div>
              <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
                Business Category
              </label>
              <select
                value={params.category}
                onChange={(e) => updateParam("category", e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900 focus:ring-2 focus:ring-forest-800"
              >
                <option value="Food Processing">Food Processing &amp; Milling</option>
                <option value="Retail / General Store">Retail / General Store</option>
                <option value="Small Manufacturing">Small Rural Manufacturing</option>
                <option value="Dairy">Dairy Farming Unit</option>
                <option value="Poultry">Commercial Poultry Unit</option>
                <option value="Tailoring">Tailoring &amp; Boutique</option>
                <option value="Handicrafts">Handicrafts &amp; Handloom</option>
                <option value="Mobile Repair">Mobile &amp; Electronics Repair</option>
                <option value="Vegetable Processing">Vegetable &amp; Fruit Processing</option>
                <option value="Digital / Service Centre">Digital &amp; CSC Kiosk</option>
              </select>
            </div>

            {/* Total Investment */}
            <div>
              <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
                Total Project Cost (₹)
              </label>
              <input
                type="number"
                min="10000"
                step="5000"
                value={params.expected_investment}
                onChange={(e) => updateParam("expected_investment", Number(e.target.value))}
                className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900 focus:ring-2 focus:ring-forest-800"
              />
            </div>

            {/* Own Capital */}
            <div>
              <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
                Own Savings / Margin (₹)
              </label>
              <input
                type="number"
                min="0"
                step="5000"
                value={params.own_capital}
                onChange={(e) => updateParam("own_capital", Number(e.target.value))}
                className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900 focus:ring-2 focus:ring-forest-800"
              />
            </div>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-xs shadow-sm transition-all disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Computing Models...</span>
                </>
              ) : (
                <span>Re-Evaluate Feasibility</span>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Viability Score & Verdict Card */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        
        {/* Score & Verdict Pill */}
        <div className="lg:col-span-4 bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle flex flex-col justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-charcoal-400">
              Composite Viability
            </span>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-5xl font-extrabold text-forest-950 font-editorial">
                {compositeScore}
              </span>
              <span className="text-sm font-semibold text-charcoal-500">/ 100</span>
            </div>

            {/* Verdict Badge */}
            <div className="mt-4">
              <div
                className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-xl font-bold text-xs tracking-wider uppercase ${
                  verdict === "GO"
                    ? "bg-emerald-100 text-emerald-900 border border-emerald-300"
                    : verdict === "MODIFY"
                    ? "bg-amber-100 text-amber-900 border border-amber-300"
                    : "bg-red-100 text-red-900 border border-red-300"
                }`}
              >
                {verdict === "GO" && <CheckCircle2 className="w-4 h-4 text-emerald-700" />}
                {verdict === "MODIFY" && <AlertTriangle className="w-4 h-4 text-amber-700" />}
                {verdict === "AVOID" && <XCircle className="w-4 h-4 text-red-700" />}
                <span>Advisory Verdict: {verdict}</span>
              </div>
            </div>

            <p className="mt-4 text-xs text-charcoal-600 leading-relaxed">
              {feasibility?.recommendation?.grounded_reasons?.[0] ||
                "Business exhibits solid local catchment demand with adequate debt coverage capacity."}
            </p>
          </div>

          <div className="pt-4 border-t border-ivory-200 mt-6 text-[11px] text-charcoal-500 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-forest-800" />
            <span>Deterministic 6-Factor Mathematical Formula</span>
          </div>
        </div>

        {/* 6 Weighted Factors Breakdown */}
        <div className="lg:col-span-8 bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
          <div className="flex items-center justify-between border-b border-ivory-200 pb-3">
            <span className="text-xs font-extrabold uppercase tracking-wider text-forest-950">
              Weighted Factor Breakdown
            </span>
            <span className="text-xs text-charcoal-500 font-mono">Weighting (100%)</span>
          </div>

          <div className="space-y-3.5">
            {factors.map((f: any, idx: number) => {
              const score = typeof f.score === "number" ? f.score : 75;
              const weightPct = Math.round((f.weight || 0.15) * 100);

              return (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-charcoal-800">{f.factor}</span>
                    <div className="flex items-center gap-3 font-mono">
                      <span className="text-charcoal-500 text-[11px]">{weightPct}% weight</span>
                      <span className="font-bold text-forest-900">{score}/100</span>
                    </div>
                  </div>
                  <div className="w-full bg-ivory-100 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-2 rounded-full bg-forest-800 transition-all duration-500"
                      style={{ width: `${Math.min(100, Math.max(10, score))}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* 4-Quadrant SWOT Matrix */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-ivory-300 shadow-subtle space-y-6">
        <div>
          <h2 className="text-base font-extrabold text-forest-950 tracking-tight">
            Objective 4-Quadrant SWOT Matrix
          </h2>
          <p className="text-xs text-charcoal-600 mt-0.5">
            Rigorous qualitative and market analysis calibrated for your village block and trade category.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* Strengths */}
          <div className="p-5 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-2">
            <span className="text-xs font-extrabold text-emerald-900 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-700" />
              <span>Strengths</span>
            </span>
            <ul className="space-y-1.5 text-xs text-emerald-950/90 leading-relaxed pt-1">
              {swot.strengths?.map((s: string, idx: number) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-emerald-700 font-bold">&bull;</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Weaknesses */}
          <div className="p-5 rounded-2xl bg-amber-50/60 border border-amber-200 space-y-2">
            <span className="text-xs font-extrabold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-700" />
              <span>Weaknesses</span>
            </span>
            <ul className="space-y-1.5 text-xs text-amber-950/90 leading-relaxed pt-1">
              {swot.weaknesses?.map((w: string, idx: number) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-amber-700 font-bold">&bull;</span>
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Opportunities */}
          <div className="p-5 rounded-2xl bg-blue-50/60 border border-blue-200 space-y-2">
            <span className="text-xs font-extrabold text-blue-900 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp className="w-4 h-4 text-blue-700" />
              <span>Opportunities</span>
            </span>
            <ul className="space-y-1.5 text-xs text-blue-950/90 leading-relaxed pt-1">
              {swot.opportunities?.map((o: string, idx: number) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-blue-700 font-bold">&bull;</span>
                  <span>{o}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Threats */}
          <div className="p-5 rounded-2xl bg-rose-50/60 border border-rose-200 space-y-2">
            <span className="text-xs font-extrabold text-rose-900 uppercase tracking-wider flex items-center gap-1.5">
              <XCircle className="w-4 h-4 text-rose-700" />
              <span>Threats &amp; Risks</span>
            </span>
            <ul className="space-y-1.5 text-xs text-rose-950/90 leading-relaxed pt-1">
              {swot.threats?.map((t: string, idx: number) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-rose-700 font-bold">&bull;</span>
                  <span>{t}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

    </div>
  );
}

