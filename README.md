# AI Skill Analyzer

## 项目简介

这是一个基于 Python 和 FastAPI 的技能匹配分析项目

## 运行方法

```bash
uvicorn main:app --reload
```

## 接口示例

### POST /analyze

#### 请求示例

```json
{
  "user_skills": ["python", "react"],
  "required_skills": ["python", "react", "vue"]
}
```

#### 返回结果

```json
{
  "matched": ["python", "react"],
  "missing": ["vue"],
  "rate": 0.6666666666666666
}
```





