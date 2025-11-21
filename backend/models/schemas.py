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

class Problem(BaseModel):
    id: str
    category: str
    question: str
    options: MCQOptions
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str
    validation_status: str = "Valid"

class GenerationRequest(BaseModel):
    num_problems: int = Field(default=12, ge=1, le=20)
    category: ProblemCategory = ProblemCategory.MIXED

class GenerationResponse(BaseModel):
    problems: List[Problem]
    stats: Dict
    total_api_calls: int
