"""
Health Check Routes
Simple status endpoints for monitoring and validation
"""

from fastapi import APIRouter
from app.services.gt3r_knowledge import NOMINAL_SETUP

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GT3 R Diagnostic Tool",
        "version": "1.0.0"
    }


@router.get("/status")
async def status():
    """Service status and capabilities"""
    return {
        "status": "ready",
        "capabilities": [
            "scenario_diagnosis",
            "telemetry_processing",
            "pdf_report_generation",
            "setup_recommendations",
            "driver_coaching"
        ],
        "supported_formats": ["json", "csv"],
        "nominal_setup": NOMINAL_SETUP
    }


@router.get("/version")
async def version():
    """Get API version"""
    return {
        "api_version": "1.0.0",
        "service": "GT3 R Diagnostic Tool",
        "build_date": "2024",
        "supported_problem_types": [
            "understeer_entry",
            "understeer_mid_corner",
            "understeer_exit",
            "oversteer_entry",
            "oversteer_mid_corner",
            "oversteer_exit",
            "tire_degradation_front",
            "tire_degradation_rear",
            "brake_fade",
            "brake_balance_instability",
            "balanced"
        ]
    }