import psycopg2, configparser

config = configparser.ConfigParser()
config.read("db.ini")

# print(config["postgres"]["user"]) # db.ini 裡的參數值可以以下格式讀取
# print(config["postgres"]["host"]) # 例： config["數據庫服務"]["參數名"]

select_sql = "SELECT * FROM class_users;"

with psycopg2.connect(
    # user=config["postgres"]["username"],
    # host=config["postgres"]["host"],
    # dbname=config["postgres"]["database"],
    # password=config["postgres"]["password"]
    **config["postgres"] # 只用 "**" 便能把 config[...] 作為 dict 去解構，結果為以上被 comment 的代碼
) as conn:
    with conn.cursor() as cur:
        cur.execute(select_sql)
        for record in cur:
            print(record)