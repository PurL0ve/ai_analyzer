from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import analyzer


load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"

client = OpenAI(
  api_key = api_key,
  base_url = base_url
)

jd = "招聘 Python 后端开发：熟悉 Python，能够使用 FastAPI 开发接口，掌握 MySQL。要求沟通清晰，有团队合作意识。"

messages = [
  {
    "role": "system",
    "content": "只提取 JD 原文明确出现的技术技能，只返回 JSON 对象，固定字段为 skills，值为字符串列表，不加解释。"
  },
  {
    "role": "user",
    "content": jd
  }
]
response = client.chat.completions.create(
  model = "deepseek-flash",
  messages = messages,
  extra_body = {"thinking":{"type":"disabled"}}
)
content = response.choices[0].message.content
try:
  data = json.loads(content)
  if isinstance(data["skills"], list):
    result = analyzer.analyze(
      ["Python","MySQL"],
      required_skills = data["skills"]
    )
    print(result)
    rate = f"{result['rate']:.1%}"
    print(rate)
  else:
    print("skills必须是列表")
except json.JSONDecodeError:
  print("返回格式不正确")
