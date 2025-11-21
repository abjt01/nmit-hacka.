from agents.base_agent import BaseAgent
from typing import Dict
import json
import random

class GeneratorAgent(BaseAgent):
    """Specialized agent for generating quantitative word problems"""
    
    def __init__(self):
        system_prompt = """You are a Quantitative Word Problem Generator.

Create realistic word problems with:
1. Clear question text
2. 4 MCQ options (A, B, C, D)
3. Exactly one correct answer
4. Numerical parameters for validation

Always output valid JSON. Vary the correct answer position."""

        super().__init__(name="GeneratorAgent", system_prompt=system_prompt)
    
    def generate_problem(self, category: str, research_data: str, problem_num: int) -> Dict:
        """Generate a single problem"""
        
        # Simpler prompt that works reliably
        prompt = f"""Generate a quantitative aptitude problem.

Category: {category}
Problem Number: {problem_num}

Output this EXACT JSON structure (no extra text):
{{
  "question": "A complete word problem with a scenario and numbers",
  "parameters": {{
    "value1": 100,
    "value2": 50,
    "formula_type": "basic_calculation"
  }},
  "options": {{
    "A": "50 units",
    "B": "75 units",
    "C": "100 units",
    "D": "125 units"
  }},
  "correct_answer": "C",
  "solution_steps": "Step 1: Do this. Step 2: Do that. Step 3: Final answer.",
  "expected_numeric_value": 100
}}

EXAMPLES BY CATEGORY:

Work & Time:
{{
  "question": "A can complete a task in 10 days. B can complete it in 15 days. Working together, how many days will they take?",
  "parameters": {{"days_a": 10, "days_b": 15, "formula_type": "work_combined"}},
  "options": {{"A": "5 days", "B": "6 days", "C": "7 days", "D": "8 days"}},
  "correct_answer": "B",
  "solution_steps": "Rate A = 1/10, Rate B = 1/15, Combined = 1/10 + 1/15 = 1/6, Time = 6 days",
  "expected_numeric_value": 6
}}

Time, Speed & Distance:
{{
  "question": "Two trains 240 km apart travel toward each other at 50 km/h and 70 km/h. After how many hours will they meet?",
  "parameters": {{"distance": 240, "speed_a": 50, "speed_b": 70, "formula_type": "meeting_time"}},
  "options": {{"A": "1.5 hours", "B": "2 hours", "C": "2.5 hours", "D": "3 hours"}},
  "correct_answer": "B",
  "solution_steps": "Combined speed = 50+70 = 120 km/h, Time = 240/120 = 2 hours",
  "expected_numeric_value": 2
}}

Now generate a UNIQUE problem for: {category}

Requirements:
- Use DIFFERENT numbers than the examples
- Make the problem realistic
- Create 4 distinct options
- Only ONE correct answer
- Vary which option (A/B/C/D) is correct

Output ONLY valid JSON, nothing else."""

        result = self.execute(prompt, temperature=0.5)
        
        # Debug output
        if "error" in result:
            print(f"      ⚠️ Generator error: {result.get('error', 'Unknown')}")
        elif not result.get("question"):
            print(f"      ⚠️ Missing question field. Got keys: {list(result.keys())}")
        
        return result
