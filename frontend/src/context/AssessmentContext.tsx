"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useAuth } from "./AuthContext";
import {
  evaluateFeasibility,
  fetchCatchment,
  calculateFinance,
  runStressTest,
  matchSchemes,
  fetchRankedAlternatives,
} from "@/lib/api";

export interface AssessmentParams {
  village_id: string;
  category: string;
  expected_investment: number;
  own_capital: number;
  annual_interest_rate: number;
  tenure_months: number;
  moratorium_months: number;
  monthly_sales?: number;
  variable_cost_ratio?: number;
  monthly_fixed_cost?: number;
}

export interface SavedAssessment {
  id: string;
  userId: string;
  date: string;
  params: AssessmentParams;
  viabilityScore: number;
  verdict: "GO" | "MODIFY" | "AVOID";
  category: string;
  villageName: string;
}

interface AssessmentContextType {
  params: AssessmentParams;
  setParams: React.Dispatch<React.SetStateAction<AssessmentParams>>;
  updateParam: <K extends keyof AssessmentParams>(key: K, value: AssessmentParams[K]) => void;
  results: {
    feasibility: any | null;
    catchment: any | null;
    finance: any | null;
    stress: any | null;
    schemes: any[] | null;
    alternatives: any[] | null;
  };
  loading: boolean;
  error: string | null;
  hasRunAssessment: boolean;
  runFullAssessment: (overrideParams?: AssessmentParams) => Promise<void>;
  loadDemoCase: (caseId: 1 | 2 | 3) => Promise<void>;
  savedAssessments: SavedAssessment[];
  saveCurrentAssessment: () => void;
  deleteSavedAssessment: (id: string) => void;
}

const defaultParams: AssessmentParams = {
  village_id: "VIL_001",
  category: "Food Processing",
  expected_investment: 215000,
  own_capital: 53750,
  annual_interest_rate: 9.5,
  tenure_months: 60,
  moratorium_months: 3,
};

const AssessmentContext = createContext<AssessmentContextType | undefined>(undefined);

export function AssessmentProvider({ children }: { children: React.ReactNode }) {
  const { user, userProfile } = useAuth();

  const [params, setParams] = useState<AssessmentParams>(defaultParams);
  const [results, setResults] = useState<{
    feasibility: any | null;
    catchment: any | null;
    finance: any | null;
    stress: any | null;
    schemes: any[] | null;
    alternatives: any[] | null;
  }>({
    feasibility: null,
    catchment: null,
    finance: null,
    stress: null,
    schemes: null,
    alternatives: null,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasRunAssessment, setHasRunAssessment] = useState(false);
  const [savedAssessments, setSavedAssessments] = useState<SavedAssessment[]>([]);

  // Sync profile preferred category / village if available
  useEffect(() => {
    if (userProfile?.businessCategory) {
      // Map category to backend category
      let mappedCat = "Food Processing";
      if (userProfile.businessCategory.includes("Retail")) mappedCat = "Retail / General Store";
      else if (userProfile.businessCategory.includes("Textile") || userProfile.businessCategory.includes("Handloom")) mappedCat = "Tailoring";
      else if (userProfile.businessCategory.includes("Poultry")) mappedCat = "Poultry";
      else if (userProfile.businessCategory.includes("Dairy")) mappedCat = "Dairy";
      else if (userProfile.businessCategory.includes("Digital") || userProfile.businessCategory.includes("CSC")) mappedCat = "Digital / Service Centre";
      else if (userProfile.businessCategory.includes("Fabrication") || userProfile.businessCategory.includes("Repair")) mappedCat = "Mobile Repair";

      setParams((prev) => ({ ...prev, category: mappedCat }));
    }
  }, [userProfile]);

  // Load saved assessments from localStorage
  useEffect(() => {
    if (!user) {
      setSavedAssessments([]);
      return;
    }
    try {
      const saved = localStorage.getItem(`ruralbiz_assessments_${user.uid}`);
      if (saved) {
        setSavedAssessments(JSON.parse(saved));
      } else {
        setSavedAssessments([]);
      }
    } catch (e) {
      console.error("Error reading saved assessments:", e);
    }
  }, [user]);

  const updateParam = <K extends keyof AssessmentParams>(key: K, value: AssessmentParams[K]) => {
    setParams((prev) => ({ ...prev, [key]: value }));
  };

  const runFullAssessment = async (overrideParams?: AssessmentParams) => {
    const current = overrideParams || params;
    setLoading(true);
    setError(null);

    try {
      // Call FastAPI endpoints concurrently using Promise.allSettled for maximum fault-tolerance
      const [feasibilityRes, catchmentRes, financeRes, stressRes, schemesRes, alternativesRes] = await Promise.allSettled([
        evaluateFeasibility({
          village_id: current.village_id,
          category: current.category,
          expected_investment: current.expected_investment,
          own_capital: current.own_capital,
          annual_interest_rate: current.annual_interest_rate,
          tenure_months: current.tenure_months,
          moratorium_months: current.moratorium_months,
          monthly_sales: current.monthly_sales,
        }),
        fetchCatchment(current.village_id, current.category),
        calculateFinance({
          project_cost: current.expected_investment,
          own_contribution: current.own_capital,
          annual_interest_rate: current.annual_interest_rate,
          tenure_months: current.tenure_months,
          moratorium_months: current.moratorium_months,
        }),
        runStressTest({
          village_id: current.village_id,
          category: current.category,
          project_cost: current.expected_investment,
          own_capital: current.own_capital,
          own_contribution: current.own_capital,
        }),
        matchSchemes({
          project_cost: current.expected_investment,
          business_category: current.category,
        }),
        fetchRankedAlternatives(current.village_id, current.own_capital),
      ]);

      const feasibility = feasibilityRes.status === "fulfilled" ? feasibilityRes.value : null;
      const catchment = catchmentRes.status === "fulfilled" ? catchmentRes.value : null;
      const finance = financeRes.status === "fulfilled" ? financeRes.value : null;
      const stress = stressRes.status === "fulfilled" ? stressRes.value : null;
      const schemes = schemesRes.status === "fulfilled" ? schemesRes.value : null;
      const alternatives = alternativesRes.status === "fulfilled" ? alternativesRes.value : null;

      if (feasibilityRes.status === "rejected") {
        console.error("Feasibility calculation failed:", feasibilityRes.reason);
      }
      if (stressRes.status === "rejected") {
        console.warn("Simulator stress calculation warning:", stressRes.reason);
      }

      setResults((prev) => ({
        feasibility: feasibility ?? prev.feasibility,
        catchment: catchment ?? prev.catchment,
        finance: finance ?? prev.finance,
        stress: stress ?? prev.stress,
        schemes: schemes ?? prev.schemes,
        alternatives: alternatives ?? prev.alternatives,
      }));
      setHasRunAssessment(true);
    } catch (err: any) {
      console.error("Assessment execution error:", err);
      setError(err?.message || "Failed to complete evaluation. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const loadDemoCase = async (caseId: 1 | 2 | 3) => {
    let demoParams: AssessmentParams;

    if (caseId === 1) {
      // Case 1: GO - High Feasibility Flour Mill & Food Processing (~85/100 GO)
      demoParams = {
        village_id: "VIL_001",
        category: "Food Processing",
        expected_investment: 215000,
        own_capital: 53750,
        annual_interest_rate: 9.5,
        tenure_months: 60,
        moratorium_months: 3,
        monthly_sales: 65000,
      };
    } else if (caseId === 2) {
      // Case 2: MODIFY - Small Manufacturing Unit (~71/100 MODIFY - Tight DSCR, needs equity)
      demoParams = {
        village_id: "VIL_005",
        category: "Small Manufacturing",
        expected_investment: 320000,
        own_capital: 64000,
        annual_interest_rate: 10.0,
        tenure_months: 48,
        moratorium_months: 2,
        monthly_sales: 56000,
      };
    } else {
      // Case 3: AVOID - Saturated Village Retail Kirana Store (~55/100 AVOID - Negative margin/DSCR < 1.0)
      demoParams = {
        village_id: "VIL_004",
        category: "Retail / General Store",
        expected_investment: 190000,
        own_capital: 20000,
        annual_interest_rate: 12.0,
        tenure_months: 36,
        moratorium_months: 0,
        monthly_sales: 30000,
      };
    }

    setParams(demoParams);
    await runFullAssessment(demoParams);
  };

  const saveCurrentAssessment = () => {
    if (!user || !results.feasibility) return;

    const newRecord: SavedAssessment = {
      id: `ASM_${Date.now()}`,
      userId: user.uid,
      date: new Date().toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
      }),
      params: { ...params },
      viabilityScore: results.feasibility.viability_score || results.feasibility.composite_score || 75,
      verdict: (results.feasibility.recommendation?.decision || results.feasibility.recommendation?.verdict || "GO") as "GO" | "MODIFY" | "AVOID",
      category: params.category,
      villageName: results.feasibility.locality_name || params.village_id,
    };

    const updated = [newRecord, ...savedAssessments.slice(0, 9)];
    setSavedAssessments(updated);
    try {
      localStorage.setItem(`ruralbiz_assessments_${user.uid}`, JSON.stringify(updated));
    } catch (e) {
      console.error("Error saving assessment to localStorage:", e);
    }
  };

  const deleteSavedAssessment = (id: string) => {
    if (!user) return;
    const updated = savedAssessments.filter((item) => item.id !== id);
    setSavedAssessments(updated);
    try {
      localStorage.setItem(`ruralbiz_assessments_${user.uid}`, JSON.stringify(updated));
    } catch (e) {
      console.error("Error deleting assessment from localStorage:", e);
    }
  };

  return (
    <AssessmentContext.Provider
      value={{
        params,
        setParams,
        updateParam,
        results,
        loading,
        error,
        hasRunAssessment,
        runFullAssessment,
        loadDemoCase,
        savedAssessments,
        saveCurrentAssessment,
        deleteSavedAssessment,
      }}
    >
      {children}
    </AssessmentContext.Provider>
  );
}

export function useAssessment(): AssessmentContextType {
  const context = useContext(AssessmentContext);
  if (context === undefined) {
    throw new Error("useAssessment must be used within an AssessmentProvider");
  }
  return context;
}

