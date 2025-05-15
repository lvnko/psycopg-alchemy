import psycopg2
from psycopg2._json import Json

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

create_sql = """
CREATE TABLE IF NOT EXISTS jsons (
    id SERIAL PRIMARY KEY,
    myJson JSONB
);
"""

insert_sql = """
INSERT INTO jsons (myJson)
VALUES (%s);
"""

select_sql = "SELECT * FROM jsons;"

myJson = {
    "name": "Jason",
    "age": 72
}

with psycopg2.connect(conf) as conn:
    with conn.cursor() as cur:
        cur.execute(create_sql)
        # Psycopg 並不能接受以 dict 來轉換成 json 類型
        # 因此這裡我們需要用到 Psycopg 所提供的 Json() 插件
        # 來做轉換
        cur.execute(insert_sql, (Json(myJson),))
        cur.execute(select_sql)
        rows = cur.fetchall()
        print(rows)