from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class TelemetryMetrics(BaseModel):
    """Computed metrics from raw telemetry"""
    lap_count: int
    avg_speed_kmh: float
    max_speed_kmh: float
    min_speed_kmh: float
    
    # Understeer/oversteer indicators
    understeer_events: int = Field(0, description="Count of potential understeer moments")
    oversteer_events: int = Field(0, description="Count of potential oversteer moments")
    
    # Tire analysis
    avg_tire_temp_c: Dict[str, float] = Field(
        default={},
        description="Average tire temps: {fl, fr, rl, rr}"
    )
    tire_temp_delta_c: Dict[str, float] = Field(
        default={},
        description="Tire temp spread (max-min): {fl, fr, rl, rr}"
    )
    tire_degradation_percent: Dict[str, float] = Field(
        default={},
        description="Estimated tire wear %: {fl, fr, rl, rr}"
    )
    
    # Pressure analysis
    avg_tire_pressure_bar: Dict[str, float] = Field(default={})
    pressure_delta_bar: Dict[str, float] = Field(
        default={},
        description="Pressure drift during lap"
    )
    
    # Braking analysis
    avg_brake_pressure_bar: float = Field(0, description="Average braking pressure")
    max_brake_pressure_bar: float = Field(0)
    braking_inefficiency_events: int = Field(
        0,
        description="High brake input with low deceleration"
    )
    
    # G-forces
    max_lateral_g: float = Field(0)
    max_longitudinal_g: float = Field(0)
    avg_lateral_g: float = Field(0)
    
    # Steering
    avg_steering_angle_deg: float = Field(0)
    max_steering_angle_deg: float = Field(0)
    
    # Throttle/brake correlation
    throttle_brake_overlap_percent: float = Field(
        0,
        description="% of lap with throttle and brake both active"
    )


class AnomalyDetection(BaseModel):
    """Detected anomalies in telemetry"""
    anomaly_type: str  # "tire_spike", "brake_fade", "understeer_corner", etc.
    severity: str = Field("medium", description="low|medium|high")
    timestamp_ms: int
    evidence: List[str] = Field(default=[], description="Supporting data points")
    lap_relative_position: str = Field("", description="turn_1, turn_6, etc.")


class ProcessedTelemetry(BaseModel):
    """Complete processed telemetry output"""
    scenario_id: str
    metrics: TelemetryMetrics
    anomalies: List[AnomalyDetection] = Field(default=[])
    raw_data_points: int = Field(0, description="Total telemetry points received")
    processing_status: str = Field("success", description="success|error|partial")