from agents.base_agent import BaseAgent
from typing import Dict
import json

class ResearchAgent(BaseAgent):
    """Specialized agent for researching problem patterns and formulas"""
    
    def __init__(self):
        system_prompt = """You are a Quantitative Aptitude Research Expert.

Your role: Analyze mathematical problem categories and provide comprehensive design guidelines.

For each category, provide:
1. Core formulas and mathematical relationships
2. Common problem variations and patterns
3. Realistic value ranges for parameters
4. Common LLM hallucination traps to avoid
5. MCQ distractor design strategies

Always output valid, structured JSON."""

        super().__init__(name="ResearchAgent", system_prompt=system_prompt)
    
    def research_category(self, category: str) -> Dict:
        """Research a specific problem category"""
        
        prompt = f"""Research the category: "{category}"

Provide comprehensive guidelines for creating problems in this category.

If "Mixed", cover these 8 categories briefly:
1. Time, Speed & Distance - Meeting time, overtaking, races, relative speed
2. Work & Time - Combined work rates, partial completion, efficiency
3. Pipes & Cisterns - Filling/emptying tanks, inlet/outlet problems
4. Profit, Loss & Discount - Cost price, selling price, markup, discount chains
5. Ratio, Mixtures & Sharing - Mixture problems, alligation, proportional sharing
6. Age Problems - Present age, past/future age ratios, age differences
7. Boats & Streams - Upstream/downstream, still water speed, current
8. Logical Math - LCM/HCF scheduling, pattern problems, allocation

For each relevant category, provide:
{{
  "category_name": "...",
  "formulas": ["formula 1", "formula 2", ...],
  "problem_types": ["type 1 description", "type 2 description", ...],
  "value_ranges": {{
    "parameter1": "min-max range with unit",
    "parameter2": "min-max range with unit"
  }},
  "common_mistakes": ["mistake 1", "mistake 2", ...],
  "distractor_strategies": ["strategy 1", "strategy 2", ...]
}}

Output as JSON array of category guidelines."""

        return self.execute(prompt, temperature=0.2)
