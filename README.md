# AI Skill Analyzer

## 项目简介

这是一个基于 Python 和 FastAPI 的技能匹配分析系统。通过分析用户技能和岗位需求,计算技能匹配程度,并保存分析历史记录。

## 技术栈
Backend:
- Python 
- FastAPI 
- SQLAlchemy 
- MySQL 
- Pydantic 

## 项目结构

main.py
- FastAPI接口

analyzer.py
- 技能匹配核心逻辑

database.py
- 数据库连接和Session管理

models.py
- ORM模型

schemas.py
- 数据校验模型

sql/init.sql
- 数据库初始化脚本

## 运行方法

```bash
uvicorn main:app --reload
```

## 接口示例

### POST /analyze

#### 请求示例

```json
{
  "position":"AI应用工程师",
  "user_skills":[
    "python",
    "react"
  ],
  "required_skills":[
    "python",
    "react",
    "vue"
  ]
}
```

#### 返回结果

```json
{
  "code":200,
  "message":"success",
  "data":{
    "matched":[
      "python",
      "react"
    ],
    "missing":[
      "vue"
    ],
    "rate":0.666
  }
}
```
## 当前进度

已完成：

- FastAPI连接MySQL
- SQLAlchemy ORM接入
- 分析记录保存
- 历史记录查询
- 数据库初始化脚本
- 统一响应格式




