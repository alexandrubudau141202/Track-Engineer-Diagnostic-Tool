import React from "react";
import { DiagnosisResult, SEVERITY_COLORS, PROBLEM_NAMES } from "../types/Diagnosis";

const DARK_SEVERITY: Record<string, { bg: string; border: string; text: string; badge: string }> = {
  critical: { bg: "rgba(255,51,85,0.06)", border: "rgba(255,51,85,0.3)", text: "#FF3355", badge: "rgba(255,51,85,0.15)" },
  high:     { bg: "rgba(255,51,85,0.04)", border: "rgba(255,51,85,0.2)", text: "#FF3355", badge: "rgba(255,51,85,0.12)" },
  medium:   { bg: "rgba(255,214,0,0.04)",  border: "rgba(255,214,0,0.2)",  text: "#FFD600", badge: "rgba(255,214,0,0.12)" },
  low:      { bg: "rgba(0,255,136,0.04)",  border: "rgba(0,255,136,0.15)", text: "#00FF88", badge: "rgba(0,255,136,0.12)" },
};
const FALLBACK_SEVERITY = DARK_SEVERITY.low;

interface ReportPreviewProps {
  diagnosis: DiagnosisResult;
  onDownloadPDF: () => void;
  loading?: boolean;
}

export const ReportPreview: React.FC<ReportPreviewProps> = ({
  diagnosis,
  onDownloadPDF,
  loading = false,
}) => {
  const primaryProblem = diagnosis.problems_detected?.[0];
  const primarySeverity = DARK_SEVERITY[primaryProblem?.severity || "low"] || FALLBACK_SEVERITY;

  return (
    <div className="space-y-5 animate-fade-up">
      {/* Report header */}
      <div className="card">
        <div className="section-header">
          <div className="section-icon bg-[#FF6B00]/10 text-[#FF6B00]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 14l2 2 4-4"/></svg>
          </div>
          <h2 className="font-semibold text-sm text-white tracking-wide">Diagnosis Report</h2>
          <div className="ml-auto flex items-center gap-3">
            <span className="text-[10px] font-mono text-white/20">{diagnosis.scenario_id?.slice(0, 8)}</span>
            {diagnosis.analysis_timestamp && (
              <span className="text-[10px] font-mono text-white/15">{diagnosis.analysis_timestamp}</span>
            )}
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="card">
        <div className="p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-4 rounded-full bg-[#FF6B00]" />
            <h3 className="text-xs font-semibold text-white/60 tracking-wider uppercase">Executive Summary</h3>
          </div>
          <p className="text-sm text-white/50 leading-relaxed">{diagnosis.summary}</p>
        </div>
      </div>

      {/* Primary Problem */}
      {primaryProblem && (
        <div className="card" style={{ borderColor: primarySeverity.border }}>
          <div className="p-5">
            <p className="text-[10px] font-semibold text-white/30 tracking-wider uppercase mb-2">Primary Issue</p>
            <p className="text-lg font-bold" style={{ color: primarySeverity.text }}>
              {PROBLEM_NAMES[diagnosis.primary_problem] || diagnosis.primary_problem}
            </p>
            <div className="flex items-center gap-4 mt-3">
              <span className="text-xs text-white/25">
                Confidence: <span className="text-white/60 font-medium">{diagnosis.overall_confidence_percent}%</span>
              </span>
              <span
                className="px-2 py-0.5 rounded text-[10px] font-semibold tracking-wider uppercase"
                style={{ background: primarySeverity.badge, color: primarySeverity.text }}
              >
                {primaryProblem.severity}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* All Detected Problems */}
      {diagnosis.problems_detected?.length > 1 && (
        <div className="card">
          <div className="section-header">
            <div className="section-icon bg-red-500/10 text-red-400">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <h3 className="font-semibold text-sm text-white tracking-wide">All Detected Issues</h3>
            <span className="ml-auto text-xs font-mono text-white/20">{diagnosis.problems_detected.length}</span>
          </div>
          <div className="p-5 space-y-2">
            {diagnosis.problems_detected.map((problem, idx) => {
              const sev = DARK_SEVERITY[problem.severity] || FALLBACK_SEVERITY;
              return (
                <div key={idx} className="rounded-xl border p-4 transition-colors" style={{ background: sev.bg, borderColor: sev.border, borderLeftWidth: 3 }}>
                  <div className="flex justify-between items-start gap-3">
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-white/80">{PROBLEM_NAMES[problem.type] || problem.type}</p>
                      <p className="text-[11px] text-white/30 mt-1 leading-relaxed">{problem.evidence?.slice(0, 2).join(" \u2022 ")}</p>
                    </div>
                    <span className="shrink-0 px-2.5 py-1 rounded-lg text-[11px] font-bold tracking-wider" style={{ background: sev.badge, color: sev.text }}>
                      {problem.confidence_percent}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Recommended Actions */}
      {diagnosis.recommendations?.length > 0 && (
        <div className="card">
          <div className="section-header">
            <div className="section-icon bg-emerald-500/10 text-emerald-400">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
            </div>
            <h3 className="font-semibold text-sm text-white tracking-wide">Recommended Actions</h3>
          </div>
          <div className="p-5 space-y-3">
            {diagnosis.recommendations.slice(0, 5).map((rec, idx) => (
              <div key={idx} className="rounded-xl bg-white/[0.02] border border-white/[0.04] p-4">
                <div className="flex justify-between items-start gap-3 mb-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-6 h-6 rounded-md bg-[#FF6B00]/10 text-[#FF6B00] flex items-center justify-center text-[11px] font-bold">{idx + 1}</span>
                    <p className="text-sm font-semibold text-white/80">{rec.action?.replace(/_/g, " ")}</p>
                  </div>
                  <span className="shrink-0 px-2 py-0.5 rounded-md bg-[#00D4FF]/10 text-[#00D4FF] text-[11px] font-mono font-medium">{rec.delta}</span>
                </div>
                <p className="text-xs text-white/40 leading-relaxed ml-[34px]">{rec.rationale}</p>
                {rec.expected_impact && (
                  <div className="mt-2 ml-[34px] flex items-center gap-1.5 text-[11px] text-emerald-400/70">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
                    {rec.expected_impact}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Setup Delta */}
      {diagnosis.setup_delta && (
        <div className="card">
          <div className="section-header">
            <div className="section-icon bg-[#FFD600]/10 text-[#FFD600]">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
            </div>
            <h3 className="font-semibold text-sm text-white tracking-wide">Setup Changes</h3>
          </div>
          <div className="p-5 grid grid-cols-2 gap-2">
            {diagnosis.setup_delta.rear_wing_angle_deg && <DeltaRow label="Rear Wing" value={diagnosis.setup_delta.rear_wing_angle_deg} />}
            {diagnosis.setup_delta.front_wing_angle_deg && <DeltaRow label="Front Wing" value={diagnosis.setup_delta.front_wing_angle_deg} />}
            {diagnosis.setup_delta.front_brake_bias_percent && <DeltaRow label="Brake Bias" value={diagnosis.setup_delta.front_brake_bias_percent} />}
            {diagnosis.setup_delta.traction_control_level && <DeltaRow label="TC Level" value={diagnosis.setup_delta.traction_control_level} />}
          </div>
        </div>
      )}

      {/* Driver Coaching */}
      {diagnosis.driver_coaching && (
        <div className="card" style={{ borderColor: "rgba(255,214,0,0.12)" }}>
          <div className="p-5">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-7 h-7 rounded-lg bg-[#FFD600]/10 text-[#FFD600] flex items-center justify-center">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 18a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v2H2v-2z"/><circle cx="12" cy="10" r="5"/><path d="M12 2v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/></svg>
              </div>
              <h3 className="text-sm font-semibold text-[#FFD600]/80 tracking-wide">Driver Coaching</h3>
            </div>
            <div className="space-y-3 text-sm">
              {diagnosis.driver_coaching.braking_points && <CoachingRow label="Braking" value={diagnosis.driver_coaching.braking_points} />}
              {diagnosis.driver_coaching.acceleration_strategy && <CoachingRow label="Acceleration" value={diagnosis.driver_coaching.acceleration_strategy} />}
              {diagnosis.driver_coaching.line_adjustments && <CoachingRow label="Lines" value={diagnosis.driver_coaching.line_adjustments} />}
            </div>
          </div>
        </div>
      )}

      {/* Download */}
      <div className="racing-divider" />
      <button
        onClick={onDownloadPDF}
        disabled={loading}
        className="w-full py-3.5 rounded-xl text-sm font-semibold tracking-wide border border-white/[0.08] bg-white/[0.03] text-white/50 hover:text-white/80 hover:border-white/[0.15] hover:bg-white/[0.05] disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            Generating PDF...
          </>
        ) : (
          <>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Download Full Report (PDF)
          </>
        )}
      </button>
    </div>
  );
};

const DeltaRow: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="rounded-lg bg-white/[0.02] border border-white/[0.04] px-3 py-2.5">
    <p className="text-[10px] text-white/25 tracking-wider uppercase">{label}</p>
    <p className="text-sm font-semibold text-white/70 font-mono mt-0.5">{value}</p>
  </div>
);

const CoachingRow: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="flex gap-3">
    <span className="shrink-0 text-[11px] font-semibold text-[#FFD600]/50 w-24 pt-0.5">{label}</span>
    <span className="text-white/40 text-xs leading-relaxed">{value}</span>
  </div>
);