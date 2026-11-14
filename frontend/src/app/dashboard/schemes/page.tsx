"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAssessment } from "@/context/AssessmentContext";
import { matchSchemes } from "@/lib/api";
import {
  Building2,
  CheckCircle2,
  XCircle,
  ExternalLink,
  Coins,
  FileCheck,
  ChevronRight,
  ShieldCheck,
  HelpCircle,
  Loader2,
} from "lucide-react";

export default function SchemesPage() {
  const { params, results } = useAssessment();
  const [schemes, setSchemes] = useState<any[]>(results.schemes || []);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!schemes || schemes.length === 0) {
      setLoading(true);
      matchSchemes({
        project_cost: params.expected_investment,
        business_category: params.category,
      })
        .then(setSchemes)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [params.expected_investment, params.category]);

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-ivory-200 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-forest-800 mb-1">
            <Building2 className="w-4 h-4 text-forest-700" />
            <span>Module 5 &bull; Rule-Based Credit Subsidy Routing</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-950 tracking-tight">
            Government Scheme &amp; Subsidy Navigator
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Match your project against verified Central and State credit programs with exact eligibility checklists, subsidy amounts, and official application portals.
          </p>
        </div>

        <Link
          href="/dashboard/alternatives"
          className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white text-xs font-bold shadow-xs transition-all self-start sm:self-auto"
        >
          <span>Next: Alternatives</span>
          <ChevronRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Verified Schemes List */}
      <div className="space-y-6">
        {loading ? (
          <div className="py-16 text-center">
            <Loader2 className="w-8 h-8 animate-spin text-forest-800 mx-auto mb-2" />
            <p className="text-xs text-charcoal-600 font-medium">Matching eligible subsidy programs...</p>
          </div>
        ) : schemes.length === 0 ? (
          <div className="py-12 text-center bg-white rounded-2xl border border-ivory-300 text-xs text-charcoal-500">
            No matching programs found for this specific investment size. Try increasing or decreasing project cost.
          </div>
        ) : (
          schemes.map((scheme: any, idx: number) => {
            const isHighMatch = scheme.match_status?.includes("HIGH") || scheme.match_status?.includes("ELIGIBLE");
            const subsidyRupees = scheme.estimated_subsidy_rupees || 0;

            return (
              <div
                key={idx}
                className="bg-white rounded-2xl p-6 sm:p-8 border border-ivory-300 shadow-subtle space-y-6"
              >
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 border-b border-ivory-200 pb-4">
                  <div>
                    <div className="flex items-center gap-2 mb-1.5">
                      <span
                        className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-md ${
                          isHighMatch
                            ? "bg-emerald-100 text-emerald-900 border border-emerald-300"
                            : "bg-amber-100 text-amber-900 border border-amber-300"
                        }`}
                      >
                        {scheme.match_status || "ELIGIBLE"}
                      </span>
                      <span className="text-xs text-charcoal-400 font-mono">
                        ID: {scheme.scheme_id}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-forest-950">
                      {scheme.name}
                    </h3>
                    <p className="text-xs text-charcoal-600 mt-1 max-w-2xl leading-relaxed">
                      {scheme.description}
                    </p>
                  </div>

                  {/* Subsidy Highlight Badge */}
                  {subsidyRupees > 0 && (
                    <div className="p-3.5 rounded-xl bg-forest-50 border border-forest-200 text-right shrink-0">
                      <span className="text-[10px] uppercase font-bold text-forest-800 block">
                        Estimated Credit Subsidy
                      </span>
                      <span className="text-xl font-extrabold text-forest-950 font-editorial">
                        ₹{Math.round(subsidyRupees).toLocaleString("en-IN")}
                      </span>
                    </div>
                  )}
                </div>

                {/* Eligibility Checkpoints Grid */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-charcoal-700 mb-3">
                    Eligibility Checkpoints
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    {scheme.eligibility_checks?.map((check: any, cIdx: number) => (
                      <div
                        key={cIdx}
                        className={`p-3 rounded-xl border flex items-start gap-2.5 ${
                          check.passed
                            ? "bg-emerald-50/50 border-emerald-200 text-emerald-950"
                            : "bg-rose-50/50 border-rose-200 text-rose-950"
                        }`}
                      >
                        {check.passed ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                        ) : (
                          <XCircle className="w-4 h-4 text-rose-700 shrink-0 mt-0.5" />
                        )}
                        <div>
                          <div className="font-semibold">{check.criterion}</div>
                          <div className="text-[11px] text-charcoal-600 mt-0.5">{check.detail}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Terms & Documents Summary */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-ivory-200 text-xs">
                  <div>
                    <span className="text-charcoal-400 font-bold block mb-1">OWN MARGIN REQUIREMENT</span>
                    <span className="font-medium text-charcoal-900">{scheme.margin_requirement || "5%–10% of total outlay"}</span>
                  </div>
                  <div>
                    <span className="text-charcoal-400 font-bold block mb-1">COLLATERAL REQUIREMENT</span>
                    <span className="font-medium text-charcoal-900">{scheme.collateral_notes || "Zero third-party collateral (CGTMSE covered)"}</span>
                  </div>
                  <div>
                    <span className="text-charcoal-400 font-bold block mb-1">APPLICATION ROUTE</span>
                    {scheme.source_url ? (
                      <a
                        href={scheme.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 font-bold text-forest-800 hover:text-forest-950 underline"
                      >
                        <span>Official Portal</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="font-medium text-charcoal-900">{scheme.application_route || "District Industries Centre (DIC)"}</span>
                    )}
                  </div>
                </div>

              </div>
            );
          })
        )}
      </div>

    </div>
  );
}

