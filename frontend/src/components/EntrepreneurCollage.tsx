"use client";

import Image from "next/image";
import { Sparkles, TrendingUp, Users, MapPin } from "lucide-react";

export function EntrepreneurCollage() {
  const entrepreneurs = [
    {
      title: "Textile & Handloom Unit",
      sector: "Women-Led Manufacturing",
      location: "Coastal Cluster, Odisha",
      image: "https://images.unsplash.com/photo-1606744888344-493238955de0?auto=format&fit=crop&w=700&q=80",
      metric: "₹93k Outlay • 67 Viability",
      highlight: "Artisan SHG cooperative",
    },
    {
      title: "Agro-Processing & Milling",
      sector: "Food Manufacturing",
      location: "Agri Hub, Nashik, MH",
      image: "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=700&q=80",
      metric: "₹2.15L Outlay • 82 Viability",
      highlight: "High local mandi demand",
    },
    {
      title: "Common Service Centre (CSC)",
      sector: "Digital & Citizen Services",
      location: "Panchayat Hub, Telangana",
      image: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=700&q=80",
      metric: "₹1.40L Outlay • 79 Viability",
      highlight: "Essential service footfall",
    },
    {
      title: "Small Light Fabrication Workshop",
      sector: "Repair & Mechanical",
      location: "Rural Highway, Karnataka",
      image: "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=700&q=80",
      metric: "₹1.80L Outlay • 74 Viability",
      highlight: "Tractor & farm implement repair",
    },
    {
      title: "Modern Rural General Store",
      sector: "Village Retail & FMCG",
      location: "Peri-Urban Mandi, Punjab",
      image: "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=700&q=80",
      metric: "₹1.90L Outlay • 61 Viability",
      highlight: "High-density daily footfall",
    },
    {
      title: "Rural Logistics & Auto Fleet",
      sector: "Transport Services",
      location: "Market Catchment, Gujarat",
      image: "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=700&q=80",
      metric: "₹3.20L Outlay • 81 Viability",
      highlight: "Cold-chain farm-to-mandi links",
    },
  ];

  return (
    <section className="py-16 md:py-24 bg-[#F7F4EB] border-y border-ivory-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 text-forest-800 text-xs font-bold tracking-wider uppercase mb-2">
            <Users className="w-4 h-4" />
            <span>Powering Diverse Rural Enterprise Sectors</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-forest-950 tracking-tight">
            Built for Every Rural Business, Beyond Agriculture Alone.
          </h2>
          <p className="mt-3 text-base sm:text-lg text-charcoal-600">
            From women-led handloom collectives to fabrication workshops, retail grocery hubs, digital kiosks, and logistics providers—RuralBiz Navigator provides exact local catchment economics for all 10 core rural trade categories.
          </p>
        </div>

        {/* 6-Card Visual Collage */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {entrepreneurs.map((item, idx) => (
            <div
              key={idx}
              className="group relative bg-white rounded-2xl overflow-hidden border border-ivory-200 shadow-subtle hover:shadow-card transition-all duration-300 flex flex-col"
            >
              {/* Image Container */}
              <div className="relative h-56 w-full overflow-hidden bg-ivory-200">
                <Image
                  src={item.image}
                  alt={item.title}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-500"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/10 to-transparent" />
                
                {/* Sector Pill */}
                <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-sm px-3 py-1 rounded-full text-[11px] font-bold text-forest-900 shadow-sm">
                  {item.sector}
                </div>

                {/* Location */}
                <div className="absolute bottom-3 left-3 flex items-center gap-1.5 text-white text-xs font-medium drop-shadow">
                  <MapPin className="w-3.5 h-3.5 text-sage-300" />
                  <span>{item.location}</span>
                </div>
              </div>

              {/* Card Body */}
              <div className="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="text-lg font-bold text-charcoal-900 group-hover:text-forest-900 transition-colors">
                    {item.title}
                  </h3>
                  <p className="text-xs text-charcoal-500 mt-1">
                    {item.highlight}
                  </p>
                </div>

                {/* Metric Strip */}
                <div className="mt-4 pt-3 border-t border-ivory-200 flex items-center justify-between text-xs">
                  <span className="font-semibold text-forest-800 bg-forest-50 px-2.5 py-1 rounded-md">
                    {item.metric}
                  </span>
                  <span className="text-charcoal-400 group-hover:text-forest-700 font-semibold flex items-center gap-1 transition-colors">
                    Analyze &rarr;
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}

