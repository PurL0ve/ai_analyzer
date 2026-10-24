import json
import analyzer
import os # 导入os模块，用于获取环境变量
from dotenv import load_dotenv  # 导入load_dotenv函数，用于加载环境变量
from openai import OpenAI,APITimeoutError 




def evaluate_prompt(system_prompt,jd):
  if not jd.strip():
    print("JD不能为空")
    return None
  load_dotenv()

  client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
  )
  messages = [
    {
      "role": "system",
      "content": system_prompt
    },
    {
      "role": "user",
      "content": jd
    }
  ]
  try:
    # 调用模型
    response = client.chat.completions.create(
      model = "deepseek-flash",
      messages = messages,
      extra_body = {"thinking":{"type":"disabled"}}
    ) 
  except APITimeoutError:
    print("请求超时，请稍后再试")
    return None
  content = response.choices[0].message.content
  return content

original_prompt = "只提取 JD 原文明确出现的技术技能，只返回 JSON 对象，固定字段为 skills，值为字符串列表，不加解释。"

jd = """岗位名称：大模型应用产品经理
岗位职责：1. 负责大模型应用产品的需求调研、场景拆解和产品规划，输出PRD及原型；2. 与算法、研发、设计、运营团队协作，推动RAG、Agent、知识库等能力落地；3. 设计产品评测方案与效果指标，基于用户反馈和数据分析持续迭代；4. 跟踪行业趋势与竞品动态，沉淀产品方法论和最佳实践。
任职要求：1. 本科及以上学历，3年以上产品经验，有AI/大模型应用落地经验优先；2. 熟悉Prompt Engineering、RAG、Agent、向量数据库等基本概念；3. 具备较强的需求分析、跨团队沟通和项目推进能力；4. 能使用SQL/Excel进行基础数据分析，有数据驱动意识；5. 有B端或SaaS产品经验优先。"""

revised_prompt = "提取JD原文明确出现的技术技能、工具和AI技术概念。不把通用产品工作职责、学历年限、软能力作为技能，但岗位职责中明确出现的技术技能、工具和AI技术概念仍须提取。只返回JSON对象，固定字段为skills，值为字符串列表，不加解释。"

def compare_skills(reference, extracted):
    reference_set = set(reference)
    extracted_set = set(extracted)

    missing = sorted(reference_set - extracted_set)
    extra = sorted(extracted_set - reference_set)
    
    return {"missing":missing, "extra":extra}

# if __name__ == "__main__":
#     result = evaluate_prompt(revised_prompt, jd)
#     print(result)
if __name__ == "__main__":
  reference = [
    "Prompt Engineering", "RAG", "Agent",
    "向量数据库", "SQL", "Excel", "知识库"
]

  extracted = [
    "大模型", "PRD", "RAG", "Agent", "知识库",
    "Prompt Engineering", "向量数据库", "SQL", "Excel"
]
  result = compare_skills(reference, extracted)

  data = {
  "missing": result["missing"],
  "extra": result["extra"]
}

  with open("jd_comparison.json","w",encoding = "utf-8") as file:
    json.dump(data,file,ensure_ascii=False,indent=2)

  with open("jd_comparison.json","r",encoding = "utf-8") as file:
    data = json.load(file)

  print(data["extra"])
