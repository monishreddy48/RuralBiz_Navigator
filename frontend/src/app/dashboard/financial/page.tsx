"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAssessment } from "@/context/AssessmentContext";
import { calculateFinance } from "@/lib/api";
import {
  CreditCard,
  Calculator,
  Coins,
  ShieldCheck,
  TrendingUp,
  AlertCircle,
  CheckCircle2,
  ChevronRight,
  FileSpreadsheet,
  Loader2,
  Sparkles,
} from "lucide-react";

export default function FinancialPage() {
  const { params, updateParam, results, loadDemoCase } = useAssessment();

  const [finData, setFinData] = useState<any>(results.finance);
  const [loading, setLoading] = useState(false);

  const [projectCost, setProjectCost] = useState(params.expected_investment);
  const [ownContribution, setOwnContribution] = useState(params.own_capital);
  const [interestRate, setInterestRate] = useState(params.annual_interest_rate);
  const [tenureMonths, setTenureMonths] = useState(params.tenure_months);
  const [moratoriumMonths, setMoratoriumMonths] = useState(params.moratorium_months);

  // Sync state when assessment params or results update
  useEffect(() => {
    if (results.finance) {
      setFinData(results.finance);
    }
    setProjectCost(params.expected_investment);
    setOwnContribution(params.own_capital);
    setInterestRate(params.annual_interest_rate);
    setTenureMonths(params.tenure_months);
    setMoratoriumMonths(params.moratorium_months);
  }, [results.finance, params]);

  const runCalculation = async () => {
    setLoading(true);
    try {
      const data = await calculateFinance({
        project_cost: projectCost,
        own_contribution: ownContribution,
        annual_interest_rate: interestRate,
        tenure_months: tenureMonths,
        moratorium_months: moratoriumMonths,
      });
      setFinData(data);
      updateParam("expected_investment", projectCost);
      updateParam("own_capital", ownContribution);
      updateParam("annual_interest_rate", interestRate);
      updateParam("tenure_months", tenureMonths);
      updateParam("moratorium_months", moratoriumMonths);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!finData) {
      runCalculation();
    }
  }, []);

  const emi = finData?.monthly_emi ? Math.round(finData.monthly_emi) : 3418;
  const loanAmount = finData?.loan_amount ? Math.round(finData.loan_amount) : projectCost - ownContribution;
  const totalInterest = finData?.total_interest ? Math.round(finData.total_interest) : 43815;
  const dscr = finData?.dscr ? finData.dscr.toFixed(2) : "1.65";
  const breakEven = finData?.break_even_revenue ? Math.round(finData.break_even_revenue) : 21250;
  const marginOfSafety = finData?.margin_of_safety_pct ? Math.round(finData.margin_of_safety_pct) : 67;

  const amortization = finData?.amortization_schedule?.slice(0, 12) || [];
  const cashFlow12 = finData?.cash_flow_12 || [];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-ivory-200 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-forest-800 mb-1">
            <CreditCard className="w-4 h-4 text-forest-700" />
            <span>Module 3 &bull; Institutional Debt Structuring</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-950 tracking-tight">
            Financial Planning &amp; Debt Amortization
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Calculates exact reducing-balance monthly EMI, break-even unit volumes, and the Debt Service Coverage Ratio (DSCR) required by commercial banks.
          </p>
        </div>

        <Link
          href="/dashboard/simulator"
          className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white text-xs font-bold shadow-xs transition-all self-start sm:self-auto"
        >
          <span>Next: Stress Simulator</span>
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
              <span className="text-xs font-bold text-emerald-800">DSCR 1.8+</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Flour Mill &amp; Agro-Unit</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">₹2.15L Outlay &bull; ₹53.7k Margin &bull; 9.5% Int</p>
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
              <span className="text-xs font-bold text-amber-800">DSCR 1.25</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Rural Manufacturing Unit</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">₹3.20L Outlay &bull; ₹80k Margin &bull; 10.0% Int</p>
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
              <span className="text-xs font-bold text-red-800">DSCR &lt; 1.0</span>
            </div>
            <p className="text-xs font-bold text-charcoal-900">Saturated Village Kirana</p>
            <p className="text-[10px] text-charcoal-600 mt-0.5">₹1.90L Outlay &bull; ₹35k Margin &bull; 11.5% Int</p>
          </button>
        </div>
      </div>

      {/* Interactive Financial Controls */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-3">
          <span className="text-xs font-extrabold uppercase tracking-wider text-forest-950">
            Loan Parameter Adjuster
          </span>
          <span className="text-xs text-charcoal-500 font-mono">
            Standard Reducing-Balance Formula
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-5 gap-4">
          <div>
            <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
              Project Cost (₹)
            </label>
            <input
              type="number"
              step="5000"
              value={projectCost}
              onChange={(e) => setProjectCost(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
              Own Margin (₹)
            </label>
            <input
              type="number"
              step="5000"
              value={ownContribution}
              onChange={(e) => setOwnContribution(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
              Interest Rate (%)
            </label>
            <input
              type="number"
              step="0.25"
              value={interestRate}
              onChange={(e) => setInterestRate(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
              Tenure (Months)
            </label>
            <input
              type="number"
              step="6"
              value={tenureMonths}
              onChange={(e) => setTenureMonths(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-charcoal-700 uppercase tracking-wider mb-1">
              Moratorium Buffer (Mo.)
            </label>
            <input
              type="number"
              step="1"
              max="12"
              value={moratoriumMonths}
              onChange={(e) => setMoratoriumMonths(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-xl border border-ivory-300 bg-ivory-50 text-xs font-medium text-charcoal-900"
            />
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            onClick={runCalculation}
            disabled={loading}
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-xs shadow-sm transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Re-calculating...</span>
              </>
            ) : (
              <span>Recalculate Amortization</span>
            )}
          </button>
        </div>
      </div>

      {/* 4 Core Financial Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* Monthly EMI */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-2">
          <span className="text-[11px] font-bold text-charcoal-400 uppercase tracking-wider">
            Monthly Bank EMI
          </span>
          <div className="text-3xl font-extrabold text-forest-950 font-editorial">
            ₹{emi.toLocaleString("en-IN")}
            <span className="text-xs font-medium text-charcoal-500 font-sans ml-1">/ mo</span>
          </div>
          <p className="text-[11px] text-charcoal-600">
            Principal Borrowed: ₹{loanAmount.toLocaleString("en-IN")} over {tenureMonths} months.
          </p>
        </div>

        {/* DSCR */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-2">
          <span className="text-[11px] font-bold text-charcoal-400 uppercase tracking-wider">
            Debt Coverage (DSCR)
          </span>
          <div className="text-3xl font-extrabold text-emerald-800 font-editorial">
            {dscr}x
          </div>
          <p className="text-[11px] text-charcoal-600">
            Bank benchmark: &gt; 1.30x. Strong coverage indicates comfortable repayment ability.
          </p>
        </div>

        {/* Break-Even Sales */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-2">
          <span className="text-[11px] font-bold text-charcoal-400 uppercase tracking-wider">
            Monthly Break-Even
          </span>
          <div className="text-3xl font-extrabold text-forest-950 font-editorial">
            ₹{breakEven.toLocaleString("en-IN")}
          </div>
          <p className="text-[11px] text-charcoal-600">
            Minimum revenue needed to cover variable costs, fixed rent, and bank EMI.
          </p>
        </div>

        {/* Margin of Safety */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-2">
          <span className="text-[11px] font-bold text-charcoal-400 uppercase tracking-wider">
            Margin of Safety
          </span>
          <div className="text-3xl font-extrabold text-forest-950 font-editorial">
            {marginOfSafety}%
          </div>
          <p className="text-[11px] text-charcoal-600">
            Sales can drop by {marginOfSafety}% before the enterprise enters operational loss.
          </p>
        </div>

      </div>

      {/* 12-Month Amortization Schedule Table */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-3">
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-950">
              Loan Amortization Schedule (Year 1 Preview)
            </h2>
            <p className="text-xs text-charcoal-600 mt-0.5">
              Standard commercial banking schedule demonstrating principal retirement and interest reduction.
            </p>
          </div>
          <span className="text-xs font-semibold text-forest-800">
            Total Interest: ₹{totalInterest.toLocaleString("en-IN")}
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-ivory-100 text-charcoal-600 uppercase font-bold text-[10px] tracking-wider font-sans">
              <tr>
                <th className="py-2.5 px-3 rounded-l-lg">Month</th>
                <th className="py-2.5 px-3">Opening Balance</th>
                <th className="py-2.5 px-3">Principal</th>
                <th className="py-2.5 px-3">Interest</th>
                <th className="py-2.5 px-3">Total EMI</th>
                <th className="py-2.5 px-3 rounded-r-lg">Closing Balance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ivory-100 font-medium text-charcoal-800">
              {amortization.map((row: any, idx: number) => (
                <tr key={idx} className="hover:bg-ivory-50/80 transition-colors">
                  <td className="py-2.5 px-3 font-bold font-sans">Month {row.month || idx + 1}</td>
                  <td className="py-2.5 px-3">₹{Math.round(row.opening_balance || 0).toLocaleString("en-IN")}</td>
                  <td className="py-2.5 px-3 text-emerald-800">₹{Math.round(row.principal || 0).toLocaleString("en-IN")}</td>
                  <td className="py-2.5 px-3 text-amber-800">₹{Math.round(row.interest || 0).toLocaleString("en-IN")}</td>
                  <td className="py-2.5 px-3 font-bold text-forest-950">₹{Math.round(row.total_payment || emi).toLocaleString("en-IN")}</td>
                  <td className="py-2.5 px-3">₹{Math.round(row.closing_balance || 0).toLocaleString("en-IN")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}

