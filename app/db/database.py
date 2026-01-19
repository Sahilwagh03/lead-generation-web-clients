import sqlite3
from pathlib import Path

# app/db/
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "leads.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        followers INTEGER,
        following INTEGER,
        posts INTEGER,
        bio TEXT,
        website TEXT,
        email TEXT,
        phone TEXT,
        whatsapp TEXT,
        is_verified INTEGER NOT NULL DEFAULT 0,
        is_business INTEGER NOT NULL DEFAULT 0,
        category TEXT,
        full_name TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
