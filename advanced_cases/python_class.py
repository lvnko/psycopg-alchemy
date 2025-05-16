from psycopg2.extensions import adapt, register_adapter, AsIs
import psycopg2

conf = "dbname=postgres host=localhost user=postgres password=lvnko"

create_sql = """
CREATE TABLE IF NOT EXISTS class_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    age FLOAT
);
"""

insert_sql = """
INSERT INTO class_users (name, age)
VALUES %s;
"""

class User():
    def __init__(self, name, age):
        self.name = name
        self.age = age

def user_adapt(user):
    name = adapt(user.name)
    age = adapt(user.age)
    return AsIs(f"({name}, {age})")

register_adapter(User, user_adapt)

users = [User("Riley Allans", 19), User("Alex Johnsons", 32), User("Terry Bridge", 56)]

with psycopg2.connect(conf) as conn:
    with conn.cursor() as cur:
        cur.execute(create_sql)
        for user in users:
            cur.execute(insert_sql, (user,))