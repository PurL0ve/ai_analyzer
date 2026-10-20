from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")

if not database_url:
  raise RuntimeError("DATABASE_URL环境变量未设置")

engine = create_engine(
  database_url
) #引擎

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind = engine
) #session对话

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
#get_db方法