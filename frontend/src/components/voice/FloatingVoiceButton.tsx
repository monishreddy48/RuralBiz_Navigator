"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Mic, Sparkles, X, ChevronRight } from "lucide-react";
import { usePathname } from "next/navigation";

export default function FloatingVoiceButton() {
  const pathname = usePathname();
  const [showTooltip, setShowTooltip] = useState(true);

  // Hide the floating button on the assistant page itself to avoid redundancy
  if (pathname === "/dashboard/assistant") {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3">
      {/* Informative Tooltip for First-time Users */}
      {showTooltip && (
        <div className="hidden sm:flex items-center gap-2 bg-forest-900 text-ivory-50 px-3.5 py-2 rounded-xl text-xs shadow-xl border border-forest-700 animate-fade-in">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
          <span>Ask questions via voice in Kannada, Telugu, Hindi, or English</span>
          <button
            type="button"
            onClick={() => setShowTooltip(false)}
            className="text-charcoal-400 hover:text-ivory-100 ml-1"
          >
            <X className="w-3 h-3" />
          </button>
        </div>
      )}

      {/* Floating Action Button */}
      <Link
        href="/dashboard/assistant"
        className="group flex items-center gap-2.5 px-4 py-3 rounded-full bg-gradient-to-r from-emerald-600 to-forest-800 hover:from-emerald-500 hover:to-forest-700 text-white shadow-xl shadow-emerald-950/40 border border-emerald-500/40 transition-all transform hover:scale-105 active:scale-95"
      >
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </span>
        <Mic className="w-5 h-5 text-emerald-200 group-hover:animate-pulse" />
        <span className="text-xs font-bold tracking-wide hidden md:inline">Voice Advisor</span>
      </Link>
    </div>
  );
}

