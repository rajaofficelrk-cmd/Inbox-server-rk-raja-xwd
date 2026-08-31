import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
import base64
import os

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RK RAJA XWD SERVER",
    page_icon="🥷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# BACKGROUND PHOTO
# =========================================================

BG_IMAGE = Path("background.png")

@st.cache_data
def get_background_base64():
    """Cache background image to avoid reloading"""
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
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.52),
                    rgba(0, 0, 0, 0.78)
                ),
                url("data:image/png;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        .rk-title {{
            text-align: center;
            font-size: clamp(32px, 7vw, 64px);
            font-weight: 900;
            letter-spacing: 2px;
            background: linear-gradient(
                90deg,
                #ff0000, #ff7a00, #ffff00, #00ff00,
                #00ffff, #008cff, #7b00ff, #ff00c8, #ff0000
            );
            background-size: 600% 100%;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbowText 6s linear infinite;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.25));
            margin-bottom: 5px;
        }}

        @keyframes rainbowText {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 600% 50%; }}
        }}

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

        .small-text {{
            color: #d0d0d0;
            font-size: 13px;
        }}

        [data-testid="stSidebar"] {{
            background: rgba(0,0,0,0.72);
        }}

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

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="rk-title">🥷 RK RAJA XWD SERVER 🥷</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="rk-subtitle">📩 Facebook Page Inbox Dashboard</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("### 🔐 Facebook Page")

# Option: Use environment variable if available
env_token = os.environ.get("FB_ACCESS_TOKEN", "")

access_token = st.sidebar.text_input(
    "Page Access Token",
    type="password",
    placeholder="Paste Page Access Token",
    value=env_token if env_token else ""
)

conversation_limit = st.sidebar.slider(
    "📨 Conversations",
    min_value=1,
    max_value=50,
    value=10
)

st.sidebar.markdown("---")

refresh_button = st.sidebar.button(
    "🔄 Refresh Inbox",
    use_container_width=True
)

if refresh_button:
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **Status**
    
    🟢 Dashboard Online
    
    🔐 Token required for API access.
    
    ⚠️ Token ko public source code mein hard-code mat karo.
    """
)

# =========================================================
# FACEBOOK GRAPH API FUNCTION
# =========================================================

def fetch_inbox(token, limit):
    """Fetch conversations from Facebook Graph API"""
    url = "https://graph.facebook.com/v19.0/me/conversations"
    
    params = {
        "access_token": token,
        "fields": "id,updated_time,participants,messages.limit(1){message,from,created_time}",
        "limit": limit,
        "platform": "messenger"  # Important for Messenger
    }
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {str(e)}")
    
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON response: {str(e)}")

# =========================================================
# TOKEN REQUIRED
# =========================================================

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

# =========================================================
# LOAD FACEBOOK INBOX
# =========================================================

try:
    with st.spinner("📥 Facebook Page inbox load ho raha hai..."):
        result = fetch_inbox(access_token, conversation_limit)
    
    conversations = result.get("data", [])
    
    # =====================================================
    # DASHBOARD STATS
    # =====================================================
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💬 Conversations", len(conversations))
    
    with col2:
        st.metric("🟢 API Status", "Connected")
    
    with col3:
        st.metric(
            "🕒 Last Check",
            datetime.now().strftime("%H:%M:%S")
        )
    
    st.divider()
    
    # =====================================================
    # NO CONVERSATIONS
    # =====================================================
    
    if not conversations:
        st.warning("⚠️ Koi conversation nahi mili.")
    
    # =====================================================
    # DISPLAY CONVERSATIONS
    # =====================================================
    
    for conversation in conversations:
        conversation_id = conversation.get("id", "N/A")
        updated_time = conversation.get("updated_time", "N/A")
        
        participants = conversation.get("participants", {}).get("data", [])
        messages = conversation.get("messages", {}).get("data", [])
        
        sender = "Unknown"
        message = "No text message"
        created_time = "N/A"
        
        # -------------------------------------------------
        # LAST MESSAGE
        # -------------------------------------------------
        
        if messages and len(messages) > 0:
            last_message = messages[0]
            message = last_message.get("message", "No text message")
            created_time = last_message.get("created_time", "N/A")
            
            sender_data = last_message.get("from", {})
            sender = sender_data.get("name", "Unknown")
        
        # -------------------------------------------------
        # CONVERSATION EXPANDER
        # -------------------------------------------------
        
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
            
            # ---------------------------------------------
            # PARTICIPANTS
            # ---------------------------------------------
            
            if participants:
                st.markdown("### 👥 Participants")
                for person in participants:
                    person_name = person.get("name", "Unknown")
                    st.write(f"• {person_name}")

# =========================================================
# ERROR HANDLING
# =========================================================

except Exception as error:
    st.error("❌ Facebook inbox load nahi ho paya.")
    st.code(str(error))
    
    # Helpful troubleshooting tips
    st.markdown(
        """
        **Possible solutions:**
        - Check if token is valid and not expired
        - Ensure Page has messaging permissions
        - Verify token has `pages_read_engagement` permission
        - Check if Page has any conversations
        """
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:white;
        font-weight:700;
        padding:18px;
        font-size:16px;
    ">
        🥷 RK RAJA XWD SERVER 🥷
        <br>
        📩 Facebook Page Inbox Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
