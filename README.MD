# GT3 R Track Engineer Diagnostic Tool – Project Architecture

## 1. Project Overview

**Goal:** Build a web-based diagnostic tool that ingests race scenario data (telemetry, driver feedback, setup state) for a Porsche 911 GT3 R, diagnoses problems, and generates a professional PDF report with actionable setup recommendations.

**Core Loop:**
User Input → Data Processing → Diagnosis Engine → PDF Generation + 3D Visualization

---

## 2. Technology Stack

### Frontend
- **React 18** (TypeScript preferred)
- **Three.js** (GLB model loading, 3D visualization)
- **React Hook Form** (scenario builder form)
- **Chart.js or Recharts** (telemetry preview graphs)
- **Tailwind CSS** (styling)
- **Axios** (API calls to backend)

### Backend
- **Python 3.10+**
- **FastAPI** (REST API server)
- **Pydantic** (data validation)
- **Pandas/NumPy** (telemetry processing)
- **ReportLab or FPDF2** (PDF generation)
- **Matplotlib/Seaborn** (graph generation for PDFs)
- **WebSocket** (optional: real-time telemetry streaming)

### Dev Tools
- **Vite** (frontend bundler)
- **Uvicorn** (ASGI server for FastAPI)
- **Docker** (containerization, optional but recommended)
- **Git** (version control)

---

## 3. Project Structure

```
gt3r-diagnostic-tool/
│
├── frontend/                          # React application
│   ├── public/
│   │   ├── models/
│   │   │   └── gt3r.glb              # 3D model
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── ScenarioBuilder.tsx   # Form for inputting race data
│   │   │   ├── TelemetryUpload.tsx   # File upload & preview
│   │   │   ├── CarViewer.tsx         # 3D GT3 R viewer (Three.js)
│   │   │   ├── TelemetryChart.tsx    # Graph preview
│   │   │   ├── ReportPreview.tsx     # PDF preview/download
│   │   │   └── Dashboard.tsx         # Main layout
│   │   │
│   │   ├── hooks/
│   │   │   ├── useScenario.ts        # State management for scenario
│   │   │   └── useAPI.ts             # API calls to backend
│   │   │
│   │   ├── types/
│   │   │   ├── Scenario.ts           # TypeScript interfaces
│   │   │   ├── Telemetry.ts
│   │   │   └── Diagnosis.ts
│   │   │
│   │   ├── styles/
│   │   │   └── globals.css
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── .env.local
│
├── backend/                           # Python FastAPI server
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry point
│   │   │
│   │   ├── models/                   # Pydantic data models
│   │   │   ├── scenario.py           # ScenarioRequest, ScenarioResponse
│   │   │   ├── telemetry.py          # TelemetryData, TelemetryPoint
│   │   │   └── diagnosis.py          # DiagnosisResult, Recommendation
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── telemetry_processor.py
│   │   │   │   - clean_data()
│   │   │   │   - compute_metrics()
│   │   │   │   - detect_anomalies()
│   │   │   │
│   │   │   ├── diagnosis_engine.py
│   │   │   │   - diagnose(telemetry, setup, feedback)
│   │   │   │   - GT3 R-specific logic (understeer, tire deg, brake fade, etc.)
│   │   │   │
│   │   │   ├── pdf_generator.py
│   │   │   │   - generate_report(diagnosis_result)
│   │   │   │   - embed_graphs()
│   │   │   │   - format_recommendations()
│   │   │   │
│   │   │   └── gt3r_knowledge.py     # GT3 R setup reference data
│   │   │       - nominal_setups
│   │   │       - problem_solutions
│   │   │       - setup_adjustment_guide
│   │   │
│   │   ├── routes/
│   │   │   ├── scenarios.py          # POST /scenarios/diagnose
│   │   │   └── health.py             # GET /health
│   │   │
│   │   ├── utils/
│   │   │   ├── config.py             # Settings
│   │   │   └── logger.py             # Logging
│   │   │
│   │   └── __init__.py
│   │
│   ├── data/
│   │   ├── gt3r_specs.json           # GT3 R reference data
│   │   └── problem_matrices.json     # Problem → Solution mapping
│   │
│   ├── tests/
│   │   ├── test_telemetry_processor.py
│   │   ├── test_diagnosis_engine.py
│   │   └── test_pdf_generator.py
│   │
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
├── docker-compose.yml                # (Optional) Local dev environment
├── README.md                          # Project overview
└── .gitignore
```

---

## 4. Data Schemas

### 4.1 Scenario Request (Frontend → Backend)

```json
{
  "scenario_id": "uuid",
  "car_setup": {
    "front_wing_angle_deg": 8,
    "rear_wing_angle_deg": 15,
    "front_brake_bias_percent": 52,
    "fuel_load_liters": 45,
    "tire_compound": "soft",
    "tire_pressures": {
      "fl_bar": 28.5,
      "fr_bar": 28.5,
      "rl_bar": 29.0,
      "rr_bar": 29.0
    }
  },
  "driver_feedback": {
    "understeer": 0,           # -5 to +5 scale (negative = oversteer)
    "brake_stability": 0,
    "mid_corner_balance": 0,
    "exit_traction": 0,
    "notes": "Car feels loose on entry to Turn 6"
  },
  "track_conditions": {
    "track_temp_c": 32,
    "ambient_temp_c": 24,
    "fuel_level_start_percent": 100,
    "session_type": "race|qualifying|practice",
    "lap_number": 5
  },
  "telemetry_data": {
    "upload_file": "file_bytes",  # CSV or JSON, parsed on backend
    "or_json": [...]  # Or embedded as JSON array
  }
}
```

### 4.2 Telemetry Data Point

```json
{
  "timestamp_ms": 1000,
  "speed_kmh": 220,
  "throttle_percent": 85,
  "brake_percent": 0,
  "brake_pressure_bar": 0,
  "steering_angle_deg": 5,
  "yaw_rate_deg_per_sec": 2.3,
  "lateral_g": 1.2,
  "longitudinal_g": 0.5,
  "gear": 5,
  "rpm": 7500,
  "tire_temp_fl_c": 95,
  "tire_temp_fr_c": 94,
  "tire_temp_rl_c": 96,
  "tire_temp_rr_c": 97,
  "tire_pressure_fl_bar": 28.5,
  "tire_pressure_fr_bar": 28.4,
  "tire_pressure_rl_bar": 29.1,
  "tire_pressure_rr_bar": 29.2
}
```

### 4.3 Diagnosis Result (Backend → Frontend)

```json
{
  "scenario_id": "uuid",
  "primary_problem": "understeer_mid_corner",
  "confidence_percent": 85,
  "problems_detected": [
    {
      "type": "understeer_mid_corner",
      "severity": "high",
      "evidence": [
        "High yaw rate at Turn 6 entry",
        "Steering angle increasing but speed decreasing",
        "Driver feedback: +3 understeer"
      ]
    },
    {
      "type": "tire_deg_rear_right",
      "severity": "medium",
      "evidence": ["RR tire temp spike on lap 5"]
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "action": "increase_rear_wing_angle",
      "delta": "+1 degree",
      "rationale": "Increase rear downforce to reduce understeer in mid-corner",
      "expected_impact": "Reduce yaw rate by ~0.5 deg/s, improve mid-corner balance"
    },
    {
      "priority": 2,
      "action": "adjust_front_brake_bias",
      "delta": "-2%",
      "rationale": "Reduce front bias to help mid-corner stability"
    }
  ],
  "setup_delta": {
    "rear_wing_angle_deg": "+1",
    "front_brake_bias_percent": "-2"
  }
}
```

### 4.4 PDF Report Structure

```
1. Executive Summary
   - Scenario info (track, fuel, lap #, conditions)
   - Primary problem & confidence
   - Top 3 recommendations

2. Telemetry Analysis
   - Speed/Throttle/Brake graphs
   - G-force plot
   - Tire temp/pressure trends

3. Problem Diagnosis
   - Problem list with severity
   - Evidence from telemetry + feedback
   - Root cause analysis

4. Recommended Setup Changes
   - Table: Current → Recommended
   - Rationale for each change
   - Expected impact

5. Driver Notes
   - If applicable, coaching points
```

---

## 5. Service Architecture

### 5.1 Telemetry Processor

**Input:** Raw telemetry data (CSV/JSON), metadata (track, setup, conditions)

**Process:**
1. Parse and validate telemetry
2. Smooth data (optional low-pass filter for noise)
3. Compute derived metrics:
   - Cornering speed at peak G
   - Braking pressure profile
   - Tire temp rate-of-change
   - Understeer angle (steering input vs. lateral G)
4. Segment lap (throttle zones, braking zones, cornering)
5. Detect anomalies (tire spikes, brake fade, etc.)

**Output:** ProcessedTelemetry object with metrics and anomalies

---

### 5.2 Diagnosis Engine

**Input:** ProcessedTelemetry, DriverFeedback, CarSetup, TrackConditions

**Logic:**
1. **Pattern matching** against GT3 R knowledge base:
   - IF (yaw_rate_high AND steering_angle_high AND understeer_feedback) → understeer_problem
   - IF (tire_temp_rear_spike AND pressure_high) → tire_deg_problem
   - IF (brake_pressure_fade AND long_braking_zone) → brake_fade_problem

2. **Severity scoring:**
   - confidence_percent = signal_strength × evidence_weight

3. **Generate recommendations** from problem → solution matrix:
   - Problem: understeer_mid_corner
   - Solutions: [increase_rear_wing, reduce_front_brake_bias, driver_input_notes]

**Output:** DiagnosisResult with problems, confidence, and recommendations

---

### 5.3 PDF Generator

**Input:** DiagnosisResult, ProcessedTelemetry

**Process:**
1. Create PDF structure (ReportLab)
2. Embed title page (scenario, metadata)
3. Generate graphs (Matplotlib → PNG) and embed
4. Format problem diagnosis section
5. Create recommendation table
6. Add footer with timestamp

**Output:** PDF bytes (returned as file download)

---

### 5.4 GT3 R Knowledge Base

**File: `gt3r_knowledge.py`**

```python
GT3R_SETUP_REFERENCE = {
    "nominal": {
        "front_wing_angle": 8,
        "rear_wing_angle": 15,
        "front_brake_bias": 52,
        ...
    },
    "problem_solutions": {
        "understeer_entry": {
            "primary": {"action": "increase_front_brake_bias", "delta": "+1-2%"},
            "secondary": [
                {"action": "reduce_front_wing", "delta": "-0.5°"},
                {"action": "driver_technique", "note": "Trail brake later"}
            ]
        },
        "understeer_mid_corner": {
            "primary": {"action": "increase_rear_wing_angle", "delta": "+1°"},
            ...
        },
        "tire_deg_rear": {
            "primary": {"action": "reduce_tire_pressure_rear", "delta": "-0.2 bar"},
            ...
        }
    }
}
```

---

## 6. API Endpoints

### POST `/scenarios/diagnose`

**Request:**
```
{
  "scenario": ScenarioRequest,
  "telemetry": TelemetryData[]
}
```

**Response:**
```
{
  "diagnosis": DiagnosisResult,
  "pdf_url": "http://..../reports/uuid.pdf"
}
```

**Process:**
1. Validate input
2. Process telemetry
3. Run diagnosis
4. Generate PDF
5. Return diagnosis + PDF link

### GET `/reports/{report_id}.pdf`

Return the generated PDF file.

### GET `/health`

Basic health check.

---

## 7. Data Flow Diagram

```
┌─────────────────────────────────────────┐
│  Frontend: React App                    │
│  ├─ Scenario Builder Form               │
│  ├─ Telemetry Upload                    │
│  ├─ 3D Car Viewer (GLB)                 │
│  └─ Report Preview                      │
└──────────────┬──────────────────────────┘
               │ POST /scenarios/diagnose
               │ (Scenario + Telemetry)
               ▼
┌─────────────────────────────────────────┐
│  Backend: FastAPI                       │
│  ├─ Route Handler                       │
│  ├─ Telemetry Processor                 │
│  │  └─ Validate, Clean, Compute Metrics │
│  ├─ Diagnosis Engine                    │
│  │  └─ Pattern Match, Score, Recommend  │
│  └─ PDF Generator                       │
│     └─ Create Report with Graphs        │
└──────────────┬──────────────────────────┘
               │ DiagnosisResult + PDF URL
               ▼
┌─────────────────────────────────────────┐
│  Frontend: Display & Download           │
│  ├─ Diagnosis Summary                   │
│  ├─ Recommendation List                 │
│  ├─ PDF Preview / Download Link         │
│  └─ Option to Export Report             │
└─────────────────────────────────────────┘
```

---

## 8. Development Phases

### Phase 1: Core Backend (Weeks 1–2)
- [ ] FastAPI scaffolding
- [ ] Pydantic models (Scenario, Telemetry, Diagnosis)
- [ ] Telemetry processor (parsing, basic metrics)
- [ ] Diagnosis engine stub (simple pattern matching)
- [ ] GT3 R knowledge base (problem → solution mapping)
- [ ] Unit tests for processor & engine

### Phase 2: PDF Generation (Week 2–3)
- [ ] ReportLab / FPDF2 setup
- [ ] Graph generation (Matplotlib)
- [ ] PDF template + styling
- [ ] Embed graphs + recommendations
- [ ] Test PDF output quality

### Phase 3: Frontend Core (Weeks 3–4)
- [ ] React app scaffolding
- [ ] Scenario builder form (React Hook Form)
- [ ] Telemetry upload component
- [ ] API integration (Axios, error handling)
- [ ] Report preview component

### Phase 4: 3D Viewer (Week 4–5)
- [ ] Three.js setup
- [ ] GLB model loading (GT3 R)
- [ ] Camera controls, lighting
- [ ] Optional: highlight setup components (wing, brakes)

### Phase 5: Polish & Testing (Week 5+)
- [ ] End-to-end testing
- [ ] Error handling & edge cases
- [ ] UI/UX refinement
- [ ] Performance optimization
- [ ] Documentation

---

## 9. Key Design Decisions

1. **Diagnosis as Rule-Based (Not ML):** Simpler, explainable, interpretable. You *know* why a recommendation was made.

2. **PDF as Primary Output:** Professional, shareable, archive-able. Matches real engineering workflow.

3. **Specific to GT3 R:** Not generic. Depth over breadth. Shows expertise.

4. **Modular Services:** Easy to test, refactor, extend. Clean separation of concerns.

5. **Frontend Preview Before Download:** User sees the diagnosis before committing to PDF. Faster iteration.

---
