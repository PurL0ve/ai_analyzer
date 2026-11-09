import main
from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient

client = TestClient(main.app)

request = main.AnalyzeJDRequest(
  jd = "岗位要求熟悉Python",
  user_skills = ["Python"]
)

with patch("main.jd_extractor.extract_required_skills",return_value = None):
  response = client.post("/analyze-jd",json = {"jd": request.jd, "user_skills": request.user_skills})
  print(response.status_code)
  print(response.json())
