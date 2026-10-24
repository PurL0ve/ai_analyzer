import json
import analyzer
import os
from dotenv import load_dotenv
from openai import OpenAI,APITimeoutError


def parse_required_skills(content):
    try:
      data = json.loads(content)
      if isinstance(data, dict): 
        skills = data.get("skills")
      else:
        print("返回的JSON必须是对象")
        return None
      if isinstance(skills, list):
        for skill in skills:
          if not isinstance(skill, str):
            print("skills字段必须是字符串列表")
            return None
        return skills
      else:
        print("skills字段缺失或不是列表")
    except json.JSONDecodeError:
      print("返回格式不正确")
    return None
# 解析函数
def extract_required_skills(jd):
    if not jd.strip():
        print("JD不能为空")
        return None
    load_dotenv()

    client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    timeout = 30,
    max_retries = 0
    )
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
    try:
        response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = messages,
        extra_body = {"thinking":{"type":"disabled"}}
    )
    except APITimeoutError:
        print("请求超时，请稍后再试")
        return None
    content = response.choices[0].message.content
    return parse_required_skills(content)
# 提取函数



if __name__ == "__main__":
    content = '{"skills": ["Python", "FastAPI"]}'
    required_skills = parse_required_skills(content)
    if required_skills is not None:
        result = analyzer.analyze(
        ["Python", "MySQL"],
        required_skills=required_skills
        )
        print(result)
    else:
        print("提取失败，停止匹配")

