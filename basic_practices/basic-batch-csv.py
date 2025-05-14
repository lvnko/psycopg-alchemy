import sys
import os
import psycopg2

# Add the parent directory to the system path to allow importing from sibling directories
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.FilePathGen import generate_path_to_file

conf = "dbname=postgres host=localhost user=postgres password=lvnko"
sql_insert = "INSERT INTO users (name, age) VALUES (%s, %s);"

with open(generate_path_to_file('data_import/users.csv'), 'r') as f:
    
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