import argparse
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def run_sql_file(sql_file: str, db_url: str) -> None:
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = psycopg2.connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print(f"Successfully executed '{sql_file}'.")
    except Exception as e:
        conn.rollback()
        print(f"Error executing '{sql_file}': {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a .sql file against a PostgreSQL database.")
    parser.add_argument("sql_file", help="Path to the .sql file to execute.")
    parser.add_argument("--db-url", default=os.getenv("DATABASE_URL"), help="PostgreSQL connection URL. Defaults to DATABASE_URL env var.")
    args = parser.parse_args()

    if not args.db_url:
        sys.exit(1)

    run_sql_file(args.sql_file, args.db_url)
