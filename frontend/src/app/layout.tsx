import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RuralBiz Navigator | AI Hyper-Local Business Advisory & Financial Structuring",
  description: "Empowering rural micro-entrepreneurs and MSMEs across India with hyper-local catchment analysis, reducing-balance debt math, and bank-ready DPR generation.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="min-h-screen bg-[#FBF9F2] text-charcoal-900 selection:bg-forest-100 selection:text-forest-900">
        {children}
      </body>
    </html>
  );
}

