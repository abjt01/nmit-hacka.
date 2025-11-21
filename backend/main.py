import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import uvicorn
from dotenv import load_dotenv
import json

from models.schemas import *
from agents.base_agent import BaseAgent
from agents.orchestrator import Orchestrator
from utils.prompts import RESEARCH_AGENT_PROMPT, GENERATOR_AGENT_PROMPT
from utils.config import get_settings

load_dotenv()
settings = get_settings()

app = FastAPI(title="HydraHacks Quant Validator API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
orchestrator = Orchestrator()
current_status = {
    "agents": [],
    "current_problem": None,
    "problems": [],
    "research_summary": ""
}

@app.get("/")
async def root():
    return {"message": "HydraHacks Quant Validator API", "status": "running"}

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_problems(request: GenerationRequest):
    """Main endpoint: Generate validated quantitative problems"""
    
    try:
        # Reset state
        orchestrator.stats = {
            "total_generated": 0,
            "total_valid": 0,
            "total_rejected": 0,
            "solver_agreements": 0,
            "ground_truth_matches": 0,
            "error_breakdown": {}
        }
        
        problems = []
        
        # Step 1: Research phase
        current_status["agents"] = [
            AgentStatus(name="Research Agent", status="running", progress=10, message="Analyzing problem patterns...")
        ]
        
        research_summaries = {}
        research_agent = BaseAgent("Research", RESEARCH_AGENT_PROMPT)
        
        for category in request.categories:
            prompt = f"Research and provide comprehensive guidelines for creating {category} problems."
            result = research_agent.execute(prompt)
            research_summaries[category] = result
        
        current_status["agents"][0].status = "completed"
        current_status["agents"][0].progress = 100
        current_status["research_summary"] = str(research_summaries)
        
        # Step 2: Generation phase
        generator_agent = BaseAgent("Generator", GENERATOR_AGENT_PROMPT)
        
        for category in request.categories:
            for difficulty, count in request.difficulty_distribution.items():
                for i in range(count):
                    current_status["agents"] = [
                        AgentStatus(name="Generator", status="running", progress=30, 
                                  message=f"Generating {difficulty} {category} problem..."),
                        AgentStatus(name="Solver A", status="idle", progress=0),
                        AgentStatus(name="Solver B", status="idle", progress=0),
                        AgentStatus(name="Validator", status="idle", progress=0)
                    ]
                    
                    problem = await orchestrator.generate_problem(
                        generator_agent,
                        category,
                        difficulty,
                        str(research_summaries.get(category, "")),
                        max_retries=3
                    )
                    
                    if problem:
                        problems.append(problem)
                        current_status["problems"] = problems
                        current_status["current_problem"] = problem
                    
                    if len(problems) >= request.num_problems:
                        break
                
                if len(problems) >= request.num_problems:
                    break
            
            if len(problems) >= request.num_problems:
                break
        
        # Final stats
        stats = {
            "total_generated": len(problems),
            "total_valid": orchestrator.stats["total_valid"],
            "total_rejected": orchestrator.stats["total_rejected"],
            "solver_agreement_rate": orchestrator.stats["solver_agreements"] / max(len(problems), 1),
            "ground_truth_accuracy": orchestrator.stats["ground_truth_matches"] / max(len(problems), 1),
            "error_breakdown": orchestrator.stats["error_breakdown"],
            "difficulty_distribution": {
                "EASY": sum(1 for p in problems if p.difficulty == Difficulty.EASY),
                "MEDIUM": sum(1 for p in problems if p.difficulty == Difficulty.MEDIUM),
                "HARD": sum(1 for p in problems if p.difficulty == Difficulty.HARD)
            }
        }
        
        return GenerationResponse(
            problems=problems,
            stats=stats,
            research_summary=str(research_summaries)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status", response_model=SystemStatus)
async def get_status():
    """Get current system status (for real-time updates)"""
    return SystemStatus(
        agents=current_status.get("agents", []),
        current_problem=current_status.get("current_problem"),
        total_generated=len(current_status.get("problems", [])),
        total_valid=orchestrator.stats.get("total_valid", 0)
    )

@app.get("/api/problems")
async def get_problems():
    """Get all generated problems"""
    return {"problems": current_status.get("problems", [])}

@app.post("/api/export/google-form")
async def export_google_form(problems: List[Problem]):
    """Export problems to Google Form (mock for now)"""
    return {
        "message": "Google Form export not implemented yet",
        "form_url": "https://forms.google.com/mock-form-id"
    }

@app.post("/api/export/html")
async def export_html(problems: List[Problem]):
    """Generate HTML quiz"""
    html_content = generate_html_quiz(problems)
    return {"html": html_content}

def generate_html_quiz(problems: List[Problem]) -> str:
    """Generate standalone HTML quiz"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantitative Aptitude Quiz</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
        .problem { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: white; }
        .options { margin: 15px 0; }
        .option { margin: 8px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }
        h2 { color: #2c3e50; }
        .correct { background: #d4edda !important; border-left: 4px solid #28a745; }
    </style>
</head>
<body>
    <h1>🎓 Quantitative Aptitude Quiz</h1>
    <p><strong>Total Questions:</strong> """ + str(len(problems)) + """</p>
    <p><strong>Generated by:</strong> HydraHacks Multi-Agent System</p>
    <hr>
"""
    
    for idx, problem in enumerate(problems, 1):
        html += f"""
    <div class="problem">
        <h2>Question {idx}</h2>
        <p><strong>Category:</strong> {problem.category} | <strong>Difficulty:</strong> {problem.difficulty}</p>
        <p style="font-size: 1.1em; line-height: 1.6;">{problem.question}</p>
        <div class="options">
            <div class="option {'correct' if 'A' == problem.correct_answer else ''}">A) {problem.options.A}</div>
            <div class="option {'correct' if 'B' == problem.correct_answer else ''}">B) {problem.options.B}</div>
            <div class="option {'correct' if 'C' == problem.correct_answer else ''}">C) {problem.options.C}</div>
            <div class="option {'correct' if 'D' == problem.correct_answer else ''}">D) {problem.options.D}</div>
        </div>
        <p><strong>✓ Correct Answer:</strong> {problem.correct_answer}</p>
        <p style="font-size: 0.9em; color: #666;"><strong>Ground Truth:</strong> {problem.ground_truth:.3f} | <strong>Validation Score:</strong> {problem.validation_score*100:.0f}%</p>
    </div>
"""
    
    html += """
    <footer style="margin-top: 40px; padding: 20px; text-align: center; color: #666;">
        <p>Generated by HydraHacks Multi-Agent Validation System</p>
        <p>Validated using SymPy Ground Truth + Dual Solver Agreement</p>
    </footer>
</body>
</html>"""
    return html

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
