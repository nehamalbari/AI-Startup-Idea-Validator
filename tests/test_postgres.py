import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

with psycopg.connect(DATABASE_URL) as conn:
    print("✅ PostgreSQL connection successful!")

    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print(cur.fetchone()[0])