import json
import analyzer
import os
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APITimeoutError,
    APIConnectionError,
    AuthenticationError,
)

# 解析函数
def parse_required_skills(content):
    if not isinstance(content, str):
        print("模型返回内容必须是字符串")
        return None
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
          else:
             skill = skill.strip()
             if skill == "":
                print("skills字段中不能包含空白技能")
                return None
        return skills
      else:
        print("skills字段缺失或不是列表")
    except json.JSONDecodeError:
      print("返回格式不正确")
    return None

# 提取函数
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
    except APIConnectionError:
        print("模型服务连接失败，请检查网络")
        return None
    except AuthenticationError:
        print("模型服务认证失败，请检查本地密钥配置")
        return None
    content = response.choices[0].message.content
    return parse_required_skills(content)


def parse_jd_sections(content):
    if not isinstance(content,str):
      print("模型返回内容必须是字符串")
      return None
    try:
      data = json.loads(content)
      if isinstance(data, dict):
        responsibilities = data.get("responsibilities")
        required_skills = data.get("required_skills")
        preferred_skills = data.get("preferred_skills") 
      else: 
         print("返回的JSON必须是对象")
         return None
      if responsibilities is None or required_skills is None or preferred_skills is None:
         print("返回的JSON必须包含responsibilities、required_skills和preferred_skills字段")
         return None
      if isinstance(responsibilities,list) and isinstance(required_skills,list) and isinstance(preferred_skills,list):
        for item in responsibilities:
            if not isinstance(item,str):
                print("responsibilities字段必须是字符串列表")
                return None
            if item.strip() == "":
                print("responsibilities字段中的字符串不能为空")
                return None
        for skills in required_skills + preferred_skills:
            if not isinstance(skills,str):
                print("required_skills和preferred_skills字段必须是字符串列表")
                return None
            if skills.strip() == "":
                print("required_skills和preferred_skills字段中的字符串不能为空")
                return None
        return {
            "responsibilities": responsibilities,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills
         }
      else:
        print("responsibilities、required_skills和preferred_skills字段必须是列表")
        return None
    except json.JSONDecodeError:
        print("返回格式不正确")
        return None

def analyze_jd_response(response, user_skills):
    sections = extract_jd_sections_from_response(response)
    if sections is not None:
      result = analyzer.analyze(
          user_skills=user_skills,
          required_skills=sections["required_skills"]
      )
      return {
          "sections": sections,
          "analysis": result
      }
    else:
      return None

def extract_jd_sections_from_response(response):
   content = response.choices[0].message.content
   return parse_jd_sections(content)

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

