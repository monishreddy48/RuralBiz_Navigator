import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { EntrepreneurCollage } from "@/components/EntrepreneurCollage";
import { PlatformIntro } from "@/components/PlatformIntro";
import { ServicesGrid } from "@/components/ServicesGrid";
import { HowItWorks } from "@/components/HowItWorks";
import { Benefits } from "@/components/Benefits";
import { Footer } from "@/components/Footer";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col bg-[#FBF9F2] text-charcoal-900 selection:bg-forest-100 selection:text-forest-900 font-sans antialiased">
      <Navbar />
      <Hero />
      <EntrepreneurCollage />
      <PlatformIntro />
      <ServicesGrid />
      <HowItWorks />
      <Benefits />
      <Footer />
    </main>
  );
}

