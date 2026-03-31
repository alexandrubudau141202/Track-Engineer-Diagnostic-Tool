// Diagnosis.ts - Diagnosis results and recommendations types

export interface Recommendation {
  priority: number;
  action: string;
  delta: string;
  rationale: string;
  expected_impact: string;
  implementation?: string;
}

export interface Problem {
  type: string;
  severity: "low" | "medium" | "high";
  confidence_percent: number;
  evidence: string[];
  affected_area: string;
}

export interface SetupDelta {
  front_wing_angle_deg?: string;
  rear_wing_angle_deg?: string;
  front_brake_bias_percent?: string;
  fuel_load_liters?: string;
  tire_pressures?: Record<string, string>;
  abs_level?: string;
  traction_control_level?: string;
}

export interface DriverCoaching {
  braking_points: string;
  acceleration_strategy: string;
  line_adjustments: string;
  gear_strategy: string;
}

export interface DiagnosisResult {
  scenario_id: string;
  primary_problem: string;
  overall_confidence_percent: number;
  problems_detected: Problem[];
  recommendations: Recommendation[];
  setup_delta: SetupDelta;
  driver_coaching?: DriverCoaching;
  summary: string;
  session_notes: string;
  analysis_timestamp?: string;
  lap_analyzed?: number;
}

export interface DiagnosisResponse {
  scenario_id: string;
  status: "success" | "error";
  diagnosis: DiagnosisResult;
  pdf_url: string;
  message: string;
}

export const SEVERITY_COLORS = {
  high: "#c41e3a",
  medium: "#ff8c00",
  low: "#4CAF50",
};

export const PROBLEM_NAMES: Record<string, string> = {
  understeer_entry: "Understeer on Entry",
  understeer_mid_corner: "Understeer Mid-Corner",
  understeer_exit: "Understeer on Exit",
  oversteer_entry: "Oversteer on Entry",
  oversteer_mid_corner: "Oversteer Mid-Corner",
  oversteer_exit: "Oversteer on Exit",
  tire_degradation_front: "Front Tire Degradation",
  tire_degradation_rear: "Rear Tire Degradation",
  brake_fade: "Brake Fade",
  brake_balance_instability: "Brake Balance Instability",
  balanced: "Balanced Setup",
};