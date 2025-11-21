from sympy import symbols, Eq, solve, sympify
from typing import Dict, Tuple
import re

class MathValidator:
    """Ground truth calculator using SymPy - eliminates LLM arithmetic hallucinations"""
    
    @staticmethod
    def calculate_ground_truth(problem_params: Dict, category: str) -> Tuple[float, str]:
        """Calculate mathematically correct answer based on problem type"""
        
        try:
            if "meeting" in problem_params.get("type", "").lower() or "toward" in problem_params.get("scenario", "").lower():
                # Meeting time: distance = (speed1 + speed2) * time
                d = problem_params.get("distance", 0)
                s1 = problem_params.get("speed_1", 0)
                s2 = problem_params.get("speed_2", 0)
                
                if s1 + s2 == 0:
                    return None, "Invalid: Combined speed is zero"
                
                result = d / (s1 + s2)
                return float(result), f"Meeting time = {d} / ({s1} + {s2}) = {result:.3f}"
            
            elif "overtaking" in problem_params.get("type", "").lower():
                # Overtaking: distance = (speed1 - speed2) * time
                d = problem_params.get("distance", 0)
                s1 = problem_params.get("speed_1", 0)
                s2 = problem_params.get("speed_2", 0)
                
                if s1 <= s2:
                    return None, "Invalid: Slower can't overtake faster"
                
                result = d / (s1 - s2)
                return float(result), f"Overtaking time = {d} / ({s1} - {s2}) = {result:.3f}"
            
            elif "work" in category.lower():
                # Work: 1/A + 1/B = 1/T (combined rate)
                work_a = problem_params.get("days_a", 0)
                work_b = problem_params.get("days_b", 0)
                
                if work_a == 0 or work_b == 0:
                    return None, "Invalid: Zero work rate"
                
                combined_rate = 1/work_a + 1/work_b
                result = 1 / combined_rate
                return float(result), f"Combined time = 1 / (1/{work_a} + 1/{work_b}) = {result:.3f}"
            
            elif "pipe" in category.lower():
                # Similar to work problems
                fill_a = problem_params.get("fill_time_a", 0)
                fill_b = problem_params.get("fill_time_b", 0)
                
                if fill_a == 0 or fill_b == 0:
                    return None, "Invalid: Zero fill rate"
                
                combined_rate = 1/fill_a + 1/fill_b
                result = 1 / combined_rate
                return float(result), f"Combined fill time = 1 / (1/{fill_a} + 1/{fill_b}) = {result:.3f}"
            
            # Generic symbolic solver as fallback
            elif "equation" in problem_params:
                eq_str = problem_params["equation"]
                var = problem_params.get("variable", "x")
                
                x = symbols(var)
                equation = sympify(eq_str)
                solution = solve(equation, x)
                
                if solution:
                    return float(solution[0]), f"Solved {eq_str} = {solution[0]}"
                
            return None, "Unknown problem type"
            
        except Exception as e:
            return None, f"Calculation error: {str(e)}"
    
    @staticmethod
    def validate_answer(calculated: float, ground_truth: float, tolerance: float = 0.05) -> bool:
        """Check if calculated answer matches ground truth within tolerance"""
        if ground_truth == 0:
            return abs(calculated) < tolerance
        
        relative_error = abs(calculated - ground_truth) / abs(ground_truth)
        return relative_error <= tolerance
    
    @staticmethod
    def extract_numeric_value(text: str) -> float:
        """Extract numeric value from text (handles '2.5 hours', '$50', etc.)"""
        # Remove common units and extract number
        cleaned = re.sub(r'[^\d.-]', '', text)
        try:
            return float(cleaned)
        except:
            return 0.0
