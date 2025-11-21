from typing import List, Dict
import json
import asyncio

from agents.base_agent import BaseAgent
from validators.math_validator import MathValidator
from validators.rule_validator import RuleValidator
from models.schemas import Problem, ValidationStatus, SolverResult
from utils.prompts import SOLVER_A_PROMPT, SOLVER_B_PROMPT

class Orchestrator:
    def __init__(self):
        self.solver_a = BaseAgent("Solver_A", SOLVER_A_PROMPT)
        self.solver_b = BaseAgent("Solver_B", SOLVER_B_PROMPT)
        self.math_validator = MathValidator()
        self.rule_validator = RuleValidator()
        
        self.stats = {
            "total_generated": 0,
            "total_valid": 0,
            "total_rejected": 0,
            "solver_agreements": 0,
            "ground_truth_matches": 0,
            "error_breakdown": {}
        }
    
    async def generate_problem(
        self,
        generator_agent: BaseAgent,
        category: str,
        difficulty: str,
        research_summary: str,
        max_retries: int = 3
    ) -> Problem:
        """Generate and validate a single problem with retry logic"""
        
        for attempt in range(1, max_retries + 1):
            # Generate problem
            gen_prompt = f"""Generate a {difficulty} difficulty {category} word problem.

Research Context: {research_summary[:500]}

Create a story-based quantitative problem with:
1. Clear scenario (trains, workers, pipes, etc.)
2. Numerical values that are realistic
3. 4 MCQ options (A, B, C, D)
4. Include parameters for ground truth calculation

Output as JSON with keys: question, parameters, options, correct_answer, expected_value"""
            
            problem_data = generator_agent.execute(gen_prompt)
            
            if "error" in problem_data:
                continue
            
            # Rule validation
            is_valid, errors = self.rule_validator.validate_problem(problem_data)
            if not is_valid:
                self.stats["total_rejected"] += 1
                self.stats["error_breakdown"]["rule_violation"] = \
                    self.stats["error_breakdown"].get("rule_violation", 0) + 1
                continue
            
            # Calculate ground truth
            params = problem_data.get("parameters", {})
            ground_truth, calc_explanation = self.math_validator.calculate_ground_truth(
                params, category
            )
            
            if ground_truth is None:
                self.stats["total_rejected"] += 1
                self.stats["error_breakdown"]["calculation_failed"] = \
                    self.stats["error_breakdown"].get("calculation_failed", 0) + 1
                continue
            
            # Solve with both agents
            question = problem_data.get("question", "")
            options = problem_data.get("options", {})
            
            solver_a_result = self._solve_with_agent(
                self.solver_a,
                question,
                options
            )
            
            solver_b_result = self._solve_with_agent(
                self.solver_b,
                question,
                options
            )
            
            # Validate solver results
            validation_result = self._validate_solvers(
                solver_a_result,
                solver_b_result,
                ground_truth
            )
            
            if validation_result["is_valid"]:
                self.stats["total_valid"] += 1
                self.stats["total_generated"] += 1
                
                if validation_result["solvers_agree"]:
                    self.stats["solver_agreements"] += 1
                
                if validation_result["matches_ground_truth"]:
                    self.stats["ground_truth_matches"] += 1
                
                # Create Problem object
                from models.schemas import MCQOptions
                problem = Problem(
                    id=f"{category[:3].upper()}_{self.stats['total_generated']:03d}",
                    category=category,
                    difficulty=difficulty,
                    question=question,
                    options=MCQOptions(**options),
                    correct_answer=problem_data.get("correct_answer", "A"),
                    ground_truth=ground_truth,
                    solver_a_result=solver_a_result,
                    solver_b_result=solver_b_result,
                    validation_status=ValidationStatus.VALID,
                    validation_score=validation_result["score"],
                    attempts=attempt
                )
                
                return problem
            else:
                self.stats["total_rejected"] += 1
                error_type = validation_result.get("error_reason", "solver_disagreement")
                self.stats["error_breakdown"][error_type] = \
                    self.stats["error_breakdown"].get(error_type, 0) + 1
        
        # All retries exhausted
        return None
    
    def _solve_with_agent(
        self,
        agent: BaseAgent,
        question: str,
        options: Dict
    ) -> SolverResult:
        """Execute solver agent and parse result"""
        
        prompt = f"""Solve this problem:

PROBLEM: {question}
OPTIONS: {json.dumps(options)}

Provide step-by-step solution and select the correct option.
Output as JSON with keys: reasoning, calculated_value, selected_option, confidence, approach"""
        
        result = agent.execute(prompt)
        
        if "error" in result:
            return SolverResult(
                answer=0.0,
                confidence=0.0,
                reasoning="Solver error",
                approach=agent.name
            )
        
        return SolverResult(
            answer=result.get("calculated_value", result.get("answer", 0.0)),
            confidence=result.get("confidence", 0.5),
            reasoning=result.get("reasoning", ""),
            approach=result.get("approach", agent.name)
        )
    
    def _validate_solvers(
        self,
        solver_a: SolverResult,
        solver_b: SolverResult,
        ground_truth: float
    ) -> Dict:
        """Compare solver results with ground truth using confidence weighting"""
        
        # Calculate distances from ground truth
        a_error = abs(solver_a.answer - ground_truth) / (abs(ground_truth) + 0.001)
        b_error = abs(solver_b.answer - ground_truth) / (abs(ground_truth) + 0.001)
        
        # Confidence-weighted scores
        a_score = solver_a.confidence * max(0, 1 - a_error)
        b_score = solver_b.confidence * max(0, 1 - b_error)
        
        # Check agreement
        solvers_agree = abs(solver_a.answer - solver_b.answer) / (abs(ground_truth) + 0.001) < 0.1
        
        # Check ground truth match
        a_matches = self.math_validator.validate_answer(solver_a.answer, ground_truth, tolerance=0.05)
        b_matches = self.math_validator.validate_answer(solver_b.answer, ground_truth, tolerance=0.05)
        
        # Validation logic
        avg_score = (a_score + b_score) / 2
        
        is_valid = (
            avg_score > 0.75 and  # High confidence weighted score
            (a_matches or b_matches) and  # At least one matches ground truth
            solvers_agree  # Solvers agree with each other
        )
        
        error_reason = None
        if not is_valid:
            if not solvers_agree:
                error_reason = "solver_disagreement"
            elif not (a_matches or b_matches):
                error_reason = "ground_truth_mismatch"
            else:
                error_reason = "low_confidence"
        
        return {
            "is_valid": is_valid,
            "score": avg_score,
            "solvers_agree": solvers_agree,
            "matches_ground_truth": a_matches or b_matches,
            "error_reason": error_reason
        }
