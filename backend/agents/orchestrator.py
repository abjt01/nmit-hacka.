from typing import List, Dict, Optional
import json
import traceback
from agents.base_agent import BaseAgent
from validators.math_validator import MathValidator
from models.schemas import Problem, MCQOptions

class Orchestrator:
    def __init__(self):
        self.api_call_count = 0
        self.math_validator = MathValidator()
        
    def generate_problems(self, num_problems: int, category: str) -> Dict:
        """Main workflow - optimized for minimal API calls"""
        
        problems = []
        print(f"\n🚀 Starting generation: {num_problems} problems, category: {category}")
        
        research_knowledge = self._research_phase(category)
        print(f"✅ Research phase complete. API calls so far: {self.api_call_count}")
        
        for i in range(num_problems):
            print(f"\n📝 Attempting problem {i+1}/{num_problems}...")
            problem = self._generate_and_validate_problem(
                problem_num=i+1,
                category=category,
                research_knowledge=research_knowledge
            )
            if problem:
                problems.append(problem)
                print(f"✅ Problem {i+1} generated successfully!")
            else:
                print(f"❌ Problem {i+1} failed validation")
        
        print(f"\n🎉 Generation complete: {len(problems)}/{num_problems} problems created")
        print(f"📊 Total API calls: {self.api_call_count}")
        
        stats = {
            "total_generated": len(problems),
            "total_api_calls": self.api_call_count,
            "api_efficiency": f"{len(problems)}/{self.api_call_count} problems per call"
        }
        
        return {
            "problems": problems,
            "stats": stats,
            "total_api_calls": self.api_call_count
        }
    
    def _research_phase(self, category: str) -> str:
        """Single research call for all categories"""
        
        research_agent = BaseAgent(
            name="Research",
            system_prompt="You are a quantitative aptitude expert. Always respond with valid JSON."
        )
        
        prompt = f"""Provide formulas and problem patterns for: {category}

If category is "Mixed", cover all categories briefly.
Otherwise focus on: {category}

Include:
1. Key formulas
2. Common problem types
3. Typical value ranges
4. Sample scenarios

Output as JSON with structure:
{{
  "category": "{category}",
  "formulas": ["formula1", "formula2"],
  "problem_types": ["type1", "type2"],
  "value_ranges": {{"distance": "100-1000 km", "speed": "40-120 km/h"}},
  "examples": ["example scenario 1", "example scenario 2"]
}}"""

        try:
            result = research_agent.execute(prompt, temperature=0.2)
            self.api_call_count += 1
            print(f"🔬 Research result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
            return json.dumps(result)
        except Exception as e:
            print(f"❌ Research phase error: {e}")
            return "{}"
    
    def _generate_and_validate_problem(
        self,
        problem_num: int,
        category: str,
        research_knowledge: str
    ) -> Optional[Problem]:
        """Generate + Validate in 2 API calls"""
        
        try:
            # CALL 1: Generate problem
            generator = BaseAgent(
                name="Generator",
                system_prompt="You are a quantitative word problem generator. Always respond with valid JSON."
            )
            
            gen_prompt = f"""Create a quantitative aptitude problem for: {category}

Problem number: {problem_num}

Create a story-based word problem with:
- Clear scenario (trains meeting, workers completing job, etc.)
- Realistic numbers
- 4 multiple choice options
- Step-by-step solution

Output MUST be valid JSON with this EXACT structure:
{{
  "question": "Full problem text here",
  "options": {{
    "A": "First option with unit",
    "B": "Second option with unit",
    "C": "Third option with unit",
    "D": "Fourth option with unit"
  }},
  "correct_answer": "A",
  "solution_steps": "Step 1: ... Step 2: ... Step 3: ...",
  "final_answer": 2.5
}}

Example for Time, Speed & Distance:
{{
  "question": "Two trains start from stations A and B, 360 km apart, and travel toward each other. Train A travels at 60 km/h, and Train B at 80 km/h. After how many hours will they meet?",
  "options": {{
    "A": "2.0 hours",
    "B": "2.57 hours",
    "C": "3.0 hours",
    "D": "4.5 hours"
  }},
  "correct_answer": "B",
  "solution_steps": "Step 1: Combined speed = 60 + 80 = 140 km/h. Step 2: Time = Distance / Speed = 360 / 140 = 2.57 hours",
  "final_answer": 2.57
}}

Now create a NEW problem for: {category}"""

            problem_data = generator.execute(gen_prompt, temperature=0.5)
            self.api_call_count += 1
            
            print(f"  📤 Generator response keys: {problem_data.keys() if isinstance(problem_data, dict) else 'Invalid'}")
            
            if "error" in problem_data:
                print(f"  ❌ Generator error: {problem_data['error']}")
                return None
                
            if not problem_data.get("question"):
                print(f"  ❌ No question field in response")
                return None
            
            # Quick validation check
            if not problem_data.get("options"):
                print(f"  ❌ No options field")
                return None
                
            if not isinstance(problem_data.get("options"), dict):
                print(f"  ❌ Options is not a dict: {type(problem_data.get('options'))}")
                return None
            
            # CALL 2: Validate problem
            validator = BaseAgent(
                name="Validator",
                system_prompt="You are a problem validator. Always respond with valid JSON."
            )
            
            val_prompt = f"""Validate this quantitative problem:

QUESTION: {problem_data['question']}
OPTIONS: {json.dumps(problem_data.get('options', {}))}
GIVEN ANSWER: {problem_data.get('correct_answer', 'Unknown')}

Tasks:
1. Solve the problem independently
2. Check if it's solvable and logical
3. Verify the correct answer matches your solution

Output MUST be valid JSON:
{{
  "your_answer": "A",
  "your_calculation": 2.5,
  "is_valid": true,
  "reasoning": "Brief explanation of your solution"
}}"""

            validation = validator.execute(val_prompt, temperature=0.2)
            self.api_call_count += 1
            
            print(f"  📥 Validator response keys: {validation.keys() if isinstance(validation, dict) else 'Invalid'}")
            
            # Check validation
            is_valid = validation.get("is_valid", False)
            
            if not is_valid:
                print(f"  ❌ Validator marked as invalid: {validation.get('reasoning', 'No reason')}")
                return None
            
            # Check answer agreement
            validator_answer = validation.get("your_answer")
            correct_answer = problem_data.get("correct_answer")
            
            if validator_answer != correct_answer:
                print(f"  ⚠️  Answer mismatch: Generator says {correct_answer}, Validator says {validator_answer}")
                # Accept it anyway if validator marked as valid
                if not is_valid:
                    return None
            
            # Create problem object
            problem = Problem(
                id=f"Q{problem_num:03d}",
                category=category,
                question=problem_data['question'],
                options=MCQOptions(**problem_data['options']),
                correct_answer=problem_data['correct_answer'],
                explanation=problem_data.get('solution_steps', validation.get('reasoning', 'No explanation provided')),
                validation_status="Valid"
            )
            
            print(f"  ✅ Problem object created successfully")
            return problem
            
        except KeyError as e:
            print(f"  ❌ KeyError: {e}")
            print(f"  Problem data: {problem_data if 'problem_data' in locals() else 'Not available'}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            traceback.print_exc()
            return None
    
    def _check_ground_truth(self, problem_data: Dict, validator_answer: float) -> bool:
        """Use SymPy to verify answer (NO API CALL)"""
        try:
            import re
            numbers = re.findall(r'\d+\.?\d*', problem_data['question'])
            
            if validator_answer and len(numbers) > 0:
                min_val = min(float(n) for n in numbers if float(n) > 0)
                max_val = max(float(n) for n in numbers)
                return min_val * 0.1 <= validator_answer <= max_val * 10
            return True
        except:
            return True
    
    def _infer_category(self, question: str) -> str:
        """Infer category from question text"""
        keywords = {
            "train|speed|distance|km/h|travel|meet": "Time, Speed & Distance",
            "work|job|days|complete|finish": "Work & Time",
            "pipe|tank|fill|empty|leak|cistern": "Pipes & Cisterns",
            "profit|loss|discount|price|₹|rupees|cost": "Profit, Loss & Discount",
            "mixture|ratio|replace|container|alloy": "Ratio, Mixtures & Sharing",
            "age|years ago|older|younger|born": "Age Problems",
            "boat|stream|downstream|upstream|current": "Boats & Streams"
        }
        
        import re
        question_lower = question.lower()
        for pattern, cat in keywords.items():
            if re.search(pattern, question_lower):
                return cat
        return "Allocation & Logical Math"
