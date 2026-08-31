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
    clear_database,
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RK RAJA XWD SERVER",
    page_icon="🥷",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG_IMAGE = Path("background.png")


# =========================================================
# BACKGROUND
# =========================================================

@st.cache_data
def get_background_base64():
    if BG_IMAGE.exists():
        try:
            with open(BG_IMAGE, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception:
            return None
    return None


image_base64 = get_background_base64()

if image_base64:
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image:
                linear-gradient(
                    rgba(0,0,0,0.52),
                    rgba(0,0,0,0.78)
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
                #ff0000,
                #ff7a00,
                #ffff00,
                #00ff00,
                #00ffff,
                #008cff,
                #7b00ff,
                #ff00c8,
                #ff0000
            );

            background-size: 600% 100%;

            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;

            animation: rainbowText 6s linear infinite;

            filter:
                drop-shadow(0 0 10px rgba(255,255,255,0.25));

            margin-bottom: 5px;
        }}

        @keyframes rainbowText {{
            0% {{
                background-position: 0% 50%;
            }}

            100% {{
                background-position: 600% 50%;
            }}
        }}

        .rk-subtitle {{
            text-align: center;
            color: white;
            font-size: clamp(15px, 3vw, 21px);
            font-weight: 700;

            text-shadow:
                0 0 8px rgba(255,255,255,0.5);

            margin-bottom: 20px;
        }}

        .glass-box {{
            background: rgba(0,0,0,0.52);
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 20px;
            padding: 20px;

            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);

            color: white;

            box-shadow:
                0 8px 35px rgba(0,0,0,0.35);
        }}

        .message-box {{
            background: rgba(0,0,0,0.60);
            border-left: 4px solid #00e5ff;
            border-radius: 14px;

            padding: 16px;
            margin: 8px 0 15px 0;

            color: white;

            box-shadow:
                0 5px 20px rgba(0,0,0,0.30);
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

            border:
                1px solid rgba(255,255,255,0.15);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="rk-title">🥷 RK RAJA XWD SERVER 🥷</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="rk-subtitle">📩 Facebook Page Inbox Dashboard</div>',
    unsafe_allow_html=True,
)

st.divider()


# =========================================================
# SESSION STATE
# =========================================================

if "show_database" not in st.session_state:
    st.session_state.show_database = False

if "show_search" not in st.session_state:
    st.session_state.show_search = False


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("### 🔐 Facebook Page")

env_token = os.environ.get("FB_ACCESS_TOKEN", "")

access_token = st.sidebar.text_input(
    "Page Access Token",
    type="password",
    placeholder="Paste Page Access Token",
    value=env_token,
)

conversation_limit = st.sidebar.slider(
    "📨 Conversations",
    min_value=1,
    max_value=50,
    value=10,
)

st.sidebar.markdown("---")

refresh_button = st.sidebar.button(
    "🔄 Refresh Inbox",
    use_container_width=True,
)

st.sidebar.markdown("---")

if st.sidebar.button(
    "📊 View Database",
    use_container_width=True,
):
    st.session_state.show_database = True
    st.session_state.show_search = False

if st.sidebar.button(
    "🔍 Search Conversations",
    use_container_width=True,
):
    st.session_state.show_search = True
    st.session_state.show_database = False

if st.sidebar.button(
    "🗑️ Clear Database",
    use_container_width=True,
):
    clear_database()
    st.success("Database cleared!")

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
# FACEBOOK API
# =========================================================

def fetch_inbox(token, limit):
    url = "https://graph.facebook.com/v19.0/me/conversations"

    params = {
        "access_token": token,
        "fields": (
            "id,"
            "updated_time,"
            "participants,"
            "messages.limit(1)"
            "{message,from,created_time}"
        ),
        "limit": limit,
        "platform": "messenger",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as error:
        try:
            error_data = response.json()
        except Exception:
            error_data = response.text

        raise RuntimeError(
            f"Facebook API error: {error_data}"
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Network error: {error}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            f"Invalid JSON response: {error}"
        ) from error


# =========================================================
# DATABASE VIEW
# =========================================================

if st.session_state.show_database:

    st.markdown("## 📊 Database Conversations")

    try:
        all_convs = get_all_conversations()

        if all_convs:

            st.success(
                f"Total: {len(all_convs)} conversations saved"
            )

            for conv in all_convs:

                sender_name = conv.get(
                    "sender_name",
                    "Unknown",
                )

                conversation_id = conv.get(
                    "id",
                    "N/A",
                )

                with st.expander(
                    f"💬 {sender_name} • {conversation_id}"
                ):

                    st.write(
                        f"**Last Message:** "
                        f"{conv.get('last_message', 'N/A')}"
                    )

                    st.write(
                        f"**Time:** "
                        f"{conv.get('created_time', 'N/A')}"
                    )

                    st.write(
                        f"**Fetched:** "
                        f"{conv.get('fetched_at', 'N/A')}"
                    )

        else:
            st.warning(
                "Database empty hai. "
                "Pehle inbox refresh karo!"
            )

    except Exception as error:
        st.error(
            f"Database error: {error}"
        )

    if st.button("← Back to Inbox"):
        st.session_state.show_database = False
        st.rerun()

    st.divider()


# =========================================================
# SEARCH VIEW
# =========================================================

if st.session_state.show_search:

    st.markdown("## 🔍 Search Conversations")

    search_query = st.text_input(
        "Search by sender name or message:"
    )

    if search_query:

        try:
            results = search_conversations(
                search_query
            )

            if results:

                st.success(
                    f"Found {len(results)} results"
                )

                for conv in results:

                    sender_name = conv.get(
                        "sender_name",
                        "Unknown",
                    )

                    conversation_id = conv.get(
                        "id",
                        "N/A",
                    )

                    with st.expander(
                        f"💬 {sender_name} • "
                        f"{conversation_id}"
                    ):

                        st.write(
                            f"**Message:** "
                            f"{conv.get('last_message', 'N/A')}"
                        )

                        st.write(
                            f"**Time:** "
                            f"{conv.get('created_time', 'N/A')}"
                        )

            else:
                st.warning(
                    "Koi result nahi mila."
                )

        except Exception as error:
            st.error(
                f"Search error: {error}"
            )

    if st.button("← Back to Inbox"):
        st.session_state.show_search = False
        st.rerun()

    st.divider()


# =========================================================
# TOKEN CHECK
# =========================================================

if not access_token:

    st.markdown(
        """
        <div class="glass-box">
            <h2>🔐 Facebook Page Token Required</h2>

            <p>
                Sidebar mein apna
                <b>Facebook Page Access Token</b>
                enter karo.
            </p>

            <p>
                Token valid hone ke baad dashboard
                Page conversations load karega.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# =========================================================
# FETCH INBOX
# =========================================================

try:

    if refresh_button:

        with st.spinner(
            "📥 Facebook Page inbox load ho raha hai..."
        ):

            result = fetch_inbox(
                access_token,
                conversation_limit,
            )

        conversations = result.get(
            "data",
            [],
        )

        if conversations:

            saved_count = save_conversations(
                conversations
            )

            st.success(
                f"✅ {saved_count} conversations "
                f"saved to database!"
            )

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💬 Conversations",
                len(conversations),
            )

        with col2:
            st.metric(
                "🟢 API Status",
                "Connected",
            )

        with col3:
            st.metric(
                "🕒 Last Check",
                datetime.now().strftime(
                    "%H:%M:%S"
                ),
            )

        st.divider()

        if not conversations:

            st.warning(
                "⚠️ Koi conversation nahi mili."
            )

        # -------------------------------------------------
        # CONVERSATIONS
        # -------------------------------------------------

        for conversation in conversations:

            conversation_id = conversation.get(
                "id",
                "N/A",
            )

            updated_time = conversation.get(
                "updated_time",
                "N/A",
            )

            participants = (
                conversation
                .get("participants", {})
                .get("data", [])
            )

            messages = (
                conversation
                .get("messages", {})
                .get("data", [])
            )

            sender = "Unknown"
            message = "No text message"
            created_time = "N/A"

            if messages:

                last_message = messages[0]

                message = last_message.get(
                    "message",
                    "No text message",
                )

                created_time = last_message.get(
                    "created_time",
                    "N/A",
                )

                sender_data = last_message.get(
                    "from",
                    {},
                )

                sender = sender_data.get(
                    "name",
                    "Unknown",
                )

            with st.expander(
                f"💬 {sender} • {conversation_id}"
            ):

                # Escape HTML-sensitive content
                # before inserting API data into HTML.
                import html

                safe_sender = html.escape(
                    str(sender)
                )

                safe_message = html.escape(
                    str(message)
                )

                safe_created = html.escape(
                    str(created_time)
                )

                safe_id = html.escape(
                    str(conversation_id)
                )

                safe_updated = html.escape(
                    str(updated_time)
                )

                st.markdown(
                    f"""
                    <div class="message-box">

                        <b>👤 Sender:</b>
                        {safe_sender}

                        <br><br>

                        <b>💬 Last Message:</b>
                        {safe_message}

                        <br><br>

                        <b>🕒 Message Time:</b>
                        {safe_created}

                        <br><br>

                        <span class="small-text">
                            Conversation ID:
                            {safe_id}
                        </span>

                        <br>

                        <span class="small-text">
                            Updated:
                            {safe_updated}
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if participants:

                    st.markdown(
                        "### 👥 Participants"
                    )

                    for person in participants:

                        person_name = person.get(
                            "name",
                            "Unknown",
                        )

                        st.write(
                            f"• {person_name}"
                        )

        # -------------------------------------------------
        # DATABASE STATS
        # -------------------------------------------------

        st.divider()

        stats = get_stats()

        st.markdown(
            "### 📈 Database Stats"
        )

        stat_col1, stat_col2, stat_col3 = (
            st.columns(3)
        )

        with stat_col1:
            st.metric(
                "🗄️ Total Saved",
                stats.get(
                    "total_conversations",
                    0,
                ),
            )

        with stat_col2:
            st.metric(
                "💾 Total Messages",
                stats.get(
                    "total_messages",
                    0,
                ),
            )

        with stat_col3:
            st.metric(
                "🕐 Recent (24h)",
                stats.get(
                    "recent_conversations",
                    0,
                ),
            )

    else:

        st.info(
            "👈 Sidebar se "
            "'Refresh Inbox' click karo "
            "data load karne ke liye."
        )

        stats = get_stats()

        if stats.get(
            "total_conversations",
            0,
        ) > 0:

            st.success(
                "Database mein "
                f"{stats['total_conversations']} "
                "conversations saved hain."
            )


# =========================================================
# ERROR HANDLING
# =========================================================

except Exception as error:

    st.error(
        "❌ Facebook inbox load nahi ho paya."
    )

    st.code(
        str(error)
    )

    st.markdown(
        """
        **Possible solutions:**

        - Check if token is valid and not expired
        - Ensure Page has messaging permissions
        - Verify the Page access token
        - Check if the Page has conversations
        - Check the Facebook Graph API response
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
    unsafe_allow_html=True,
)
