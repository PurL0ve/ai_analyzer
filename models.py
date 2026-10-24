from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class AnalysisHistory(Base):
  __tablename__ = 'analysis_history'
  id = Column(Integer,primary_key=True,autoincrement=True)
  position = Column(String(100))
  user_skills = Column(String(500))
  required_skills = Column(String(500)) 
  rate = Column(Float)
  created_time = Column(DateTime,default=datetime.now)
  source = Column(String(20),nullable=True)