import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    with open("schema_create.sql", "r") as schema:
        cur.execute(schema.read())

    conn.commit()
    cur.close()
    conn.close()
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_db()
