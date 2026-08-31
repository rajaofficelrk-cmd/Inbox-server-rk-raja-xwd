import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_NAME = "facebook_inbox.db"

def get_connection():
    """Database connection create karta hai"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Database tables create karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            updated_time TEXT,
            created_time TEXT,
            last_message TEXT,
            sender_name TEXT,
            sender_id TEXT,
            participants TEXT,
            fetched_at TEXT
        )
    """)
    
    # Messages table (detailed messages ke liye)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            message_id TEXT,
            sender_name TEXT,
            sender_id TEXT,
            message_text TEXT,
            created_time TEXT,
            fetched_at TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)
    
    conn.commit()
    conn.close()

def save_conversations(conversations: List[Dict]):
    """Facebook API se aayi conversations ko save karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    fetched_at = datetime.now().isoformat()
    
    for conv in conversations:
        conversation_id = conv.get("id", "N/A")
        updated_time = conv.get("updated_time", "N/A")
        
        # Participants extract karo
        participants_data = conv.get("participants", {}).get("data", [])
        participants_json = str(participants_data)
        
        # Last message extract karo
        messages_data = conv.get("messages", {}).get("data", [])
        
        last_message = "No text message"
        sender_name = "Unknown"
        sender_id = "N/A"
        message_created_time = "N/A"
        
        if messages_data and len(messages_data) > 0:
            last_msg = messages_data[0]
            last_message = last_msg.get("message", "No text message")
            message_created_time = last_msg.get("created_time", "N/A")
            
            from_data = last_msg.get("from", {})
            sender_name = from_data.get("name", "Unknown")
            sender_id = from_data.get("id", "N/A")
        
        # Conversation save/replace karo
        cursor.execute("""
            INSERT OR REPLACE INTO conversations 
            (id, updated_time, created_time, last_message, sender_name, sender_id, participants, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conversation_id,
            updated_time,
            message_created_time,
            last_message,
            sender_name,
            sender_id,
            participants_json,
            fetched_at
        ))
        
        # Messages save karo (agar multiple messages hain)
        for msg in messages_data:
            message_id = msg.get("id", "N/A")
            message_text = msg.get("message", "No text message")
            msg_created_time = msg.get("created_time", "N/A")
            
            msg_from = msg.get("from", {})
            msg_sender_name = msg_from.get("name", "Unknown")
            msg_sender_id = msg_from.get("id", "N/A")
            
            cursor.execute("""
                INSERT INTO messages 
                (conversation_id, message_id, sender_name, sender_id, message_text, created_time, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                conversation_id,
                message_id,
                msg_sender_name,
                msg_sender_id,
                message_text,
                msg_created_time,
                fetched_at
            ))
    
    conn.commit()
    conn.close()
    return len(conversations)

def get_all_conversations() -> List[Dict]:
    """Saare conversations fetch karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM conversations 
        ORDER BY fetched_at DESC
    """)
    
    rows = cursor.fetchall()
    conversations = [dict(row) for row in rows]
    
    conn.close()
    return conversations

def get_conversation_by_id(conversation_id: str) -> Optional[Dict]:
    """Specific conversation fetch karta hai by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM conversations 
        WHERE id = ?
    """, (conversation_id,))
    
    row = cursor.fetchone()
    conversation = dict(row) if row else None
    
    conn.close()
    return conversation

def get_messages_by_conversation(conversation_id: str) -> List[Dict]:
    """Specific conversation ke saare messages fetch karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM messages 
        WHERE conversation_id = ?
        ORDER BY created_time DESC
    """, (conversation_id,))
    
    rows = cursor.fetchall()
    messages = [dict(row) for row in rows]
    
    conn.close()
    return messages

def search_conversations(query: str) -> List[Dict]:
    """Sender name ya message mein search karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    search_pattern = f"%{query}%"
    
    cursor.execute("""
        SELECT * FROM conversations 
        WHERE sender_name LIKE ? OR last_message LIKE ?
        ORDER BY fetched_at DESC
    """, (search_pattern, search_pattern))
    
    rows = cursor.fetchall()
    conversations = [dict(row) for row in rows]
    
    conn.close()
    return conversations

def delete_old_conversations(days: int = 30):
    """Purane conversations delete karta hai (default: 30 days)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cutoff_date = datetime.now().isoformat()
    
    cursor.execute("""
        DELETE FROM conversations 
        WHERE fetched_at < ?
    """, (cutoff_date,))
    
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    return deleted_count

def get_stats() -> Dict:
    """Database statistics fetch karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total conversations
    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_conversations = cursor.fetchone()[0]
    
    # Total messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    
    # Recent conversations (last 24 hours)
    cursor.execute("""
        SELECT COUNT(*) FROM conversations 
        WHERE fetched_at > datetime('now', '-1 day')
    """)
    recent_conversations = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "recent_conversations": recent_conversations
    }

def clear_database():
    """Poora database clear karta hai"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM messages")
    cursor.execute("DELETE FROM conversations")
    
    conn.commit()
    conn.close()

# Initialize database on import
create_tables()

if __name__ == "__main__":
    # Test code
    print("Database initialized!")
    print(f"Database file: {DATABASE_NAME}")
    
    stats = get_stats()
    print(f"Stats: {stats}")
