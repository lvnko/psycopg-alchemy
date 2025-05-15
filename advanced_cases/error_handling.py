import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

select_sql = "SELECT * FROM non_eixting_table;"

def sqlFunction():
    with psycopg2.connect(conf) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(select_sql)
            except psycopg2.ProgrammingError as error:
                print("Programming Error Captured :")
                print(f"pgcode : {error.pgcode}")
                print(f"{error.diag.severity} : Something is broken, because {error.diag.message_primary}")
            except psycopg2.Error as error:
                print("General Error Captured :")
                print(f"pgcode : {error.pgcode}")
                print(f"severity : {error.diag.severity}")
                print(f"message_primary : {error.diag.message_primary}")
                print(f"message_detail : {error.diag.message_detail}")

try:
    sqlFunction()
except psycopg2.OperationalError as error:
    print("Operational Error Captured :")
    print(f"Function cannot be executed, because :")
    print(f"{error}")