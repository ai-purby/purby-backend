import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db():
    conn = psycopg2.connect(
        os.getenv("DATABASE_URL", "host=100.65.89.27 port=5432 user=purby password=purbyiscute dbname=purby"),
        cursor_factory=RealDictCursor,
    )
    return conn
