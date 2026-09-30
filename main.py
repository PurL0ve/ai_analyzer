import analyzer
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:5173"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
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
       