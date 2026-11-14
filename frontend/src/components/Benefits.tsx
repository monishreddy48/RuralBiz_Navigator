"use client";

import { Shield, Coins, Target, Award, Languages, FileText } from "lucide-react";

export function Benefits() {
  const benefits = [
    {
      icon: Shield,
      title: "Protect Hard-Earned Family Savings",
      desc: "Stop speculative borrowing. Know your exact break-even point and debt service risk before purchasing machinery or leasing a commercial premises.",
    },
    {
      icon: Coins,
      title: "Standard Reducing-Balance Amortization",
      desc: "No hidden flat-rate interest confusion. See true month-by-month principal reduction with configurable moratorium buffers.",
    },
    {
      icon: Target,
      title: "Real 5–10 km Catchment Grounding",
      desc: "Understand your local addressable market, nearest APMC mandi connectivity, and mapped competitor saturation in your rural block.",
    },
    {
      icon: Award,
      title: "Unlock Verified Credit-Linked Subsidies",
      desc: "Identify schemes like PMEGP (25%–35% rural subsidy), PMFME, and MUDRA Shishu/Kishore with official application checklists.",
    },
    {
      icon: Languages,
      title: "Regional Multilingual AI Advisory",
      desc: "Interact in English, Hindi (हिंदी), Telugu (తెలుగు), or Kannada (ಕನ್ನಡ) with structured, explainable financial guidance.",
    },
    {
      icon: FileText,
      title: "Bank-Ready Project Proposal (DPR)",
      desc: "Download a 20-section institutional project report ready for District Task Force Committees and commercial bank loan appraisal.",
    },
  ];

  return (
    <section id="benefits" className="py-20 md:py-28 bg-[#F7F4EB] border-t border-ivory-300/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-100 text-forest-900 text-xs font-bold uppercase tracking-wider mb-3">
            Why Micro-Entrepreneurs Trust RuralBiz
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-forest-950 tracking-tight">
            Institutional Rigor Made Simple for Rural Enterprises
          </h2>
          <p className="mt-4 text-base sm:text-lg text-charcoal-600">
            Engineered to replace informal guesswork with verified local benchmarks and mathematical certainty.
          </p>
        </div>

        {/* 6-Grid Benefits */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((b, idx) => {
            const Icon = b.icon;
            return (
              <div
                key={idx}
                className="bg-white rounded-2xl p-7 border border-ivory-200/90 shadow-subtle hover:shadow-card transition-all duration-300 flex items-start gap-4"
              >
                <div className="w-12 h-12 rounded-xl bg-forest-50 border border-forest-100 text-forest-800 flex items-center justify-center shrink-0">
                  <Icon className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-charcoal-900 mb-1.5 leading-snug">
                    {b.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-charcoal-600 leading-relaxed">
                    {b.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}

