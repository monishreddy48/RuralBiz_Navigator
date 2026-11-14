"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Globe, Menu, X, ArrowUpRight, User, LogOut, LayoutDashboard } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

export function Navbar() {
  const router = useRouter();
  const { user, userProfile, logout } = useAuth();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [selectedLang, setSelectedLang] = useState("EN");
  const [langDropdownOpen, setLangDropdownOpen] = useState(false);

  const languages = [
    { code: "EN", name: "English" },
    { code: "HI", name: "हिंदी (Hindi)" },
    { code: "TE", name: "తెలుగు (Telugu)" },
    { code: "KN", name: "ಕನ್ನಡ (Kannada)" },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-[#FBF9F2]/90 backdrop-blur-md border-b border-ivory-200/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Brand Identity */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-forest-950 via-forest-900 to-forest-700 flex items-center justify-center text-ivory-50 shadow-md group-hover:shadow-forest-900/20 transition-all">
              <span className="text-xl font-bold tracking-tight">🌾</span>
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-extrabold tracking-tight text-forest-950 font-sans leading-none">
                RuralBiz <span className="text-forest-700 font-semibold">Navigator</span>
              </span>
              <span className="text-[11px] font-medium text-charcoal-500 tracking-wide mt-1">
                Smarter decisions. Stronger rural businesses.
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-8 text-[15px] font-medium text-charcoal-700">
            <Link href="#services" className="hover:text-forest-900 transition-colors">
              Services
            </Link>
            <Link href="#how-it-works" className="hover:text-forest-900 transition-colors">
              How It Works
            </Link>
            <Link href="#benefits" className="hover:text-forest-900 transition-colors">
              Benefits
            </Link>
            <Link href="#about" className="hover:text-forest-900 transition-colors">
              About
            </Link>
          </nav>

          {/* Actions & Language Selector */}
          <div className="hidden md:flex items-center gap-4">
            {/* Language Switcher */}
            <div className="relative">
              <button
                onClick={() => setLangDropdownOpen(!langDropdownOpen)}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-charcoal-700 hover:text-forest-950 bg-ivory-100 hover:bg-ivory-200 rounded-lg border border-ivory-300 transition-all"
                aria-label="Select Language"
              >
                <Globe className="w-3.5 h-3.5 text-forest-800" />
                <span>{selectedLang}</span>
              </button>

              {langDropdownOpen && (
                <div className="absolute right-0 mt-2 w-40 bg-white rounded-xl shadow-lg border border-ivory-200 py-1.5 z-50">
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => {
                        setSelectedLang(lang.code);
                        setLangDropdownOpen(false);
                      }}
                      className="w-full text-left px-3.5 py-2 text-xs text-charcoal-700 hover:bg-forest-50 hover:text-forest-900 flex items-center justify-between transition-colors"
                    >
                      <span>{lang.name}</span>
                      {selectedLang === lang.code && <span className="text-forest-800 font-bold">✓</span>}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Auth Conditional Display */}
            {user ? (
              <div className="flex items-center gap-2.5">
                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-forest-50 hover:bg-forest-100 text-forest-900 border border-forest-200 font-semibold text-xs shadow-sm transition-all"
                >
                  <LayoutDashboard className="w-3.5 h-3.5 text-forest-700" />
                  <span>Dashboard</span>
                </Link>

                <button
                  onClick={handleLogout}
                  className="inline-flex items-center gap-1 px-3 py-2 rounded-xl text-charcoal-600 hover:text-red-700 hover:bg-ivory-100 text-xs font-semibold transition-all"
                  title="Sign Out"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/login"
                  className="px-4 py-2 text-xs font-bold text-charcoal-700 hover:text-forest-950 transition-colors"
                >
                  Sign In
                </Link>

                <Link
                  href="/register"
                  className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-semibold text-xs shadow-sm hover:shadow-md transition-all active:scale-[0.98]"
                >
                  <span>Get Started</span>
                  <ArrowUpRight className="w-3.5 h-3.5 opacity-75" />
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle Button */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-charcoal-700 hover:bg-ivory-200 focus:outline-none"
              aria-label="Toggle Menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-ivory-200 bg-[#FBF9F2] px-4 pt-3 pb-6 space-y-4">
          <nav className="flex flex-col space-y-3 text-base font-medium text-charcoal-800">
            <Link
              href="#services"
              onClick={() => setMobileMenuOpen(false)}
              className="px-2 py-1.5 rounded-lg hover:bg-ivory-100"
            >
              Services
            </Link>
            <Link
              href="#how-it-works"
              onClick={() => setMobileMenuOpen(false)}
              className="px-2 py-1.5 rounded-lg hover:bg-ivory-100"
            >
              How It Works
            </Link>
            <Link
              href="#benefits"
              onClick={() => setMobileMenuOpen(false)}
              className="px-2 py-1.5 rounded-lg hover:bg-ivory-100"
            >
              Benefits
            </Link>
            <Link
              href="#about"
              onClick={() => setMobileMenuOpen(false)}
              className="px-2 py-1.5 rounded-lg hover:bg-ivory-100"
            >
              About
            </Link>
          </nav>

          <div className="pt-2 border-t border-ivory-200 flex flex-col gap-3">
            <div className="flex items-center justify-between px-2 py-1 text-sm text-charcoal-600">
              <span className="flex items-center gap-1.5">
                <Globe className="w-4 h-4 text-forest-800" /> Language:
              </span>
              <select
                value={selectedLang}
                onChange={(e) => setSelectedLang(e.target.value)}
                className="bg-ivory-100 border border-ivory-300 rounded px-2 py-1 text-xs font-semibold"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code}>{l.name}</option>
                ))}
              </select>
            </div>

            {user ? (
              <div className="flex flex-col gap-2 pt-1">
                <Link
                  href="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center py-2.5 rounded-xl bg-forest-900 text-white font-semibold text-sm shadow-sm"
                >
                  Go to Dashboard &rarr;
                </Link>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout();
                  }}
                  className="w-full text-center py-2 rounded-xl border border-ivory-300 bg-white text-red-700 font-semibold text-xs"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="flex flex-col gap-2 pt-1">
                <Link
                  href="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center py-2.5 rounded-xl border border-ivory-300 bg-white text-charcoal-800 font-semibold text-sm"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center py-2.5 rounded-xl bg-forest-900 text-white font-semibold text-sm shadow-sm"
                >
                  Get Started (Register) &rarr;
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

