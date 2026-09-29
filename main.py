import analyzer
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnalyzeRequest(BaseModel):
  user_skills: list[str]
  required_skills: list[str]


@app.post("/analyze")
def analyze_resume(request:AnalyzeRequest):
    result = analyzer.analyze(
      request.user_skills,
      request.required_skills
    )
    return result
       