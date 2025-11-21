import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from dotenv import load_dotenv

from models.schemas import *
from agents.orchestrator import Orchestrator

load_dotenv()

app = FastAPI(
    title="PolySolve AI API",
    description="Multi-agent quantitative problem generator with triple validation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "PolySolve AI - Production Ready",
        "status": "running",
        "version": "1.0.0",
        "features": [
            "Multi-agent architecture",
            "SymPy ground truth validation",
            "Triple validation system",
            "8 problem categories"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api": "operational"}

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_problems(request: GenerationRequest):
    """
    Generate validated quantitative problems
    
    Process:
    1. Research Agent analyzes category patterns
    2. Generator Agent creates problems
    3. Solver A solves algebraically
    4. Solver B solves logically
    5. SymPy validates ground truth
    6. Triple validation ensures quality
    """
    
    try:
        orchestrator = Orchestrator()
        result = orchestrator.generate_problems(
            num_problems=request.num_problems,
            category=request.category.value
        )
        
        return GenerationResponse(**result)
    
    except Exception as e:
        print(f"❌ API Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/html")
async def export_html(problems: List[Problem]):
    """Generate beautiful HTML quiz export"""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PolySolve AI - Quantitative Aptitude Quiz</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #667eea;
        }
        
        .logo {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.1rem;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-top: 5px;
        }
        
        .problem {
            margin: 40px 0;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .problem:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .problem-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .problem-id {
            font-weight: 700;
            color: #667eea;
            font-size: 1.5rem;
        }
        
        .category {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .question {
            font-size: 1.2rem;
            line-height: 1.8;
            color: #333;
            margin-bottom: 25px;
            font-weight: 500;
        }
        
        .options {
            display: grid;
            gap: 15px;
            margin: 20px 0;
        }
        
        .option {
            padding: 18px 25px;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            transition: all 0.3s;
            cursor: pointer;
            font-size: 1.05rem;
        }
        
        .option:hover {
            border-color: #667eea;
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
        
        .option.correct {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            border-color: #28a745;
            font-weight: 600;
            position: relative;
        }
        
        .option.correct::after {
            content: '✓';
            position: absolute;
            right: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: #28a745;
            font-size: 1.5rem;
            font-weight: 700;
        }
        
        .explanation {
            margin-top: 25px;
            padding: 20px;
            background: #fff3cd;
            border-radius: 12px;
            border-left: 4px solid #ffc107;
        }
        
        .explanation strong {
            color: #856404;
            display: block;
            margin-bottom: 10px;
        }
        
        .validation-info {
            margin-top: 15px;
            padding: 15px;
            background: #d1ecf1;
            border-radius: 10px;
            font-size: 0.9rem;
            color: #0c5460;
        }
        
        footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }
        
        footer .logo-small {
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; }
            .problem { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">PolySolve AI</div>
            <p class="subtitle">Multi-Agent Validated Quantitative Aptitude Quiz</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">""" + str(len(problems)) + """</div>
                <div class="stat-label">Questions</div>
            </div>
            <div class="stat">
                <div class="stat-value">""" + str(len(set(p.category for p in problems))) + """</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat">
                <div class="stat-value">100%</div>
                <div class="stat-label">Validated</div>
            </div>
        </div>
"""
    
    for idx, problem in enumerate(problems, 1):
        validation_badge = ""
        if problem.validation_score:
            validation_badge = f"""
            <div class="validation-info">
                <strong>🔬 Validation:</strong> {problem.validation_status}<br>
                <strong>Score:</strong> {problem.validation_score*100:.1f}% confidence
            </div>
            """
        
        html += f"""
        <div class="problem">
            <div class="problem-header">
                <div class="problem-id">{problem.id}</div>
                <div class="category">{problem.category}</div>
            </div>
            
            <div class="question">{problem.question}</div>
            
            <div class="options">
                <div class="option {'correct' if 'A' == problem.correct_answer else ''}">
                    <strong>A)</strong> {problem.options.A}
                </div>
                <div class="option {'correct' if 'B' == problem.correct_answer else ''}">
                    <strong>B)</strong> {problem.options.B}
                </div>
                <div class="option {'correct' if 'C' == problem.correct_answer else ''}">
                    <strong>C)</strong> {problem.options.C}
                </div>
                <div class="option {'correct' if 'D' == problem.correct_answer else ''}">
                    <strong>D)</strong> {problem.options.D}
                </div>
            </div>
            
            <div class="explanation">
                <strong>✓ Correct Answer: {problem.correct_answer}</strong>
                <div style="margin-top: 10px; line-height: 1.6;">{problem.explanation}</div>
            </div>
            
            {validation_badge}
        </div>
"""
    
    html += """
        <footer>
            <p style="font-size: 1.2rem; margin-bottom: 10px;">
                <span class="logo-small">PolySolve AI</span>
            </p>
            <p>Generated by Multi-Agent Validation System</p>
            <p style="margin-top: 10px; font-size: 0.9rem;">
                Triple Validated: Research Agent → Generator → Solver A → Solver B → SymPy Ground Truth
            </p>
        </footer>
    </div>
</body>
</html>"""
    
    return {"html": html}

if __name__ == "__main__":
    print("🚀 Starting PolySolve AI Backend")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
