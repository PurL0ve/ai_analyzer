from database import SessionLocal
from models import AnalysisHistory

db = SessionLocal()

new_history = AnalysisHistory(
  position = "AI应用工程师",
  user_skills = "Python,React",
  required_skills = "Python,FastAPI",
  rate = 0.8
)
db.add(new_history)
db.commit()   # 增加记录

result = db.query(AnalysisHistory).all()
for item in result:
  print(item.position)
  print(item.rate) # 读取记录

history = db.query(AnalysisHistory).filter(AnalysisHistory.id == 2).first()
history.rate = 0.95
db.commit()    #更新记录

history = db.query(AnalysisHistory).filter(AnalysisHistory.id == 2).first()
db.delete(history)
db.commit()    #删除记录


