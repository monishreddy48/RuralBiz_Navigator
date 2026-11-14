"use client";

import React from "react";
import Link from "next/link";
import { AlertCircle } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

interface AuthCardProps {
  title: string;
  subtitle: string;
  children: React.ReactNode;
  footerText?: string;
  footerLinkText?: string;
  footerLinkHref?: string;
}

export function AuthCard({
  title,
  subtitle,
  children,
  footerText,
  footerLinkText,
  footerLinkHref,
}: AuthCardProps) {
  const { firebaseConfigured } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#FBF9F2] via-[#F8F5EB] to-[#FBF9F2] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      {/* Decorative organic background aura */}
      <div className="absolute top-10 left-1/4 w-96 h-96 bg-forest-100/30 rounded-full blur-3xl pointer-events-none -z-0" />
      <div className="absolute bottom-10 right-1/4 w-80 h-80 bg-sage-200/30 rounded-full blur-2xl pointer-events-none -z-0" />

      {/* Brand Header */}
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center relative z-10">
        <Link href="/" className="inline-flex items-center gap-3 group">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-forest-950 via-forest-900 to-forest-700 flex items-center justify-center text-ivory-50 shadow-md group-hover:shadow-forest-900/25 transition-all">
            <span className="text-2xl font-bold">🌾</span>
          </div>
          <div className="flex flex-col text-left">
            <span className="text-2xl font-extrabold tracking-tight text-forest-950 font-sans leading-none">
              RuralBiz <span className="text-forest-700 font-semibold">Navigator</span>
            </span>
            <span className="text-xs font-medium text-charcoal-500 tracking-wide mt-1">
              Smarter decisions. Stronger rural businesses.
            </span>
          </div>
        </Link>
        <h2 className="mt-6 text-2xl sm:text-3xl font-extrabold text-charcoal-900 tracking-tight font-sans">
          {title}
        </h2>
        <p className="mt-2 text-sm text-charcoal-600 max-w-sm mx-auto">
          {subtitle}
        </p>
      </div>

      {/* Card Body */}
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10 px-4 sm:px-0">
        {!firebaseConfigured && (
          <div className="mb-6 p-4 rounded-xl bg-amber-50/90 border border-amber-200 text-amber-900 text-xs flex items-start gap-3 shadow-sm">
            <AlertCircle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="font-bold">Firebase Configuration Required</p>
              <p className="text-amber-800">
                Please configure your Firebase credentials in <code className="bg-amber-100 px-1 py-0.5 rounded font-mono">frontend/.env.local</code> to activate live authentication.
              </p>
            </div>
          </div>
        )}

        <div className="bg-white py-8 px-6 sm:px-10 shadow-card rounded-3xl border border-ivory-300">
          {children}

          {footerText && footerLinkText && footerLinkHref && (
            <div className="mt-6 pt-6 border-t border-ivory-200 text-center text-xs text-charcoal-600">
              <span>{footerText} </span>
              <Link
                href={footerLinkHref}
                className="font-bold text-forest-800 hover:text-forest-950 underline underline-offset-2 transition-colors"
              >
                {footerLinkText}
              </Link>
            </div>
          )}
        </div>

        {/* Back to Home Link */}
        <div className="text-center mt-6">
          <Link
            href="/"
            className="text-xs font-semibold text-charcoal-500 hover:text-forest-900 transition-colors"
          >
            &larr; Back to RuralBiz Navigator Homepage
          </Link>
        </div>
      </div>
    </div>
  );
}

