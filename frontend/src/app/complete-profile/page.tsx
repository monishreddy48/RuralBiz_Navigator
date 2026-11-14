"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import {
  INDIAN_STATES,
  BUSINESS_CATEGORIES,
  PreferredLanguage,
  BusinessStage,
  UserProfileFormData,
} from "@/types/user";
import {
  User,
  MapPin,
  Building,
  Globe,
  Briefcase,
  Layers,
  ArrowRight,
  Loader2,
  CheckCircle2,
  ShieldCheck,
} from "lucide-react";

export default function CompleteProfilePage() {
  return (
    <ProtectedRoute requireCompletedProfile={false}>
      <ProfileForm />
    </ProtectedRoute>
  );
}

function ProfileForm() {
  const router = useRouter();
  const { user, userProfile, updateUserProfile } = useAuth();

  const [fullName, setFullName] = useState("");
  const [state, setState] = useState<string>(INDIAN_STATES[11]); // Default Maharashtra or first
  const [district, setDistrict] = useState("");
  const [village, setVillage] = useState("");
  const [preferredLanguage, setPreferredLanguage] = useState<PreferredLanguage>("en");
  const [businessCategory, setBusinessCategory] = useState<string>(BUSINESS_CATEGORIES[0]);
  const [businessStage, setBusinessStage] = useState<BusinessStage>("new_plan");

  const [submitting, setSubmitting] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (userProfile) {
      if (userProfile.fullName) setFullName(userProfile.fullName);
      if (userProfile.state) setState(userProfile.state as any);
      if (userProfile.district) setDistrict(userProfile.district);
      if (userProfile.village) setVillage(userProfile.village);
      if (userProfile.preferredLanguage) setPreferredLanguage(userProfile.preferredLanguage);
      if (userProfile.businessCategory) setBusinessCategory(userProfile.businessCategory);
      if (userProfile.businessStage) setBusinessStage(userProfile.businessStage);
    } else if (user?.displayName) {
      setFullName(user.displayName);
    }
  }, [userProfile, user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fullName.trim() || !village.trim() || !district.trim()) {
      alert("Please fill in your Full Name, District, and Village/Locality.");
      return;
    }

    setSubmitting(true);
    try {
      const formData: UserProfileFormData = {
        fullName: fullName.trim(),
        state,
        district: district.trim(),
        village: village.trim(),
        preferredLanguage,
        businessCategory,
        businessStage,
      };

      await updateUserProfile(formData);
      setSavedSuccess(true);
      setTimeout(() => {
        router.push("/dashboard");
      }, 800);
    } catch (err: any) {
      console.error("Error updating profile:", err);
      alert("Failed to save profile. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#FBF9F2] via-[#F8F5EB] to-[#FBF9F2] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-forest-100 text-forest-900 text-xs font-bold uppercase tracking-wider mb-3">
            <ShieldCheck className="w-4 h-4 text-forest-700" />
            <span>Step 2: Entrepreneur Profile</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-forest-950 tracking-tight">
            Complete Your Rural Business Profile
          </h1>
          <p className="mt-2 text-sm sm:text-base text-charcoal-600 max-w-xl mx-auto">
            Your location, preferred language, and trade sector calibrate your 5–10 km catchment mapping and credit subsidy routing.
          </p>
        </div>

        {/* Form Container */}
        <div className="bg-white rounded-3xl border border-ivory-300 shadow-card p-6 sm:p-10">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Section 1: Personal Details */}
            <div className="pb-6 border-b border-ivory-200">
              <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-900 mb-4 flex items-center gap-2">
                <User className="w-4 h-4 text-forest-700" />
                <span>Personal Information</span>
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Full Name */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Enter your full name"
                    className="w-full px-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 transition-all"
                  />
                </div>

                {/* Email (Read-Only) */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    Registered Email
                  </label>
                  <input
                    type="email"
                    disabled
                    value={user?.email || ""}
                    className="w-full px-4 py-2.5 rounded-xl border border-ivory-200 bg-ivory-100 text-sm text-charcoal-500 cursor-not-allowed"
                  />
                </div>
              </div>
            </div>

            {/* Section 2: Location & Catchment */}
            <div className="pb-6 border-b border-ivory-200">
              <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-900 mb-4 flex items-center gap-2">
                <MapPin className="w-4 h-4 text-forest-700" />
                <span>Locality &amp; Catchment</span>
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {/* State */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    State *
                  </label>
                  <select
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-forest-800 transition-all"
                  >
                    {INDIAN_STATES.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </div>

                {/* District */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    District *
                  </label>
                  <input
                    type="text"
                    required
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    placeholder="e.g., Nashik / Warangal"
                    className="w-full px-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 transition-all"
                  />
                </div>

                {/* Village / Locality */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    Village / Town *
                  </label>
                  <input
                    type="text"
                    required
                    value={village}
                    onChange={(e) => setVillage(e.target.value)}
                    placeholder="e.g., Pimpalgaon / Shamirpet"
                    className="w-full px-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-forest-800 transition-all"
                  />
                </div>
              </div>
            </div>

            {/* Section 3: Enterprise & Sector */}
            <div className="pb-6 border-b border-ivory-200">
              <h2 className="text-sm font-extrabold uppercase tracking-wider text-forest-900 mb-4 flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-forest-700" />
                <span>Enterprise Focus &amp; Category</span>
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Business Category */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    Target Enterprise Trade *
                  </label>
                  <select
                    value={businessCategory}
                    onChange={(e) => setBusinessCategory(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-forest-800 transition-all"
                  >
                    {BUSINESS_CATEGORIES.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Preferred Language */}
                <div>
                  <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-1.5">
                    Advisory Language *
                  </label>
                  <select
                    value={preferredLanguage}
                    onChange={(e) => setPreferredLanguage(e.target.value as PreferredLanguage)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-forest-800 transition-all"
                  >
                    <option value="en">English</option>
                    <option value="hi">हिंदी (Hindi)</option>
                    <option value="te">తెలుగు (Telugu)</option>
                    <option value="kn">ಕನ್ನಡ (Kannada)</option>
                  </select>
                </div>
              </div>

              {/* Business Stage (New vs Existing) */}
              <div className="mt-4">
                <label className="block text-xs font-bold text-charcoal-800 uppercase tracking-wider mb-2">
                  Enterprise Lifecycle Stage *
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <label
                    className={`flex items-start gap-3 p-3.5 rounded-xl border cursor-pointer transition-all ${
                      businessStage === "new_plan"
                        ? "border-forest-800 bg-forest-50/70 shadow-sm"
                        : "border-ivory-300 bg-white hover:bg-ivory-50"
                    }`}
                  >
                    <input
                      type="radio"
                      name="businessStage"
                      value="new_plan"
                      checked={businessStage === "new_plan"}
                      onChange={() => setBusinessStage("new_plan")}
                      className="mt-1 text-forest-800 focus:ring-forest-800"
                    />
                    <div>
                      <div className="font-bold text-sm text-charcoal-900">
                        New Business Plan
                      </div>
                      <div className="text-xs text-charcoal-600 mt-0.5">
                        Starting a brand-new enterprise from idea to loan appraisal.
                      </div>
                    </div>
                  </label>

                  <label
                    className={`flex items-start gap-3 p-3.5 rounded-xl border cursor-pointer transition-all ${
                      businessStage === "existing_business"
                        ? "border-forest-800 bg-forest-50/70 shadow-sm"
                        : "border-ivory-300 bg-white hover:bg-ivory-50"
                    }`}
                  >
                    <input
                      type="radio"
                      name="businessStage"
                      value="existing_business"
                      checked={businessStage === "existing_business"}
                      onChange={() => setBusinessStage("existing_business")}
                      className="mt-1 text-forest-800 focus:ring-forest-800"
                    />
                    <div>
                      <div className="font-bold text-sm text-charcoal-900">
                        Existing Business Expansion
                      </div>
                      <div className="text-xs text-charcoal-600 mt-0.5">
                        Refinancing, adding machinery, or expanding capacity.
                      </div>
                    </div>
                  </label>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-4">
              <button
                type="button"
                onClick={() => router.push("/dashboard")}
                className="text-xs font-semibold text-charcoal-500 hover:text-charcoal-800 transition-colors"
              >
                Skip for now &amp; explore dashboard &rarr;
              </button>

              <button
                type="submit"
                disabled={submitting}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all disabled:opacity-50"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Saving Profile...</span>
                  </>
                ) : savedSuccess ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 text-forest-200" />
                    <span>Saved! Opening Dashboard...</span>
                  </>
                ) : (
                  <>
                    <span>Save &amp; Go to Business Dashboard</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>

          </form>
        </div>

      </div>
    </div>
  );
}

