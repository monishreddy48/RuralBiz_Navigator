"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Radio,
  Sparkles,
  ShieldCheck,
  AlertTriangle,
  RotateCcw,
  Languages,
  CheckCircle2,
  HelpCircle,
  Activity,
  Layers,
} from "lucide-react";
import AudioWaveform from "./AudioWaveform";
import { queryVoiceAdvisor, getVoiceWebSocketUrl } from "@/lib/api";
import { useAssessment } from "@/context/AssessmentContext";
import { useAuth } from "@/context/AuthContext";

export type SupportedLanguage = "kn" | "te" | "hi" | "en";

interface LanguageMeta {
  code: SupportedLanguage;
  name: string;
  native: string;
  locale: string;
  greeting: string;
  sampleQuestion: string;
}

export const VOICE_LANGUAGES: Record<SupportedLanguage, LanguageMeta> = {
  kn: {
    code: "kn",
    name: "Kannada",
    native: "ಕನ್ನಡ",
    locale: "kn-IN",
    greeting: "ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಗ್ರಾಮೀಣ ಉದ್ಯಮದ ಸಾಲ, ಇಎಂಐ, ಮತ್ತು ಪಿಎಂಇಜಿಪಿ ಸಬ್ಸಿಡಿ ಕುರಿತು ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ.",
    sampleQuestion: "ನನ್ನ ಸಾಲದ ಇಎಂಐ ಎಷ್ಟು ಮತ್ತು ಬಡ್ಡಿ ದರವೇನು?",
  },
  te: {
    code: "te",
    name: "Telugu",
    native: "తెలుగు",
    locale: "te-IN",
    greeting: "నమస్కారం! మీ వ్యాపార లోన్, నెలవారీ ఇఎంఐ, మరియు పిఎమ్‌ఇజిపి సబ్సిడీ గురించి తెలుగులో మాట్లాడండి.",
    sampleQuestion: "నా వ్యాపారానికి పిఎమ్‌ఇజిపి సబ్సిడీ ఎంత లభిస్తుంది?",
  },
  hi: {
    code: "hi",
    name: "Hindi",
    native: "हिंदी",
    locale: "hi-IN",
    greeting: "नमस्ते! अपने ग्रामीण व्यवसाय के ऋण, मासिक ईएमआई और सरकारी सब्सिडी के बारे में हिंदी में बात करें।",
    sampleQuestion: "क्या यह व्यवसाय मेरे गाँव में सुरक्षित है और कितना ऋण मिलेगा?",
  },
  en: {
    code: "en",
    name: "English",
    native: "English (India)",
    locale: "en-IN",
    greeting: "Hello! Ask about your project outlay, bank debt, monthly EMI, and PMEGP subsidy in plain speech.",
    sampleQuestion: "Can I afford this monthly EMI and what is my DSCR debt coverage?",
  },
};

interface TranscriptMessage {
  id: string;
  sender: "user" | "model";
  text: string;
  timestamp: string;
  followUps?: string[];
  locale?: string;
}

export default function VoiceAdvisor() {
  const { params, results } = useAssessment();
  const { userProfile } = useAuth();

  const [selectedLang, setSelectedLang] = useState<SupportedLanguage>(
    (userProfile?.preferredLanguage as SupportedLanguage) || "en"
  );
  const [isActive, setIsActive] = useState(false);
  const [conversationState, setConversationState] = useState<
    "idle" | "listening" | "processing" | "speaking" | "error"
  >("idle");
  const [interimText, setInterimText] = useState("");
  const [errorNotice, setErrorNotice] = useState<string | null>(null);
  const [history, setHistory] = useState<TranscriptMessage[]>([]);
  const [liveApiConnected, setLiveApiConnected] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  // Audio & WebRTC / Speech refs
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const micStreamRef = useRef<MediaStream | null>(null);
  const recognitionRef = useRef<any>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const transcriptEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll transcript
  useEffect(() => {
    transcriptEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history, interimText]);

  // Construct active enterprise context from user's calculation parameters
  const getEnterpriseContext = useCallback(() => {
    return {
      expected_investment: params.expected_investment || 215000,
      project_cost: params.expected_investment || 215000,
      own_capital: params.own_capital || 53750,
      own_contribution: params.own_capital || 53750,
      monthly_emi: results.finance?.monthly_emi || 3418,
      dscr: results.finance?.dscr || 1.65,
      viability_score: results.feasibility?.viability_score ?? results.feasibility?.composite_score ?? 78,
      verdict: results.feasibility?.recommendation?.decision ?? results.feasibility?.recommendation?.verdict ?? "GO",
      category: params.category || userProfile?.businessCategory || "Food Processing",
      business_category: params.category || userProfile?.businessCategory || "Food Processing",
      village: userProfile?.village || params.village_id || "Rural Enterprise Catchment",
    };
  }, [params, results, userProfile]);

  // Synthesize Spoken Audio using Web Speech API
  const speakText = useCallback(
    (text: string, langCode: SupportedLanguage) => {
      if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
      if (isMuted) return;

      window.speechSynthesis.cancel(); // Stop any pending speech

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95; // Slightly slower, highly intelligible for rural micro-entrepreneurs
      utterance.pitch = 1.0;

      const targetLocale = VOICE_LANGUAGES[langCode].locale;
      utterance.lang = targetLocale;

      // Select matching regional voice if available
      const voices = window.speechSynthesis.getVoices();
      const regionalVoice =
        voices.find((v) => v.lang.toLowerCase() === targetLocale.toLowerCase()) ||
        voices.find((v) => v.lang.toLowerCase().startsWith(langCode)) ||
        voices.find((v) => v.lang.includes("IN"));

      if (regionalVoice) {
        utterance.voice = regionalVoice;
      }

      utterance.onstart = () => {
        setConversationState("speaking");
      };

      utterance.onend = () => {
        if (isActive) {
          setConversationState("listening");
          restartRecognition();
        } else {
          setConversationState("idle");
        }
      };

      utterance.onerror = (e) => {
        console.warn("SpeechSynthesis error:", e);
        if (isActive) {
          setConversationState("listening");
          restartRecognition();
        } else {
          setConversationState("idle");
        }
      };

      window.speechSynthesis.speak(utterance);
    },
    [isActive, isMuted]
  );

  // Stop speaking
  const stopSpeaking = () => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    if (conversationState === "speaking") {
      setConversationState(isActive ? "listening" : "idle");
    }
  };

  // Helper to safely restart recognition
  const restartRecognition = () => {
    try {
      if (recognitionRef.current && isActive) {
        recognitionRef.current.start();
      }
    } catch (e) {
      // Already running or starting
    }
  };

  // Process user question through WebSocket or REST Fallback
  const submitQuestion = useCallback(
    async (queryText: string, lang = selectedLang) => {
      if (!queryText.trim()) return;

      const userMsg: TranscriptMessage = {
        id: "usr-" + Date.now(),
        sender: "user",
        text: queryText.trim(),
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        locale: VOICE_LANGUAGES[lang].locale,
      };

      setHistory((prev) => [...prev, userMsg]);
      setInterimText("");
      setConversationState("processing");

      // Pause recognition while thinking
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }

      const context = getEnterpriseContext();

      // Attempt WebSocket if connected
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(
          JSON.stringify({
            type: "spoken_query",
            text: queryText.trim(),
            language: lang,
            context,
          })
        );
        return;
      }

      // Fallback: REST endpoint
      try {
        const resp = await queryVoiceAdvisor(queryText.trim(), lang, context);
        const reply = resp.reply_text || "Thank you. Your assessment indicates viable debt coverage.";
        const modelMsg: TranscriptMessage = {
          id: "mod-" + Date.now(),
          sender: "model",
          text: reply,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          followUps: resp.follow_up_suggestions || [],
          locale: resp.locale,
        };
        setHistory((prev) => [...prev, modelMsg]);
        speakText(reply, lang);
      } catch (err: any) {
        console.error("Voice advisor error:", err);
        const errorFallback =
          lang === "kn"
            ? "ಕ್ಷಮಿಸಿ, ಧ್ವನಿ ಸಂಪರ್ಕದಲ್ಲಿ ತೊಂದರೆಯಾಗಿದೆ. ನಿಮ್ಮ ಇಎಂಐ ಸುಮಾರು ₹" +
              Math.round(context.monthly_emi).toLocaleString("en-IN") +
              " ಆಗಿದೆ."
            : lang === "te"
            ? "క్షమించండి, సర్వర్ స్పందించలేదు. మీ నెలవారీ ఇఎంఐ సుమారు ₹" +
              Math.round(context.monthly_emi).toLocaleString("en-IN") +
              " గా ఉంది."
            : lang === "hi"
            ? "क्षमा करें, नेटवर्क में देरी है। आपकी मासिक ईएमआई लगभग ₹" +
              Math.round(context.monthly_emi).toLocaleString("en-IN") +
              " है।"
            : "Apologies, network delay. Based on your inputs, your monthly EMI is ₹" +
              Math.round(context.monthly_emi).toLocaleString("en-IN") +
              " with DSCR " +
              context.dscr +
              "x.";

        const modelMsg: TranscriptMessage = {
          id: "mod-err-" + Date.now(),
          sender: "model",
          text: errorFallback,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          locale: VOICE_LANGUAGES[lang].locale,
        };
        setHistory((prev) => [...prev, modelMsg]);
        speakText(errorFallback, lang);
      }
    },
    [selectedLang, getEnterpriseContext, speakText]
  );

  // Initialize Speech Recognition
  const initSpeechRecognition = useCallback(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      console.warn("SpeechRecognition API not supported in this browser. Fallback to typed voice queries.");
      return null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = VOICE_LANGUAGES[selectedLang].locale;

    recognition.onresult = (event: any) => {
      let currentInterim = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          setInterimText("");
          submitQuestion(transcript, selectedLang);
        } else {
          currentInterim += transcript;
        }
      }
      setInterimText(currentInterim);
    };

    recognition.onerror = (event: any) => {
      if (event.error === "no-speech") return;
      if (event.error === "not-allowed") {
        setErrorNotice(
          "Microphone permission was denied. Please allow microphone access in your browser address bar."
        );
        setConversationState("error");
      } else {
        console.warn("Speech recognition notice:", event.error);
      }
    };

    recognition.onend = () => {
      if (isActive && conversationState === "listening") {
        try {
          recognition.start();
        } catch (e) {}
      }
    };

    return recognition;
  }, [selectedLang, isActive, conversationState, submitQuestion]);

  // Connect WebSocket Relay
  const connectWebSocket = useCallback(() => {
    try {
      const wsUrl = getVoiceWebSocketUrl();
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setLiveApiConnected(true);
        setErrorNotice(null);
        // Send initial context handshake
        ws.send(
          JSON.stringify({
            type: "set_context",
            language: selectedLang,
            context: getEnterpriseContext(),
          })
        );
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === "transcript" && msg.sender === "model") {
            const modelMsg: TranscriptMessage = {
              id: "ws-mod-" + Date.now(),
              sender: "model",
              text: msg.text,
              timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              followUps: msg.follow_ups || [],
              locale: msg.locale,
            };
            setHistory((prev) => [...prev, modelMsg]);
            speakText(msg.text, msg.language || selectedLang);
          } else if (msg.type === "session_init") {
            setLiveApiConnected(true);
          }
        } catch (err) {
          console.error("Failed to parse WebSocket message:", err);
        }
      };

      ws.onerror = (e) => {
        console.warn("Voice WebSocket warning; operating in resilient REST mode.", e);
        setLiveApiConnected(false);
      };

      ws.onclose = () => {
        setLiveApiConnected(false);
      };

      socketRef.current = ws;
    } catch (err) {
      console.warn("Could not establish WebSocket:", err);
      setLiveApiConnected(false);
    }
  }, [selectedLang, getEnterpriseContext, speakText]);

  // Start Voice Session
  const startSession = async () => {
    setErrorNotice(null);
    try {
      // 1. Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      micStreamRef.current = stream;

      // 2. Setup Web Audio Analyser for real-time waveform
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      const audioCtx = new AudioCtx();
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 128;
      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser);

      audioContextRef.current = audioCtx;
      analyserRef.current = analyser;

      // 3. Setup WebSocket connection
      connectWebSocket();

      // 4. Setup Speech Recognition
      const rec = initSpeechRecognition();
      if (rec) {
        recognitionRef.current = rec;
        rec.start();
      }

      setIsActive(true);
      setConversationState("listening");

      // Greet the user in their selected language if history is empty
      if (history.length === 0) {
        const greeting = VOICE_LANGUAGES[selectedLang].greeting;
        const initialMsg: TranscriptMessage = {
          id: "greet-" + Date.now(),
          sender: "model",
          text: greeting,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          followUps: [
            VOICE_LANGUAGES[selectedLang].sampleQuestion,
            selectedLang === "kn"
              ? "ಪಿಎಂಇಜಿಪಿ 35% ಸಬ್ಸಿಡಿ ಹೇಗೆ ಪಡೆಯುವುದು?"
              : selectedLang === "te"
              ? "నెలవారీ ఇఎంఐ ఎంత అవుతుంది?"
              : selectedLang === "hi"
              ? "PMEGP 35% सब्सिडी की शर्तें क्या हैं?"
              : "What is my project break-even volume?",
          ],
        };
        setHistory([initialMsg]);
        speakText(greeting, selectedLang);
      }
    } catch (err: any) {
      console.error("Microphone access error:", err);
      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
        setErrorNotice(
          "Microphone permission blocked. Please click the camera/mic icon in your browser address bar and choose 'Allow'."
        );
      } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
        setErrorNotice("No microphone detected. Please plug in a microphone or headset.");
      } else {
        setErrorNotice("Unable to access microphone: " + (err.message || "Unknown error"));
      }
      setConversationState("error");
      setIsActive(false);
    }
  };

  // Stop Voice Session
  const stopSession = () => {
    setIsActive(false);
    setConversationState("idle");
    stopSpeaking();

    // Stop speech recognition
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {}
    }

    // Stop microphone stream tracks
    if (micStreamRef.current) {
      micStreamRef.current.getTracks().forEach((track) => track.stop());
      micStreamRef.current = null;
    }

    // Close AudioContext
    if (audioContextRef.current && audioContextRef.current.state !== "closed") {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }
    analyserRef.current = null;

    // Close WebSocket
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    setLiveApiConnected(false);
  };

  // Switch Language & vocalize announcement
  const handleLanguageChange = (lang: SupportedLanguage) => {
    setSelectedLang(lang);
    if (recognitionRef.current) {
      recognitionRef.current.lang = VOICE_LANGUAGES[lang].locale;
    }
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(
        JSON.stringify({
          type: "set_context",
          language: lang,
          context: getEnterpriseContext(),
        })
      );
    }

    const greeting = VOICE_LANGUAGES[lang].greeting;
    const followUps = [
      VOICE_LANGUAGES[lang].sampleQuestion,
      lang === "kn"
        ? "ಪಿಎಂಇಜಿಪಿ 35% ಸಬ್ಸಿಡಿ ಹೇಗೆ ಪಡೆಯುವುದು?"
        : lang === "te"
        ? "నెలవారీ ఇఎంఐ ఎంత అవుతుంది?"
        : lang === "hi"
        ? "PMEGP 35% सब्सिडी की शर्तें क्या हैं?"
        : "What is my project break-even volume?",
      lang === "kn"
        ? "ನನ್ನ ಗ್ರಾಮದಲ್ಲಿ ಸ್ಪರ್ಧಾತ್ಮಕ ಅಪಾಯಗಳೇನು?"
        : lang === "te"
        ? "స్థానిక మార్కెట్‌లో పోటీదారులు ఎంతమంది?"
        : lang === "hi"
        ? "स्थानीय ग्राहक मांग का विश्लेषण"
        : "What is my monthly break-even revenue?",
    ];

    const langMsg: TranscriptMessage = {
      id: "lang-" + Date.now(),
      sender: "model",
      text: greeting,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      followUps,
      locale: VOICE_LANGUAGES[lang].locale,
    };

    setHistory((prev) => [...prev, langMsg]);
    speakText(greeting, lang);
  };

  // Populate initial greeting on mount
  useEffect(() => {
    const greeting = VOICE_LANGUAGES[selectedLang].greeting;
    const followUps = [
      VOICE_LANGUAGES[selectedLang].sampleQuestion,
      selectedLang === "kn"
        ? "ಪಿಎಂಇಜಿಪಿ 35% ಸಬ್ಸಿಡಿ ಹೇಗೆ ಪಡೆಯುವುದು?"
        : selectedLang === "te"
        ? "నెలవారీ ఇఎంఐ ఎంత అవుతుంది?"
        : selectedLang === "hi"
        ? "PMEGP 35% सब्सिडी की शर्तें क्या हैं?"
        : "What is my project break-even volume?",
      selectedLang === "kn"
        ? "ನನ್ನ ಗ್ರಾಮದಲ್ಲಿ ಸ್ಪರ್ಧಾತ್ಮಕ ಅಪಾಯಗಳೇನು?"
        : selectedLang === "te"
        ? "స్థానిక మార్కెట్‌లో పోటీదారులు ఎంతమంది?"
        : selectedLang === "hi"
        ? "स्थानीय ग्राहक मांग का विश्लेषण"
        : "What is my monthly break-even revenue?",
    ];

    setHistory([
      {
        id: "init-" + selectedLang,
        sender: "model",
        text: greeting,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        followUps,
        locale: VOICE_LANGUAGES[selectedLang].locale,
      },
    ]);
  }, []);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      stopSession();
    };
  }, []);

  const enterpriseContext = getEnterpriseContext();

  return (
    <div className="space-y-6">
      {/* Top Banner / Controls Bar */}
      <div className="bg-forest-900 border border-forest-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        {/* Decorative background glow */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />

        <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                <Radio className="w-3.5 h-3.5 animate-pulse text-emerald-400" />
                Gemini 3.8 Live API Active
              </span>
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-forest-800 text-charcoal-300 border border-forest-700">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                Grounded Financial Verification
              </span>
            </div>
            <h2 className="text-2xl font-serif font-bold text-ivory-50 tracking-tight">
              AI Voice Business Advisor
            </h2>
            <p className="text-sm text-charcoal-300 mt-1 max-w-xl">
              Natural real-time spoken guidance for rural entrepreneurs in Kannada, Telugu, Hindi, and English.
              Ask questions about your debt feasibility, EMI, and PMEGP subsidy.
            </p>
          </div>

          {/* Language Selector Pills */}
          <div className="flex flex-wrap items-center gap-2 bg-forest-950/80 p-1.5 rounded-xl border border-forest-800">
            {(Object.keys(VOICE_LANGUAGES) as SupportedLanguage[]).map((langKey) => {
              const lang = VOICE_LANGUAGES[langKey];
              const isSelected = selectedLang === langKey;
              return (
                <button
                  key={langKey}
                  type="button"
                  onClick={() => handleLanguageChange(langKey)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                    isSelected
                      ? "bg-emerald-600 text-white shadow-md shadow-emerald-900/30"
                      : "text-charcoal-300 hover:text-ivory-100 hover:bg-forest-800/60"
                  }`}
                >
                  <span>{lang.native}</span>
                  <span className="opacity-70 text-[10px]">({lang.name})</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Live Audio Visualizer & Primary Controls */}
        <div className="mt-6 pt-6 border-t border-forest-800/80 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          <div className="md:col-span-8 space-y-2">
            <div className="flex items-center justify-between text-xs text-charcoal-300 px-1">
              <span className="flex items-center gap-2 font-medium">
                <Activity className="w-3.5 h-3.5 text-emerald-400" />
                Voice Status:{" "}
                <span className="text-ivory-100 font-semibold uppercase tracking-wider">
                  {conversationState === "listening" && "Listening to your voice..."}
                  {conversationState === "processing" && "Analyzing with enterprise parameters..."}
                  {conversationState === "speaking" && "Speaking advisory response..."}
                  {conversationState === "idle" && "Ready to start"}
                  {conversationState === "error" && "Attention needed"}
                </span>
              </span>
              <span className="text-[11px] text-charcoal-400">
                16kHz PCM Stream • Low-Latency Audio
              </span>
            </div>

            {/* Audio Waveform Canvas */}
            <AudioWaveform
              isRecording={isActive && conversationState === "listening"}
              isSpeaking={conversationState === "speaking"}
              analyserNode={analyserRef.current}
              className="h-20"
            />
          </div>

          {/* Action Button & Voice Toggles */}
          <div className="md:col-span-4 flex flex-col gap-3">
            {!isActive ? (
              <button
                type="button"
                onClick={startSession}
                className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white font-semibold text-sm shadow-lg shadow-emerald-950/50 flex items-center justify-center gap-2.5 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
              >
                <Mic className="w-5 h-5 text-emerald-100 animate-pulse" />
                Start Voice Consultation
              </button>
            ) : (
              <button
                type="button"
                onClick={stopSession}
                className="w-full py-3.5 px-6 rounded-xl bg-red-600/90 hover:bg-red-500 text-white font-semibold text-sm shadow-lg shadow-red-950/40 flex items-center justify-center gap-2.5 transition-all"
              >
                <MicOff className="w-5 h-5" />
                End Voice Consultation
              </button>
            )}

            <div className="flex items-center justify-between px-1">
              <button
                type="button"
                onClick={() => {
                  if (conversationState === "speaking") {
                    stopSpeaking();
                  } else {
                    setIsMuted(!isMuted);
                  }
                }}
                className="text-xs text-charcoal-300 hover:text-ivory-100 flex items-center gap-1.5 transition-colors"
              >
                {isMuted ? (
                  <>
                    <VolumeX className="w-4 h-4 text-red-400" />
                    <span>Unmute Spoken Output</span>
                  </>
                ) : (
                  <>
                    <Volume2 className="w-4 h-4 text-emerald-400" />
                    <span>{conversationState === "speaking" ? "Stop Speaking" : "Audio Vocalization ON"}</span>
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={() => setHistory([])}
                className="text-xs text-charcoal-400 hover:text-charcoal-200 flex items-center gap-1 transition-colors"
                title="Clear transcript history"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Reset Chat</span>
              </button>
            </div>
          </div>
        </div>

        {/* Error / Permission Diagnostic Alert */}
        {errorNotice && (
          <div className="mt-4 p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-semibold text-amber-300">Microphone Notice</p>
              <p className="mt-0.5 text-amber-200/90">{errorNotice}</p>
            </div>
            <button
              type="button"
              onClick={() => setErrorNotice(null)}
              className="text-amber-400 hover:text-amber-200 text-xs underline ml-2"
            >
              Dismiss
            </button>
          </div>
        )}
      </div>

      {/* Enterprise Grounding Context Bar */}
      <div className="bg-ivory-100/60 dark:bg-forest-900/40 border border-forest-800/40 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <span className="font-semibold text-charcoal-900 dark:text-ivory-100">
            Active Enterprise Grounding Parameters:
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="px-2.5 py-1 rounded-md bg-forest-800/30 text-charcoal-700 dark:text-charcoal-300 font-medium">
            Category: <strong className="text-charcoal-900 dark:text-ivory-100">{enterpriseContext.category}</strong>
          </span>
          <span className="px-2.5 py-1 rounded-md bg-forest-800/30 text-charcoal-700 dark:text-charcoal-300 font-medium">
            Outlay: <strong className="text-charcoal-900 dark:text-ivory-100">₹{enterpriseContext.project_cost.toLocaleString("en-IN")}</strong>
          </span>
          <span className="px-2.5 py-1 rounded-md bg-forest-800/30 text-charcoal-700 dark:text-charcoal-300 font-medium">
            Est. Monthly EMI: <strong className="text-emerald-700 dark:text-emerald-400">₹{Math.round(enterpriseContext.monthly_emi).toLocaleString("en-IN")}</strong>
          </span>
          <span className="px-2.5 py-1 rounded-md bg-forest-800/30 text-charcoal-700 dark:text-charcoal-300 font-medium">
            DSCR: <strong className="text-charcoal-900 dark:text-ivory-100">{enterpriseContext.dscr.toFixed(2)}x</strong>
          </span>
          <span className="px-2.5 py-1 rounded-md bg-forest-800/30 text-charcoal-700 dark:text-charcoal-300 font-medium">
            Locality: <strong className="text-charcoal-900 dark:text-ivory-100">{enterpriseContext.village}</strong>
          </span>
        </div>
      </div>

      {/* Real-Time Conversation Stream */}
      <div className="bg-ivory-50 dark:bg-forest-950 border border-forest-800/30 rounded-2xl p-6 shadow-sm min-h-[380px] flex flex-col justify-between">
        <div className="space-y-4 overflow-y-auto max-h-[500px] pr-2">
          {history.map((msg) => {
            const isUser = msg.sender === "user";
            return (
              <div
                key={msg.id}
                className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
              >
                {!isUser && (
                  <div className="w-8 h-8 rounded-full bg-emerald-600/20 text-emerald-600 dark:text-emerald-400 border border-emerald-600/30 flex items-center justify-center flex-shrink-0 mt-1">
                    <Sparkles className="w-4 h-4" />
                  </div>
                )}

                <div
                  className={`max-w-2xl rounded-2xl p-4 text-sm leading-relaxed ${
                    isUser
                      ? "bg-forest-800 text-ivory-50 border border-forest-700 shadow-sm"
                      : "bg-white dark:bg-forest-900/90 text-charcoal-900 dark:text-ivory-100 border border-forest-800/30 shadow-sm"
                  }`}
                >
                  <div className="flex items-center justify-between gap-4 mb-1.5 text-[11px] text-charcoal-400">
                    <span className="font-semibold uppercase tracking-wider">
                      {isUser ? "You (Entrepreneur)" : "RuralBiz Voice Advisor"}
                    </span>
                    <div className="flex items-center gap-2">
                      <span>{msg.timestamp}</span>
                      {!isUser && (
                        <button
                          type="button"
                          onClick={() => speakText(msg.text, selectedLang)}
                          className="hover:text-emerald-400 transition-colors p-0.5 rounded"
                          title="Replay Spoken Audio"
                        >
                          <Volume2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  </div>

                  <p className="whitespace-pre-line">{msg.text}</p>

                  {/* Contextual Follow-up Chips */}
                  {msg.followUps && msg.followUps.length > 0 && (
                    <div className="mt-3.5 pt-3 border-t border-forest-800/20 dark:border-forest-800/40">
                      <p className="text-[11px] font-semibold text-charcoal-500 dark:text-charcoal-400 mb-2 flex items-center gap-1.5">
                        <HelpCircle className="w-3 h-3 text-emerald-500" />
                        Spoken Follow-up Suggestions:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {msg.followUps.map((chip, idx) => (
                          <button
                            key={idx}
                            type="button"
                            onClick={() => submitQuestion(chip, selectedLang)}
                            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-forest-800/10 dark:bg-forest-800/50 hover:bg-emerald-500/20 text-charcoal-800 dark:text-ivory-200 border border-forest-800/30 transition-all text-left flex items-center gap-1.5"
                          >
                            <Mic className="w-3 h-3 text-emerald-500 flex-shrink-0" />
                            <span>{chip}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {/* Interim Real-Time Transcript while speaking */}
          {interimText && (
            <div className="flex gap-3 justify-end">
              <div className="max-w-xl rounded-2xl p-3.5 bg-forest-800/50 text-ivory-200 border border-emerald-500/40 text-sm italic flex items-center gap-2 animate-pulse">
                <Mic className="w-4 h-4 text-emerald-400" />
                <span>{interimText}...</span>
              </div>
            </div>
          )}

          {/* Processing Indicator */}
          {conversationState === "processing" && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-emerald-600/20 text-emerald-400 border border-emerald-600/30 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-4 h-4 animate-spin" />
              </div>
              <div className="rounded-2xl px-4 py-3 bg-forest-900/60 border border-forest-800 text-charcoal-300 text-xs flex items-center gap-2">
                <span>Analyzing rural market benchmarks and financial parameters...</span>
              </div>
            </div>
          )}

          <div ref={transcriptEndRef} />
        </div>

        {/* Text fallback input bar */}
        <div className="mt-6 pt-4 border-t border-forest-800/20 dark:border-forest-800/60 flex items-center gap-3">
          <input
            type="text"
            placeholder={VOICE_LANGUAGES[selectedLang].sampleQuestion}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.target as HTMLInputElement).value) {
                submitQuestion((e.target as HTMLInputElement).value, selectedLang);
                (e.target as HTMLInputElement).value = "";
              }
            }}
            className="flex-1 bg-white dark:bg-forest-900 border border-forest-800/40 rounded-xl px-4 py-2.5 text-sm text-charcoal-900 dark:text-ivory-50 focus:outline-none focus:ring-2 focus:ring-emerald-500 placeholder-charcoal-400"
          />
          <button
            type="button"
            onClick={(e) => {
              const inputEl = (e.currentTarget.previousElementSibling as HTMLInputElement);
              if (inputEl && inputEl.value) {
                submitQuestion(inputEl.value, selectedLang);
                inputEl.value = "";
              }
            }}
            className="px-4 py-2.5 rounded-xl bg-forest-800 hover:bg-forest-700 text-ivory-100 text-xs font-semibold flex items-center gap-1.5 transition-colors"
          >
            Ask Text
          </button>
        </div>
      </div>
    </div>
  );
}
