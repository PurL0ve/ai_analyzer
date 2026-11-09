from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as db:
    try:
        db.add(Record(name="第一次分析"))
        db.flush()
        print("提交前记录数：", db.query(Record).count())

        # name 不允许重复，让提交真正遇到数据库错误
        db.add(Record(name="第一次分析"))
        db.commit()
    except SQLAlchemyError:
        # TODO：补一行，回滚本次事务
        db.rollback()

    print("处理失败后记录数：", db.query(Record).count())