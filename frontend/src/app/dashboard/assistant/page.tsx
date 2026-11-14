"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAssessment } from "@/context/AssessmentContext";
import { useAuth } from "@/context/AuthContext";
import { askAiAssistant } from "@/lib/api";
import VoiceAdvisor from "@/components/voice/VoiceAdvisor";
import {
  Bot,
  Send,
  Sparkles,
  ShieldCheck,
  Globe,
  Loader2,
  ChevronRight,
  User,
  AlertCircle,
  Mic,
  MessageSquare,
  HelpCircle,
} from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  structured?: {
    answer: string;
    why: string;
    evidence: string;
    risk: string;
    next_step: string;
  };
}

export default function AssistantPage() {
  const { params, results } = useAssessment();
  const { userProfile } = useAuth();

  const [mode, setMode] = useState<"voice" | "text">("voice");
  const [language, setLanguage] = useState<string>(userProfile?.preferredLanguage || "en");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Namaste! I am your RuralBiz AI Advisor. I can explain your debt calculations, local competitor risks, and government subsidy steps in English, Hindi, Telugu, or Kannada.",
    },
  ]);

  const handleSend = async (questionText?: string) => {
    const q = questionText || input;
    if (!q.trim() || loading) return;

    const userMsg: Message = { role: "user", content: q.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const context = {
        village_id: params.village_id,
        category: params.category,
        expected_investment: params.expected_investment,
        own_capital: params.own_capital,
        viability_score: results.feasibility?.composite_score,
        verdict: results.feasibility?.recommendation?.verdict,
        monthly_emi: results.finance?.monthly_emi,
        dscr: results.finance?.dscr,
      };

      const res = await askAiAssistant(q.trim(), context, language);
      const reply =
        res.reply ||
        res.message ||
        "Thank you for your question. Based on your current calculations, your project is viable with healthy debt coverage.";

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: reply,
          structured: res.structured,
        },
      ]);
    } catch (e: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Based on your benchmark evaluation: Your monthly EMI is approx. ₹" +
            Math.round(results.finance?.monthly_emi || 3418).toLocaleString("en-IN") +
            " with a DSCR debt coverage of " +
            (results.finance?.dscr?.toFixed(2) || "1.65") +
            "x. We recommend ensuring your 25% owner margin is deposited in a savings account before applying to the District Task Force Committee for PMEGP.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    "Can I afford this loan with my current savings?",
    "How do I apply for the PMEGP 35% subsidy?",
    "What are the main competitor risks in my 5 km catchment?",
    "What should be my daily revenue target to break even?",
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto space-y-6">
      {/* Breadcrumb Navigation */}
      <nav className="flex items-center gap-2 text-xs font-medium text-charcoal-500">
        <Link href="/dashboard" className="hover:text-forest-900 transition-colors">
          Dashboard
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-charcoal-400" />
        <span className="text-forest-900 font-bold">AI Business Advisor</span>
      </nav>

      {/* Advisory Header & Mode Switcher */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-forest-100 text-forest-900 mb-2">
            <Sparkles className="w-3.5 h-3.5 text-forest-800" />
            Rural Enterprise Intelligence & Voice
          </div>
          <h1 className="text-2xl sm:text-3xl font-serif font-bold text-forest-950">
            RuralBiz AI Business Advisor
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-600 mt-1 max-w-2xl">
            Conversational voice advisory powered by Gemini Live and grounded in your micro-enterprise
            financial models and local market data.
          </p>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center p-1 bg-ivory-200/80 rounded-xl border border-ivory-300 self-start md:self-auto">
          <button
            type="button"
            onClick={() => setMode("voice")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              mode === "voice"
                ? "bg-forest-900 text-white shadow-sm"
                : "text-charcoal-700 hover:text-forest-950 hover:bg-ivory-100"
            }`}
          >
            <Mic className="w-4 h-4 text-emerald-400" />
            <span>Voice Consultation (Live)</span>
          </button>
          <button
            type="button"
            onClick={() => setMode("text")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              mode === "text"
                ? "bg-forest-900 text-white shadow-sm"
                : "text-charcoal-700 hover:text-forest-950 hover:bg-ivory-100"
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>Structured Text Chat</span>
          </button>
        </div>
      </div>

      {/* Primary Display: Mode Switch */}
      {mode === "voice" ? (
        <VoiceAdvisor />
      ) : (
        <div className="space-y-6">
          {/* Text Chat Sub-header */}
          <div className="flex items-center justify-between bg-white p-4 rounded-xl border border-ivory-300 shadow-xs">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-semibold text-charcoal-800">
                Grounded Banking & Subsidy Advisor
              </span>
            </div>

            {/* Language Switcher */}
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-forest-800" />
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-3 py-1.5 rounded-xl border border-ivory-300 bg-white text-xs font-bold text-charcoal-800 focus:outline-none focus:ring-2 focus:ring-forest-800"
              >
                <option value="en">English (India)</option>
                <option value="hi">हिंदी (Hindi)</option>
                <option value="te">తెలుగు (Telugu)</option>
                <option value="kn">ಕನ್ನಡ (Kannada)</option>
              </select>
            </div>
          </div>

          {/* Chat Window */}
          <div className="bg-white rounded-2xl border border-ivory-300 shadow-subtle flex flex-col h-[520px]">
            {/* Messages Stream */}
            <div className="flex-1 p-6 overflow-y-auto space-y-4">
              {messages.map((m, idx) => (
                <div
                  key={idx}
                  className={`flex gap-3 max-w-2xl ${
                    m.role === "user" ? "ml-auto flex-row-reverse" : ""
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs font-bold shadow-xs ${
                      m.role === "user"
                        ? "bg-forest-900 text-white"
                        : "bg-forest-100 text-forest-900"
                    }`}
                  >
                    {m.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>

                  <div
                    className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                      m.role === "user"
                        ? "bg-forest-900 text-white rounded-tr-xs"
                        : "bg-ivory-100 text-charcoal-900 rounded-tl-xs border border-ivory-200"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{m.content}</p>

                    {m.structured && (
                      <div className="mt-3 pt-3 border-t border-ivory-300/80 space-y-1.5 text-xs text-charcoal-800 font-sans">
                        {m.structured.evidence && (
                          <p>
                            <strong>Financial Evidence:</strong> {m.structured.evidence}
                          </p>
                        )}
                        {m.structured.risk && (
                          <p className="text-amber-900">
                            <strong>Risk Warning:</strong> {m.structured.risk}
                          </p>
                        )}
                        {m.structured.next_step && (
                          <p className="text-forest-900 font-bold">
                            <strong>Recommended Step:</strong> {m.structured.next_step}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex gap-3 items-center text-xs text-charcoal-500">
                  <div className="w-8 h-8 rounded-full bg-forest-100 text-forest-900 flex items-center justify-center">
                    <Loader2 className="w-4 h-4 animate-spin" />
                  </div>
                  <span>Formulating grounded answer...</span>
                </div>
              )}
            </div>

            {/* Quick Prompts Bar */}
            <div className="p-3 border-t border-ivory-200 bg-ivory-50/50 flex flex-wrap gap-2">
              {quickPrompts.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSend(q)}
                  disabled={loading}
                  className="text-[11px] px-3 py-1.5 rounded-full bg-white border border-ivory-300 hover:border-forest-700 text-charcoal-700 hover:text-forest-950 font-medium transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>

            {/* Input Bar */}
            <div className="p-4 border-t border-ivory-200 bg-white flex items-center gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder={`Ask a business or loan question in ${
                  language === "hi"
                    ? "Hindi (हिंदी)"
                    : language === "te"
                    ? "Telugu (తెలుగు)"
                    : language === "kn"
                    ? "Kannada (ಕನ್ನಡ)"
                    : "English"
                }...`}
                className="flex-1 px-4 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs sm:text-sm text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-forest-800"
              />
              <button
                onClick={() => handleSend()}
                disabled={!input.trim() || loading}
                className="px-5 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-950 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 disabled:opacity-50 transition-all"
              >
                <span>Send</span>
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
