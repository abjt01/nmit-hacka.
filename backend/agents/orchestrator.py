from typing import List, Dict, Optional
import json
import traceback

from agents.research_agent import ResearchAgent
from agents.generator_agent import GeneratorAgent
from agents.solver_agent import SolverAgentA, SolverAgentB
from validators.math_validator import MathValidator
from validators.rule_validator import RuleValidator
from models.schemas import Problem, MCQOptions, SolverResult

class Orchestrator:
    """
    Production orchestrator coordinating all agents
    
    Architecture:
    1. Research Agent → Learns problem patterns (1 call)
    2. Generator Agent → Creates problems (N calls)
    3. Solver A → Solves algebraically (N calls)
    4. Solver B → Solves logically (N calls)
    5. Math Validator → SymPy ground truth (0 calls - local)
    6. Final validation and problem assembly
    """
    
    def __init__(self):
        # Initialize all agents
        self.research_agent = ResearchAgent()
        self.generator_agent = GeneratorAgent()
        self.solver_a = SolverAgentA()
        self.solver_b = SolverAgentB()
        
        # Initialize validators
        self.math_validator = MathValidator()
        self.rule_validator = RuleValidator()
        
        # Stats tracking
        self.api_call_count = 0
        self.stats = {
            "total_generated": 0,
            "total_valid": 0,
            "solver_agreements": 0,
            "ground_truth_matches": 0,
            "validation_failures": {}
        }
    
    def generate_problems(self, num_problems: int, category: str) -> Dict:
        """Main workflow"""
        
        print(f"\n🚀 PolySolve AI - Starting generation")
        print(f"   Target: {num_problems} problems")
        print(f"   Category: {category}\n")
        
        problems = []
        
        # PHASE 1: Research
        research_data = self._research_phase(category)
        
        # PHASE 2: Generate & Validate
        for i in range(num_problems):
            print(f"\n{'='*60}")
            print(f"📝 Generating Problem {i+1}/{num_problems}")
            print(f"{'='*60}")
            
            problem = self._generate_and_validate_problem(
                problem_num=i+1,
                category=category,
                research_data=research_data
            )
            
            if problem:
                problems.append(problem)
                print(f"✅ Problem {i+1} successfully validated and added")
            else:
                print(f"❌ Problem {i+1} failed validation - skipped")
        
        # PHASE 3: Final stats
        print(f"\n{'='*60}")
        print(f"🎉 Generation Complete!")
        print(f"{'='*60}")
        print(f"✓ Successfully generated: {len(problems)}/{num_problems}")
        print(f"✓ Total API calls: {self.api_call_count}")
        print(f"✓ Efficiency: {len(problems)}/{self.api_call_count} problems per call")
        print(f"✓ Solver agreement rate: {self.stats['solver_agreements']}/{len(problems)}")
        print(f"{'='*60}\n")
        
        return {
            "problems": problems,
            "stats": {
                "total_generated": len(problems),
                "total_api_calls": self.api_call_count,
                "api_efficiency": f"{len(problems)}/{self.api_call_count}",
                "solver_agreement_rate": self.stats['solver_agreements'] / max(len(problems), 1),
                "ground_truth_matches": self.stats['ground_truth_matches'],
                "validation_failures": self.stats['validation_failures']
            },
            "total_api_calls": self.api_call_count
        }
    
    def _research_phase(self, category: str) -> str:
        """Phase 1: Research problem patterns"""
        
        print(f"🔬 Phase 1: Research Agent analyzing '{category}'...")
        
        research_result = self.research_agent.research_category(category)
        self.api_call_count += 1
        
        if "error" in research_result:
            print(f"   ⚠️  Research returned error, using fallback knowledge")
            return json.dumps({"category": category, "status": "fallback"})
        
        print(f"   ✓ Research complete (API calls: {self.api_call_count})")
        return json.dumps(research_result)
    
    def _generate_and_validate_problem(
        self,
        problem_num: int,
        category: str,
        research_data: str
    ) -> Optional[Problem]:
        """Phase 2: Generate + Triple Validation (Generator → Solver A → Solver B → SymPy)"""
        
        try:
            # STEP 1: Generate problem
            print(f"   🎲 Generator Agent creating problem...")
            problem_data = self.generator_agent.generate_problem(
                category=category,
                research_data=research_data,
                problem_num=problem_num
            )
            self.api_call_count += 1
            
            if "error" in problem_data or not problem_data.get("question"):
                print(f"   ❌ Generation failed")
                self.stats['validation_failures']['generation_error'] = \
                    self.stats['validation_failures'].get('generation_error', 0) + 1
                return None
            
            print(f"   ✓ Problem generated")
            
            # STEP 2: Solve with Solver A
            print(f"   🔢 Solver A (Algebraic) analyzing...")
            solver_a_result = self.solver_a.solve(
                question=problem_data['question'],
                options=problem_data['options']
            )
            self.api_call_count += 1
            
            if "error" in solver_a_result:
                print(f"   ❌ Solver A failed")
                return None
            
            print(f"   ✓ Solver A: Option {solver_a_result.get('selected_option')} "
                  f"(confidence: {solver_a_result.get('confidence', 0)*100:.0f}%)")
            
            # STEP 3: Solve with Solver B
            print(f"   💭 Solver B (Logical) analyzing...")
            solver_b_result = self.solver_b.solve(
                question=problem_data['question'],
                options=problem_data['options']
            )
            self.api_call_count += 1
            
            if "error" in solver_b_result:
                print(f"   ❌ Solver B failed")
                return None
            
            print(f"   ✓ Solver B: Option {solver_b_result.get('selected_option')} "
                  f"(confidence: {solver_b_result.get('confidence', 0)*100:.0f}%)")
            
            # STEP 4: SymPy Ground Truth Validation
            print(f"   🧮 SymPy calculating ground truth...")
            ground_truth, explanation = self.math_validator.calculate_ground_truth(
                problem_params=problem_data.get('parameters', {}),
                question=problem_data['question']
            )
            
            if ground_truth is not None:
                print(f"   ✓ Ground truth: {ground_truth:.4f}")
                print(f"      {explanation}")
            else:
                print(f"   ⚠️  Ground truth calculation not available: {explanation}")
                # Continue anyway if solvers agree
            
            # STEP 5: Triple Validation
            print(f"   ⚖️  Validating agreement...")
            validation_result = self._triple_validate(
                generator_answer=problem_data.get('correct_answer'),
                solver_a_result=solver_a_result,
                solver_b_result=solver_b_result,
                ground_truth=ground_truth,
                options=problem_data['options']
            )
            
            if not validation_result['is_valid']:
                print(f"   ❌ Validation failed: {validation_result.get('reason')}")
                self.stats['validation_failures'][validation_result.get('reason', 'unknown')] = \
                    self.stats['validation_failures'].get(validation_result.get('reason', 'unknown'), 0) + 1
                return None
            
            print(f"   ✅ Triple validation passed!")
            
            # Update stats
            self.stats['total_valid'] += 1
            if validation_result['solvers_agree']:
                self.stats['solver_agreements'] += 1
            if validation_result['matches_ground_truth']:
                self.stats['ground_truth_matches'] += 1
            
            # STEP 6: Create Problem object
            problem = Problem(
                id=f"Q{problem_num:03d}",
                category=category,
                question=problem_data['question'],
                options=MCQOptions(**problem_data['options']),
                correct_answer=problem_data['correct_answer'],
                explanation=problem_data.get('solution_steps', ''),
                validation_status=f"Valid - {validation_result['validation_method']}",
                solver_a_result=SolverResult(
                    answer=solver_a_result.get('calculated_value', 0),
                    confidence=solver_a_result.get('confidence', 0),
                    reasoning=solver_a_result.get('reasoning', ''),
                    approach="algebraic"
                ),
                solver_b_result=SolverResult(
                    answer=solver_b_result.get('calculated_value', 0),
                    confidence=solver_b_result.get('confidence', 0),
                    reasoning=solver_b_result.get('reasoning', ''),
                    approach="logical"
                ),
                ground_truth=ground_truth if ground_truth else solver_a_result.get('calculated_value', 0),
                validation_score=validation_result['score']
            )
            
            return problem
            
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            traceback.print_exc()
            return None
    
    def _triple_validate(
        self,
        generator_answer: str,
        solver_a_result: Dict,
        solver_b_result: Dict,
        ground_truth: Optional[float],
        options: Dict
    ) -> Dict:
        """
        Triple validation system:
        1. Do both solvers agree?
        2. Does generator match solvers?
        3. Does ground truth confirm?
        """
        
        solver_a_option = solver_a_result.get('selected_option')
        solver_b_option = solver_b_result.get('selected_option')
        solver_a_value = solver_a_result.get('calculated_value', 0)
        solver_b_value = solver_b_result.get('calculated_value', 0)
        solver_a_conf = solver_a_result.get('confidence', 0)
        solver_b_conf = solver_b_result.get('confidence', 0)
        
        # Check 1: Solver agreement
        solvers_agree = (solver_a_option == solver_b_option)
        
        # Check 2: Generator vs Solvers
        generator_matches_solvers = (generator_answer == solver_a_option == solver_b_option)
        
        # Check 3: Ground truth validation
        matches_ground_truth = False
        if ground_truth is not None:
            # Extract numeric values from options
            correct_option_text = options.get(generator_answer, "")
            correct_value = self.math_validator.extract_numeric_value(correct_option_text)
            
            if correct_value is not None:
                matches_ground_truth = self.math_validator.validate_answer(
                    correct_value, ground_truth, tolerance=0.05
                )
        
        # Validation Logic (Priority order):
        
        # BEST: All three agree
        if generator_matches_solvers and (matches_ground_truth or ground_truth is None):
            return {
                "is_valid": True,
                "solvers_agree": True,
                "matches_ground_truth": matches_ground_truth,
                "score": (solver_a_conf + solver_b_conf) / 2,
                "validation_method": "Triple agreement (Generator + Solver A + Solver B" + 
                                    (" + SymPy)" if ground_truth else ")"),
                "reason": None
            }
        
        # GOOD: Both solvers agree (even if generator differs)
        if solvers_agree and solver_a_conf > 0.7 and solver_b_conf > 0.7:
            return {
                "is_valid": True,
                "solvers_agree": True,
                "matches_ground_truth": matches_ground_truth,
                "score": (solver_a_conf + solver_b_conf) / 2,
                "validation_method": "Solver consensus",
                "reason": None
            }
        
        # ACCEPTABLE: Ground truth confirms (even if solvers disagree)
        if matches_ground_truth and ground_truth is not None:
            return {
                "is_valid": True,
                "solvers_agree": False,
                "matches_ground_truth": True,
                "score": 0.85,
                "validation_method": "SymPy ground truth",
                "reason": None
            }
        
        # REJECT: No agreement
        if not solvers_agree:
            reason = f"Solver disagreement (A:{solver_a_option} vs B:{solver_b_option})"
        elif not matches_ground_truth and ground_truth is not None:
            reason = "Ground truth mismatch"
        else:
            reason = "Low confidence"
        
        return {
            "is_valid": False,
            "solvers_agree": solvers_agree,
            "matches_ground_truth": matches_ground_truth,
            "score": 0.0,
            "validation_method": "Failed",
            "reason": reason
        }