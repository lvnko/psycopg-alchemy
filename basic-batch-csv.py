import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"
sql_insert = "INSERT INTO users (name, age) VALUES (%s, %s);"

with open('data_import/users.csv', 'r') as f:
    
    with psycopg2.connect(conf) as conn:
        
        with conn.cursor() as cur:
            
            # Create table if it doesn't exist
            cur.execute("CREATE TABLE IF NOT EXISTS users(id serial primary key, name varchar, age int);")

            for line in f:
                (name, age) = line.rstrip().split(",")
                age = None if age == '' else int(age)
                # Insert data into the table
                cur.execute(sql_insert, (name, age))
            
            # Fetch all rows from the table
            cur.execute("SELECT * FROM users;")
            rows = cur.fetchall()
            print(rows)

        # conn.commit()  # Not needed with 'with' statement