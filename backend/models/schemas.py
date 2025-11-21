from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from enum import Enum

class ProblemCategory(str, Enum):
    TIME_SPEED_DISTANCE = "Time, Speed & Distance"
    WORK_TIME = "Work & Time"
    PIPES_CISTERNS = "Pipes & Cisterns"
    AGE_PROBLEMS = "Age Problems"
    MIXTURE_ALLIGATION = "Mixture & Alligation"

class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class ValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    PENDING = "PENDING"

class MCQOptions(BaseModel):
    A: str
    B: str
    C: str
    D: str

class SolverResult(BaseModel):
    answer: float
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    approach: str

class Problem(BaseModel):
    id: str
    category: ProblemCategory
    difficulty: Difficulty
    question: str
    options: MCQOptions
    correct_answer: Literal["A", "B", "C", "D"]
    ground_truth: float
    solver_a_result: Optional[SolverResult] = None
    solver_b_result: Optional[SolverResult] = None
    validation_status: ValidationStatus = ValidationStatus.PENDING
    validation_score: float = 0.0
    attempts: int = 1
    error_reason: Optional[str] = None

class GenerationRequest(BaseModel):
    num_problems: int = Field(default=12, ge=1, le=20)
    categories: List[ProblemCategory] = Field(default_factory=lambda: [
        ProblemCategory.TIME_SPEED_DISTANCE,
        ProblemCategory.WORK_TIME,
        ProblemCategory.PIPES_CISTERNS
    ])
    difficulty_distribution: Dict[Difficulty, int] = Field(default_factory=lambda: {
        Difficulty.EASY: 4,
        Difficulty.MEDIUM: 5,
        Difficulty.HARD: 3
    })

class GenerationResponse(BaseModel):
    problems: List[Problem]
    stats: Dict
    research_summary: str

class AgentStatus(BaseModel):
    name: str
    status: Literal["idle", "running", "completed", "error"]
    progress: int = Field(ge=0, le=100)
    message: str = ""

class SystemStatus(BaseModel):
    agents: List[AgentStatus]
    current_problem: Optional[Problem] = None
    total_generated: int = 0
    total_valid: int = 0
