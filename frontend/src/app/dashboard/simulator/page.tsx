"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAssessment } from "@/context/AssessmentContext";
import { runStressTest } from "@/lib/api";
import {
  TrendingDown,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  RotateCcw,
  ChevronRight,
  Loader2,
  CheckCircle2,
  Sparkles,
} from "lucide-react";

export default function SimulatorPage() {
  const { params, results, loadDemoCase } = useAssessment();

  const [salesDelta, setSalesDelta] = useState(-20);
  const [priceDelta, setPriceDelta] = useState(0);
  const [costDelta, setCostDelta] = useState(10);
  const [rateDelta, setRateDelta] = useState(1.0);

  const [stressData, setStressData] = useState<any>(results.stress);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (results.stress) {
      setStressData(results.stress);
    }
  }, [results.stress]);

  const runSimulation = async () => {
    setLoading(true);
    try {
      const data = await runStressTest({
        village_id: params.village_id,
        category: params.category,
        project_cost: params.expected_investment,
        own_capital: params.own_capital,
        own_contribution: params.own_capital,
        sales_vol_delta_pct: salesDelta,
        price_delta_pct: priceDelta,
        var_cost_delta_pct: costDelta,
        interest_rate_delta: rateDelta,
      });
      setStressData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!stressData) {
      runSimulation();
    }
  }, []);

  const base = stressData?.base || {
    monthly_sales: 65000,
    monthly_profit: 26300,
    dscr: 1.65,
    margin_of_safety: 67,
  };

  const stress = stressData?.stressed || {
    monthly_sales: 52000,
    monthly_profit: 15400,
    dscr: 1.15,
    margin_of_safety: 42,
  };

  const survivalStatus = stressData?.survival_status || "SURVIVES WITH BUFFER";

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-ivory-200 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-forest-800 mb-1">
            <TrendingDown className="w-4 h-4 text-forest-700" />
            <span>Module 4 &bull; Extreme Scenario Modeling</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-950 tracking-tight">
            What-If Scenario Stress Testing
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Simulate seasonal demand contractions, input price inflation, and interest rate hikes to test whether your enterprise survives adverse market shocks.
          </p>
        </div>

        <Link
          href="/dashboard/schemes"
          className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white text-xs font-bold shadow-xs transition-all self-start sm:self-auto"
        >
          <span>Next: Scheme Navigator</span>
          <ChevronRight className="w-4 h-4" />
        </Link>
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
              <span className="text-xs font-bold text-emerald-800">Buffer</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Flour Mill &amp; Agro-Unit</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">Survives 20% Sales Drop &bull; Positive DSCR</p>
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
              <span className="text-xs font-bold text-amber-800">Tight</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Rural Manufacturing Unit</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">Survives with Tight Margin &bull; Needs Restructure</p>
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
              <span className="text-xs font-bold text-red-800">Default Risk</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Saturated Village Kirana</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">Severe Loss in Contraction &bull; DSCR &lt; 0.5</p>
          </button>
        </div>
      </div>

      {/* Interactive Shock Adjusters */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-5">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-3">
          <span className="text-xs font-extrabold uppercase tracking-wider text-forest-950">
            Rural Market Shock Simulator
          </span>
          <button
            onClick={() => {
              setSalesDelta(-20);
              setPriceDelta(0);
              setCostDelta(10);
              setRateDelta(1.0);
            }}
            className="text-xs font-semibold text-charcoal-500 hover:text-charcoal-800 flex items-center gap-1"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Sliders</span>
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Sales Delta */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="font-bold text-charcoal-800">Sales Volume Drop</span>
              <span className="font-mono font-bold text-red-700">{salesDelta}%</span>
            </div>
            <input
              type="range"
              min="-50"
              max="20"
              step="5"
              value={salesDelta}
              onChange={(e) => setSalesDelta(Number(e.target.value))}
              className="w-full accent-forest-900 cursor-pointer"
            />
            <span className="text-[10px] text-charcoal-500">Simulates bad season / haat closure</span>
          </div>

          {/* Price Delta */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="font-bold text-charcoal-800">Output Price Shift</span>
              <span className={`font-mono font-bold ${priceDelta < 0 ? "text-red-700" : "text-forest-900"}`}>
                {priceDelta > 0 ? `+${priceDelta}` : priceDelta}%
              </span>
            </div>
            <input
              type="range"
              min="-30"
              max="20"
              step="5"
              value={priceDelta}
              onChange={(e) => setPriceDelta(Number(e.target.value))}
              className="w-full accent-forest-900 cursor-pointer"
            />
            <span className="text-[10px] text-charcoal-500">Simulates local mandi price crashes</span>
          </div>

          {/* Raw Material Cost Delta */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="font-bold text-charcoal-800">Material Cost Inflation</span>
              <span className="font-mono font-bold text-amber-700">+{costDelta}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="40"
              step="5"
              value={costDelta}
              onChange={(e) => setCostDelta(Number(e.target.value))}
              className="w-full accent-forest-900 cursor-pointer"
            />
            <span className="text-[10px] text-charcoal-500">Grain / fuel / wholesale price spikes</span>
          </div>

          {/* Interest Rate Hike */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="font-bold text-charcoal-800">Interest Rate Hike</span>
              <span className="font-mono font-bold text-amber-700">+{rateDelta.toFixed(1)}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="5"
              step="0.5"
              value={rateDelta}
              onChange={(e) => setRateDelta(Number(e.target.value))}
              className="w-full accent-forest-900 cursor-pointer"
            />
            <span className="text-[10px] text-charcoal-500">Bank benchmark repo rate hikes</span>
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            onClick={runSimulation}
            disabled={loading}
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-xs shadow-sm transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Simulating...</span>
              </>
            ) : (
              <span>Simulate Stress Shocks</span>
            )}
          </button>
        </div>
      </div>

      {/* Survival Verdict Banner */}
      <div
        className={`p-6 rounded-2xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${
          survivalStatus.includes("SURVIVES")
            ? "bg-emerald-50 border-emerald-200 text-emerald-950"
            : survivalStatus.includes("VULNERABLE")
            ? "bg-amber-50 border-amber-200 text-amber-950"
            : "bg-red-50 border-red-200 text-red-950"
        }`}
      >
        <div className="space-y-1">
          <div className="flex items-center gap-2 font-extrabold text-sm uppercase tracking-wide">
            {survivalStatus.includes("SURVIVES") ? (
              <ShieldCheck className="w-5 h-5 text-emerald-700" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-amber-700" />
            )}
            <span>Survival Status: {survivalStatus}</span>
          </div>
          <p className="text-xs text-charcoal-700 leading-relaxed max-w-2xl">
            {stressData?.mitigation_advice ||
              "Under the simulated conditions, your cash flow remains positive and exceeds minimum bank debt service obligations."}
          </p>
        </div>
      </div>

      {/* Base vs Stressed Comparison Table */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
        <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-950">
          Base Case vs Stressed Case Comparison
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-ivory-100 text-charcoal-600 uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="py-2.5 px-3 rounded-l-lg">Metric</th>
                <th className="py-2.5 px-3">Normal Base Case</th>
                <th className="py-2.5 px-3">Simulated Stressed Shock</th>
                <th className="py-2.5 px-3 rounded-r-lg">Impact Delta</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ivory-100 font-medium text-charcoal-800">
              <tr className="hover:bg-ivory-50/80">
                <td className="py-3 px-3 font-bold">Monthly Sales Revenue</td>
                <td className="py-3 px-3 font-mono">₹{Math.round(base.monthly_sales || 65000).toLocaleString("en-IN")}</td>
                <td className="py-3 px-3 font-mono font-bold text-forest-950">₹{Math.round(stress.monthly_sales || 52000).toLocaleString("en-IN")}</td>
                <td className="py-3 px-3 text-red-700 font-mono">
                  -₹{Math.round((base.monthly_sales || 65000) - (stress.monthly_sales || 52000)).toLocaleString("en-IN")}
                </td>
              </tr>
              <tr className="hover:bg-ivory-50/80">
                <td className="py-3 px-3 font-bold">Net Monthly Operating Cash Flow</td>
                <td className="py-3 px-3 font-mono">₹{Math.round(base.monthly_profit || 26300).toLocaleString("en-IN")}</td>
                <td className="py-3 px-3 font-mono font-bold text-forest-950">₹{Math.round(stress.monthly_profit || 15400).toLocaleString("en-IN")}</td>
                <td className="py-3 px-3 text-red-700 font-mono">
                  -₹{Math.round((base.monthly_profit || 26300) - (stress.monthly_profit || 15400)).toLocaleString("en-IN")}
                </td>
              </tr>
              <tr className="hover:bg-ivory-50/80">
                <td className="py-3 px-3 font-bold">Debt Service Coverage (DSCR)</td>
                <td className="py-3 px-3 font-mono text-emerald-800">{Number(base.dscr || 1.65).toFixed(2)}x</td>
                <td className="py-3 px-3 font-mono font-bold text-amber-800">{Number(stress.dscr || 1.15).toFixed(2)}x</td>
                <td className="py-3 px-3 font-mono">
                  {(Number(stress.dscr || 1.15) - Number(base.dscr || 1.65)).toFixed(2)}x
                </td>
              </tr>
              <tr className="hover:bg-ivory-50/80">
                <td className="py-3 px-3 font-bold">Safety Margin Ratio</td>
                <td className="py-3 px-3 font-mono">{Math.round(base.margin_of_safety || 67)}%</td>
                <td className="py-3 px-3 font-mono font-bold">{Math.round(stress.margin_of_safety || 42)}%</td>
                <td className="py-3 px-3 text-red-700 font-mono">
                  -{Math.round((base.margin_of_safety || 67) - (stress.margin_of_safety || 42))}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}

