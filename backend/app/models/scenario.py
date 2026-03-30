from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ============ TELEMETRY DATA ============
class TelemetryPoint(BaseModel):
    """Single telemetry data point from a lap"""
    timestamp_ms: int
    speed_kmh: float
    throttle_percent: float = Field(0, ge=0, le=100)
    brake_percent: float = Field(0, ge=0, le=100)
    brake_pressure_bar: float = Field(0, ge=0)
    steering_angle_deg: float
    yaw_rate_deg_per_sec: float
    lateral_g: float
    longitudinal_g: float
    gear: int = Field(1, ge=1, le=6)
    rpm: int = Field(6000, ge=0)
    
    # Tire telemetry
    tire_temp_fl_c: float
    tire_temp_fr_c: float
    tire_temp_rl_c: float
    tire_temp_rr_c: float
    
    tire_pressure_fl_bar: float
    tire_pressure_fr_bar: float
    tire_pressure_rl_bar: float
    tire_pressure_rr_bar: float


# ============ DRIVER FEEDBACK ============
class DriverFeedback(BaseModel):
    """Driver's subjective feedback about car balance and behavior"""
    # -5 to +5 scale
    understeer: int = Field(0, ge=-5, le=5, description="Negative = oversteer, Positive = understeer")
    brake_stability: int = Field(0, ge=-5, le=5, description="Stability under braking")
    mid_corner_balance: int = Field(0, ge=-5, le=5, description="Balance mid-corner")
    exit_traction: int = Field(0, ge=-5, le=5, description="Traction on corner exit")
    notes: str = Field("", description="Free-form driver comments")


# ============ CAR SETUP ============
class CarSetup(BaseModel):
    """GT3 R setup parameters"""
    # Wings (in degrees)
    front_wing_angle_deg: float = Field(8, ge=0, le=15)
    rear_wing_angle_deg: float = Field(15, ge=0, le=20)
    
    # Brakes
    front_brake_bias_percent: float = Field(52, ge=40, le=65, description="Front brake bias %")
    
    # Fuel
    fuel_load_liters: float = Field(45, ge=20, le=70)
    
    # Tires
    tire_compound: str = Field("soft", description="soft|medium|hard")
    tire_pressures: dict = Field(
        {"fl_bar": 28.5, "fr_bar": 28.5, "rl_bar": 29.0, "rr_bar": 29.0},
        description="Tire pressures in bar"
    )
    
    # Suspension (optional for v1, can expand later)
    abs_level: int = Field(1, ge=0, le=3, description="ABS level 0-3")
    traction_control_level: int = Field(1, ge=0, le=3, description="TC level 0-3")


# ============ TRACK CONDITIONS ============
class TrackConditions(BaseModel):
    """Environmental and session-specific data"""
    track_temp_c: float = Field(32, description="Track surface temperature")
    ambient_temp_c: float = Field(24, description="Ambient air temperature")
    fuel_level_start_percent: float = Field(100, ge=0, le=100)
    fuel_level_end_percent: float = Field(50, ge=0, le=100)
    session_type: str = Field("race", description="race|qualifying|practice|warmup")
    lap_number: int = Field(1, ge=1, description="Which lap is this?")
    total_laps: int = Field(1, ge=1, description="Total laps in session")
    weather: str = Field("dry", description="dry|wet|intermediate")


# ============ MAIN SCENARIO REQUEST ============
class ScenarioRequest(BaseModel):
    """Complete race scenario for diagnosis"""
    scenario_id: Optional[str] = Field(default=None)
    
    car_setup: CarSetup
    driver_feedback: DriverFeedback
    track_conditions: TrackConditions
    
    telemetry: List[TelemetryPoint] = Field(default=[], description="Raw telemetry data")
    
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


# ============ SCENARIO RESPONSE ============
class ScenarioResponse(BaseModel):
    """Response confirming scenario receipt"""
    scenario_id: str
    status: str = "received"
    message: str = ""