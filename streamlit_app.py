import streamlit as st
import time
import hashlib
import os
import base64
import threading
from datetime import datetime, timedelta
from pathlib import Path

import database as db


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RK RAJA XWD",
    page_icon="☠️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CONFIG
# =========================================================

OWNER_USERNAME = os.getenv("OWNER_USERNAME", "rkraja")
OWNER_LICENSE = os.getenv(
    "OWNER_LICENSE",
    "RKRAJA-PREMIUM-2026"
)

LICENSE_DAYS = 30

BASE_DIR = Path(__file__).resolve().parent

BG_IMAGE = BASE_DIR / "155933.png"
WELCOME_AUDIO = BASE_DIR / "welcome.mp3"


# =========================================================
# CSS
# =========================================================

CUSTOM_CSS = r"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Share+Tech+Mono&display=swap'
);

* {
    box-sizing: border-box;
}

html,
body,
[class*="css"] {
    font-family: 'Share Tech Mono', monospace !important;
}

.stApp {
    background-color: #000000 !important;
    color: #00ff41 !important;
    background-image:
        linear-gradient(
            rgba(0,0,0,.78),
            rgba(0,0,0,.86)
        ),
        url("155933.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(0,255,65,.025) 0px,
            rgba(0,255,65,.025) 1px,
            transparent 1px,
            transparent 4px
        );
    z-index: 0;
}

.main .block-container {
    position: relative;
    z-index: 1;
    background: rgba(0,0,0,.84);
    border: 1px solid rgba(0,255,65,.38);
    border-radius: 20px;
    padding: 30px;
    box-shadow:
        0 0 25px rgba(0,255,65,.10),
        inset 0 0 25px rgba(0,255,65,.025);
    backdrop-filter: blur(8px);
}

.main-header {
    padding: 32px 18px;
    text-align: center;
    border: 1px solid #00ff41;
    border-radius: 18px;
    background: rgba(0,0,0,.78);
    box-shadow:
        0 0 22px rgba(0,255,65,.18),
        inset 0 0 20px rgba(0,255,65,.04);
    margin-bottom: 22px;
}

.main-header h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: 5px;
    color: #00ff41 !important;
    text-shadow:
        0 0 5px #00ff41,
        0 0 15px #00ff41,
        0 0 35px rgba(0,255,65,.65);
}

.main-header p {
    color: #00ff41 !important;
    letter-spacing: 4px;
    text-shadow: 0 0 8px #00ff41;
}

h1, h2, h3, h4 {
    font-family: 'Orbitron', monospace !important;
    color: #00ff41 !important;
    text-shadow: 0 0 8px rgba(0,255,65,.55);
    letter-spacing: 2px !important;
}

label {
    color: #00ff41 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 800 !important;
    text-shadow: 0 0 6px #00ff41;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #000000 !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    border-radius: 8px !important;
    font-family: 'Share Tech Mono', monospace !important;
    caret-color: #00ff41 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #00ff41 !important;
    box-shadow: 0 0 12px rgba(0,255,65,.30) !important;
}

.stButton > button {
    min-height: 46px;
    background: #000000 !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 900 !important;
    letter-spacing: 1px !important;
    text-shadow: 0 0 5px #00ff41;
    box-shadow: 0 0 10px rgba(0,255,65,.12);
}

.stButton > button:hover {
    background: #00ff41 !important;
    color: #000000 !important;
    text-shadow: none;
    box-shadow: 0 0 22px rgba(0,255,65,.60);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    background: #000000;
    padding: 7px;
    border: 1px solid rgba(0,255,65,.30);
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    color: #00ff41 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 800;
}

.stTabs [aria-selected="true"] {
    color: #000000 !important;
    background: #00ff41 !important;
    border-radius: 7px;
}

[data-testid="stMetric"] {
    background: #000000;
    border: 1px solid rgba(0,255,65,.38);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 0 12px rgba(0,255,65,.08);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #00ff41 !important;
    font-family: 'Orbitron', monospace !important;
}

[data-testid="stMetricValue"] {
    font-weight: 900 !important;
    text-shadow: 0 0 8px #00ff41;
}

.voice-box {
    margin: 18px 0;
    padding: 18px;
    border: 1px solid #00ff41;
    border-radius: 12px;
    text-align: center;
    background: rgba(0,0,0,.82);
    color: #00ff41;
    font-family: 'Orbitron', monospace !important;
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow: 0 0 10px #00ff41;
}

.console-output {
    background: #000000;
    border: 1px solid #00ff41;
    border-radius: 10px;
    padding: 16px;
    max-height: 400px;
    overflow-y: auto;
}

.console-line {
    padding: 8px 10px;
    margin-bottom: 6px;
    background: rgba(0,255,65,.035);
    border-left: 3px solid #00ff41;
    border-radius: 4px;
    color: #00ff41;
    text-shadow: 0 0 5px rgba(0,255,65,.45);
}

.success-box {
    background: rgba(0,255,65,.05);
    border: 1px solid #00ff41;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    color: #00ff41;
    font-family: 'Orbitron', monospace !important;
    font-weight: 900;
}

section[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid rgba(0,255,65,.25);
}

.stAlert {
    background: #000000 !important;
    border: 1px solid rgba(0,255,65,.30) !important;
}

.footer {
    text-align: center;
    margin-top: 30px;
    padding: 20px;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 3px;
    font-weight: 900;
    color: #00ff41;
    text-shadow:
        0 0 8px #00ff41,
        0 0 20px rgba(0,255,65,.55);
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "logged_in": False,
    "user_id": None,
    "username": None,
    "license_ok": False,
    "license_expiry": None,
    "logs": [],
    "running": False,
    "message_count": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================

def add_log(message):
    stamp = datetime.now().strftime("%H:%M:%S")

    logs = st.session_state.get("logs", [])

    logs.append(f"[{stamp}] {message}")

    st.session_state.logs = logs[-50:]


def cookie_fingerprint(value):
    if not value:
        return "NOT SET"

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:12]


def is_owner():
    username = st.session_state.get("username")

    return bool(
        username
        and username.lower() == OWNER_USERNAME.lower()
    )


def activate_license():
    st.session_state.license_ok = True

    st.session_state.license_expiry = (
        datetime.now()
        + timedelta(days=LICENSE_DAYS)
    )


def license_valid():
    if is_owner():
        return True

    if not st.session_state.get("license_ok"):
        return False

    expiry = st.session_state.get("license_expiry")

    if not expiry:
        return False

    return datetime.now() < expiry


def get_safe_config(uid):
    try:
        config = db.get_user_config(uid)

        if not isinstance(config, dict):
            config = {}

    except Exception:
        config = {}

    return {
        "chat_id": config.get("chat_id", ""),
        "name_prefix": config.get("name_prefix", ""),
        "delay": config.get("delay", 3),
        "cookies": config.get("cookies", ""),
        "messages": config.get(
            "messages",
            "RK RAJA XWD TEST MESSAGE"
        ),
    }


# =========================================================
# WELCOME AUDIO
# =========================================================

def render_welcome_audio():

    if not WELCOME_AUDIO.exists():

        st.markdown(
            """
            <div class="voice-box">
                🔊 WELCOME AUDIO NOT FOUND
                <br><br>
                <small>
                Put <b>welcome.mp3</b> beside streamlit_app.py
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

        return

    try:

        audio_bytes = WELCOME_AUDIO.read_bytes()

        st.markdown(
            """
            <div class="voice-box">
                🔊 RK RAJA XWD WELCOME VOICE
                <br>
                <small>
                Press PLAY to start voice
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

    except Exception as exc:

        st.error(
            "Audio load error: " + str(exc)
        )


# =========================================================
# LOCAL TEST WORKER
# =========================================================

def start_demo(messages, delay):

    if st.session_state.running:
        return

    st.session_state.running = True
    st.session_state.message_count = 0
    st.session_state.logs = []

    add_log("LOCAL TEST STARTED")

    def worker():

        try:

            for message in messages:

                if not st.session_state.running:
                    break

                time.sleep(delay)

                if not st.session_state.running:
                    break

                st.session_state.message_count += 1

                add_log(
                    "TEST #"
                    + str(st.session_state.message_count)
                    + " : "
                    + message[:80]
                )

        except Exception as exc:

            add_log(
                "WORKER ERROR: "
                + str(exc)
            )

        finally:

            st.session_state.running = False

            add_log(
                "LOCAL TEST FINISHED"
            )

    thread = threading.Thread(
        target=worker,
        daemon=True
    )

    thread.start()


# =========================================================
# HEADER
# =========================================================

def show_header(title="☠ RK RAJA XWD ☠",
                subtitle="// SECURE HACKER TERMINAL //"):

    st.markdown(
        f"""
        <div class="main-header">

            <h1>{title}</h1>

            <p>{subtitle}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LOGIN
# =========================================================

def login_page():

    show_header()

    render_welcome_audio()

    login_tab, signup_tab = st.tabs(
        [
            "🔐 LOGIN",
            "➕ SIGN-UP"
        ]
    )

    with login_tab:

        username = st.text_input(
            "USERNAME",
            key="login_user"
        )

        password = st.text_input(
            "PASSWORD",
            key="login_pass",
            type="password"
        )

        if st.button(
            "⚡ LOGIN",
            use_container_width=True
        ):

            if not username.strip() or not password:

                st.warning(
                    "⚠ ENTER USERNAME AND PASSWORD"
                )

            else:

                try:

                    uid = db.verify_user(
                        username.strip(),
                        password
                    )

                except Exception as exc:

                    st.error(
                        "DATABASE ERROR: "
                        + str(exc)
                    )
                    return

                if uid:

                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    st.session_state.username = username.strip()

                    if is_owner():
                        st.session_state.license_ok = True

                    st.success(
                        "✅ LOGIN SUCCESSFUL"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ ACCESS DENIED"
                    )

    with signup_tab:

        username = st.text_input(
            "CHOOSE USERNAME",
            key="signup_user"
        )

        password = st.text_input(
            "CHOOSE PASSWORD",
            key="signup_pass",
            type="password"
        )

        confirm = st.text_input(
            "CONFIRM PASSWORD",
            key="signup_confirm",
            type="password"
        )

        if st.button(
            "🚀 CREATE ACCOUNT",
            use_container_width=True
        ):

            username = username.strip()

            if not username or not password or not confirm:

                st.warning(
                    "⚠ FILL ALL FIELDS"
                )

            elif password != confirm:

                st.error(
                    "❌ PASSWORDS DO NOT MATCH"
                )

            elif len(password) < 4:

                st.error(
                    "❌ PASSWORD MUST BE AT LEAST 4 CHARACTERS"
                )

            else:

                try:

                    result = db.create_user(
                        username,
                        password
                    )

                    if isinstance(result, tuple):

                        ok, msg = result

                    else:

                        ok = bool(result)
                        msg = (
                            "ACCOUNT CREATED"
                            if ok
                            else "ACCOUNT CREATION FAILED"
                        )

                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

                except Exception as exc:

                    st.error(
                        "DATABASE ERROR: "
                        + str(exc)
                    )


# =========================================================
# LICENSE PAGE
# =========================================================

def license_page():

    show_header(
        "💀 PREMIUM ACCESS",
        "// 30 DAY LICENSE TERMINAL //"
    )

    st.info(
        "Premium access requires a valid license key."
    )

    key = st.text_input(
        "ENTER LICENSE KEY",
        type="password"
    )

    if st.button(
        "🔓 ACTIVATE 30 DAYS",
        use_container_width=True
    ):

        if key == OWNER_LICENSE:

            activate_license()

            st.success(
                "✅ 30-DAY LICENSE ACTIVATED"
            )

            st.rerun()

        else:

            st.error(
                "❌ INVALID LICENSE"
            )


# =========================================================
# MAIN APP
# =========================================================

def main_app():

    uid = st.session_state.user_id

    config = get_safe_config(uid)

    show_header(
        "☠ RK RAJA XWD ☠",
        "// HACKER TERMINAL ONLINE //"
    )

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    st.sidebar.markdown(
        "## 👤 USER TERMINAL"
    )

    st.sidebar.write(
        "**USERNAME:** "
        + str(
            st.session_state.username
        )
    )

    if is_owner():

        st.sidebar.markdown(
            """
            <div class="success-box">
                👑 OWNER • FREE ACCESS
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        expiry = st.session_state.get(
            "license_expiry"
        )

        if expiry:

            remaining = expiry - datetime.now()

            days = max(
                0,
                remaining.days
            )

            st.sidebar.success(
                f"💎 PREMIUM • {days} DAYS LEFT"
            )

    if st.sidebar.button(
        "🚪 LOGOUT",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.license_ok = False
        st.session_state.license_expiry = None
        st.session_state.running = False
        st.session_state.logs = []
        st.session_state.message_count = 0

        st.rerun()

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "🍪 TEST SET-UP",
            "🚀 LOCAL AUTOMATION",
            "🖼 PHOTO"
        ]
    )

    # =====================================================
    # SETUP
    # =====================================================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            chat_id = st.text_input(
                "TEST CHAT ID",
                value=config["chat_id"]
            )

            name_prefix = st.text_input(
                "NAME PREFIX",
                value=config["name_prefix"]
            )

            delay = st.number_input(
                "DELAY (SECONDS)",
                min_value=1,
                max_value=60,
                value=max(
                    1,
                    min(
                        60,
                        int(config["delay"])
                    )
                )
            )

        with col2:

            cookies = st.text_area(
                "🍪 TEST COOKIE VALUE",
                value="",
                height=150,
                placeholder="Dummy/test data only"
            )

            messages = st.text_area(
                "TYPE TEST MESSAGE — ONE PER LINE",
                value=config["messages"],
                height=180
            )

        st.info(
            "🔒 Safe local test mode. "
            "Cookie values are not used to access "
            "third-party accounts."
        )

        if st.button(
            "💾 SAVE SETTINGS",
            use_container_width=True
        ):

            try:

                db.update_user_config(
                    uid,
                    chat_id,
                    name_prefix,
                    int(delay),
                    cookies,
                    messages
                )

                st.success(
                    "✅ SETTINGS SAVED • FINGERPRINT: "
                    + cookie_fingerprint(cookies)
                )

            except Exception as exc:

                st.error(
                    "DATABASE ERROR: "
                    + str(exc)
                )

    # =====================================================
    # AUTOMATION
    # =====================================================

    with tab2:

        config = get_safe_config(uid)

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "TESTS",
                st.session_state.message_count
            )

        with c2:

            st.metric(
                "STATUS",
                (
                    "🟢 RUNNING"
                    if st.session_state.running
                    else "🔴 STOPPED"
                )
            )

        with c3:

            st.metric(
                "COOKIE",
                cookie_fingerprint(
                    config["cookies"]
                )
            )

        st.divider()

        messages = [
            item.strip()
            for item in str(
                config["messages"]
            ).splitlines()
            if item.strip()
        ]

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "▶️ START LOCAL TEST",
                disabled=st.session_state.running,
                use_container_width=True
            ):

                if not messages:

                    st.error(
                        "❌ ADD TEST MESSAGE"
                    )

                else:

                    start_demo(
                        messages,
                        int(config["delay"])
                    )

                    st.rerun()

        with c2:

            if st.button(
                "⏹️ STOP TEST",
                disabled=not st.session_state.running,
                use_container_width=True
            ):

                st.session_state.running = False

                add_log(
                    "STOPPED BY USER"
                )

                st.rerun()

        # -------------------------------------------------
        # TERMINAL
        # -------------------------------------------------

        if st.session_state.logs:

            st.markdown(
                "### 💻 LIVE TERMINAL"
            )

            html = '<div class="console-output">'

            for item in st.session_state.logs:

                safe = (
                    str(item)
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                html += (
                    '<div class="console-line">'
                    + safe
                    + "</div>"
                )

            html += "</div>"

            st.markdown(
                html,
                unsafe_allow_html=True
            )

            if st.button(
                "🔄 REFRESH TERMINAL"
            ):

                st.rerun()

    # =====================================================
    # PHOTO
    # =====================================================

    with tab3:

        st.markdown(
            """
            <div class="voice-box">
                🖼 RK RAJA PHOTO TERMINAL
            </div>
            """,
            unsafe_allow_html=True
        )

        if BG_IMAGE.exists():

            st.image(
                str(BG_IMAGE),
                caption="RK RAJA XWD",
                use_container_width=True
            )

        else:

            st.warning(
                "⚠ 155933.png NOT FOUND"
            )


# =========================================================
# DATABASE INIT
# =========================================================

try:

    db.init_db()

except Exception as exc:

    st.error(
        "❌ DATABASE INITIALIZATION ERROR"
    )

    st.code(str(exc))

    st.stop()


# =========================================================
# APP ROUTING
# =========================================================

if not st.session_state.logged_in:

    login_page()

elif is_owner():

    main_app()

elif license_valid():

    main_app()

else:

    license_page()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ⚡ RK RAJA XWD • SYSTEM ONLINE • MADE IN INDIA 🇮🇳 ⚡
    </div>
    """,
    unsafe_allow_html=True
)
