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
} from "lucide-react";

export default function MarketPage() {
  const { params, results } = useAssessment();
  const [catchmentData, setCatchmentData] = useState<any>(results.catchment);
  const [loading, setLoading] = useState(false);

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
