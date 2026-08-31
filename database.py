import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_FILE = Path("conversations.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            sender_name TEXT,
            last_message TEXT,
            created_time TEXT,
            fetched_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_conversations(conversations):
    init_database()

    conn = get_connection()
    saved = 0

    for conversation in conversations:

        conversation_id = conversation.get("id")

        if not conversation_id:
            continue

        messages = (
            conversation
            .get("messages", {})
            .get("data", [])
        )

        sender_name = "Unknown"
        last_message = "No text message"
        created_time = conversation.get(
            "updated_time",
            "N/A"
        )

        if messages:
            msg = messages[0]

            last_message = msg.get(
                "message",
                "No text message"
            )

            created_time = msg.get(
                "created_time",
                created_time
            )

            sender_name = (
                msg.get("from", {})
                .get("name", "Unknown")
            )

        fetched_at = datetime.now().isoformat()

        conn.execute("""
            INSERT OR REPLACE INTO conversations
            (
                id,
                sender_name,
                last_message,
                created_time,
                fetched_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            conversation_id,
            sender_name,
            last_message,
            created_time,
            fetched_at
        ))

        saved += 1

    conn.commit()
    conn.close()

    return saved


def get_all_conversations():
    init_database()

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            sender_name,
            last_message,
            created_time,
            fetched_at
        FROM conversations
        ORDER BY fetched_at DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def search_conversations(query):
    init_database()

    conn = get_connection()

    search = f"%{query}%"

    rows = conn.execute("""
        SELECT
            id,
            sender_name,
            last_message,
            created_time,
            fetched_at
        FROM conversations
        WHERE
            sender_name LIKE ?
            OR last_message LIKE ?
            OR id LIKE ?
        ORDER BY fetched_at DESC
    """, (
        search,
        search,
        search
    )).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_stats():
    init_database()

    conn = get_connection()

    total_conversations = conn.execute(
        "SELECT COUNT(*) FROM conversations"
    ).fetchone()[0]

    total_messages = conn.execute(
        """
        SELECT COUNT(*)
        FROM conversations
        WHERE last_message IS NOT NULL
        AND last_message != ''
        AND last_message != 'No text message'
        """
    ).fetchone()[0]

    cutoff = (
        datetime.now() -
        timedelta(hours=24)
    ).isoformat()

    recent_conversations = conn.execute(
        """
        SELECT COUNT(*)
        FROM conversations
        WHERE fetched_at >= ?
        """,
        (cutoff,)
    ).fetchone()[0]

    conn.close()

    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "recent_conversations": recent_conversations,
    }


def clear_database():
    init_database()

    conn = get_connection()

    conn.execute(
        "DELETE FROM conversations"
    )

    conn.commit()
    conn.close()


# Create database automatically
init_database()
