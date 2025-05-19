import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

select_sql = "SELECT * FROM cursor_batch_test;"

with psycopg2.connect(conf) as conn:
    with conn.cursor("myCursor") as cur: # 在 conn.cursro() 函式中輸入名字，便觸發使用伺服器端 Cursor
        cur.itersize = 3
        try:
            cur.execute(select_sql)
            for record in cur:
                print(cur.rowcount, cur.rownumber, record)

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