import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

# Import the agent and models
# Note: In a real run, we need to ensure the import works (same dir)
try:
    from backend.agent import mechanic_agent, DiagnosticResult
except ImportError:
    # Safe fallback if running from root without package context
    from agent import mechanic_agent, DiagnosticResult

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
# We assume 'static' is a sibling of 'backend' or relative to root
static_path = Path(__file__).resolve().parent.parent / "static"
if not static_path.exists():
    # Fallback for different CWD
    static_path = Path("static")

if static_path.exists():
    app.mount("/static", StaticFiles(directory=static_path), name="static")


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
    try:
        # Construct the user prompt
        prompt = (
            f"Car: {request.car_year} {request.car_make} {request.car_model} "
            f"({request.mileage} miles). \n"
            f"Symptoms: {request.symptoms}"
        )
        
        # Run the agent
        # We assume OPENAI_API_KEY is set in environment
        result = await mechanic_agent.run(prompt)
        return result.data
        
    except Exception as e:
        # Log the error (would use logfire in real app)
        print(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "AutoMedic AI"}
