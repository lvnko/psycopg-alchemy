import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"
with psycopg2.connect(conf) as conn:
    conn.set_session(autocommit=True)  # Set autocommit to True
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS products(id serial primary key, name varchar, price float, quantity int);")
        # cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);", ('ASUS Laptop', 999.99, 10))
        # cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);", ('Samsung G50', 499.99, 20))
        try:
            # Wrapped a db command in try-except block to handle errors
            cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);", ('Google Pixel', 799.99, 8))
            cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);", ('Nokia 3310', 49.99, 100))
            # Simulate an error
            raise Exception("Simulated error")
        except Exception as excp:
            # In case of error, this try-except brackets structure would
            # rollback all the transactions within try brackets
            # This will undo any changes made in the current transaction
            # and return the database to its previous state
            # This is important to maintain data integrity
            # and avoid leaving the database in an inconsistent state
            conn.rollback()
            # Above, conn.rollback() is supposed not be executed with autocommit=True
            # But it is executed either because:
            # 1. because the error occurs in the try block
            # 2. or this version of psycopg2 respect the Exception catch mechanism
            print(f"Error occurred: {excp}")

        cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);", ('Apple Watch', 399.99, 15))
        cur.execute("SELECT * FROM products;")

        rows = cur.fetchall()
        print(rows)
        
    # conn.commit() # Not needed with autocommit=True