"use client";

import React from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { Sidebar } from "@/components/dashboard/Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedRoute requireCompletedProfile={false}>
      <div className="min-h-screen bg-[#FBF9F2] flex flex-col">
        <Sidebar />
        <div className="flex-1 lg:pl-72 flex flex-col min-h-screen">
          {children}
        </div>
      </div>
    </ProtectedRoute>
  );
}
