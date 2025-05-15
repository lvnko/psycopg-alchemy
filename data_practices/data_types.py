import sys
import os
import psycopg2

# Add the parent directory to the system path to allow importing from sibling directories
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.FilePathGen import generate_path_to_file

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

sql_create = """
CREATE TABLE IF NOT EXISTS date_types_test (
    id SERIAL PRIMARY KEY,
    myBool BOOLEAN,
    myDec DECIMAL(10),
    myDouble DOUBLE PRECISION,
    myInt INT,
    myVar VARCHAR
);
"""

sql_insert = """
INSERT INTO date_types_test (myBool, myDec, myDouble, myInt, myVar)
VALUES (%s, %s, %s, %s, %s);
"""

sql_select = """
SELECT * FROM date_types_test;
"""

# 這個練習是為了實現 PostgreSQL 是如何
# 自動對用戶輸入的資料進行類型轉換的
# 1. 在 PostgreSQL 中，BOOLEAN 類型的資料可以是 TRUE、FALSE、't'、'f'、'1'、'0'
# 2. DECIMAL 類型的資料可以是小數點後有 10 位數的數字
#   - 在業內使用 DECIMAL 類型的資料時，通常都會把它轉成 Float 類型去閱讀，
#     但要注意這樣有機會把 DECIMAL 的 precision digits 犧牲掉
#     例：從 30 個變成 Float 類型的 15 個，這樣原來後面的 15 個數字就會被捨去
# 3. DOUBLE PRECISION 類型的資料可以是小數點後有 15 位數的數字
# 4. INT 類型的資料可以是整數
# 5. VARCHAR 類型的資料可以是字串

with psycopg2.connect(conf) as conn:
    print(f"Connection Encoding : {conn.encoding}")
    with conn.cursor() as cur:
        cur.execute(sql_create)
        cur.execute(sql_insert, (False, 10.0, 10.0, 10, "Hi, how are you?"))
        with open(generate_path_to_file("data_import/data_types.csv"), "r") as f:
            for line in f:
                cur.execute(sql_insert, line.rstrip().split(","))
        cur.execute(sql_select)
        rows = cur.fetchall()
        print(rows)
        myDec = rows[0][2]
        print(myDec)
        print(float(myDec) * 1.0)
