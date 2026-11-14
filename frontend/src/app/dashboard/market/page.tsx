"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAssessment } from "@/context/AssessmentContext";
import { fetchCatchment } from "@/lib/api";
import {
  MapPin,
  Users,
  Store,
  Compass,
  ArrowRight,
  TrendingUp,
  ShieldCheck,
  Building,
  Target,
  ChevronRight,
  Loader2,
  Info,
} from "lucide-react";

export default function MarketPage() {
  const { params, results } = useAssessment();
  const [catchmentData, setCatchmentData] = useState<any>(results.catchment);
  const [loading, setLoading] = useState(false);
  const [hoveredComp, setHoveredComp] = useState<any | null>(null);

  useEffect(() => {
    if (!catchmentData) {
      setLoading(true);
      fetchCatchment(params.village_id, params.category)
        .then(setCatchmentData)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [params.village_id, params.category, catchmentData]);

  const competitors = catchmentData?.competitors || [];
  const loc = catchmentData?.locality || {
    village_name: "Demo Village A (Agri Hub)",
    district: "Ludhiana",
    state: "Punjab",
    latitude: 30.901,
    longitude: 75.8573,
    population: 4200,
    households: 750,
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-ivory-200 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-forest-800 mb-1">
            <MapPin className="w-4 h-4 text-forest-700" />
            <span>Module 2 &bull; GIS Hyperlocal Catchment Intelligence</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-forest-950 tracking-tight">
            Hyperlocal Market &amp; Catchment Mapping
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Calculates customer footfall density, competitor saturation, and unmet demand gaps within the 5 km walk-in and 10 km weekly haat circles.
          </p>
        </div>

        <Link
          href="/dashboard/financial"
          className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white text-xs font-bold shadow-xs transition-all self-start sm:self-auto"
        >
          <span>Next: Financial Planning</span>
          <ChevronRight className="w-4 h-4" />
        </Link>
      </div>

      {/* 2-Circle Catchment Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* 5 km Catchment */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold uppercase tracking-wider text-forest-900">
              5 km Primary Radius
            </span>
            <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 text-[10px] font-bold">
              WALK-IN &bull; DAILY
            </span>
          </div>
          <div className="text-2xl font-extrabold text-forest-950">
            {loc.population ? loc.population.toLocaleString("en-IN") : "4,200"}
            <span className="text-xs font-medium text-charcoal-500 ml-1.5">Residents</span>
          </div>
          <p className="text-xs text-charcoal-600 leading-relaxed">
            Primary walk-in customer base across approx. {loc.households || 750} households. Generates consistent daily repeat footfall.
          </p>
          <div className="pt-2 border-t border-ivory-200 text-[11px] text-charcoal-500">
            Purchasing Power Index: <strong className="text-charcoal-900">{loc.purchasing_power_index || 82}/100</strong>
          </div>
        </div>

        {/* 10 km Catchment */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold uppercase tracking-wider text-forest-900">
              10 km Secondary Radius
            </span>
            <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-800 text-[10px] font-bold">
              WEEKLY HAAT &bull; MANDI
            </span>
          </div>
          <div className="text-2xl font-extrabold text-forest-950">
            {loc.population ? (loc.population * 2.8).toFixed(0).toLocaleString() : "11,760"}
            <span className="text-xs font-medium text-charcoal-500 ml-1.5">Residents</span>
          </div>
          <p className="text-xs text-charcoal-600 leading-relaxed">
            Extended trading cluster connected by rural link roads. Feeds weekly haat market stalls and bulk commercial buyers.
          </p>
          <div className="pt-2 border-t border-ivory-200 text-[11px] text-charcoal-500">
            Nearest APMC Mandi: <strong className="text-charcoal-900">{loc.market_distance_km || 3.5} km</strong>
          </div>
        </div>

        {/* Unmet Demand Gap */}
        <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold uppercase tracking-wider text-forest-900">
              Unmet Market Gap
            </span>
            <Target className="w-4 h-4 text-forest-700" />
          </div>
          <div className="text-2xl font-extrabold text-emerald-800">
            ₹{catchmentData?.unmet_demand_gap_rupees
              ? Math.round(catchmentData.unmet_demand_gap_rupees).toLocaleString("en-IN")
              : "28,500"}
            <span className="text-xs font-medium text-charcoal-500 ml-1.5">/ month</span>
          </div>
          <p className="text-xs text-charcoal-600 leading-relaxed">
            Estimated unserved customer spending currently flowing out of the village to peri-urban commercial markets.
          </p>
          <div className="pt-2 border-t border-ivory-200 text-[11px] text-charcoal-500">
            Saturation Index: <strong className="text-charcoal-900">{catchmentData?.competitor_saturation_index || "Moderate"}</strong>
          </div>
        </div>

      </div>

      {/* Interactive GIS Catchment Radar Visualization */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-ivory-200 pb-3">
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-950 flex items-center gap-2">
              <Compass className="w-4 h-4 text-forest-700" />
              <span>Interactive Catchment GIS Radar</span>
            </h2>
            <p className="text-xs text-charcoal-600 mt-0.5">
              Hover over competitor entities to view distance, monthly sales volume, and customer rating.
            </p>
          </div>
          <div className="flex items-center gap-4 text-[11px] font-semibold">
            <span className="flex items-center gap-1.5 text-emerald-800">
              <span className="w-2.5 h-2.5 rounded-full border border-emerald-600 bg-emerald-100" />
              5 km Daily Walk-in Circle
            </span>
            <span className="flex items-center gap-1.5 text-blue-800">
              <span className="w-2.5 h-2.5 rounded-full border border-blue-600 bg-blue-100" />
              10 km Weekly Haat Circle
            </span>
            <span className="flex items-center gap-1.5 text-red-700">
              <span className="w-2.5 h-2.5 rounded-full bg-red-600" />
              Competitor Entity
            </span>
          </div>
        </div>

        {/* SVG Radar Container */}
        <div className="relative w-full h-[380px] bg-gradient-to-b from-forest-950/5 via-forest-900/5 to-forest-950/10 rounded-2xl border border-ivory-200 flex items-center justify-center overflow-hidden">
          <svg className="w-full h-full" viewBox="0 0 600 360">
            {/* Grid Crosshairs */}
            <line x1="300" y1="20" x2="300" y2="340" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="3 3" />
            <line x1="60" y1="180" x2="540" y2="180" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="3 3" />

            {/* Compass Labels */}
            <text x="300" y="32" textAnchor="middle" fill="#64748b" fontSize="10" fontWeight="bold">NORTH (MANDI LINK)</text>
            <text x="300" y="335" textAnchor="middle" fill="#64748b" fontSize="10" fontWeight="bold">SOUTH (CANAL BELT)</text>
            <text x="525" y="184" textAnchor="end" fill="#64748b" fontSize="10" fontWeight="bold">EAST</text>
            <text x="75" y="184" textAnchor="start" fill="#64748b" fontSize="10" fontWeight="bold">WEST</text>

            {/* 10 km Outer Catchment Circle */}
            <circle cx="300" cy="180" r="150" fill="#3b82f6" fillOpacity="0.05" stroke="#3b82f6" strokeWidth="1.5" strokeDasharray="5 5" />
            <text x="440" y="165" fill="#2563eb" fontSize="9" fontWeight="bold">10 km Haat Circle</text>

            {/* 5 km Inner Catchment Circle */}
            <circle cx="300" cy="180" r="85" fill="#059669" fillOpacity="0.08" stroke="#059669" strokeWidth="1.5" strokeDasharray="4 4" />
            <text x="375" y="172" fill="#047857" fontSize="9" fontWeight="bold">5 km Walk-in</text>

            {/* Center: Village Core */}
            <circle cx="300" cy="180" r="7" fill="#0f5132" stroke="#ffffff" strokeWidth="2" />
            <text x="300" y="202" textAnchor="middle" fill="#0f5132" fontSize="11" fontWeight="bold">
              {loc.village_name}
            </text>

            {/* Plot Competitors */}
            {competitors.map((c: any, idx: number) => {
              // Calculate deterministic polar offset from index & distance
              const angle = (idx * 65 * Math.PI) / 180 + 0.4;
              const dist = c.distance_from_center || (idx + 1) * 1.5;
              // Map distance to pixels (10 km = 150px)
              const radiusPixels = Math.min(145, Math.max(30, (dist / 10) * 150));
              const cx = 300 + radiusPixels * Math.cos(angle);
              const cy = 180 + radiusPixels * Math.sin(angle);

              const isHovered = hoveredComp?.competitor_id === c.competitor_id;

              return (
                <g
                  key={idx}
                  className="cursor-pointer transition-all duration-150"
                  onMouseEnter={() => setHoveredComp(c)}
                  onMouseLeave={() => setHoveredComp(null)}
                >
                  <circle
                    cx={cx}
                    cy={cy}
                    r={isHovered ? 8 : 5}
                    fill={isHovered ? "#b91c1c" : "#dc2626"}
                    stroke="#ffffff"
                    strokeWidth="1.5"
                  />
                  <text
                    x={cx}
                    y={cy - 8}
                    textAnchor="middle"
                    fill="#1f2937"
                    fontSize="9"
                    fontWeight="600"
                  >
                    {c.business_name}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Hover Tooltip Box */}
          {hoveredComp && (
            <div className="absolute bottom-4 right-4 bg-white/95 backdrop-blur-md p-3.5 rounded-xl border border-ivory-300 shadow-md text-xs space-y-1 max-w-xs animate-in fade-in duration-150">
              <div className="font-bold text-forest-950 flex items-center justify-between">
                <span>{hoveredComp.business_name}</span>
                <span className="text-[10px] text-red-700 bg-red-50 px-1.5 py-0.2 rounded font-mono">
                  {hoveredComp.distance_from_center ? `${hoveredComp.distance_from_center} km` : "1.8 km"}
                </span>
              </div>
              <p className="text-[11px] text-charcoal-600">
                Type: {hoveredComp.business_type} &bull; Rating: {hoveredComp.customer_rating || "3.8"}/5.0
              </p>
              <div className="text-[11px] font-mono font-semibold text-charcoal-800 pt-1 border-t border-ivory-200 flex justify-between">
                <span>Est. Sales:</span>
                <span>₹{hoveredComp.estimated_monthly_sales ? hoveredComp.estimated_monthly_sales.toLocaleString("en-IN") : "48,000"}/mo</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Mapped Competitors Table */}
      <div className="bg-white rounded-2xl p-6 border border-ivory-300 shadow-subtle space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-ivory-200 pb-3">
          <div>
            <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-950 flex items-center gap-2">
              <Store className="w-4 h-4 text-forest-700" />
              <span>Competitor Entities in Catchment ({competitors.length} Mapped)</span>
            </h2>
            <p className="text-xs text-charcoal-600 mt-0.5">
              Verified local businesses operating in the same or adjacent product categories within your village block.
            </p>
          </div>
          <span className="text-xs text-charcoal-500 font-mono">
            GPS Center: {loc.latitude?.toFixed(4)}, {loc.longitude?.toFixed(4)}
          </span>
        </div>

        {competitors.length === 0 ? (
          <div className="py-8 text-center text-xs text-charcoal-500">
            No direct competitors detected in immediate 2 km walk-in cluster.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-ivory-100 text-charcoal-600 uppercase font-bold text-[10px] tracking-wider">
                <tr>
                  <th className="py-2.5 px-3 rounded-l-lg">Entity Name</th>
                  <th className="py-2.5 px-3">Category</th>
                  <th className="py-2.5 px-3">Distance</th>
                  <th className="py-2.5 px-3">Est. Monthly Sales</th>
                  <th className="py-2.5 px-3">Price Level</th>
                  <th className="py-2.5 px-3 rounded-r-lg">Competitive Strength</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-ivory-100 font-medium text-charcoal-800">
                {competitors.map((c: any, idx: number) => (
                  <tr key={idx} className="hover:bg-ivory-50/80 transition-colors">
                    <td className="py-3 px-3 font-bold text-forest-950">{c.business_name}</td>
                    <td className="py-3 px-3 text-charcoal-600">{c.business_type}</td>
                    <td className="py-3 px-3 font-mono">{c.distance_from_center ? `${c.distance_from_center} km` : "1.2 km"}</td>
                    <td className="py-3 px-3 font-mono">₹{c.estimated_monthly_sales ? c.estimated_monthly_sales.toLocaleString("en-IN") : "45,000"}</td>
                    <td className="py-3 px-3">{c.price_level || "Medium"}</td>
                    <td className="py-3 px-3">
                      <span className="inline-block px-2 py-0.5 rounded bg-ivory-200 text-charcoal-700 text-[10px] font-semibold">
                        {c.strength || "Established local trust"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
}
