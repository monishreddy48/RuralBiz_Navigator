"use client";

import Link from "next/link";
import { ShieldAlert, ExternalLink, Heart } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-forest-950 text-white/90 pt-16 pb-12 border-t border-forest-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Top Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-forest-800 flex items-center justify-center text-ivory-50 text-xl font-bold shadow-sm">
                🌾
              </div>
              <span className="text-xl font-extrabold text-white tracking-tight">
                RuralBiz <span className="text-forest-400 font-semibold">Navigator</span>
              </span>
            </div>
            
            <p className="text-xs sm:text-sm text-forest-200/80 leading-relaxed max-w-sm">
              AI-driven hyper-local business advisory and financial debt structuring assistant for rural micro-entrepreneurs and MSMEs across India.
            </p>

            <div className="text-xs text-forest-300/70 font-mono">
              SIH 2026 Problem Statement: SIH26091 / PS 91
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-forest-300">
              Platform Modules
            </h4>
            <ul className="space-y-2 text-xs text-forest-100/75">
              <li><Link href="#services" className="hover:text-white transition-colors">Business Feasibility</Link></li>
              <li><Link href="#services" className="hover:text-white transition-colors">Hyperlocal Market GIS</Link></li>
              <li><Link href="#services" className="hover:text-white transition-colors">Financial Calculator</Link></li>
              <li><Link href="#services" className="hover:text-white transition-colors">What-If Simulator</Link></li>
            </ul>
          </div>

          {/* Scheme & Support */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-forest-300">
              Government Schemes
            </h4>
            <ul className="space-y-2 text-xs text-forest-100/75">
              <li><span className="text-white/90">PMEGP</span> (25%–35% Rural Subsidy)</li>
              <li><span className="text-white/90">PM MUDRA</span> (Shishu/Kishore/Tarun)</li>
              <li><span className="text-white/90">PMFME</span> (Micro Food Enterprises)</li>
              <li><span className="text-white/90">PM Vishwakarma</span> (Artisans &amp; Trades)</li>
            </ul>
          </div>

          {/* Architecture & Tech */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-forest-300">
              Architecture &amp; Tech
            </h4>
            <ul className="space-y-2 text-xs text-forest-100/75">
              <li>Next.js 14 &bull; TypeScript &bull; Tailwind</li>
              <li>Python FastAPI Deterministic Backend</li>
              <li>ReportLab 20-Section PDF DPR</li>
              <li>Gemini 3.8 Flash &amp; Live Voice API</li>
            </ul>
          </div>

        </div>

        {/* Mandatory Transparency & Legal Disclaimer Box */}
        <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 text-xs text-forest-200/80 leading-relaxed space-y-2">
          <div className="flex items-center gap-2 font-bold text-forest-200 uppercase tracking-wide text-[11px]">
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            <span>Institutional, Legal &amp; Prototype Notice</span>
          </div>
          <p>
            <strong>1. No Government Affiliation:</strong> RuralBiz Navigator is an independent technological decision-support platform designed for Smart India Hackathon 2026 (Problem Statement 91). It is not an official government agency and does not issue loan approvals, registrations, or subsidy sanctions directly.
          </p>
          <p>
            <strong>2. Informational Decision-Support Only:</strong> Calculations, viability scores, and financial models are deterministic estimates based on standard banking formulas (reducing-balance EMI, DSCR, BEP) and benchmark unit economics. They do not constitute formal commercial lending or investment advice.
          </p>
          <p>
            <strong>3. Synthetic Prototype Baseline:</strong> Locality demographic indices, competitor listings, and customer catchment numbers in this prototype are synthetically constructed for demonstration purposes. Final lending decisions remain the sole discretion of commercial banks and District Task Force Committees.
          </p>
        </div>

        {/* Bottom Credits */}
        <div className="pt-6 border-t border-forest-900 flex flex-col sm:flex-row items-center justify-between text-xs text-forest-400 gap-4">
          <div>
            &copy; {new Date().getFullYear()} RuralBiz Navigator &bull; SIH 2026 Problem Statement SIH26091 / PS 91.
          </div>
          <div className="flex items-center gap-1">
            Built with rigor for rural micro-entrepreneurs across India.
          </div>
        </div>

      </div>
    </footer>
  );
}

