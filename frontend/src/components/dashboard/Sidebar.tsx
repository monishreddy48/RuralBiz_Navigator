"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import {
  LayoutDashboard,
  BarChart3,
  MapPin,
  Lightbulb,
  CreditCard,
  TrendingDown,
  FileSpreadsheet,
  Building2,
  Bot,
  User,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  ShieldCheck,
} from "lucide-react";

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
}

interface NavGroup {
  label: string;
  items: NavItem[];
}

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, userProfile, logout } = useAuth();

  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const navigationGroups: NavGroup[] = [
    {
      label: "OVERVIEW",
      items: [{ name: "Dashboard", href: "/dashboard", icon: LayoutDashboard }],
    },
    {
      label: "BUSINESS INTELLIGENCE",
      items: [
        { name: "Business Feasibility", href: "/dashboard/feasibility", icon: BarChart3 },
        { name: "Hyperlocal Market", href: "/dashboard/market", icon: MapPin },
        { name: "Business Alternatives", href: "/dashboard/alternatives", icon: Lightbulb },
      ],
    },
    {
      label: "FINANCIAL TOOLS",
      items: [
        { name: "Financial Calculator", href: "/dashboard/financial", icon: CreditCard },
        { name: "What-If Simulator", href: "/dashboard/simulator", icon: TrendingDown },
        { name: "DPR Report", href: "/dashboard/dpr", icon: FileSpreadsheet },
      ],
    },
    {
      label: "GOVERNMENT SUPPORT",
      items: [
        { name: "Scheme Navigator", href: "/dashboard/schemes", icon: Building2 },
      ],
    },
    {
      label: "AI SUPPORT",
      items: [
        { name: "AI Assistant", href: "/dashboard/assistant", icon: Bot },
      ],
    },
    {
      label: "ADDITIONAL",
      items: [
        { name: "Entrepreneur Profile", href: "/complete-profile", icon: User },
      ],
    },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/login");
    } catch (e) {
      console.error("Logout error:", e);
    }
  };

  const isActive = (href: string) => {
    if (href === "/dashboard") return pathname === "/dashboard";
    return pathname.startsWith(href);
  };

  return (
    <>
      {/* Mobile Menu Bar (visible on sm/md screens) */}
      <div className="lg:hidden sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-ivory-200 px-4 py-3 flex items-center justify-between shadow-xs">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-forest-900 text-ivory-50 flex items-center justify-center font-bold text-base shadow-sm">
            🌾
          </div>
          <span className="font-extrabold text-base tracking-tight text-forest-950">
            RuralBiz <span className="text-forest-700 font-semibold">Navigator</span>
          </span>
        </Link>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-2 rounded-lg text-charcoal-700 hover:bg-ivory-100"
          aria-label="Toggle navigation menu"
        >
          {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer Backdrop */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 z-50 bg-black/40 backdrop-blur-xs transition-opacity"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar Container (Desktop fixed + Mobile slide-over) */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 bg-white border-r border-ivory-200 flex flex-col justify-between transition-all duration-300 ${
          collapsed ? "w-20" : "w-72"
        } ${
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        {/* Top: Brand Header */}
        <div>
          <div className="h-20 px-6 border-b border-ivory-200 flex items-center justify-between">
            {!collapsed ? (
              <Link href="/" className="flex items-center gap-2.5 group">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-forest-950 via-forest-900 to-forest-700 flex items-center justify-center text-ivory-50 shadow-md group-hover:shadow-forest-900/20 transition-all shrink-0">
                  <span className="text-lg font-bold">🌾</span>
                </div>
                <div className="flex flex-col overflow-hidden">
                  <span className="text-lg font-extrabold tracking-tight text-forest-950 font-sans leading-none truncate">
                    RuralBiz <span className="text-forest-700 font-semibold">Nav</span>
                  </span>
                  <span className="text-[10px] font-medium text-charcoal-500 tracking-wide mt-1 truncate">
                    Smarter rural businesses.
                  </span>
                </div>
              </Link>
            ) : (
              <Link href="/" className="mx-auto" title="RuralBiz Navigator">
                <div className="w-10 h-10 rounded-xl bg-forest-900 text-ivory-50 flex items-center justify-center font-bold text-lg shadow-sm">
                  🌾
                </div>
              </Link>
            )}

            {/* Desktop Collapse Toggle */}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="hidden lg:flex p-1.5 rounded-lg text-charcoal-400 hover:text-charcoal-700 hover:bg-ivory-100 transition-colors"
              title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              {collapsed ? (
                <ChevronRight className="w-4 h-4" />
              ) : (
                <ChevronLeft className="w-4 h-4" />
              )}
            </button>
          </div>

          {/* Navigation Groups List */}
          <div className="px-3 py-4 space-y-6 overflow-y-auto max-h-[calc(100vh-170px)]">
            {navigationGroups.map((group, gIdx) => (
              <div key={gIdx} className="space-y-1">
                {!collapsed && (
                  <div className="px-3 text-[10px] font-bold text-charcoal-400 uppercase tracking-wider mb-1.5">
                    {group.label}
                  </div>
                )}
                {group.items.map((item, idx) => {
                  const Icon = item.icon;
                  const active = isActive(item.href);

                  return (
                    <Link
                      key={idx}
                      href={item.href}
                      onClick={() => setMobileOpen(false)}
                      title={collapsed ? item.name : undefined}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all duration-150 ${
                        active
                          ? "bg-forest-900 text-white shadow-sm font-bold"
                          : "text-charcoal-700 hover:bg-forest-50 hover:text-forest-900"
                      } ${collapsed ? "justify-center px-0" : ""}`}
                    >
                      <Icon
                        className={`w-4 h-4 shrink-0 ${
                          active ? "text-forest-200" : "text-charcoal-500 group-hover:text-forest-800"
                        }`}
                      />
                      {!collapsed && <span className="truncate">{item.name}</span>}
                    </Link>
                  );
                })}
              </div>
            ))}
          </div>
        </div>

        {/* Bottom: User Card & Sign Out */}
        <div className="p-3 border-t border-ivory-200 bg-ivory-50/60">
          {!collapsed ? (
            <div className="flex items-center justify-between p-2 rounded-xl bg-white border border-ivory-200">
              <div className="flex items-center gap-2.5 overflow-hidden">
                <div className="w-8 h-8 rounded-full bg-forest-100 text-forest-900 flex items-center justify-center font-bold text-xs shrink-0">
                  {userProfile?.fullName?.[0]?.toUpperCase() || user?.displayName?.[0]?.toUpperCase() || "E"}
                </div>
                <div className="flex flex-col overflow-hidden text-left">
                  <span className="text-xs font-bold text-charcoal-900 truncate">
                    {userProfile?.fullName || user?.displayName || "Entrepreneur"}
                  </span>
                  <span className="text-[10px] text-charcoal-500 font-mono truncate">
                    {userProfile?.village ? `${userProfile.village}` : user?.email || "Local User"}
                  </span>
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="p-1.5 rounded-lg text-charcoal-500 hover:text-red-700 hover:bg-red-50 transition-colors"
                title="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center p-2 rounded-xl text-charcoal-600 hover:text-red-700 hover:bg-red-50 transition-colors"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          )}
        </div>
      </aside>
    </>
  );
}
