import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, type Auth } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "",
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "",
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "",
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || "",
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID || "",
};

export function isFirebaseConfigured(): boolean {
  const { apiKey, projectId } = firebaseConfig;
  return Boolean(
    apiKey &&
    projectId &&
    !apiKey.includes("your_firebase_api_key") &&
    apiKey.length > 10
  );
}

let app: FirebaseApp | undefined;
let auth: Auth | undefined;
const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({ prompt: "select_account" });

if (typeof window !== "undefined") {
  if (isFirebaseConfigured()) {
    try {
      app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
      auth = getAuth(app);
    } catch (error) {
      console.error("Firebase initialization error:", error);
    }
  } else {
    // Provide development warning
    console.warn(
      "[RuralBiz Navigator] Firebase client credentials not detected in NEXT_PUBLIC_FIREBASE_*. Please set them in frontend/.env.local."
    );
  }
}

export { app, auth, googleProvider };

