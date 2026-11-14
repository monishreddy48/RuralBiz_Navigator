import assert from "node:assert";
import { getFriendlyAuthErrorMessage } from "../src/lib/auth-errors.ts";
import { INDIAN_STATES, BUSINESS_CATEGORIES } from "../src/types/user.ts";

console.log("=== Running RuralBiz Navigator Auth Validation Tests ===");

// Test 1: Friendly Auth Error Mapping
console.log("Test 1: Error message mapping...");
const credError = getFriendlyAuthErrorMessage("auth/invalid-credential");
assert(credError.includes("does not match our records"), "Should map invalid credentials");

const emailInUse = getFriendlyAuthErrorMessage("auth/email-already-in-use");
assert(emailInUse.includes("already registered"), "Should map email in use");

const weakPass = getFriendlyAuthErrorMessage("auth/weak-password");
assert(weakPass.includes("at least 6 characters"), "Should map weak password");

const unauthDomain = getFriendlyAuthErrorMessage("auth/unauthorized-domain");
assert(unauthDomain.includes("localhost"), "Should mention localhost for authorized domains");

const popupClosed = getFriendlyAuthErrorMessage("auth/popup-closed-by-user");
assert(popupClosed.includes("closed before completing"), "Should map popup cancellation");

console.log("✓ All error message mappings passed.");

// Test 2: Profile Data Validations
console.log("Test 2: Profile data constraints...");
assert(INDIAN_STATES.length >= 20, "Should list major Indian states");
assert(INDIAN_STATES.includes("Maharashtra"), "Should contain Maharashtra");
assert(INDIAN_STATES.includes("Telangana"), "Should contain Telangana");
assert(INDIAN_STATES.includes("Karnataka"), "Should contain Karnataka");

assert(BUSINESS_CATEGORIES.length === 10, "Should include all 10 micro-enterprise sectors");
assert(BUSINESS_CATEGORIES.includes("Food Processing & Milling"), "Should include food processing");
assert(BUSINESS_CATEGORIES.includes("Retail & Village Kirana Store"), "Should include village retail");
assert(BUSINESS_CATEGORIES.includes("Common Service Centre (CSC) & Digital Kiosk"), "Should include CSC");

console.log("✓ All profile constraint tests passed.");

console.log("=== All Auth Tests Passed Successfully ===");

