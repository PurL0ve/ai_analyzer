from pydantic import BaseModel
from datetime import datetime
from typing import Any

class HistoryResponse(BaseModel):
  id: int
  position: str
  user_skills: str
  required_skills: str
  rate: float
  created_time: datetime | None
  class Config:
    from_attributes = True


class ResponseModel(BaseModel):
  code: int
  message: str
  data: Any