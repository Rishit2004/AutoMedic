import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

# Import the agent and models
# Note: In a real run, we need to ensure the import works (same dir)
app = FastAPI(title="AutoMedic AI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Static files (Frontend)
static_path = Path(__file__).resolve().parent.parent / "static"
if not static_path.exists():
    static_path = Path("static")

if static_path.exists():
    app.mount("/static", StaticFiles(directory=static_path), name="static")

class DiagnosticResult(BaseModel):
    issue_title: str
    severity_score: int
    confidence_level: float
    description: str
    recommended_action: str
    diy_possible: bool
    estimated_cost_range_usd: str

class DiagnosisRequest(BaseModel):
    symptoms: str
    car_make: str
    car_model: str
    car_year: int
    mileage: int = 0

@app.post("/api/diagnose", response_model=DiagnosticResult)
async def diagnose_car(request: DiagnosisRequest):
    """
    Run the mechanic agent to diagnose the issue.
    """
    # Lazy import to prevent boot-time crashes if environment is unstable
    try:
        try:
            from backend.agent import mechanic_agent
        except ImportError:
            from agent import mechanic_agent
            
        # Construct the user prompt
        prompt = (
            f"Car: {request.car_year} {request.car_make} {request.car_model} "
            f"({request.mileage} miles). \n"
            f"Symptoms: {request.symptoms}"
        )
        
        # Run the agent
        result = await mechanic_agent.run(prompt)
        return result.data
        
    except Exception as e:
        print(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "AutoMedic AI"}
