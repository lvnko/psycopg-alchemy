import psycopg2, uuid
from psycopg2.extras import UUID_adapter

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

create_sql = """
CREATE TABLE IF NOT EXISTS uuids (
    id SERIAL PRIMARY KEY,
    myUUID UUID
);
"""

insert_sql = """
INSERT INTO uuids (myUUID)
VALUES (%s);
"""

select_sql = "SELECT * FROM uuids;"

with psycopg2.connect(conf) as conn:
    with conn.cursor() as cur:
        cur.execute(create_sql)
        # 在這裡我們再次用到 Psycopg 所提供的插件 (UUID_adapter())
        # 來做轉換
        cur.execute(insert_sql, (UUID_adapter(uuid.uuid4()),))
        cur.execute(select_sql)
        rows = cur.fetchall()
        print(rows)