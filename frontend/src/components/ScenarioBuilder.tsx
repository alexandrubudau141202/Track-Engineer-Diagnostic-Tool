import React from "react";
import { CarSetup, DriverFeedback, TrackConditions } from "../types/Scenario";

interface ScenarioBuilderProps {
  setup: CarSetup;
  feedback: DriverFeedback;
  conditions: TrackConditions;
  onSetupChange: (setup: Partial<CarSetup>) => void;
  onFeedbackChange: (feedback: Partial<DriverFeedback>) => void;
  onConditionsChange: (conditions: Partial<TrackConditions>) => void;
}

export const ScenarioBuilder: React.FC<ScenarioBuilderProps> = ({
  setup,
  feedback,
  conditions,
  onSetupChange,
  onFeedbackChange,
  onConditionsChange,
}) => {
  return (
    <div className="space-y-5">
      {/* ═══ CAR SETUP ═══ */}
      <div className="card">
        <div className="section-header">
          <div className="section-icon bg-[#FF6B00]/10 text-[#FF6B00]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          </div>
          <h3 className="font-semibold text-sm text-white tracking-wide">
            Car Setup
          </h3>
        </div>

        <div className="p-5 space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
            <SliderField
              label="Front Wing"
              value={setup.front_wing_angle_deg ?? 0}
              unit="°"
              min={0}
              max={15}
              step={0.5}
              onChange={(v) => onSetupChange({ front_wing_angle_deg: v })}
            />
            <SliderField
              label="Rear Wing"
              value={setup.rear_wing_angle_deg ?? 0}
              unit="°"
              min={0}
              max={20}
              step={0.5}
              onChange={(v) => onSetupChange({ rear_wing_angle_deg: v })}
            />
            <SliderField
              label="Brake Bias"
              value={setup.front_brake_bias_percent ?? 0}
              unit="%"
              min={40}
              max={65}
              step={1}
              onChange={(v) => onSetupChange({ front_brake_bias_percent: v })}
            />
            <SliderField
              label="Fuel Load"
              value={setup.fuel_load_liters ?? 0}
              unit="L"
              min={20}
              max={70}
              step={1}
              onChange={(v) => onSetupChange({ fuel_load_liters: v })}
            />
            <SliderField
              label="Traction Control"
              value={setup.traction_control_level ?? 0}
              unit=""
              min={0}
              max={3}
              step={1}
              onChange={(v) =>
                onSetupChange({ traction_control_level: v as any })
              }
            />

            <div>
              <label className="flex items-baseline justify-between mb-2">
                <span className="text-xs text-white/40">Tire Compound</span>
                <span className="text-xs font-mono text-[#FF6B00]">
                  {(setup.tire_compound ?? "medium").toUpperCase()}
                </span>
              </label>
              <select
                value={setup.tire_compound ?? "medium"}
                onChange={(e) =>
                  onSetupChange({
                    tire_compound: e.target.value as "soft" | "medium" | "hard",
                  })
                }
              >
                <option value="soft">Soft (60)</option>
                <option value="medium">Medium (62)</option>
                <option value="hard">Hard (64)</option>
              </select>
            </div>
          </div>

          <div className="racing-divider" />
          <div>
            <p className="text-[10px] font-semibold text-white/25 tracking-wider uppercase mb-3">
              Tire Pressures (bar)
            </p>
            <div className="grid grid-cols-4 gap-2">
              {(["fl", "fr", "rl", "rr"] as const).map((corner) => (
                <div
                  key={corner}
                  className="rounded-lg bg-white/[0.02] border border-white/[0.04] p-2"
                >
                  <label className="text-[10px] text-white/20 font-mono block mb-1.5">
                    {corner.toUpperCase()}
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={
                      setup.tire_pressures?.[corner as keyof typeof setup.tire_pressures] ?? ""
                    }
                    onChange={(e) =>
                      onSetupChange({
                        tire_pressures: {
                          ...(setup.tire_pressures ?? {}),
                          [corner]: parseFloat(e.target.value) || 0,
                        },
                      })
                    }
                    className="w-full px-2 py-1 text-sm font-mono text-white/70 border-0 bg-transparent rounded"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ═══ DRIVER FEEDBACK ═══ */}
      <div className="card">
        <div className="section-header">
          <div className="section-icon bg-[#00D4FF]/10 text-[#00D4FF]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
          </div>
          <h3 className="font-semibold text-sm text-white tracking-wide">
            Driver Feedback
          </h3>
        </div>

        <div className="p-5 space-y-4">
          {[
            { key: "understeer", label: "Understeer", hint: "-5 Oversteer → +5 Understeer" },
            { key: "brake_stability", label: "Brake Stability", hint: "-5 Unstable → +5 Stable" },
            { key: "mid_corner_balance", label: "Mid-Corner Balance", hint: "-5 Loose → +5 Pushy" },
            { key: "exit_traction", label: "Exit Traction", hint: "-5 Wheelspin → +5 Clean" },
          ].map(({ key, label, hint }) => (
            <SliderField
              key={key}
              label={label}
              hint={hint}
              value={feedback[key as keyof DriverFeedback] ?? 0}
              unit=""
              min={-5}
              max={5}
              step={1}
              showSign
              onChange={(v) => onFeedbackChange({ [key]: v })}
            />
          ))}

          <div className="racing-divider" />
          <div>
            <label className="text-xs text-white/40 mb-2 block">
              Additional Notes
            </label>
            <textarea
              value={feedback.notes ?? ""}
              onChange={(e) => onFeedbackChange({ notes: e.target.value })}
              placeholder="e.g., Car feels loose on entry to Turn 6..."
              rows={3}
              className="w-full px-3 py-2.5 text-sm text-white/60 placeholder:text-white/15 border-0 bg-white/[0.02] rounded-xl resize-none leading-relaxed"
            />
          </div>
        </div>
      </div>

      {/* ═══ TRACK CONDITIONS ═══ */}
      <div className="card">
        <div className="section-header">
          <div className="section-icon bg-emerald-500/10 text-emerald-400">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19l4-14 4 8 4-10 4 16"/></svg>
          </div>
          <h3 className="font-semibold text-sm text-white tracking-wide">
            Track Conditions
          </h3>
        </div>

        <div className="p-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4">
            <SliderField
              label="Track Temp"
              value={conditions.track_temp_c ?? 0}
              unit="°C"
              min={0}
              max={50}
              step={1}
              onChange={(v) => onConditionsChange({ track_temp_c: v })}
            />
            <SliderField
              label="Air Temp"
              value={conditions.ambient_temp_c ?? 0}
              unit="°C"
              min={0}
              max={50}
              step={1}
              onChange={(v) => onConditionsChange({ ambient_temp_c: v })}
            />

            <div>
              <label className="flex items-baseline justify-between mb-2">
                <span className="text-xs text-white/40">Session</span>
                <span className="text-xs font-mono text-emerald-400/70">
                  {(conditions.session_type ?? "practice").toUpperCase()}
                </span>
              </label>
              <select
                value={conditions.session_type ?? "practice"}
                onChange={(e) =>
                  onConditionsChange({ session_type: e.target.value as any })
                }
              >
                <option value="practice">Practice</option>
                <option value="qualifying">Qualifying</option>
                <option value="race">Race</option>
                <option value="warmup">Warmup</option>
              </select>
            </div>

            <div>
              <label className="flex items-baseline justify-between mb-2">
                <span className="text-xs text-white/40">Weather</span>
                <span className="text-xs font-mono text-emerald-400/70">
                  {(conditions.weather ?? "dry").toUpperCase()}
                </span>
              </label>
              <select
                value={conditions.weather ?? "dry"}
                onChange={(e) =>
                  onConditionsChange({ weather: e.target.value as any })
                }
              >
                <option value="dry">Dry</option>
                <option value="wet">Wet</option>
                <option value="intermediate">Intermediate</option>
              </select>
            </div>

            <div className="sm:col-span-2">
              <label className="text-xs text-white/40 mb-2 block">Lap</label>
              <div className="flex gap-2">
                <div className="flex-1 rounded-lg bg-white/[0.02] border border-white/[0.04] px-3 py-2">
                  <span className="text-[10px] text-white/20 font-mono block mb-1">CURRENT</span>
                  <input
                    type="number"
                    min={1}
                    value={conditions.lap_number ?? ""}
                    onChange={(e) =>
                      onConditionsChange({ lap_number: parseInt(e.target.value) || 0 })
                    }
                    className="w-full text-sm font-mono text-white/70 border-0 bg-transparent p-0"
                  />
                </div>
                <div className="flex items-center text-white/10 text-xs">/</div>
                <div className="flex-1 rounded-lg bg-white/[0.02] border border-white/[0.04] px-3 py-2">
                  <span className="text-[10px] text-white/20 font-mono block mb-1">TOTAL</span>
                  <input
                    type="number"
                    min={1}
                    value={conditions.total_laps ?? ""}
                    onChange={(e) =>
                      onConditionsChange({ total_laps: parseInt(e.target.value) || 0 })
                    }
                    className="w-full text-sm font-mono text-white/70 border-0 bg-transparent p-0"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

/* ─────────────────────────────────────
   SliderField — dark themed, with fill
   ───────────────────────────────────── */
const SliderField: React.FC<{
  label: string;
  value: number;
  unit: string;
  min: number;
  max: number;
  step: number;
  hint?: string;
  showSign?: boolean;
  onChange: (value: number) => void;
}> = ({ label, value, unit, min, max, step, hint, showSign, onChange }) => {
  const displayValue = showSign
    ? `${value > 0 ? "+" : ""}${value}`
    : `${value}`;

  // Fill percentage for the track
  const pct = Math.max(0, Math.min(100, ((value - min) / (max - min)) * 100));
  const trackBg = `linear-gradient(to right, #FF6B00 0%, #FF6B00 ${pct}%, #1a1a28 ${pct}%, #1a1a28 100%)`;

  return (
    <div>
      <label className="flex items-baseline justify-between mb-2">
        <span className="text-xs text-white/40">{label}</span>
        <span className="text-xs font-mono text-[#FF6B00]">
          {displayValue}
          {unit && <span className="text-white/20 ml-0.5">{unit}</span>}
        </span>
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ background: trackBg }}
      />
      {hint && <p className="text-[10px] text-white/15 mt-1">{hint}</p>}
    </div>
  );
};