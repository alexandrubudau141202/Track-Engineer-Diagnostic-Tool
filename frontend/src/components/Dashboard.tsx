// Dashboard.tsx - Main application dashboard

import React, { useState } from "react";
import { ScenarioBuilder } from "./ScenarioBuilder";
import { TelemetryUpload } from "./TelemetryUpload";
import { TelemetryChart } from "./TelemetryChart";
import { CarViewer } from "./CarViewer";
import { ReportPreview } from "./ReportPreview";
import { useScenario } from "../hooks/useScenario";
import { useAPI } from "../hooks/useAPI";

export const Dashboard: React.FC = () => {
  const {
    scenario,
    updateSetup,
    updateFeedback,
    updateConditions,
    setTelemetry,
    reset,
    isValid,
  } = useScenario();

  const { loading, error, result, diagnose, downloadPDF } = useAPI();

  const [activeTab, setActiveTab] = useState<"input" | "preview">("input");

  const handleDiagnose = async () => {
    if (!isValid()) {
      alert("Please fill in all required fields");
      return;
    }

    await diagnose(scenario);
    setActiveTab("preview");
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Background layers */}
      <div className="fixed inset-0 bg-grid pointer-events-none z-0" />
      {/*<div className="fixed inset-0 scanlines pointer-events-none z-0" />*/}

      {/* Ambient glow orbs */}
      <div
        className="fixed pointer-events-none z-0"
        style={{
          width: 700,
          height: 700,
          top: -250,
          left: -150,
          background: "radial-gradient(circle, rgba(255,107,0,0.06) 0%, transparent 65%)",
          animation: "float1 20s ease-in-out infinite",
        }}
      />
      <div
        className="fixed pointer-events-none z-0"
        style={{
          width: 500,
          height: 500,
          bottom: -100,
          right: -80,
          background: "radial-gradient(circle, rgba(0,212,255,0.04) 0%, transparent 65%)",
          animation: "float2 25s ease-in-out infinite",
        }}
      />

      {/* Content shell */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* ── Header ── */}
        <header className="sticky top-0 z-40 backdrop-blur-xl bg-[#050508]/80">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-5 flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Logo mark */}
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#FF6B00] to-orange-700 flex items-center justify-center text-[#050508] shadow-lg shadow-orange-900/20">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>

              <div>
                <h1 className="text-xl font-bold text-white tracking-tight">
                  <span className="text-gradient">GT3 R</span>{" "}
                  <span className="text-white/90">Diagnostic</span>
                </h1>
                <p className="text-[11px] text-white/30 tracking-wide mt-0.5 hidden sm:block">
                  AI-Powered Setup Analysis &middot; Porsche 911 GT3 R &middot; WEC / GTWC
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="badge-online hidden sm:flex">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                ONLINE
              </div>
              <div className="px-2.5 py-1 rounded-md bg-white/[0.03] border border-white/[0.06] text-[10px] font-mono text-white/25 tracking-widest">
                v1.0
              </div>
            </div>
          </div>

          {/* Animated border line */}
          <div className="header-glow" />
        </header>

        {/* ── Main Content ── */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 sm:py-8">
          {/* Tab navigation */}
          <nav className="flex gap-2 mb-8" role="tablist">
            <button
              onClick={() => setActiveTab("input")}
              role="tab"
              aria-selected={activeTab === "input"}
              className={`px-5 py-2.5 rounded-xl text-sm font-semibold tracking-wide border transition-all duration-300 ${
                activeTab === "input"
                  ? "tab-active border-orange-500/35"
                  : "bg-transparent border-white/[0.04] text-white/35 hover:text-white/60 hover:border-white/[0.08]"
              }`}
            >
              <span className="mr-2 opacity-70">☰</span>
              Input Scenario
            </button>
            <button
              onClick={() => setActiveTab("preview")}
              disabled={!result}
              role="tab"
              aria-selected={activeTab === "preview"}
              className={`px-5 py-2.5 rounded-xl text-sm font-semibold tracking-wide border transition-all duration-300 ${
                activeTab === "preview"
                  ? "tab-active border-orange-500/35"
                  : !result
                  ? "bg-transparent border-white/[0.03] text-white/15 cursor-not-allowed"
                  : "bg-transparent border-white/[0.04] text-white/35 hover:text-white/60 hover:border-white/[0.08]"
              }`}
            >
              <span className="mr-2 opacity-70">◇</span>
              Results
            </button>
          </nav>

          {/* ══════════ INPUT TAB ══════════ */}
          {activeTab === "input" && (
            <div className="animate-fade-up space-y-5">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                {/* Left column — forms */}
                <div className="lg:col-span-2 space-y-5">
                  <ScenarioBuilder
                    setup={scenario.car_setup}
                    feedback={scenario.driver_feedback}
                    conditions={scenario.track_conditions}
                    onSetupChange={updateSetup}
                    onFeedbackChange={updateFeedback}
                    onConditionsChange={updateConditions}
                  />

                  <TelemetryUpload onTelemetryLoaded={setTelemetry} />

                  {scenario.telemetry.length > 0 && (
                    <div className="animate-fade-up">
                      <TelemetryChart telemetry={scenario.telemetry} />
                    </div>
                  )}
                </div>

                {/* Right column — 3D viewer */}
                <div className="lg:col-span-1">
                  <div className="lg:sticky lg:top-24">
                    <CarViewer />
                  </div>
                </div>
              </div>

              {/* Error banner */}
              {error && (
                <div className="animate-fade-up flex items-start gap-3 p-4 rounded-xl bg-red-500/[0.06] border border-red-500/20 text-red-300">
                  <span className="text-red-400 mt-0.5">⚠</span>
                  <div>
                    <p className="font-semibold text-sm text-red-200">Analysis Error</p>
                    <p className="text-xs mt-1 text-red-300/70">{error}</p>
                  </div>
                </div>
              )}

              {/* Action bar */}
              <div className="racing-divider mt-6" />
              <div className="flex gap-3 pt-5">
                <button
                  onClick={handleDiagnose}
                  disabled={loading || !isValid()}
                  className="btn-diagnose flex-1 py-3.5 px-6 disabled:opacity-40 disabled:cursor-not-allowed disabled:transform-none"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3"/>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                      </svg>
                      Analyzing...
                    </span>
                  ) : (
                    <span className="flex items-center justify-center gap-2">
                      <span>⚡</span> Run Diagnosis
                    </span>
                  )}
                </button>

                <button
                  onClick={reset}
                  disabled={loading}
                  className="px-6 py-3.5 rounded-xl text-sm font-semibold border border-white/[0.06] bg-white/[0.02] text-white/30 hover:text-white/60 hover:border-white/[0.12] disabled:opacity-30 transition-all duration-200"
                >
                  Reset
                </button>
              </div>
            </div>
          )}

          {/* ══════════ PREVIEW TAB ══════════ */}
          {activeTab === "preview" && result && (
            <div className="animate-fade-up">
              <ReportPreview
                diagnosis={result.diagnosis}
                onDownloadPDF={() => downloadPDF(result.scenario_id)}
                loading={loading}
              />
            </div>
          )}

          {/* Empty state for preview */}
          {activeTab === "preview" && !result && (
            <div className="animate-fade-up flex flex-col items-center justify-center py-24">
              <div className="w-16 h-16 rounded-2xl bg-white/[0.02] border border-white/[0.04] flex items-center justify-center text-2xl text-white/10 mb-5">
                ◇
              </div>
              <p className="text-white/25 text-sm text-center max-w-md leading-relaxed">
                No diagnosis results yet. Complete the scenario inputs and run a diagnosis to generate your engineering report.
              </p>
            </div>
          )}
        </main>

        {/* ── Footer ── */}
        <footer className="relative mt-auto border-t border-white/[0.03] bg-[#050508]/60">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-5 flex flex-col sm:flex-row justify-between items-center gap-2">
            <p className="text-[11px] text-white/15 tracking-wide">
              GT3 R Diagnostic Tool v1.0 &middot; Powered by REWS Race Engineering Workstation
            </p>
            <p className="text-[11px] text-white/10">
              For professional motorsport use. Consult qualified engineers for race-critical decisions.
            </p>
          </div>
        </footer>
      </div>

      {/* Keyframes for floating glow orbs — injected once */}
      <style>{`
        @keyframes float1 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -20px) scale(1.05); }
          66% { transform: translate(-20px, 30px) scale(0.95); }
        }
        @keyframes float2 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(-25px, -35px) scale(1.08); }
        }
      `}</style>
    </div>
  );
};