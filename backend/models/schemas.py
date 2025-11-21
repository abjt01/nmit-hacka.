from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from enum import Enum

class ProblemCategory(str, Enum):
    TIME_SPEED_DISTANCE = "Time, Speed & Distance"
    WORK_TIME = "Work & Time"
    PIPES_CISTERNS = "Pipes & Cisterns"
    PROFIT_LOSS = "Profit, Loss & Discount"
    RATIO_MIXTURE = "Ratio, Mixtures & Sharing"
    AGE_PROBLEMS = "Age Problems"
    BOATS_STREAMS = "Boats & Streams"
    LOGICAL_MATH = "Allocation & Logical Math"
    MIXED = "Mixed (All Categories)"

class MCQOptions(BaseModel):
    A: str
    B: str
    C: str
    D: str

class SolverResult(BaseModel):
    """Results from a solver agent"""
    answer: float
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    approach: str  # "algebraic" or "logical"

class Problem(BaseModel):
    """Complete problem with validation results"""
    id: str
    category: str
    question: str
    options: MCQOptions
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str
    validation_status: str = "Valid"
    
    # Solver results (optional for backwards compatibility)
    solver_a_result: Optional[SolverResult] = None
    solver_b_result: Optional[SolverResult] = None
    ground_truth: Optional[float] = None
    validation_score: Optional[float] = None

class GenerationRequest(BaseModel):
    num_problems: int = Field(default=12, ge=1, le=20)
    category: ProblemCategory = ProblemCategory.MIXED

class GenerationResponse(BaseModel):
    problems: List[Problem]
    stats: Dict
    total_api_calls: int

class AgentStatus(BaseModel):
    """Real-time agent status for frontend"""
    name: str
    status: Literal["idle", "running", "completed", "error"]
    progress: int = Field(ge=0, le=100)
    message: str = ""

class SystemStatus(BaseModel):
    """Overall system status"""
    agents: List[AgentStatus]
    current_problem: Optional[Problem] = None
    total_generated: int = 0
    total_valid: int = 0
