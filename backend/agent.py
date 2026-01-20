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
from pydantic_ai.models.openai import OpenAIModel

# Check if we have the API key
if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY not found in environment")

# We use OpenRouter via the OpenAI compatible interface
# The openai client will automatically pick up OPENAI_BASE_URL and OPENAI_API_KEY from env
model = OpenAIModel('anthropic/claude-3-haiku')

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
