import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
import base64
import os
from database import (
    save_conversations,
    get_all_conversations,
    get_stats,
    search_conversations,
    clear_database
)

st.set_page_config(
    page_title="RK RAJA XWD SERVER",
    page_icon="🥷",
    layout="wide",
    initial_sidebar_state="expanded"
)

BG_IMAGE = Path("background.png")

@st.cache_data
def get_background_base64():
    if BG_IMAGE.exists():
        with open(BG_IMAGE, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

image_base64 = get_background_base64()

if image_base64:
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.52), rgba(0, 0, 0, 0.78)), url("data:image/png;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        [data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
        .rk-title {{
            text-align: center;
            font-size: clamp(32px, 7vw, 64px);
            font-weight: 900;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #ff0000, #ff7a00, #ffff00, #00ff00, #00ffff, #008cff, #7b00ff, #ff00c8, #ff0000);
            background-size: 600% 100%;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbowText 6s linear infinite;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.25));
            margin-bottom: 5px;
        }}
        @keyframes rainbowText {{ 0% {{ background-position: 0% 50%; }} 100% {{ background-position: 600% 50%; }} }}
        .rk-subtitle {{
            text-align: center;
            color: white;
            font-size: clamp(15px, 3vw, 21px);
            font-weight: 700;
            text-shadow: 0 0 8px rgba(255,255,255,0.5);
            margin-bottom: 20px;
        }}
        .glass-box {{
            background: rgba(0, 0, 0, 0.52);
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 20px;
            padding: 20px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            color: white;
            box-shadow: 0 8px 35px rgba(0,0,0,0.35);
        }}
        .message-box {{
            background: rgba(0,0,0,0.60);
            border-left: 4px solid #00e5ff;
            border-radius: 14px;
            padding: 16px;
            margin: 8px 0 15px 0;
            color: white;
            box-shadow: 0 5px 20px rgba(0,0,0,0.30);
        }}
        .small-text {{ color: #d0d0d0; font-size: 13px; }}
        [data-testid="stSidebar"] {{ background: rgba(0,0,0,0.72); }}
        [data-testid="stMetric"] {{
            background: rgba(0,0,0,0.52);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 15px;
            padding: 12px;
            backdrop-filter: blur(10px);
        }}
        [data-testid="stExpander"] {{
            background: rgba(0,0,0,0.45);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.15);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="rk-title">🥷 RK RAJA XWD SERVER 🥷</div>', unsafe_allow_html=True)
st.markdown('<div class="rk-subtitle">📩 Facebook Page Inbox Dashboard</div>', unsafe_allow_html=True)
st.divider()

st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("### 🔐 Facebook Page")

env_token = os.environ.get("FB_ACCESS_TOKEN", "")
access_token = st.sidebar.text_input(
    "Page Access Token",
    type="password",
    placeholder="Paste Page Access Token",
    value=env_token if env_token else ""
)

conversation_limit = st.sidebar.slider("📨 Conversations", min_value=1, max_value=50, value=10)

st.sidebar.markdown("---")

refresh_button = st.sidebar.button("🔄 Refresh Inbox", use_container_width=True)

st.sidebar.markdown("---")

if st.sidebar.button("📊 View Database", use_container_width=True):
    st.session_state.show_database = True

if st.sidebar.button("🔍 Search Conversations", use_container_width=True):
    st.session_state.show_search = True

if st.sidebar.button("🗑️ Clear Database", use_container_width=True):
    clear_database()
    st.success("Database cleared!")

st.sidebar.markdown("---")
st.sidebar.markdown("**Status**

🟢 Dashboard Online

🔐 Token required for API access.

⚠️ Token ko public source code mein hard-code mat karo.")

def fetch_inbox(token, limit):
    url = "https://graph.facebook.com/v19.0/me/conversations"
    params = {
        "access_token": token,
        "fields": "id,updated_time,participants,messages.limit(1){message,from,created_time}",
        "limit": limit,
        "platform": "messenger"
    }
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {str(e)}")
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON response: {str(e)}")

# Database view
if st.session_state.get("show_database", False):
    st.markdown("## 📊 Database Conversations")
    
    all_convs = get_all_conversations()
    
    if all_convs:
        st.success(f"Total: {len(all_convs)} conversations saved")
        
        for conv in all_convs:
            with st.expander(f"💬 {conv['sender_name']} • {conv['id']}"):
                st.write(f"**Last Message:** {conv['last_message']}")
                st.write(f"**Time:** {conv['created_time']}")
                st.write(f"**Fetched:** {conv['fetched_at']}")
    else:
        st.warning("Database empty hai. Pehle inbox refresh karo!")
    
    if st.button("← Back to Inbox"):
        st.session_state.show_database = False
        st.rerun()
    
    st.divider()

# Search view
if st.session_state.get("show_search", False):
    st.markdown("## 🔍 Search Conversations")
    
    search_query = st.text_input("Search by sender name or message:")
    
    if search_query:
        results = search_conversations(search_query)
        
        if results:
            st.success(f"Found {len(results)} results")
            
            for conv in results:
                with st.expander(f"💬 {conv['sender_name']} • {conv['id']}"):
                    st.write(f"**Message:** {conv['last_message']}")
                    st.write(f"**Time:** {conv['created_time']}")
        else:
            st.warning("Koi result nahi mila.")
    
    if st.button("← Back to Inbox"):
        st.session_state.show_search = False
        st.rerun()
    
    st.divider()

if not access_token:
    st.markdown(
        """
        <div class="glass-box">
        <h2>🔐 Facebook Page Token Required</h2>
        <p>Sidebar mein apna <b>Facebook Page Access Token</b> enter karo.</p>
        <p>Token valid hone ke baad dashboard Page conversations load karega.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

try:
    if refresh_button:
        with st.spinner("📥 Facebook Page inbox load ho raha hai..."):
            result = fetch_inbox(access_token, conversation_limit)
        
        conversations = result.get("data", [])
        
        if conversations:
            saved_count = save_conversations(conversations)
            st.success(f"✅ {saved_count} conversations saved to database!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💬 Conversations", len(conversations))
        with col2:
            st.metric("🟢 API Status", "Connected")
        with col3:
            st.metric("🕒 Last Check", datetime.now().strftime("%H:%M:%S"))
        
        st.divider()
        
        if not conversations:
            st.warning("⚠️ Koi conversation nahi mili.")
        
        for conversation in conversations:
            conversation_id = conversation.get("id", "N/A")
            updated_time = conversation.get("updated_time", "N/A")
            participants = conversation.get("participants", {}).get("data", [])
            messages = conversation.get("messages", {}).get("data", [])
            
            sender = "Unknown"
            message = "No text message"
            created_time = "N/A"
            
            if messages and len(messages) > 0:
                last_message = messages[0]
                message = last_message.get("message", "No text message")
                created_time = last_message.get("created_time", "N/A")
                sender_data = last_message.get("from", {})
                sender = sender_data.get("name", "Unknown")
            
            with st.expander(f"💬 {sender} • {conversation_id}"):
                st.markdown(
                    f"""
                    <div class="message-box">
                        <b>👤 Sender:</b> {sender}
                        <br><br>
                        <b>💬 Last Message:</b> {message}
                        <br><br>
                        <b>🕒 Message Time:</b> {created_time}
                        <br><br>
                        <span class="small-text">Conversation ID: {conversation_id}</span>
                        <br>
                        <span class="small-text">Updated: {updated_time}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if participants:
                    st.markdown("### 👥 Participants")
                    for person in participants:
                        person_name = person.get("name", "Unknown")
                        st.write(f"• {person_name}")
        
        st.divider()
        
        stats = get_stats()
        st.markdown("### 📈 Database Stats")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("🗄️ Total Saved", stats["total_conversations"])
        with stat_col2:
            st.metric("💾 Total Messages", stats["total_messages"])
        with stat_col3:
            st.metric("🕐 Recent (24h)", stats["recent_conversations"])
    
    else:
        st.info("👈 Sidebar se 'Refresh Inbox' click karo data load karne ke liye.")
        
        stats = get_stats()
        if stats["total_conversations"] > 0:
            st.success(f"Database mein {stats['total_conversations']} conversations saved hain.")

except Exception as error:
    st.error("❌ Facebook inbox load nahi ho paya.")
    st.code(str(error))
    st.markdown("**Possible solutions:**
- Check if token is valid and not expired
- Ensure Page has messaging permissions
- Verify token has `pages_read_engagement` permission
- Check if Page has any conversations")

st.divider()
st.markdown(
    """
    <div style="text-align:center; color:white; font-weight:700; padding:18px; font-size:16px;">
        🥷 RK RAJA XWD SERVER 🥷
        <br>
        📩 Facebook Page Inbox Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
