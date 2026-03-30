"""
Application Configuration
"""

import os
from typing import Optional


class Settings:
    """Application settings"""
    
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_VERSION: str = "1.0.0"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # PDF Generation
    PDF_OUTPUT_DIR: str = os.getenv("PDF_OUTPUT_DIR", "/tmp")
    PDF_DPI: int = int(os.getenv("PDF_DPI", "100"))
    
    # CORS
    CORS_ORIGINS: list = ["*"]  # Allow all in dev; restrict in production
    
    # Diagnosis
    MIN_CONFIDENCE_THRESHOLD: int = 40
    MAX_PROBLEMS_TO_REPORT: int = 5
    
    # Database (if using one in future)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    def __init__(self):
        """Validate and initialize settings"""
        # Create log directory if needed
        if self.LOG_FILE:
            os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        
        # Create PDF output directory if needed
        if self.PDF_OUTPUT_DIR:
            os.makedirs(self.PDF_OUTPUT_DIR, exist_ok=True)


# Global settings instance
settings = Settings()