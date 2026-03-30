"""
GT3 R Diagnostic Tool - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routes import scenarios, health
from app.utils.logger import setup_logging

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="GT3 R Track Diagnostic Tool",
    description="AI-powered race engineering diagnostic tool for Porsche 911 GT3 R in WEC/GTWC",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ========== MIDDLEWARE ==========
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== ROUTES ==========
# Include route modules
app.include_router(health.router)
app.include_router(scenarios.router)


# ========== STARTUP/SHUTDOWN EVENTS ==========
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("GT3 R Diagnostic Tool started")
    logger.info("API docs available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("GT3 R Diagnostic Tool shutting down")


# ========== ROOT ENDPOINT ==========
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "service": "GT3 R Track Diagnostic Tool",
        "version": "1.0.0",
        "status": "operational",
        "docs_url": "/docs",
        "endpoints": {
            "health": "/api/health",
            "status": "/api/status",
            "diagnose": "/api/scenarios/diagnose",
            "upload_telemetry": "/api/scenarios/upload-telemetry",
            "validate_scenario": "/api/scenarios/validate-scenario",
            "get_report": "/api/reports/{scenario_id}.pdf"
        }
    }


# ========== CUSTOM OPENAPI SCHEMA ==========
def custom_openapi():
    """Customize OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="GT3 R Diagnostic Tool API",
        version="1.0.0",
        description="Race engineering diagnostic system for Porsche 911 GT3 R",
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.porsche.com/international/en/brand/"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ========== ERROR HANDLERS ==========
from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected error occurred",
            "detail": str(exc)
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )