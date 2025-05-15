import psycopg2
from datetime import datetime, timezone, timedelta

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

create_sql = """
CREATE TABLE IF NOT EXISTS times (
    id SERIAL PRIMARY KEY,
    myTime TIME,
    myTimetz TIMETZ,
    myDate DATE,
    myDatetime TIMESTAMP,
    myDatetimeTz TIMESTAMPTZ
);
"""

insert_sql = """
INSERT INTO times (myTime, myTimetz, myDate, myDatetime, myDatetimeTz)
VALUES (%s, %s, %s, %s, %s);
"""

select_sql = "SELECT * FROM times;"

dt = datetime.now()
# print(dt)

dttz = datetime.now(timezone(timedelta(hours=5)))
# print(dttz)

dtBrt = datetime.now(timezone(timedelta(hours=-3)))
# print(dtBrt)

dtTpe = datetime.now(timezone(timedelta(hours=8)))
print("source : ", dtTpe)

with psycopg2.connect(conf) as conn:
    with conn.cursor() as cur:
        cur.execute(create_sql)
        cur.execute(insert_sql, (dt.time(), dt.timetz(), dt.date(), dt, dt))
        cur.execute(insert_sql, (dttz.time(), dttz.timetz(), dttz.date(), dttz, dttz))
        cur.execute(insert_sql, (dtBrt.time(), dtBrt.timetz(), dtBrt.date(), dtBrt, dtBrt))
        cur.execute(insert_sql, (dtTpe.time(), dtTpe.timetz(), dtTpe.date(), dtTpe, dtTpe))
        cur.execute(select_sql)
        rows = cur.fetchall()
        print(rows[3])
        # TIME : datetime.time(4, 36, 14, 410157),
        # TIMETZ : datetime.time(4, 36, 14, 410157, tzinfo=datetime.timezone(datetime.timedelta(seconds=28800))),
        # DATE : datetime.date(2025, 5, 15),
        # TIMESTAMP : datetime.datetime(2025, 5, 14, 20, 36, 14, 410157),
        # TIMESTAMPTZ : datetime.datetime(2025, 5, 14, 20, 36, 14, 410157, tzinfo=datetime.timezone.utc)

        # for col in rows[3]:
        #     print(col)