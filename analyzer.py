def clean_skills(skills):
  cleaned = []
  for skill in skills:
    new_skill = skill.strip()
    new_skill = new_skill.lower()
    cleaned.append(new_skill)
  return list(set(cleaned))

def analyze(user_skills,required_skills):
  matched = []
  missing = []
  rate = 0
  user_skills = clean_skills(user_skills)
  required_skills = clean_skills(required_skills)

  for skill in required_skills:
    if skill in user_skills:
      matched.append(skill)
    else:
      missing.append(skill)
  if len(required_skills) > 0:
    rate = len(matched) / len(required_skills)
  else:
    rate = 0
  return {
    "matched": matched,
    "missing": missing,
    "rate": rate,
  }

