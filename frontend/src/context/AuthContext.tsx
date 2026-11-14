"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import {
  type User,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  signOut,
  sendPasswordResetEmail,
  confirmPasswordReset,
  verifyPasswordResetCode,
  updateProfile,
} from "firebase/auth";
import { auth, googleProvider, isFirebaseConfigured } from "@/lib/firebase";
import { UserProfile, UserProfileFormData } from "@/types/user";

interface AuthContextType {
  user: User | null;
  userProfile: UserProfile | null;
  loading: boolean;
  firebaseConfigured: boolean;
  loginWithEmail: (email: string, password: string) => Promise<User>;
  registerWithEmail: (email: string, password: string, fullName: string) => Promise<User>;
  loginWithGoogle: () => Promise<User>;
  logout: () => Promise<void>;
  sendResetEmail: (email: string) => Promise<void>;
  verifyResetCode: (oobCode: string) => Promise<string>;
  confirmReset: (oobCode: string, newPassword: string) => Promise<void>;
  updateUserProfile: (data: UserProfileFormData) => Promise<UserProfile>;
  refreshUserProfile: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [configured, setConfigured] = useState(false);

  // Helper to load profile from storage
  const loadProfile = (firebaseUser: User): UserProfile => {
    const storageKey = `ruralbiz_profile_${firebaseUser.uid}`;
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {
      console.error("Error reading profile from localStorage:", e);
    }

    // Default uncompleted profile
    const defaultProfile: UserProfile = {
      uid: firebaseUser.uid,
      email: firebaseUser.email,
      fullName: firebaseUser.displayName || "",
      state: "",
      district: "",
      village: "",
      preferredLanguage: "en",
      businessCategory: "",
      businessStage: "new_plan",
      createdAt: new Date().toISOString(),
      profileCompleted: false,
    };
    return defaultProfile;
  };

  // Helper to save profile to storage
  const saveProfileLocally = (profile: UserProfile) => {
    try {
      localStorage.setItem(`ruralbiz_profile_${profile.uid}`, JSON.stringify(profile));
      setUserProfile(profile);
    } catch (e) {
      console.error("Error saving profile to localStorage:", e);
    }
  };

  useEffect(() => {
    const isConfig = isFirebaseConfigured();
    setConfigured(isConfig);

    if (!isConfig || !auth) {
      setLoading(false);
      return;
    }

    // Subscribe to Firebase Auth state listener
    const unsubscribe = onAuthStateChanged(
      auth,
      (firebaseUser) => {
        if (firebaseUser) {
          setUser(firebaseUser);
          const profile = loadProfile(firebaseUser);
          setUserProfile(profile);
        } else {
          setUser(null);
          setUserProfile(null);
        }
        setLoading(false);
      },
      (error) => {
        console.error("Firebase auth state error:", error);
        setUser(null);
        setUserProfile(null);
        setLoading(false);
      }
    );

    return () => unsubscribe();
  }, []);

  const loginWithEmail = async (email: string, password: string): Promise<User> => {
    if (!auth) throw new Error("auth/missing-credentials");
    const cred = await signInWithEmailAndPassword(auth, email.trim(), password);
    const profile = loadProfile(cred.user);
    setUserProfile(profile);
    return cred.user;
  };

  const registerWithEmail = async (
    email: string,
    password: string,
    fullName: string
  ): Promise<User> => {
    if (!auth) throw new Error("auth/missing-credentials");
    const cred = await createUserWithEmailAndPassword(auth, email.trim(), password);
    
    // Update display name on Firebase user
    if (fullName.trim()) {
      await updateProfile(cred.user, { displayName: fullName.trim() });
    }

    // Initialize baseline profile
    const newProfile: UserProfile = {
      uid: cred.user.uid,
      email: cred.user.email,
      fullName: fullName.trim(),
      state: "",
      district: "",
      village: "",
      preferredLanguage: "en",
      businessCategory: "",
      businessStage: "new_plan",
      createdAt: new Date().toISOString(),
      profileCompleted: false,
    };
    saveProfileLocally(newProfile);

    return cred.user;
  };

  const loginWithGoogle = async (): Promise<User> => {
    if (!auth) throw new Error("auth/missing-credentials");
    const cred = await signInWithPopup(auth, googleProvider);
    
    // Check if profile exists, otherwise initialize
    const existing = loadProfile(cred.user);
    if (!existing.fullName && cred.user.displayName) {
      existing.fullName = cred.user.displayName;
    }
    saveProfileLocally(existing);

    return cred.user;
  };

  const logout = async (): Promise<void> => {
    if (!auth) return;
    await signOut(auth);
    setUser(null);
    setUserProfile(null);
  };

  const sendResetEmail = async (email: string): Promise<void> => {
    if (!auth) throw new Error("auth/missing-credentials");
    await sendPasswordResetEmail(auth, email.trim(), {
      url: typeof window !== "undefined" ? `${window.location.origin}/login` : "http://localhost:3000/login",
    });
  };

  const verifyResetCode = async (oobCode: string): Promise<string> => {
    if (!auth) throw new Error("auth/missing-credentials");
    return await verifyPasswordResetCode(auth, oobCode);
  };

  const confirmReset = async (oobCode: string, newPassword: string): Promise<void> => {
    if (!auth) throw new Error("auth/missing-credentials");
    await confirmPasswordReset(auth, oobCode, newPassword);
  };

  const updateUserProfile = async (data: UserProfileFormData): Promise<UserProfile> => {
    if (!user) throw new Error("User must be authenticated to update profile");
    
    const updated: UserProfile = {
      uid: user.uid,
      email: user.email,
      fullName: data.fullName.trim(),
      state: data.state,
      district: data.district.trim(),
      village: data.village.trim(),
      preferredLanguage: data.preferredLanguage,
      businessCategory: data.businessCategory,
      businessStage: data.businessStage,
      createdAt: userProfile?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      profileCompleted: true,
    };

    saveProfileLocally(updated);

    // Also update Firebase auth displayName if changed
    if (auth?.currentUser && data.fullName.trim() !== auth.currentUser.displayName) {
      try {
        await updateProfile(auth.currentUser, { displayName: data.fullName.trim() });
      } catch (e) {
        console.warn("Could not update Firebase displayName:", e);
      }
    }

    return updated;
  };

  const refreshUserProfile = () => {
    if (user) {
      const p = loadProfile(user);
      setUserProfile(p);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        userProfile,
        loading,
        firebaseConfigured: configured,
        loginWithEmail,
        registerWithEmail,
        loginWithGoogle,
        logout,
        sendResetEmail,
        verifyResetCode,
        confirmReset,
        updateUserProfile,
        refreshUserProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

