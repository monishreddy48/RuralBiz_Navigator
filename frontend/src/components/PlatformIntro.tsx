"use client";

import { Scale, Cpu, Database, Check, ShieldAlert } from "lucide-react";

export function PlatformIntro() {
  return (
    <section id="about" className="py-20 md:py-28 bg-[#FBF9F2]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Two-Column Editorial Narrative */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
          
          {/* Left Column: Strong Typography & Mission */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-forest-100 text-forest-900 text-xs font-bold uppercase tracking-wider">
              The Crucial Missing Link Before Borrowing
            </div>

            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-forest-950 tracking-tight leading-tight">
              Most platforms help after you borrow. We protect your capital{" "}
              <span className="font-editorial italic text-forest-800 font-normal">
                before you commit.
              </span>
            </h2>

            <p className="text-base sm:text-lg text-charcoal-700 leading-relaxed">
              In rural India, millions of aspiring entrepreneurs—from village shopkeepers to food millers, fabricators, and tailoring cooperatives—take on high-interest commercial debt without ever knowing their local catchment numbers or true debt service ratios.
            </p>

            <blockquote className="border-l-4 border-forest-800 pl-4 py-1 italic font-editorial text-lg text-forest-900 bg-ivory-100/60 rounded-r-lg">
              &ldquo;Should I start this specific enterprise HERE, with MY personal budget, given MY local competition and seasonal demand?&rdquo;
            </blockquote>

            <p className="text-base text-charcoal-600 leading-relaxed">
              RuralBiz Navigator combines hyper-local demographic mapping (5–10 km radius), deterministic reducing-balance debt mathematics, institutional credit coverage (DSCR), and rule-based government scheme discovery into one unified decision cockpit.
            </p>

            <div className="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-charcoal-800 font-medium">
              <div className="flex items-start gap-2.5">
                <div className="mt-0.5 rounded-full p-1 bg-forest-100 text-forest-800">
                  <Check className="w-3.5 h-3.5" />
                </div>
                <span><strong>Zero Mathematical Guesswork:</strong> Pure deterministic Python calculation engines.</span>
              </div>
              <div className="flex items-start gap-2.5">
                <div className="mt-0.5 rounded-full p-1 bg-forest-100 text-forest-800">
                  <Check className="w-3.5 h-3.5" />
                </div>
                <span><strong>Hyper-Local Catchment:</strong> 5 km walk-in &amp; 10 km weekly haat market radii.</span>
              </div>
            </div>
          </div>

          {/* Right Column: Architectural Highlights Card */}
          <div className="lg:col-span-5">
            <div className="bg-white rounded-3xl p-8 border border-ivory-300 shadow-card space-y-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-forest-50 rounded-bl-full pointer-events-none -z-0" />
              
              <div className="relative z-10">
                <span className="text-xs font-bold uppercase tracking-wider text-forest-800">
                  Hybrid Architecture Guarantee
                </span>
                <h3 className="text-2xl font-bold text-forest-950 mt-1">
                  How We Protect You from AI Hallucinations
                </h3>
              </div>

              {/* Pillar 1 */}
              <div className="flex gap-4 items-start relative z-10">
                <div className="w-10 h-10 rounded-xl bg-forest-100 text-forest-900 flex items-center justify-center shrink-0">
                  <Cpu className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-sm">Deterministic Mathematical Engine</h4>
                  <p className="text-xs text-charcoal-600 mt-1 leading-relaxed">
                    Reducing-balance EMI, 12-month dynamic P&amp;L cash flow, and DSCR debt coverage ratios are computed purely in Python formulas.
                  </p>
                </div>
              </div>

              {/* Pillar 2 */}
              <div className="flex gap-4 items-start relative z-10">
                <div className="w-10 h-10 rounded-xl bg-forest-100 text-forest-900 flex items-center justify-center shrink-0">
                  <Scale className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-sm">Explainable Multilingual AI</h4>
                  <p className="text-xs text-charcoal-600 mt-1 leading-relaxed">
                    Gemini 3.8 Flash explains the calculation results in Hindi, Telugu, Kannada, or English. The LLM never computes financial numbers.
                  </p>
                </div>
              </div>

              {/* Pillar 3 */}
              <div className="flex gap-4 items-start relative z-10">
                <div className="w-10 h-10 rounded-xl bg-forest-100 text-forest-900 flex items-center justify-center shrink-0">
                  <Database className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-sm">Verified Central &amp; State Schemes</h4>
                  <p className="text-xs text-charcoal-600 mt-1 leading-relaxed">
                    Rule-based matching against official PMEGP, MUDRA, and PMFME guidelines with exact verified subsidy ceilings and checklists.
                  </p>
                </div>
              </div>

            </div>
          </div>

        </div>

      </div>
    </section>
  );
}

