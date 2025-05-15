import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

create_sql = """
CREATE TABLE IF NOT EXISTS arrays (
    id SERIAL PRIMARY KEY,
    intArr INT[],
    strArr VARCHAR[]
);
"""

insert_sql = """
INSERT INTO arrays (intArr, strArr)
VALUES (%s, %s);
"""

select_sql = "SELECT * FROM arrays WHERE id IN %s;"

with psycopg2.connect(conf) as conn:
    with conn.cursor() as cur:
        cur.execute(create_sql)
        cur.execute(insert_sql, (
            [4,5,5],
            ["d","e"]
        ))
        # 注意：
        # 用 Psycopg 撰寫 SQL 時
        # 若有需要用到 data/parameter binding
        # 這時如果需要 binding 的參數只有一個
        # 那麼在包含 data 的 tuple 中
        # 一定要在唯一一個值的後面加一個逗點
        # 例：cur.execute(select_sql, (value,))
        #                                  ^
        # 不然就會出現 syntax error
        cur.execute(select_sql,((1,3),))
        rows = cur.fetchall()
        for data in rows:
            print(data)