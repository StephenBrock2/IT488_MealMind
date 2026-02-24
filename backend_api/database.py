import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_PASS = os.getenv("DATABASE_PASS")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, password=DATABASE_PASS)
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    with open('schema.sql', 'r') as file:
        sql = file.read()

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    print("Database initialized")


if __name__ == "__main__":
    init_db()
