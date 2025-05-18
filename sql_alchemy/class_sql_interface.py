import configparser
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
# from sqlalchemy.ext.declarative import declarative_base # 舊的 declarative_base 引用方法
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer

parser = configparser.ConfigParser()
parser.read("../config_parser/db.ini")
pg_conf = parser["postgres"]

db_url = URL.create(drivername="postgresql", **pg_conf)
# ！注意：
# 有別於教程所示，這裡是需要使用 URL.create()
# 並且用 drivename 去命名所使用的 db sql 種類
# 才是正確的用法。

engine = create_engine(db_url, echo=True)

Base = declarative_base()
# 移除了 bind=engine 的設定，
# 因為這個已經不是 SQLAlchemy 2.0 的標準用法了

class Users(Base):
    __tablename__ = 'sqlalchemy_complex_users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)

print(Base.metadata.tables)

# --- Create the table(s) in the database ---
# This is the key step for creating tables:
try:
    Base.metadata.create_all(engine) # 根據 2.0 的標準用法，這裡需要提供 engine
    print(f"Table '{Users.__tablename__}' and any other tables in Base.metadata created successfully (if they didn't already exist).")
except Exception as e:
    print(f"An error occurred during table creation: {e}")

with engine.begin() as conn:
    result_set = conn.execute(Users.__table__.select())
    print(result_set)
    for user in result_set.fetchall():
        print(user)