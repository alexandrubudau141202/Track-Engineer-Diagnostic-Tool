"""
Scenario Routes
API endpoints for scenario diagnosis and report generation
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import uuid
import json
from app.models.scenario import ScenarioRequest, ScenarioResponse
from app.services.diagnosis_engine import diagnose
from app.services.telemetry_processor import process_telemetry
from app.services.pdf_generator import generate_report

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.post("/diagnose", response_model=dict)
async def diagnose_scenario(scenario: ScenarioRequest):
    """
    Run full diagnosis on a scenario.
    
    Returns:
    - diagnosis: DiagnosisResult object with identified problems and recommendations
    - pdf_url: URL path to download the generated PDF report
    """
    try:
        # Generate scenario ID if not provided
        if not scenario.scenario_id:
            scenario.scenario_id = str(uuid.uuid4())
        
        # Run diagnosis
        diagnosis_result = diagnose(scenario)
        
        # Process telemetry for PDF
        processed_telemetry = process_telemetry(scenario.telemetry, scenario.scenario_id)
        
        # Generate PDF
        pdf_filename = f"/tmp/report_{scenario.scenario_id}.pdf"
        generate_report(diagnosis_result, processed_telemetry, pdf_filename)
        
        # Return diagnosis + PDF URL
        return {
            "scenario_id": scenario.scenario_id,
            "status": "success",
            "diagnosis": diagnosis_result.dict(),
            "pdf_url": f"/api/reports/{scenario.scenario_id}.pdf",
            "message": f"Diagnosis complete. Primary issue: {diagnosis_result.primary_problem}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")


@router.get("/reports/{scenario_id}.pdf")
async def get_report(scenario_id: str):
    """Download generated PDF report"""
    try:
        pdf_filename = f"/tmp/report_{scenario_id}.pdf"
        return FileResponse(
            pdf_filename,
            media_type="application/pdf",
            filename=f"gt3r_diagnosis_{scenario_id}.pdf"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Report not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving report: {str(e)}")


@router.post("/upload-telemetry")
async def upload_telemetry(file: UploadFile = File(...)):
    """
    Upload a telemetry CSV/JSON file.
    
    Returns:
    - parsed telemetry data ready for diagnosis
    """
    try:
        contents = await file.read()
        
        # Parse based on file extension
        if file.filename.endswith('.json'):
            telemetry_data = json.loads(contents.decode())
        elif file.filename.endswith('.csv'):
            # Simple CSV parsing (assumes header row + data)
            telemetry_data = _parse_csv(contents.decode())
        else:
            raise ValueError("Unsupported file format. Use .json or .csv")
        
        return {
            "status": "success",
            "filename": file.filename,
            "data_points": len(telemetry_data),
            "data": telemetry_data[:100] if len(telemetry_data) > 100 else telemetry_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")


def _parse_csv(csv_content: str) -> list:
    """Simple CSV parser for telemetry data"""
    lines = csv_content.strip().split('\n')
    if not lines:
        return []
    
    # Parse header
    headers = lines[0].split(',')
    data = []
    
    # Parse rows
    for line in lines[1:]:
        values = line.split(',')
        row = {}
        for i, header in enumerate(headers):
            try:
                # Try to convert to float
                row[header.strip()] = float(values[i].strip())
            except (ValueError, IndexError):
                row[header.strip()] = values[i].strip() if i < len(values) else None
        data.append(row)
    
    return data


@router.post("/validate-scenario")
async def validate_scenario(scenario: ScenarioRequest):
    """
    Validate a scenario without running diagnosis.
    Returns validation errors if any.
    """
    errors = []
    
    # Basic validation
    if not scenario.car_setup:
        errors.append("car_setup is required")
    if not scenario.driver_feedback:
        errors.append("driver_feedback is required")
    if not scenario.track_conditions:
        errors.append("track_conditions is required")
    
    if errors:
        return {
            "status": "invalid",
            "errors": errors
        }
    
    return {
        "status": "valid",
        "scenario_id": scenario.scenario_id or str(uuid.uuid4()),
        "telemetry_points": len(scenario.telemetry),
        "message": "Scenario is valid and ready for diagnosis"
    }