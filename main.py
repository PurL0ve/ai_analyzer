import analyzer

from fastapi import FastAPI, Depends ,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from models import AnalysisHistory
from schemas import HistoryResponse

from sqlalchemy.exc import SQLAlchemyError
from schemas import ResponseModel

import jd_extractor


app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:5173"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
) # 跨域配置

class AnalyzeRequest(BaseModel):
  position: str
  user_skills: list[str]
  required_skills: list[str] 
# 分析请求模型
class AnalyzeJDRequest(BaseModel):
   jd:str
   user_skills: list[str]
   position: str
@app.post(
      "/analyze",
      response_model = ResponseModel
      )
def analyze_resume(
   request:AnalyzeRequest,
   db = Depends(get_db)
   ):
    try:
      result = analyzer.analyze(
        request.user_skills,
        request.required_skills
    ) 
    except Exception:
      raise HTTPException(
          status_code = 500,
          detail = "分析服务异常"
       )
    history = AnalysisHistory(
       position = request.position,
       user_skills = ",".join(request.user_skills),
       required_skills = ",".join(request.required_skills),
       rate = result["rate"],
       source = "manual"
    )
    try: 
        db.add(history)
        db.commit()
    except SQLAlchemyError:
       db.rollback()
       raise HTTPException(
          status_code = 500,
          detail = "数据库保存失败"
       )
    return ResponseModel(
       code = 200,
       message = "success",
       data = result
    )
# 分析简历接口

@app.get(
   "/history",
   response_model = ResponseModel
)
def get_history(db = Depends(get_db)):
   result = db.query(AnalysisHistory).all()
   histories = [
      HistoryResponse.model_validate(item)
      for item in result
   ]
   return ResponseModel(
      code = 200,
      message = "success",
      data = histories
   )
# 获取分析历史接口

@app.post(
      "/analyze-jd",
      response_model = ResponseModel
      )
def analyze_jd(
   request:AnalyzeJDRequest,
   db = Depends(get_db)
   ):

   if request.jd.strip() == "":
      raise HTTPException(
         status_code = 400,
         detail = "JD不能为空"
      )
   if request.position.strip() == "":
      raise HTTPException(
         status_code = 400,
         detail = "岗位名称不能为空"
      )
   required_skills = jd_extractor.extract_required_skills(request.jd)
   if required_skills is None:
      raise HTTPException(
         status_code = 502,
         detail = "JD技能提取失败"
      )
   result = analyzer.analyze(request.user_skills,required_skills)

   history = AnalysisHistory(
      position = request.position,
      user_skills = ",".join(request.user_skills),
      required_skills = ",".join(required_skills),
      rate = result["rate"],
      source = "jd"
   )

   try:
      db.add(history)
      db.commit()
   except SQLAlchemyError:
      db.rollback()
      raise HTTPException(
         status_code = 500,
         detail = "数据库保存失败"
      )
   return ResponseModel(
      code = 200,
      message = "success",
      data = result
   )
