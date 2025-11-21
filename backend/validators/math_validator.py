from sympy import symbols, Eq, solve, sympify, simplify
from typing import Dict, Tuple, Optional
import re

class MathValidator:
    """Ground truth calculator using SymPy - eliminates LLM hallucinations"""
    
    @staticmethod
    def calculate_ground_truth(problem_params: Dict, question: str) -> Tuple[Optional[float], str]:
        """Calculate mathematically correct answer using SymPy"""
        
        # If parameters are missing or invalid, try extracting from question
        if not problem_params or all(v == 0 for k, v in problem_params.items() if isinstance(v, (int, float))):
            # Try to infer category from question
            category = ""
            if "work" in question.lower():
                category = "Work & Time"
            elif "speed" in question.lower() or "train" in question.lower():
                category = "Time, Speed & Distance"
            elif "pipe" in question.lower():
                category = "Pipes & Cisterns"
            
            problem_params = MathValidator.extract_parameters_from_question(question, category)
            
            if not problem_params:
                return None, "Could not extract parameters from question"
        
        try:
            formula_type = problem_params.get("formula_type", "").lower()
            
            # TIME, SPEED & DISTANCE
            if "meeting" in formula_type or "toward" in question.lower():
                d = problem_params.get("distance", 0)
                s1 = problem_params.get("speed_a", problem_params.get("speed_1", 0))
                s2 = problem_params.get("speed_b", problem_params.get("speed_2", 0))
                
                if s1 + s2 == 0:
                    return None, "Invalid: Combined speed is zero"
                
                result = d / (s1 + s2)
                return float(result), f"Meeting time = {d} / ({s1} + {s2}) = {result:.4f}"
            
            elif "overtaking" in formula_type or "catch" in question.lower():
                d = problem_params.get("distance", problem_params.get("lead_distance", 0))
                s1 = problem_params.get("speed_a", problem_params.get("faster_speed", 0))
                s2 = problem_params.get("speed_b", problem_params.get("slower_speed", 0))
                
                if s1 <= s2:
                    return None, "Invalid: Slower can't overtake faster"
                
                result = d / (s1 - s2)
                return float(result), f"Overtaking time = {d} / ({s1} - {s2}) = {result:.4f}"
            
            elif "average_speed" in formula_type:
                s1 = problem_params.get("speed_a", problem_params.get("speed_1", 0))
                s2 = problem_params.get("speed_b", problem_params.get("speed_2", 0))
                
                # Harmonic mean for same distance
                result = (2 * s1 * s2) / (s1 + s2)
                return float(result), f"Harmonic mean = (2 * {s1} * {s2}) / ({s1} + {s2}) = {result:.4f}"
            
            # WORK & TIME
            elif "work" in formula_type or "combined" in formula_type:
                days_a = problem_params.get("days_a", problem_params.get("work_a", 0))
                days_b = problem_params.get("days_b", problem_params.get("work_b", 0))
                
                if days_a == 0 or days_b == 0:
                    return None, "Invalid: Zero work rate"
                
                # Combined work rate: 1/A + 1/B = 1/T
                combined_rate = 1/days_a + 1/days_b
                result = 1 / combined_rate
                return float(result), f"Combined time = 1 / (1/{days_a} + 1/{days_b}) = {result:.4f}"
            
            # PIPES & CISTERNS
            elif "pipe" in formula_type or "cistern" in formula_type:
                fill_a = problem_params.get("fill_time_a", problem_params.get("pipe_a", 0))
                fill_b = problem_params.get("fill_time_b", problem_params.get("pipe_b", 0))
                
                if fill_a == 0 or fill_b == 0:
                    return None, "Invalid: Zero fill rate"
                
                combined_rate = 1/fill_a + 1/fill_b
                result = 1 / combined_rate
                return float(result), f"Combined fill time = 1 / (1/{fill_a} + 1/{fill_b}) = {result:.4f}"
            
            # PROFIT & LOSS
            elif "profit" in formula_type or "loss" in formula_type:
                cost = problem_params.get("cost_price", problem_params.get("cp", 0))
                selling = problem_params.get("selling_price", problem_params.get("sp", 0))
                
                if cost == 0:
                    return None, "Invalid: Cost price is zero"
                
                if selling > cost:
                    profit = selling - cost
                    profit_percent = (profit / cost) * 100
                    return float(profit_percent), f"Profit% = ({profit} / {cost}) * 100 = {profit_percent:.4f}%"
                else:
                    loss = cost - selling
                    loss_percent = (loss / cost) * 100
                    return float(loss_percent), f"Loss% = ({loss} / {cost}) * 100 = {loss_percent:.4f}%"
            
            # AGE PROBLEMS
            elif "age" in formula_type:
                present_a = problem_params.get("present_age_a", 0)
                present_b = problem_params.get("present_age_b", 0)
                years_ago = problem_params.get("years_ago", 0)
                years_hence = problem_params.get("years_hence", 0)
                
                if years_ago > 0:
                    age_a_then = present_a - years_ago
                    age_b_then = present_b - years_ago
                    return float(age_a_then / age_b_then if age_b_then != 0 else 0), f"Ratio {years_ago} years ago"
                
                if years_hence > 0:
                    age_a_future = present_a + years_hence
                    age_b_future = present_b + years_hence
                    return float(age_a_future / age_b_future if age_b_future != 0 else 0), f"Ratio {years_hence} years hence"
            
            # Generic SymPy solver for custom equations
            if "equation" in problem_params:
                eq_str = problem_params["equation"]
                var = problem_params.get("variable", "x")
                
                x = symbols(var)
                equation = sympify(eq_str)
                solution = solve(equation, x)
                
                if solution:
                    result = float(solution[0])
                    return result, f"Solved {eq_str} = {result:.4f}"
            
            # Fallback: extract numbers and make educated guess
            numbers = [float(problem_params[k]) for k in problem_params if isinstance(problem_params.get(k), (int, float))]
            if len(numbers) >= 2:
                # Simple heuristic: if it looks like a rate problem, use harmonic mean
                if any(word in question.lower() for word in ["speed", "rate", "work"]):
                    result = len(numbers) / sum(1/n for n in numbers if n != 0)
                    return float(result), f"Heuristic calculation: {result:.4f}"
            
            return None, f"Unknown formula type: {formula_type}"
            
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
    def extract_numeric_value(text: str) -> Optional[float]:
        """Extract numeric value from text"""
        try:
            # Remove units and extract number
            cleaned = re.sub(r'[^\d.-]', '', str(text))
            return float(cleaned) if cleaned else None
        except:
            return None
        
    @staticmethod
    def extract_parameters_from_question(question: str, category: str) -> Dict:
        """Fallback: Extract parameters directly from question text"""
        import re
        
        params = {}
        
        # Extract all numbers from question
        numbers = re.findall(r'\d+\.?\d*', question)
        numbers = [float(n) for n in numbers]
        
        # Category-specific extraction
        if "work" in category.lower():
            if len(numbers) >= 2:
                params = {
                    "days_a": numbers[0],
                    "days_b": numbers[1],
                    "formula_type": "work_combined"
                }
        
        elif "speed" in category.lower() or "distance" in category.lower():
            if "toward" in question.lower() or "meet" in question.lower():
                if len(numbers) >= 3:
                    params = {
                        "distance": numbers[0],
                        "speed_a": numbers[1],
                        "speed_b": numbers[2],
                        "formula_type": "meeting_time"
                    }
        
        elif "pipe" in category.lower():
            if len(numbers) >= 2:
                params = {
                    "fill_time_a": numbers[0],
                    "fill_time_b": numbers[1],
                    "formula_type": "pipe_combined"
                }
        
        return params

    @staticmethod
    def extract_parameters_from_question(question: str, category: str) -> Dict:
        """Fallback: Extract parameters directly from question text"""
        import re
        
        params = {}
        
        # Extract all numbers from question
        numbers = re.findall(r'\d+\.?\d*', question)
        numbers = [float(n) for n in numbers]
        
        # Category-specific extraction
        if "work" in category.lower():
            if len(numbers) >= 2:
                params = {
                    "days_a": numbers[0],
                    "days_b": numbers[1],
                    "formula_type": "work_combined"
                }
        
        elif "speed" in category.lower() or "distance" in category.lower():
            if "toward" in question.lower() or "meet" in question.lower():
                if len(numbers) >= 3:
                    params = {
                        "distance": numbers[0],
                        "speed_a": numbers[1],
                        "speed_b": numbers[2],
                        "formula_type": "meeting_time"
                    }
        
        elif "pipe" in category.lower():
            if len(numbers) >= 2:
                params = {
                    "fill_time_a": numbers[0],
                    "fill_time_b": numbers[1],
                    "formula_type": "pipe_combined"
                }
        
        return params
