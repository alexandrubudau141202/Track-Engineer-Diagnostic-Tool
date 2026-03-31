// TelemetryChart.tsx - Telemetry visualization component

import React from "react";
import { TelemetryPoint } from "../types/Scenario";

interface TelemetryChartProps {
  telemetry: TelemetryPoint[];
}

export const TelemetryChart: React.FC<TelemetryChartProps> = ({ telemetry }) => {
  if (!telemetry || telemetry.length === 0) {
    return null;
  }

  // Calculate stats
  const speeds = telemetry.map((p) => p.speed_kmh);
  const maxSpeed = Math.max(...speeds);
  const avgSpeed = speeds.reduce((a, b) => a + b, 0) / speeds.length;

  const lateralGs = telemetry.map((p) => Math.abs(p.lateral_g));
  const maxLateralG = Math.max(...lateralGs);

  const throttles = telemetry.map((p) => p.throttle_percent);
  const avgThrottle = throttles.reduce((a, b) => a + b, 0) / throttles.length;

  const understeerEvents = telemetry.filter(
    (p) => Math.abs(p.steering_angle_deg) > 10 && p.lateral_g < 1.0
  ).length;

  const lastPoint = telemetry[telemetry.length - 1];
  const duration = (lastPoint?.timestamp_ms || 0) / 1000;

  // Generate SVG path for speed trace
  const speedPath = telemetry
    .map((point, idx) => {
      const x = (idx / (telemetry.length - 1)) * 100;
      const y = 100 - (point.speed_kmh / maxSpeed) * 90 - 5;
      return `${idx === 0 ? "M" : "L"} ${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

  const throttlePath = telemetry
    .map((point, idx) => {
      const x = (idx / (telemetry.length - 1)) * 100;
      const y = 100 - point.throttle_percent - 5;
      return `${idx === 0 ? "M" : "L"} ${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

  return (
    <div className="card">
      {/* Header */}
      <div className="section-header">
        <div className="section-icon bg-[#00D4FF]/10 text-[#00D4FF]">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12h4l3-9 4 18 3-9h4"/></svg>
        </div>
        <h3 className="font-semibold text-sm text-white tracking-wide">
          Telemetry Analysis
        </h3>
        <span className="ml-auto text-[10px] font-mono text-white/20">
          {telemetry.length} pts &middot; {duration.toFixed(1)}s
        </span>
      </div>

      <div className="p-5 space-y-5">
        {/* Stat grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard
            label="Max Speed"
            value={`${maxSpeed.toFixed(0)}`}
            unit="km/h"
            accent="#FF6B00"
          />
          <StatCard
            label="Avg Speed"
            value={`${avgSpeed.toFixed(0)}`}
            unit="km/h"
            accent="#FF9A44"
          />
          <StatCard
            label="Peak Lateral"
            value={`${maxLateralG.toFixed(2)}`}
            unit="G"
            accent="#00D4FF"
          />
          <StatCard
            label="Avg Throttle"
            value={`${avgThrottle.toFixed(0)}`}
            unit="%"
            accent="#00FF88"
          />
        </div>

        {/* Speed trace SVG */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-medium text-white/40 tracking-wide uppercase">
              Speed Trace
            </p>
            <div className="flex items-center gap-4 text-[10px]">
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-0.5 rounded bg-[#FF6B00]" /> Speed
              </span>
              <span className="flex items-center gap-1.5 text-white/30">
                <span className="w-3 h-0.5 rounded bg-[#00D4FF]/50" /> Throttle
              </span>
            </div>
          </div>
          <div className="rounded-xl overflow-hidden border border-white/[0.04] bg-[#08080e] p-2">
            <svg
              viewBox="0 0 100 100"
              preserveAspectRatio="none"
              className="w-full"
              style={{ height: 120 }}
            >
              {/* Grid lines */}
              {[25, 50, 75].map((y) => (
                <line
                  key={y}
                  x1="0"
                  y1={y}
                  x2="100"
                  y2={y}
                  stroke="rgba(255,255,255,0.03)"
                  strokeWidth="0.3"
                />
              ))}

              {/* Throttle trace (behind) */}
              <path
                d={throttlePath}
                fill="none"
                stroke="rgba(0,212,255,0.2)"
                strokeWidth="0.8"
              />

              {/* Speed trace */}
              <path
                d={speedPath}
                fill="none"
                stroke="#FF6B00"
                strokeWidth="1"
                strokeLinecap="round"
                strokeLinejoin="round"
              />

              {/* Speed trace glow */}
              <path
                d={speedPath}
                fill="none"
                stroke="#FF6B00"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.15"
              />
            </svg>
          </div>
        </div>

        {/* Bottom info grid */}
        <div className="grid grid-cols-2 gap-4">
          {/* Detected issues */}
          <div className="rounded-xl bg-white/[0.02] border border-white/[0.04] p-4">
            <p className="text-[10px] font-medium text-white/30 tracking-wider uppercase mb-3">
              Detected Issues
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <span
                  className={`w-1.5 h-1.5 rounded-full ${
                    understeerEvents > 2 ? "bg-red-400" : "bg-emerald-400"
                  }`}
                />
                <span className="text-white/50">
                  Understeer events:{" "}
                  <span className="text-white/80 font-medium">
                    {understeerEvents}
                  </span>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-white/20" />
                <span className="text-white/50">
                  Data points:{" "}
                  <span className="text-white/80 font-medium">
                    {telemetry.length}
                  </span>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-white/20" />
                <span className="text-white/50">
                  Duration:{" "}
                  <span className="text-white/80 font-medium">
                    {duration.toFixed(1)}s
                  </span>
                </span>
              </div>
            </div>
          </div>

          {/* Tire temps */}
          <div className="rounded-xl bg-white/[0.02] border border-white/[0.04] p-4">
            <p className="text-[10px] font-medium text-white/30 tracking-wider uppercase mb-3">
              Tire Temperatures
            </p>
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: "FL", temp: lastPoint?.tire_temp_fl_c },
                { label: "FR", temp: lastPoint?.tire_temp_fr_c },
                { label: "RL", temp: lastPoint?.tire_temp_rl_c },
                { label: "RR", temp: lastPoint?.tire_temp_rr_c },
              ].map(({ label, temp }) => {
                const t = temp || 0;
                const color =
                  t > 100
                    ? "text-red-400"
                    : t > 85
                    ? "text-[#FFD600]"
                    : "text-emerald-400";
                return (
                  <div
                    key={label}
                    className="rounded-lg bg-white/[0.02] border border-white/[0.03] px-3 py-2 text-center"
                  >
                    <p className="text-[10px] text-white/25 font-mono">
                      {label}
                    </p>
                    <p className={`text-sm font-bold ${color}`}>
                      {t.toFixed(0)}°
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

/** Reusable dark stat card with colored accent border */
const StatCard: React.FC<{
  label: string;
  value: string;
  unit: string;
  accent: string;
}> = ({ label, value, unit, accent }) => (
  <div
    className="rounded-xl bg-white/[0.02] border border-white/[0.04] p-3"
    style={{ borderLeftColor: accent, borderLeftWidth: 2 }}
  >
    <p className="text-[10px] text-white/30 tracking-wider uppercase mb-1">
      {label}
    </p>
    <div className="flex items-baseline gap-1">
      <span className="text-xl font-bold" style={{ color: accent }}>
        {value}
      </span>
      <span className="text-[10px] text-white/25">{unit}</span>
    </div>
  </div>
);