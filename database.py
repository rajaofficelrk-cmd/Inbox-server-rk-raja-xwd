import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path("app.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS configs (
            user_id INTEGER PRIMARY KEY,
            chat_id TEXT DEFAULT '',
            name_prefix TEXT DEFAULT '',
            delay INTEGER DEFAULT 3,
            cookies TEXT DEFAULT '',
            messages TEXT DEFAULT 'Hello!'
        )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    username = username.strip()

    if len(username) < 3 or len(password) < 4:
        return False, "Username/password too short."

    conn = get_conn()

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users(username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        user_id = cur.lastrowid

        cur.execute(
            "INSERT INTO configs(user_id) VALUES (?)",
            (user_id,)
        )

        conn.commit()
        return True, "✅ ACCOUNT CREATED. PLEASE LOGIN."
    except sqlite3.IntegrityError:
        return False, "❌ USERNAME ALREADY EXISTS."
    finally:
        conn.close()


def verify_user(username, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM users WHERE username=? AND password_hash=?",
        (username.strip(), hash_password(password))
    ).fetchone()
    conn.close()
    return row["id"] if row else None


def get_user_config(user_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM configs WHERE user_id=?",
        (user_id,)
    ).fetchone()
    conn.close()

    if not row:
        return {
            "chat_id": "",
            "name_prefix": "",
            "delay": 3,
            "cookies": "",
            "messages": "Hello!"
        }

    return dict(row)


def update_user_config(
    user_id, chat_id, name_prefix, delay, cookies, messages
):
    conn = get_conn()
    conn.execute("""
        INSERT INTO configs(
            user_id, chat_id, name_prefix, delay, cookies, messages
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            chat_id=excluded.chat_id,
            name_prefix=excluded.name_prefix,
            delay=excluded.delay,
            cookies=excluded.cookies,
            messages=excluded.messages
    """, (
        user_id,
        chat_id,
        name_prefix,
        int(delay),
        cookies,
        messages
    ))
    conn.commit()
    conn.close()
