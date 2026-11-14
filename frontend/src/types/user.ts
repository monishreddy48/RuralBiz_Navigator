export type PreferredLanguage = "en" | "hi" | "te" | "kn";

export type BusinessStage = "new_plan" | "existing_business";

export interface UserProfile {
  uid: string;
  email: string | null;
  fullName: string;
  state: string;
  district: string;
  village: string;
  preferredLanguage: PreferredLanguage;
  businessCategory: string;
  businessStage: BusinessStage;
  createdAt: string;
  updatedAt?: string;
  profileCompleted: boolean;
}

export interface UserProfileFormData {
  fullName: string;
  state: string;
  district: string;
  village: string;
  preferredLanguage: PreferredLanguage;
  businessCategory: string;
  businessStage: BusinessStage;
}

export const INDIAN_STATES = [
  "Andhra Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Tamil Nadu",
  "Telangana",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal",
] as const;

export const BUSINESS_CATEGORIES = [
  "Food Processing & Milling",
  "Retail & Village Kirana Store",
  "Textile, Handloom & Apparel",
  "Light Fabrication & Mechanical Repair",
  "Common Service Centre (CSC) & Digital Kiosk",
  "Rural Transport & Small Logistics Fleet",
  "Animal Husbandry & Dairy Unit",
  "Poultry & Hatchery Farm",
  "Organic Fertilizer & Agri-Input Retail",
  "Village Tourism & Rural Hospitality",
] as const;

