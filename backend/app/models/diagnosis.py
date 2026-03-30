from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class Recommendation(BaseModel):
    """Single recommended action"""
    priority: int = Field(1, ge=1, le=5, description="1=highest priority, 5=lowest")
    action: str = Field(..., description="increase_rear_wing|reduce_front_brake_bias|etc.")
    delta: str = Field(..., description="e.g., '+1°', '-2%', '+0.2 bar'")
    rationale: str = Field(..., description="Why this change?")
    expected_impact: str = Field("", description="What should improve?")
    implementation: str = Field("", description="How to make the change")


class Problem(BaseModel):
    """Detected car/driver problem"""
    type: str = Field(..., description="understeer_entry|oversteer_exit|tire_deg_rear|brake_fade|etc.")
    severity: str = Field("medium", description="low|medium|high")
    confidence_percent: int = Field(50, ge=0, le=100)
    evidence: List[str] = Field(
        default=[],
        description="Telemetry & feedback items supporting this diagnosis"
    )
    affected_area: str = Field("", description="entry|mid_corner|exit|braking|all")


class SetupDelta(BaseModel):
    """Recommended setup changes"""
    front_wing_angle_deg: Optional[str] = Field(None, description="'+1°' or None")
    rear_wing_angle_deg: Optional[str] = Field(None)
    front_brake_bias_percent: Optional[str] = Field(None, description="'+2%' or None")
    fuel_load_liters: Optional[str] = Field(None)
    tire_pressures: Optional[Dict[str, str]] = Field(None, description="{'fl_bar': '+0.1', ...}")
    abs_level: Optional[str] = Field(None)
    traction_control_level: Optional[str] = Field(None)


class DriverCoaching(BaseModel):
    """Driver-focused feedback"""
    braking_points: str = Field("", description="Suggestions for braking technique")
    acceleration_strategy: str = Field("", description="How to apply throttle")
    line_adjustments: str = Field("", description="Line changes that could help")
    gear_strategy: str = Field("", description="Gear selection notes")


class DiagnosisResult(BaseModel):
    """Complete diagnosis output"""
    scenario_id: str
    
    # Main diagnosis
    primary_problem: str = Field(
        "none",
        description="Top issue: understeer_entry|oversteer_exit|tire_deg|brake_fade|balanced"
    )
    overall_confidence_percent: int = Field(
        50,
        ge=0,
        le=100,
        description="Confidence in primary diagnosis"
    )
    
    # Detailed problems
    problems_detected: List[Problem] = Field(default=[])
    
    # Recommendations
    recommendations: List[Recommendation] = Field(default=[])
    setup_delta: SetupDelta = Field(default_factory=SetupDelta)
    
    # Driver coaching
    driver_coaching: Optional[DriverCoaching] = Field(default=None)
    
    # Analysis notes
    summary: str = Field(
        "",
        description="Plain-English summary of diagnosis and recommendations"
    )
    session_notes: str = Field("", description="Context about the session")
    
    # Metadata
    analysis_timestamp: Optional[str] = Field(None)
    lap_analyzed: Optional[int] = Field(None, description="Which lap was analyzed?")