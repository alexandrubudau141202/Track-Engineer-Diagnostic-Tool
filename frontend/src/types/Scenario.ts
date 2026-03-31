// Scenario.ts - Car setup and scenario data types

export interface CarSetup {
  front_wing_angle_deg: number;
  rear_wing_angle_deg: number;
  front_brake_bias_percent: number;
  fuel_load_liters: number;
  tire_compound: "soft" | "medium" | "hard";
  tire_pressures: {
    fl_bar: number;
    fr_bar: number;
    rl_bar: number;
    rr_bar: number;
  };
  abs_level: 0 | 1 | 2 | 3;
  traction_control_level: 0 | 1 | 2 | 3;
}

export interface DriverFeedback {
  understeer: number; // -5 to +5
  brake_stability: number; // -5 to +5
  mid_corner_balance: number; // -5 to +5
  exit_traction: number; // -5 to +5
  notes: string;
}

export interface TrackConditions {
  track_temp_c: number;
  ambient_temp_c: number;
  fuel_level_start_percent: number;
  fuel_level_end_percent: number;
  session_type: "race" | "qualifying" | "practice" | "warmup";
  lap_number: number;
  total_laps: number;
  weather: "dry" | "wet" | "intermediate";
}

export interface TelemetryPoint {
  timestamp_ms: number;
  speed_kmh: number;
  throttle_percent: number;
  brake_percent: number;
  brake_pressure_bar: number;
  steering_angle_deg: number;
  yaw_rate_deg_per_sec: number;
  lateral_g: number;
  longitudinal_g: number;
  gear: number;
  rpm: number;
  tire_temp_fl_c: number;
  tire_temp_fr_c: number;
  tire_temp_rl_c: number;
  tire_temp_rr_c: number;
  tire_pressure_fl_bar: number;
  tire_pressure_fr_bar: number;
  tire_pressure_rl_bar: number;
  tire_pressure_rr_bar: number;
}

export interface ScenarioRequest {
  scenario_id?: string;
  car_setup: CarSetup;
  driver_feedback: DriverFeedback;
  track_conditions: TrackConditions;
  telemetry: TelemetryPoint[];
  timestamp?: string;
}

export const NOMINAL_SETUP: CarSetup = {
  front_wing_angle_deg: 8,
  rear_wing_angle_deg: 15,
  front_brake_bias_percent: 52,
  fuel_load_liters: 45,
  tire_compound: "soft",
  tire_pressures: {
    fl_bar: 28.5,
    fr_bar: 28.5,
    rl_bar: 29.0,
    rr_bar: 29.0,
  },
  abs_level: 1,
  traction_control_level: 1,
};

export const NOMINAL_FEEDBACK: DriverFeedback = {
  understeer: 0,
  brake_stability: 0,
  mid_corner_balance: 0,
  exit_traction: 0,
  notes: "",
};

export const NOMINAL_CONDITIONS: TrackConditions = {
  track_temp_c: 32,
  ambient_temp_c: 24,
  fuel_level_start_percent: 100,
  fuel_level_end_percent: 50,
  session_type: "practice",
  lap_number: 1,
  total_laps: 10,
  weather: "dry",
};