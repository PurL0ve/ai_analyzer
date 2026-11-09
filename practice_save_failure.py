from unittest.mock import Mock
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from main import AnalyzeRequest, analyze_resume

# 模拟数据库会话，提交时故意报错，不访问真实数据库
db = Mock()
db.commit.side_effect = SQLAlchemyError("练习：提交失败")

request = AnalyzeRequest(
    position="Python开发",
    user_skills=["python"],
    required_skills=["python", "sql"],
)

try:
    analyze_resume(request, db=db)
except HTTPException as error:
    print("异常状态码：", error.status_code)
    print("异常信息：", error.detail)
    print("回滚调用次数：", db.rollback.call_count)
else:
    print("检查失败：保存失败后没有抛出接口异常")