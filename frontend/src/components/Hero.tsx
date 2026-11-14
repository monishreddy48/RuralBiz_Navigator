"use client";

import Link from "next/link";
import { ArrowRight, CheckCircle2, Compass, ShieldCheck } from "lucide-react";

export function Hero() {
  return (
    <section className="relative pt-12 pb-20 md:pt-20 md:pb-28 overflow-hidden bg-gradient-to-b from-[#FBF9F2] via-[#F8F5EB] to-[#FBF9F2]">
      {/* Subtle organic background accent */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-forest-100/40 rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="absolute bottom-10 left-10 w-80 h-80 bg-sage-200/30 rounded-full blur-2xl pointer-events-none -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto">
          
          {/* Tag Pill */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-forest-100/80 border border-forest-200 text-forest-900 text-xs font-semibold tracking-wide uppercase mb-6 shadow-sm">
            <span className="w-2 h-2 rounded-full bg-forest-600 animate-pulse" />
            Decision Intelligence for Rural Entrepreneurs &amp; MSMEs
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-forest-950 tracking-tight leading-[1.15] mb-6">
            Your Business Journey{" "}
            <span className="relative inline-block">
              <span className="relative z-10 text-forest-800 font-editorial italic font-normal">
                Starts Here.
              </span>
              <span className="absolute bottom-1.5 left-0 w-full h-3 bg-sage-200/80 -z-0 rounded-sm" />
            </span>
          </h1>

          {/* Supporting Text */}
          <p className="text-lg sm:text-xl text-charcoal-700 leading-relaxed font-normal mb-10 max-w-2xl mx-auto">
            Discover viable local opportunities, analyze your 5–10 km village catchment, structure institutional reducing-balance debt, and make confident business decisions before borrowing money.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-14">
            <Link
              href="/dashboard"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-base shadow-lg shadow-forest-900/20 hover:shadow-xl hover:shadow-forest-900/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <span>Get Started Now</span>
              <ArrowRight className="w-5 h-5" />
            </Link>

            <Link
              href="#services"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-4 rounded-xl bg-white hover:bg-ivory-100 text-charcoal-800 font-semibold text-base border border-ivory-300 shadow-subtle hover:border-forest-700 transition-all"
            >
              <Compass className="w-4 h-4 text-forest-800" />
              <span>Explore Services</span>
            </Link>
          </div>

          {/* Micro Trust Indicators */}
          <div className="pt-6 border-t border-ivory-300/60 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-xs sm:text-sm text-charcoal-600 font-medium">
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-forest-700" />
              <span>Retail, Manufacturing &amp; Services</span>
            </div>
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-forest-700" />
              <span>Deterministic Debt Math (DSCR &amp; EMI)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-forest-700" />
              <span>Zero Fabrication &bull; 100% Unbiased</span>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

