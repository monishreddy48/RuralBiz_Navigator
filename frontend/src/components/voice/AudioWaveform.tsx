"use client";

import React, { useEffect, useRef } from "react";

interface AudioWaveformProps {
  isRecording: boolean;
  isSpeaking: boolean;
  analyserNode: AnalyserNode | null;
  className?: string;
}

export default function AudioWaveform({
  isRecording,
  isSpeaking,
  analyserNode,
  className = "w-full h-24",
}: AudioWaveformProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameId = useRef<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Handle high DPI
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    let phase = 0;
    const bufferLength = analyserNode ? analyserNode.frequencyBinCount : 64;
    const dataArray = new Uint8Array(bufferLength);

    const render = () => {
      ctx.clearRect(0, 0, rect.width, rect.height);
      phase += 0.05;

      const centerY = rect.height / 2;
      const width = rect.width;

      if (isRecording && analyserNode) {
        // Draw real-time mic waveform
        analyserNode.getByteTimeDomainData(dataArray);

        ctx.lineWidth = 2.5;
        ctx.strokeStyle = "#10b981"; // Emerald
        ctx.beginPath();

        const sliceWidth = width / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          const v = dataArray[i] / 128.0;
          const y = v * centerY;

          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
          x += sliceWidth;
        }

        ctx.stroke();

        // Draw glowing secondary harmonic wave
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = "rgba(16, 185, 129, 0.4)";
        ctx.beginPath();
        x = 0;
        for (let i = 0; i < bufferLength; i++) {
          const v = dataArray[i] / 128.0;
          const delta = (v - 1) * 0.7;
          const y = centerY + delta * centerY * Math.sin(phase + i * 0.1);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
          x += sliceWidth;
        }
        ctx.stroke();

      } else if (isSpeaking) {
        // AI Speaking: Generative audio bars / flowing sine waves
        const barCount = 48;
        const barWidth = width / (barCount * 1.5);
        const gradient = ctx.createLinearGradient(0, 0, 0, rect.height);
        gradient.addColorStop(0, "#059669");
        gradient.addColorStop(0.5, "#10b981");
        gradient.addColorStop(1, "#34d399");

        ctx.fillStyle = gradient;

        for (let i = 0; i < barCount; i++) {
          const t = phase * 2 + i * 0.35;
          const rawHeight = Math.abs(Math.sin(t) * Math.cos(t * 0.7 + i * 0.1));
          const barHeight = Math.max(6, rawHeight * (rect.height * 0.7));
          const x = i * (barWidth * 1.5) + (width - barCount * barWidth * 1.5) / 2;
          const y = centerY - barHeight / 2;

          ctx.beginPath();
          ctx.roundRect(x, y, barWidth, barHeight, 4);
          ctx.fill();
        }

      } else {
        // Idle calm breath line
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = "rgba(107, 114, 128, 0.3)";
        ctx.beginPath();

        for (let x = 0; x < width; x += 5) {
          const y = centerY + Math.sin(phase + x * 0.02) * 3;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      animFrameId.current = requestAnimationFrame(render);
    };

    render();

    return () => {
      if (animFrameId.current) {
        cancelAnimationFrame(animFrameId.current);
      }
    };
  }, [isRecording, isSpeaking, analyserNode]);

  return (
    <div className={`relative flex items-center justify-center overflow-hidden rounded-xl bg-forest-900/60 p-2 border border-forest-800 ${className}`}>
      <canvas ref={canvasRef} className="w-full h-full block" />
    </div>
  );
}

