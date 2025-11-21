from agents.base_agent import BaseAgent
from typing import Dict
import json

class SolverAgentA(BaseAgent):
    """Solver using algebraic/mathematical approach"""
    
    def __init__(self):
        system_prompt = """You are Solver A - Mathematical Analysis Specialist.

CRITICAL: Your "selected_option" MUST be exactly one of: "A", "B", "C", or "D"

Process:
1. Extract given values
2. Identify the formula/method
3. Calculate step-by-step
4. Match calculated value to CLOSEST option
5. Select that option letter

Be PRECISE. Show your work. Output valid JSON."""

        super().__init__(name="SolverA_Algebraic", system_prompt=system_prompt)
    
    def solve(self, question: str, options: Dict) -> Dict:
        """Solve problem using algebraic approach"""
        
        prompt = f"""Solve this problem algebraically:

QUESTION:
{question}

OPTIONS:
A) {options.get('A', 'N/A')}
B) {options.get('B', 'N/A')}
C) {options.get('C', 'N/A')}
D) {options.get('D', 'N/A')}

TASK:
1. Solve the problem mathematically
2. Calculate the numeric answer
3. Compare your answer to each option
4. Select the CLOSEST matching option

Output JSON (EXACT format):
{{
  "approach": "algebraic",
  "reasoning": "Step 1: Extract values... Step 2: Apply formula... Step 3: Calculate...",
  "calculated_value": 4.8,
  "selected_option": "B",
  "confidence": 0.95,
  "verification": "My calculated value 4.8 matches option B exactly"
}}

CRITICAL: "selected_option" must be ONLY the letter: "A", "B", "C", or "D"
NOT "Option A" or "A. 4.8 days" - JUST THE LETTER."""

        return self.execute(prompt, temperature=0.2)


class SolverAgentB(BaseAgent):
    """Solver using logical/intuitive approach"""
    
    def __init__(self):
        system_prompt = """You are Solver B - Logical Reasoning Specialist.

CRITICAL: Your "selected_option" MUST be exactly one of: "A", "B", "C", or "D"

Process:
1. Understand the scenario
2. Apply logical reasoning
3. Calculate the answer
4. Match to CLOSEST option
5. Select that option letter

Output valid JSON with single-letter option selection."""

        super().__init__(name="SolverB_Logical", system_prompt=system_prompt)
    
    def solve(self, question: str, options: Dict) -> Dict:
        """Solve problem using logical approach"""
        
        prompt = f"""Solve this problem logically:

QUESTION:
{question}

OPTIONS:
A) {options.get('A', 'N/A')}
B) {options.get('B', 'N/A')}
C) {options.get('C', 'N/A')}
D) {options.get('D', 'N/A')}

TASK:
1. Understand what's being asked
2. Think through the logic
3. Calculate the answer
4. Select the CLOSEST matching option

Output JSON (EXACT format):
{{
  "approach": "logical",
  "reasoning": "Logical analysis: ... Therefore: ...",
  "calculated_value": 4.8,
  "selected_option": "B",
  "confidence": 0.90,
  "reality_check": "This makes sense because..."
}}

CRITICAL: "selected_option" must be ONLY the letter: "A", "B", "C", or "D"
NOT "Option B" or "B. 4.8 days" - JUST THE LETTER."""

        return self.execute(prompt, temperature=0.2)
