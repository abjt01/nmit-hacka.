from agents.base_agent import BaseAgent
from typing import Dict
import json

class GeneratorAgent(BaseAgent):
    """Specialized agent for generating quantitative word problems"""
    
    def __init__(self):
        system_prompt = """You are a Quantitative Word Problem Generator.

CRITICAL: You must include a "parameters" field with ALL numerical values needed for calculation.

Example for Work & Time:
{
  "parameters": {
    "days_a": 12,
    "days_b": 8,
    "formula_type": "work_combined"
  }
}

Example for Time, Speed & Distance:
{
  "parameters": {
    "distance": 360,
    "speed_a": 60,
    "speed_b": 80,
    "formula_type": "meeting_time"
  }
}

Always output valid JSON with structured parameters."""

        super().__init__(name="GeneratorAgent", system_prompt=system_prompt)
    
    def generate_problem(self, category: str, research_data: str, problem_num: int) -> Dict:
        """Generate a single problem"""
        
        # Category-specific examples
        category_examples = {
            "Work & Time": """
Example:
{
  "question": "Worker A can complete a job in 12 days. Worker B can complete the same job in 8 days. If they work together, how many days will it take to complete the job?",
  "parameters": {
    "days_a": 12,
    "days_b": 8,
    "formula_type": "work_combined"
  },
  "options": {
    "A": "4.0 days",
    "B": "4.8 days",
    "C": "5.0 days",
    "D": "6.0 days"
  },
  "correct_answer": "B",
  "solution_steps": "Step 1: Work rate of A = 1/12 per day. Step 2: Work rate of B = 1/8 per day. Step 3: Combined rate = 1/12 + 1/8 = 5/24 per day. Step 4: Time = 1 / (5/24) = 24/5 = 4.8 days",
  "expected_numeric_value": 4.8
}""",
            "Time, Speed & Distance": """
Example:
{
  "question": "Two trains start from stations 360 km apart and travel toward each other. Train A travels at 60 km/h and Train B at 80 km/h. After how many hours will they meet?",
  "parameters": {
    "distance": 360,
    "speed_a": 60,
    "speed_b": 80,
    "formula_type": "meeting_time"
  },
  "options": {
    "A": "2.0 hours",
    "B": "2.57 hours",
    "C": "3.0 hours",
    "D": "4.5 hours"
  },
  "correct_answer": "B",
  "solution_steps": "Step 1: Combined speed = 60 + 80 = 140 km/h. Step 2: Meeting time = 360 / 140 = 2.57 hours",
  "expected_numeric_value": 2.57
}""",
            "Pipes & Cisterns": """
Example:
{
  "question": "Pipe A can fill a tank in 10 hours. Pipe B can fill it in 15 hours. How long will it take to fill the tank if both pipes are opened together?",
  "parameters": {
    "fill_time_a": 10,
    "fill_time_b": 15,
    "formula_type": "pipe_combined"
  },
  "options": {
    "A": "5.0 hours",
    "B": "6.0 hours",
    "C": "6.5 hours",
    "D": "7.5 hours"
  },
  "correct_answer": "B",
  "solution_steps": "Step 1: Rate A = 1/10 per hour. Step 2: Rate B = 1/15 per hour. Step 3: Combined = 1/10 + 1/15 = 1/6 per hour. Step 4: Time = 6 hours",
  "expected_numeric_value": 6.0
}"""
        }
        
        example = category_examples.get(category, category_examples["Time, Speed & Distance"])
        
        prompt = f"""Generate problem #{problem_num} for category: {category}

Research Guidelines:
{research_data[:800]}

STRICT FORMAT REQUIREMENTS:

1. "parameters" field MUST contain:
   - ALL numerical values from the problem
   - "formula_type" indicating the calculation method
   
2. "options" MUST be exactly 4 choices (A, B, C, D)

3. "correct_answer" MUST be one of: "A", "B", "C", "D"

{example}

FORMULA TYPES BY CATEGORY:
- Work & Time: "work_combined", "work_partial", "work_efficiency"
- Time, Speed & Distance: "meeting_time", "overtaking", "average_speed"
- Pipes & Cisterns: "pipe_combined", "pipe_leak", "pipe_fill_drain"
- Profit & Loss: "profit_percent", "loss_percent", "discount"
- Age Problems: "age_ratio_past", "age_ratio_future", "age_difference"

Now generate a NEW problem for: {category}

Output MUST be valid JSON with ALL these fields:
- question
- parameters (with numeric values and formula_type)
- options (A, B, C, D)
- correct_answer
- solution_steps
- expected_numeric_value"""

        return self.execute(prompt, temperature=0.4)
