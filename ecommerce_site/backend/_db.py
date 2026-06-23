import os
import sqlite3
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_database_path():
    if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
        db_dir = tempfile.gettempdir()
    else:
        db_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))

    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "database.db")


DATABASE_PATH = get_database_path()


def get_db():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product TEXT,
                status TEXT
            )
            """
        )


init_db()
