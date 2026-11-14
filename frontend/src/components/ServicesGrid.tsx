"use client";

import Link from "next/link";
import {
  BarChart3,
  MapPin,
  CreditCard,
  TrendingDown,
  Building2,
  Bot,
  Lightbulb,
  FileSpreadsheet,
  ArrowRight
} from "lucide-react";

export function ServicesGrid() {
  const services = [
    {
      icon: BarChart3,
      id: "feasibility",
      title: "1. Business Feasibility & Viability",
      desc: "Deterministic 0–100 viability score evaluating market demand, competitor saturation, road accessibility, and financial fit, accompanied by an objective 4-quadrant SWOT matrix.",
      highlight: "Weighted 6-Factor Model",
      cta: "Evaluate Feasibility",
      href: "/dashboard/feasibility",
    },
    {
      icon: MapPin,
      id: "market",
      title: "2. Hyperlocal Market Intelligence",
      desc: "Interactive GIS catchment mapping defining the 5 km daily footfall circle and 10 km weekly haat wholesale radius, with mapped competitor entities and unmet demand gap analysis.",
      highlight: "5–10 km Catchment GIS",
      cta: "Explore Local Market",
      href: "/dashboard/market",
    },
    {
      icon: CreditCard,
      id: "financial",
      title: "3. Financial Planning & Debt Structuring",
      desc: "Standard reducing-balance monthly EMI calculations, month-by-month principal and interest amortization schedules, break-even unit volumes, and Debt Service Coverage Ratio (DSCR).",
      highlight: "Institutional Debt Math",
      cta: "Structure Loan Plan",
      href: "/dashboard/financial",
    },
    {
      icon: TrendingDown,
      id: "simulator",
      title: "4. What-If Scenario Stress Testing",
      desc: "Simulate adverse rural market shocks: 20% demand drops, price deflation, raw material cost inflation, or interest rate hikes to test if your business survives or enters debt stress.",
      highlight: "Enterprise Survival Verdict",
      cta: "Simulate Stress Shocks",
      href: "/dashboard/simulator",
    },
    {
      icon: Building2,
      id: "schemes",
      title: "5. Government Scheme Navigator",
      desc: "Rule-based matching against verified Central and State programs (PMEGP 25%–35% subsidy, MUDRA Shishu/Kishore/Tarun, PMFME, Stand-Up India) with exact eligibility checklists.",
      highlight: "Verified Subsidy Rules",
      cta: "Find Subsidies",
      href: "/dashboard/schemes",
    },
    {
      icon: Bot,
      id: "ai-advisor",
      title: "6. Multilingual AI Business Assistant",
      desc: "Conversational guidance powered by Gemini in English, Hindi, Telugu, and Kannada. Explains financial calculations and scheme terms with explainable, structured advisory responses.",
      highlight: "Grounded Regional Advisory",
      cta: "Chat with Advisor",
      href: "/dashboard/assistant",
    },
    {
      icon: Lightbulb,
      id: "alternatives",
      title: "7. Business Alternatives Recommender",
      desc: "Compare and rank all 10 rural micro-enterprise categories for your exact capital and locality to identify higher-viability business ventures with one-click adoption.",
      highlight: "Capital-Matched Ranking",
      cta: "Compare 10 Sectors",
      href: "/dashboard/alternatives",
    },
    {
      icon: FileSpreadsheet,
      id: "dpr",
      title: "8. Bankable DPR Report Generation",
      desc: "Instantly compile an institutional, 20-section Detailed Project Report (DPR) into a downloadable PDF complete with KYC declarations, amortization tables, and SWOT for bank appraisal.",
      highlight: "Downloadable 20-Section PDF",
      cta: "Generate Official DPR",
      href: "/dashboard/dpr",
    },
  ];

  return (
    <section id="services" className="py-20 md:py-28 bg-[#F7F4EB] border-y border-ivory-300/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-100 text-forest-900 text-xs font-bold uppercase tracking-wider mb-3">
            Core Intelligence Capabilities
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-forest-950 tracking-tight">
            Eight Integrated Decision Engines
          </h2>
          <p className="mt-4 text-base sm:text-lg text-charcoal-600">
            Every module operates on verified local benchmark unit economics and institutional debt calculations, giving you a complete 360-degree pre-borrowing evaluation.
          </p>
        </div>

        {/* 8-Card Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map((svc, idx) => {
            const Icon = svc.icon;
            return (
              <div
                key={idx}
                className="bg-white rounded-2xl p-6 border border-ivory-200/90 shadow-subtle hover:shadow-card hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 rounded-xl bg-forest-50 border border-forest-100 text-forest-900 flex items-center justify-center group-hover:bg-forest-900 group-hover:text-white transition-colors duration-200">
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-[11px] font-bold text-forest-800 bg-forest-100/70 px-2.5 py-0.5 rounded-full">
                      {svc.highlight}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-charcoal-900 mb-2 leading-snug">
                    {svc.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-charcoal-600 leading-relaxed">
                    {svc.desc}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-ivory-100">
                  <Link
                    href={svc.href}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-forest-800 group-hover:text-forest-950 transition-colors"
                  >
                    <span>{svc.cta}</span>
                    <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}

