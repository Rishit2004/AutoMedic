from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# --- Data Models ---

class DiagnosticResult(BaseModel):
    """
    Structured output for the car diagnostic report.
    """
    issue_title: str = Field(description="A concise title for the suspected issue (e.g., 'Worn Brake Pads').")
    severity_score: int = Field(description="Severity rating from 1 (minor) to 10 (critical/dangerous).")
    confidence_level: float = Field(description="Confidence in the diagnosis from 0.0 to 1.0.")
    description: str = Field(description="Detailed explanation of why this issue is suspected based on symptoms.")
    recommended_action: str = Field(description="Immediate next steps (e.g., 'Stop driving immediately', 'Visit a mechanic soon').")
    diy_possible: bool = Field(description="Whether a skilled DIYer could likely fix this at home.")
    estimated_cost_range_usd: str = Field(description="Estimated repair cost range (e.g., '$150 - $300').")

class CarContext(BaseModel):
    """
    Context about the car provided by the user.
    """
    make: str
    model: str
    year: int
    mileage: Optional[int] = None
    last_service_date: Optional[str] = None

# --- Agent Setup ---

from pydantic_ai.models.openai import OpenAIModel

# We use OpenRouter via the OpenAI compatible interface
# This avoids "Unknown model" errors by being explicit
# Check for API key logic
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
model_name = os.getenv("LLM_MODEL", "google/gemini-2.0-flash-exp:free")

if not api_key:
    # Fallback to dummy key to prevent app crash on boot (Vercel 500 debug)
    print("CRITICAL WARNING: OPENAI_API_KEY is missing via os.getenv. Using dummy key for boot.")
    api_key = "missing-key-check-env-vars"

# Initialize model with explicit config
# Use a simple string for the model if parameters are standard, or fallback to object
# BUT: to be safe on Vercel cold boot, we must ensure we don't crash if the key is 'missing-key...'
# The OpenAIModel validation might be strict.

try:
    model = OpenAIModel(
        model_name=model_name,
        base_url=base_url,
        api_key=api_key,
    )
except Exception as e:
    print(f"Model init failed (likely invalid key): {e}")
    # Fallback to a valid dummy model object to allow app boot
    # This ensures the server starts, even if the agent will fail at runtime
    model = OpenAIModel(
        model_name="mock-model",
        base_url="https://example.com",
        api_key="mock-key"
    )

mechanic_agent = Agent(
    model=model,
    output_type=DiagnosticResult,
    system_prompt=(
        "You are AutoMedic, an expert automotive mechanic with 20 years of experience. "
        "Your goal is to diagnose car issues based on user-described symptoms. "
        "Be thorough, safety-conscious, and practical. "
        "If the symptoms are vague, make your best educated guess but reflect uncertainty in the confidence level. "
        "ALWAYS prioritize safety. If a car is unsafe to drive, emphasize it in the recommended_action."
    ),
)
