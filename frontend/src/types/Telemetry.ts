// Telemetry.ts - Telemetry metrics and processed data types

export interface TelemetryMetrics {
  lap_count: number;
  avg_speed_kmh: number;
  max_speed_kmh: number;
  min_speed_kmh: number;
  understeer_events: number;
  oversteer_events: number;
  avg_tire_temp_c: Record<string, number>;
  tire_temp_delta_c: Record<string, number>;
  tire_degradation_percent: Record<string, number>;
  avg_tire_pressure_bar: Record<string, number>;
  pressure_delta_bar: Record<string, number>;
  avg_brake_pressure_bar: number;
  max_brake_pressure_bar: number;
  braking_inefficiency_events: number;
  max_lateral_g: number;
  max_longitudinal_g: number;
  avg_lateral_g: number;
  avg_steering_angle_deg: number;
  max_steering_angle_deg: number;
  throttle_brake_overlap_percent: number;
}

export interface AnomalyDetection {
  anomaly_type: string;
  severity: "low" | "medium" | "high";
  timestamp_ms: number;
  evidence: string[];
  lap_relative_position: string;
}

export interface ProcessedTelemetry {
  scenario_id: string;
  metrics: TelemetryMetrics;
  anomalies: AnomalyDetection[];
  raw_data_points: number;
  processing_status: "success" | "error" | "partial" | "no_data";
}