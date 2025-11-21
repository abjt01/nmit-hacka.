from agents.base_agent import BaseAgent
from typing import Dict
import json
import random

class SolverAgentA(BaseAgent):
    """Solver using algebraic/mathematical approach"""
    
    def __init__(self):
        system_prompt = """You are Solver A - Mathematical Analysis Specialist.

You are an UNBIASED problem solver. Do NOT favor any particular option.

Your process:
1. Solve the problem mathematically
2. Calculate the exact numeric answer
3. Compare your answer to EACH option independently
4. Select the option with the SMALLEST difference from your calculated value

CRITICAL: Your "selected_option" must be EXACTLY one letter: "A", "B", "C", or "D"
NOT "Option B" or "B: 4.8 days" - ONLY THE LETTER.

Be completely objective. Do not assume any option is more likely to be correct."""

        super().__init__(name="SolverA_Algebraic", system_prompt=system_prompt)
    
    def solve(self, question: str, options: Dict) -> Dict:
        """Solve problem using algebraic approach"""
        
        # Randomize option order to prevent bias
        option_order = list(options.keys())
        random.shuffle(option_order)
        
        options_shuffled = "\n".join([f"{key}) {options[key]}" for key in option_order])
        
        prompt = f"""Solve this problem using PURE MATHEMATICS:

QUESTION:
{question}

OPTIONS (in random order):
{options_shuffled}

INSTRUCTIONS:
1. Ignore the option labels initially
2. Solve the problem step-by-step mathematically
3. Calculate the exact numeric answer
4. NOW compare your answer to EACH option:
   - Extract the numeric value from each option
   - Calculate absolute difference from your answer
   - Select the option with MINIMUM difference
5. State ONLY the letter of that option

Output JSON (EXACT format):
{{
  "approach": "algebraic",
  "reasoning": "Step 1: [calculation] Step 2: [calculation] Step 3: [final calculation]",
  "calculated_value": 4.8,
  "option_comparison": {{"A": 0.3, "B": 0.0, "C": 0.5, "D": 1.2}},
  "selected_option": "B",
  "confidence": 0.95
}}

CRITICAL RULES:
1. "calculated_value" must be a NUMBER (not text)
2. "selected_option" must be ONLY a single letter: "A", "B", "C", or "D"
3. Choose based on CLOSEST MATCH to your calculated value
4. Do NOT favor any option position"""

        result = self.execute(prompt, temperature=0.15)  # Lower temperature for consistency
        
        # Validate result
        if isinstance(result, dict) and 'selected_option' in result:
            # Clean the option (remove any extra text)
            option = str(result['selected_option']).strip().upper()
            # Extract just the letter
            if len(option) > 1:
                option = option[0] if option[0] in ['A', 'B', 'C', 'D'] else 'A'
            result['selected_option'] = option
        
        return result


class SolverAgentB(BaseAgent):
    """Solver using logical/intuitive approach"""
    
    def __init__(self):
        system_prompt = """You are Solver B - Logical Reasoning Specialist.

You are UNBIASED. Analyze problems from first principles.

Your process:
1. Understand the scenario logically
2. Apply reasoning to calculate the answer
3. Match to the CLOSEST option objectively

CRITICAL: Your "selected_option" must be EXACTLY one letter: "A", "B", "C", or "D"

Never assume any option is more likely. Base your choice purely on your calculation."""

        super().__init__(name="SolverB_Logical", system_prompt=system_prompt)
    
    def solve(self, question: str, options: Dict) -> Dict:
        """Solve problem using logical approach"""
        
        # Randomize options
        option_order = list(options.keys())
        random.shuffle(option_order)
        options_shuffled = "\n".join([f"{key}) {options[key]}" for key in option_order])
        
        prompt = f"""Solve this problem using LOGICAL REASONING:

QUESTION:
{question}

OPTIONS (in random order):
{options_shuffled}

INSTRUCTIONS:
1. Read the problem carefully
2. Think through the logic step-by-step
3. Calculate the answer using common sense and reasoning
4. Compare your answer to each option independently
5. Select the option that BEST matches your answer

Output JSON:
{{
  "approach": "logical",
  "reasoning": "Logical analysis: [your thought process]",
  "calculated_value": 4.8,
  "selected_option": "B",
  "confidence": 0.90
}}

RULES:
1. "calculated_value" must be a NUMBER
2. "selected_option" must be a single letter: "A", "B", "C", or "D"
3. Choose objectively based on your calculation
4. Do NOT favor any particular option"""

        result = self.execute(prompt, temperature=0.15)
        
        # Validate result
        if isinstance(result, dict) and 'selected_option' in result:
            option = str(result['selected_option']).strip().upper()
            if len(option) > 1:
                option = option[0] if option[0] in ['A', 'B', 'C', 'D'] else 'A'
            result['selected_option'] = option
        
        return result
