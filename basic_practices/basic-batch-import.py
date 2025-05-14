import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"
sql_insert = "INSERT INTO users (name, age) VALUES (%(name)s, %(age)s);"
data = [
    { "name": 'Anne Kaine', "age": 26 },
    { "name": 'Michael Fox', "age": 36 },
    { "name": 'Jane Smith', "age": None },
    { "name": 'Alice Johnson', "age": 35 },
    { "name": 'Bob Brown', "age": 22 }
]

with psycopg2.connect(conf) as conn:
    
    with conn.cursor() as cur:
        # Create table if it doesn't exist
        cur.execute("CREATE TABLE IF NOT EXISTS users(id serial primary key, name varchar, age int);")
        
        for param in data:
            # Insert data into the table
            cur.execute(sql_insert, param)
        
        # Fetch all rows from the table
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
        print(rows)
    
    # Commit the transaction
    conn.commit()  # Not needed with 'with' statement