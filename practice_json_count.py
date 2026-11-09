import json
def count_skills(content):
  try:
    data = json.loads(content)
    if isinstance(data["skills"], list):
      return len(data["skills"])
    else:
      print("skills必须是列表")
  except json.JSONDecodeError:
    print("返回格式不正确")


content1 = '{"skills": ["Python", "MySQL", "FastAPI"]}'
print(count_skills(content1))
content2 = '{"skills": "Python"}'
print(count_skills(content2))
content3 = '这不是JSON'
print(count_skills(content3))
