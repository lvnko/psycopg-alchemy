import configparser
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import text

parser = configparser.ConfigParser()
parser.read("../config_parser/db.ini")
pg_conf = parser["postgres"]

db_url = URL.create(drivername="postgresql", **pg_conf)
# ！注意：
# 有別於教程所示，這裡是需要使用 URL.create()
# 並且用 drivename 去命名所使用的 db sql 種類
# 才是正確的用法。

engine = create_engine(db_url, echo=True)

select_sql = text("SELECT * FROM users;")
# ！注意：
# 有別於教程所示，這裏我們需要使用 text(...) 來包裹 SQL 語句，
# 用以告知 SQLAlchemy 此字串為一個 SQL 查詢。
# 這是由於經 SQLAlchemy engine 所創建的 conn 並不接受普通的
# 字串為可以執行的 SQL 查詢語句。

with engine.begin() as conn:
    result_set = conn.execute(select_sql)
    print(result_set)
    for user in result_set.fetchall():
        print(user)