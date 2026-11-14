"use client";

import { MapPin, Calculator, ShieldCheck, FileCheck, ArrowRight } from "lucide-react";
import Link from "next/link";

export function HowItWorks() {
  const steps = [
    {
      num: "01",
      icon: MapPin,
      title: "Set Your Location & Capital",
      desc: "Select your village, specify your available savings, and pick your target enterprise category (manufacturing, retail, services, agro-processing).",
    },
    {
      num: "02",
      icon: Calculator,
      title: "Run Deterministic Engines",
      desc: "Our Python engines immediately compute reducing-balance EMI amortization, 12-month dynamic cash flow, break-even volume, and DSCR coverage.",
    },
    {
      num: "03",
      icon: ShieldCheck,
      title: "Stress Test & Match Schemes",
      desc: "Simulate a 20% sales contraction or 15% raw material price spike, and discover matched Central/State credit subsidy programs.",
    },
    {
      num: "04",
      icon: FileCheck,
      title: "Download Bankable DPR",
      desc: "Review your GO / MODIFY / AVOID advisory verdict and download a 20-section Detailed Project Report PDF formatted for commercial bank appraisal.",
    },
  ];

  return (
    <section id="how-it-works" className="py-20 md:py-28 bg-[#FBF9F2]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-100 text-forest-900 text-xs font-bold uppercase tracking-wider mb-3">
            Simple, Transparent 4-Stage Process
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-forest-950 tracking-tight">
            How RuralBiz Navigator Works
          </h2>
          <p className="mt-4 text-base sm:text-lg text-charcoal-600">
            From entering your initial idea to walking into a commercial bank branch with a verified project report in under 5 minutes.
          </p>
        </div>

        {/* 4 Connected Step Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
          {steps.map((s, idx) => {
            const Icon = s.icon;
            return (
              <div
                key={idx}
                className="relative bg-white rounded-2xl p-7 border border-ivory-300 shadow-subtle flex flex-col justify-between group hover:border-forest-700 transition-all"
              >
                <div>
                  {/* Step Number & Icon */}
                  <div className="flex items-center justify-between mb-6">
                    <span className="text-3xl font-extrabold font-editorial text-forest-200 group-hover:text-forest-700 transition-colors">
                      {s.num}
                    </span>
                    <div className="w-11 h-11 rounded-xl bg-forest-50 text-forest-900 flex items-center justify-center">
                      <Icon className="w-5 h-5" />
                    </div>
                  </div>

                  <h3 className="text-lg font-bold text-charcoal-900 mb-2">
                    {s.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-charcoal-600 leading-relaxed">
                    {s.desc}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-ivory-100 flex items-center text-xs font-semibold text-forest-800">
                  <span>Step {idx + 1} of 4</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom Banner CTA */}
        <div className="mt-14 p-8 rounded-2xl bg-gradient-to-r from-forest-950 via-forest-900 to-forest-800 text-white flex flex-col sm:flex-row items-center justify-between gap-6 shadow-card">
          <div>
            <h3 className="text-xl sm:text-2xl font-bold tracking-tight">
              Ready to evaluate your rural business idea?
            </h3>
            <p className="text-sm text-forest-100/90 mt-1">
              Test pre-configured SIH judging scenarios or analyze a custom business in your locality.
            </p>
          </div>
          <Link
            href="http://localhost:8501"
            target="_blank"
            className="shrink-0 inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white hover:bg-ivory-100 text-forest-950 font-bold text-sm shadow-md transition-all active:scale-[0.98]"
          >
            <span>Launch Evaluation</span>
            <ArrowRight className="w-4 h-4 text-forest-800" />
          </Link>
        </div>

      </div>
    </section>
  );
}

