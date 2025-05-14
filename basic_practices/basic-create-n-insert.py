import psycopg2

conn = psycopg2.connect("dbname=postgres host=localhost user=postgres password=lvnko")
cur = conn.cursor()
print(conn)
print(cur)

cur.execute("CREATE TABLE IF NOT EXISTS users(id serial primary key, name varchar, age int);")
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s);", ('John Doe', 30))
cur.execute("SELECT * FROM users;")
rows = cur.fetchall()
print(rows)
conn.commit()

cur.close()
conn.close()
print(cur)
print(conn)