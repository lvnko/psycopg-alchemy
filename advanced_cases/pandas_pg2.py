import pandas as pd
import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"
conn = psycopg2.connect(conf)

select_sql = "SELECT * FROM adv_users;"

create_sql = """
CREATE TABLE IF NOT EXISTS adv_users_agg (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR,
    age FLOAT
);
"""

insert_sql = """
INSERT INTO adv_users_agg (full_name, age)
VALUES (%s, %s);
"""

# 使用 pandas 的 read_sql_query 把 database 裡 table 的資料放到一個 dataframe 裡面

df = pd.read_sql_query(select_sql, conn, parse_dates={"birthday": "%Y-%m-%d"})

df["full_name"] = df["first_name"] + ", " + df["last_name"]
df["age"] = ((pd.to_datetime('now') - df["birthday"]) / pd.Timedelta(days=365.25)).astype(int)

# print(df)
# print(df.dtypes)

with conn.cursor() as cur:

    try:
        cur.execute(create_sql)
        for row in df.values:
            # print(row)
            cur.execute(insert_sql, (row[-2], row[-1]))

    except psycopg2.ProgrammingError as error:
        print("Programming Error Captured :")
        print(f"pgcode : {error.pgcode}")
        print(f"{error.diag.severity} : Something is broken, because {error.diag.message_primary}")
    except psycopg2.OperationalError as error:
        print("Operational Error Captured :")
        print(f"Function cannot be executed, because :")
        print(f"{error}")
    except psycopg2.Error as error:
        print("General Error Captured :")
        print(f"pgcode : {error.pgcode}")
        print(f"severity : {error.diag.severity}")
        print(f"message_primary : {error.diag.message_primary}")
        print(f"message_detail : {error.diag.message_detail}")

conn.commit()
conn.close()
print("program succeeded!")