from groq import Groq
import json
from typing import Dict
import os

class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "llama-3.3-70b-versatile"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def execute(self, user_prompt: str, temperature: float = 0.3, json_mode: bool = True) -> Dict:
        """Execute agent task and return structured response"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
                response_format={"type": "json_object"} if json_mode else {"type": "text"}
            )
            
            content = response.choices[0].message.content
            
            if json_mode:
                return json.loads(content)
            return {"response": content}
            
        except json.JSONDecodeError as e:
            return {"error": f"JSON parsing failed: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"error": f"Agent execution failed: {str(e)}"}
