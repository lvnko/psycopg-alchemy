import configparser
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, String, Integer

parser = configparser.ConfigParser()
parser.read("../config_parser/db.ini")
pg_conf = parser["postgres"]

db_url = URL.create(drivername="postgresql", **pg_conf)

engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False)

class Users(Base):
    __tablename__ = 'sqlalchemy_complex_users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)

try:
    Base.metadata.create_all(engine) # 根據 2.0 的標準用法，這裡需要提供 engine
    print(f"Table '{Users.__tablename__}' and any other tables in Base.metadata created successfully (if they didn't already exist).")
except Exception as e:
    print(f"An error occurred during table creation: {e}")

session = Session()

# new_user = Users(first_name="Gennie", last_name="Cole", age=27)
# session.add(new_user)
session.commit()

for user in session.query(Users):
    print(user.user_id, user.first_name, user.last_name, user.age)

session.close()
