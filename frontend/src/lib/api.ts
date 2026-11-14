/**
 * RuralBiz Navigator - FastAPI Backend API Client
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export async function fetchLocalities() {
  try {
    const res = await fetch(`${API_BASE_URL}/market/localities`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed to fetch localities from FastAPI, using fallback:", err);
    return [
      {
        village_id: "VIL_001",
        village_name: "Demo Village A (Agri Hub)",
        district: "Ludhiana",
        state: "Punjab",
        latitude: 30.901,
        longitude: 75.8573,
        population: 4200,
        purchasing_power_index: 82.0,
      },
      {
        village_id: "VIL_005",
        village_name: "Demo Village E (Horticulture Cluster)",
        district: "Nashik",
        state: "Maharashtra",
        latitude: 19.9975,
        longitude: 73.7898,
        population: 5100,
        purchasing_power_index: 78.0,
      },
    ];
  }
}

export async function fetchBusinesses() {
  try {
    const res = await fetch(`${API_BASE_URL}/market/businesses`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed to fetch businesses from FastAPI, using fallback:", err);
    return [];
  }
}

export async function evaluateFeasibility(params: {
  village_id: string;
  category: string;
  expected_investment: number;
  own_capital: number;
}) {
  const res = await fetch(`${API_BASE_URL}/feasibility/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to evaluate feasibility (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function fetchCatchment(villageId: string, category: string) {
  const url = `${API_BASE_URL}/market/catchment/${encodeURIComponent(villageId)}?category=${encodeURIComponent(category)}`;
  const res = await fetch(url);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to fetch catchment (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function calculateFinance(params: {
  project_cost: number;
  own_contribution: number;
  annual_interest_rate?: number;
  tenure_months?: number;
  moratorium_months?: number;
  monthly_sales?: number;
  variable_cost_ratio?: number;
  monthly_fixed_cost?: number;
  unit_price?: number;
}) {
  const res = await fetch(`${API_BASE_URL}/financial/calculate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      annual_interest_rate: 9.5,
      tenure_months: 60,
      moratorium_months: 3,
      monthly_sales: 65000,
      variable_cost_ratio: 0.48,
      monthly_fixed_cost: 7500,
      unit_price: 80,
      ...params,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to calculate finance (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function runStressTest(params: {
  project_cost: number;
  own_contribution: number;
  sales_vol_delta_pct?: number;
  price_delta_pct?: number;
  var_cost_delta_pct?: number;
  fixed_cost_delta_pct?: number;
  interest_rate_delta?: number;
  base_monthly_sales?: number;
  base_variable_cost_ratio?: number;
  base_monthly_fixed_cost?: number;
}) {
  const res = await fetch(`${API_BASE_URL}/simulator/stress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sales_vol_delta_pct: -20.0,
      price_delta_pct: 0.0,
      var_cost_delta_pct: 0.0,
      fixed_cost_delta_pct: 0.0,
      interest_rate_delta: 0.0,
      base_monthly_sales: 65000,
      base_variable_cost_ratio: 0.48,
      base_monthly_fixed_cost: 7500,
      ...params,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to run stress test (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function matchSchemes(params: {
  project_cost: number;
  business_category: string;
  target_group_tags?: string[];
  is_existing?: boolean;
}) {
  const res = await fetch(`${API_BASE_URL}/schemes/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      target_group_tags: ["General", "Rural"],
      is_existing: false,
      ...params,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to match schemes (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function fetchRankedAlternatives(villageId: string, availableCapital: number) {
  const url = `${API_BASE_URL}/alternatives/rank?village_id=${encodeURIComponent(villageId)}&available_capital=${availableCapital}`;
  const res = await fetch(url);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to fetch alternatives (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function askAiAssistant(question: string, context?: any, language = "en") {
  const res = await fetch(`${API_BASE_URL}/ai/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, context, language }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to query AI assistant (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function fetchVoiceSession() {
  const res = await fetch(`${API_BASE_URL}/voice/session`);
  if (!res.ok) {
    throw new Error(`Failed to initialize voice session (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function queryVoiceAdvisor(
  text: string,
  language: string,
  context?: Record<string, any>
) {
  const res = await fetch(`${API_BASE_URL}/voice/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language, context }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to query voice advisor (HTTP ${res.status})`);
  }
  return await res.json();
}

export async function downloadDprPdf(payload: {
  entrepreneur_name?: string;
  village_id: string;
  category: string;
  expected_investment: number;
  own_capital: number;
  experience_level?: string;
  is_existing?: boolean;
}): Promise<Blob> {
  const res = await fetch(`${API_BASE_URL}/reports/dpr/download`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to generate DPR PDF (HTTP ${res.status})`);
  }
  return await res.blob();
}

export function getVoiceWebSocketUrl(): string {
  // Convert http/https URL to ws/wss
  const httpUrl = API_BASE_URL;
  if (httpUrl.startsWith("https://")) {
    return `${httpUrl.replace("https://", "wss://")}/voice/live`;
  }
  return `${httpUrl.replace("http://", "ws://")}/voice/live`;
}


