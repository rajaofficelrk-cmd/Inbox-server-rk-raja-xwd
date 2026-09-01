import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
from datetime import datetime
from pathlib import Path
import database as db

st.set_page_config(
    page_title="Tha LeGenD boY Raja 😈",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Outfit', sans-serif !important;
}

.stApp {
    background-image:
        linear-gradient(rgba(0,0,0,.48), rgba(0,0,0,.48)),
        url("background.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white !important;
}

.main .block-container {
    background: rgba(5,10,25,.76);
    border-radius: 28px;
    padding: 35px;
    border: 1px solid rgba(255,255,255,.18);
    box-shadow: 0 10px 45px rgba(0,0,0,.35);
    backdrop-filter: blur(7px);
}

.main-header {
    padding: 42px 20px;
    text-align: center;
    border-radius: 25px;
    background: linear-gradient(
        120deg,
        rgba(0,234,255,.18),
        rgba(120,40,255,.18),
        rgba(255,30,160,.18),
        rgba(0,255,160,.16)
    );
    border: 1px solid rgba(255,255,255,.20);
    box-shadow: 0 0 30px rgba(0,234,255,.15);
}

.main-header h1 {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(
        90deg,
        #00eaff,
        #7b2cff,
        #ff29a8,
        #00ffa6,
        #00eaff
    );
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbowText 5s linear infinite;
}

.main-header p {
    color: #e7fbff;
    font-size: 1.1rem;
    font-weight: 700;
}

@keyframes rainbowText {
    from {
        background-position: 0% center;
    }
    to {
        background-position: 300% center;
    }
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: rgba(255,255,255,.08) !important;
    color: white !important;
    border: 1px solid #00eaff !important;
    border-radius: 13px !important;
}

label {
    color: #72f7ff !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: linear-gradient(
        100deg,
        #00bfff,
        #6c2cff,
        #ff229c,
        #00cfa0
    ) !important;
    background-size: 250% auto !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    box-shadow: 0 0 20px rgba(0,200,255,.18);
    transition: .25s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    background-position: right center !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,.06);
    padding: 8px;
    border-radius: 16px;
}

.stTabs [data-baseweb="tab"] {
    color: #8defff !important;
    border-radius: 12px;
    font-weight: 800;
}

.stTabs [aria-selected="true"] {
    color: white !important;
    background: linear-gradient(
        90deg,
        #007cff,
        #762cff,
        #ff229c
    ) !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(0,234,255,.12),
        rgba(118,44,255,.12),
        rgba(255,34,156,.10)
    );
    border: 1px solid rgba(0,234,255,.25);
    border-radius: 18px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #72f7ff !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 900 !important;
}

.console-output {
    background: rgba(0,0,0,.72);
    border: 1px solid #00eaff;
    border-radius: 16px;
    padding: 18px;
    max-height: 400px;
    overflow-y: auto;
}

.console-line {
    padding: 9px 12px;
    margin-bottom: 7px;
    border-radius: 8px;
    background: linear-gradient(
        90deg,
        rgba(0,234,255,.10),
        rgba(118,44,255,.08),
        rgba(255,34,156,.06)
    );
    border-left: 4px solid #00eaff;
    color: #dfffff;
    font-family: Consolas, monospace !important;
}

.success-box {
    background: rgba(0,255,166,.15);
    border: 1px solid #00ffa6;
    border-radius: 13px;
    padding: 15px;
    text-align: center;
    color: #00ffa6;
    font-weight: 800;
}

.footer {
    text-align: center;
    margin-top: 30px;
    padding: 20px;
    font-weight: 900;
    background: linear-gradient(
        90deg,
        #00eaff,
        #7b2cff,
        #ff29a8,
        #00ffa6
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        160deg,
        #080d20,
        #111735,
        #190b25
    ) !important;
}

.voice-box {
    margin: 18px 0;
    padding: 16px;
    border-radius: 18px;
    text-align: center;
    background: linear-gradient(
        120deg,
        rgba(0,234,255,.12),
        rgba(123,44,255,.14),
        rgba(255,41,168,.12)
    );
    border: 1px solid rgba(0,234,255,.35);
    color: white;
    font-weight: 800;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# 🔊 RK RAJA XWD AUTO WELCOME VOICE
# =========================================================

WELCOME_VOICE = """
<script>
(function () {

    const welcomeText =
        "RK RAJA XWD ke end to end mein aapka welcome hai.";

    function speakWelcome() {

        if (!("speechSynthesis" in window)) {
            return;
        }

        window.speechSynthesis.cancel();

        const speech =
            new SpeechSynthesisUtterance(welcomeText);

        speech.lang = "hi-IN";
        speech.rate = 0.88;
        speech.pitch = 1.0;
        speech.volume = 1.0;

        window.speechSynthesis.speak(speech);
    }

    // Page load hone ke baad voice try karega
    setTimeout(function () {
        speakWelcome();
    }, 1000);

    // User interaction ke baad fallback
    document.addEventListener(
        "click",
        function () {
            if (!window.__rkWelcomePlayed) {
                window.__rkWelcomePlayed = true;
                speakWelcome();
            }
        },
        { once: true }
    );

})();
</script>
"""

components.html(
    WELCOME_VOICE,
    height=1,
    scrolling=False
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "logs" not in st.session_state:
    st.session_state.logs = []

if "running" not in st.session_state:
    st.session_state.running = False

if "message_count" not in st.session_state:
    st.session_state.message_count = 0


# =========================================================
# FUNCTIONS
# =========================================================

def add_log(message):
    stamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(
        f"[{stamp}] {message}"
    )

    st.session_state.logs = (
        st.session_state.logs[-50:]
    )


def cookie_fingerprint(value):

    if not value:
        return "NOT SET"

    return hashlib.sha256(
        value.encode()
    ).hexdigest()[:12]


def demo_worker(messages, delay):

    for message in messages:

        if not st.session_state.running:
            break

        time.sleep(delay)

        st.session_state.message_count += 1

        add_log(
            f"TEST #{st.session_state.message_count}: "
            f"{message[:60]}"
        )


def start_demo(messages, delay):

    if st.session_state.running:
        return

    st.session_state.running = True
    st.session_state.message_count = 0
    st.session_state.logs = []

    add_log(
        "Demo automation started."
    )

    def worker():

        try:
            demo_worker(
                messages,
                delay
            )

        finally:

            st.session_state.running = False

            add_log(
                "Demo automation stopped."
            )

    thread = threading.Thread(
        target=worker,
        daemon=True
    )

    thread.start()


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        """
        <div class="main-header">
            <h1>🤍 professor 🏵️</h1>
            <p>COOKIE TEST • LOCAL DEMO PANEL</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Voice welcome box
    st.markdown(
        """
        <div class="voice-box">
            🔊 RK RAJA XWD KE END TO END MEIN AAPKA WELCOME HAI
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["LOGIN", "SIGN-UP"]
    )

    with tab1:

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
            "LOGIN",
            use_container_width=True
        ):

            if username and password:

                uid = db.verify_user(
                    username,
                    password
                )

                if uid:

                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "❌ INVALID USERNAME OR PASSWORD"
                    )

            else:

                st.warning(
                    "⚠️ ENTER BOTH FIELDS"
                )

    with tab2:

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
            "CREATE ACCOUNT",
            use_container_width=True
        ):

            if not username or not password or not confirm:

                st.warning(
                    "⚠️ FILL ALL FIELDS"
                )

            elif password != confirm:

                st.error(
                    "❌ PASSWORDS DO NOT MATCH"
                )

            else:

                ok, msg = db.create_user(
                    username,
                    password
                )

                (
                    st.success
                    if ok
                    else st.error
                )(msg)


# =========================================================
# MAIN APP
# =========================================================

def main_app():

    uid = st.session_state.user_id

    config = db.get_user_config(uid)

    st.markdown(
        """
        <div class="main-header">
            <h1>🤯 professor 🩷</h1>
            <p>MULTI-COLOUR COOKIE TEST SERVER</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "### 👤 USER DASHBOARD"
    )

    st.sidebar.write(
        f"**USERNAME:** "
        f"{st.session_state.username}"
    )

    st.sidebar.write(
        f"**USER ID:** {uid}"
    )

    st.sidebar.markdown(
        '<div class="success-box">'
        '✅ PREMIUM DEMO ACCESS'
        '</div>',
        unsafe_allow_html=True
    )

    if st.sidebar.button(
        "🚪 LOGOUT",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.running = False

        st.rerun()

    tab1, tab2 = st.tabs(
        [
            "🍪 COOKIE SET-UP",
            "🚀 TEST AUTOMATION"
        ]
    )

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            chat_id = st.text_input(
                "TEST CHAT ID",
                value=config["chat_id"],
                placeholder="Demo ID"
            )

            name_prefix = st.text_input(
                "NAME PREFIX",
                value=config["name_prefix"],
                placeholder="Professor"
            )

            delay = st.number_input(
                "DELAY (SECONDS)",
                min_value=1,
                max_value=60,
                value=int(config["delay"])
            )

        with col2:

            cookies = st.text_area(
                "🍪 TEST COOKIE VALUE",
                value="",
                type="password",
                height=150,
                placeholder="Use only dummy/test data"
            )

            messages = st.text_area(
                "TYPE TEST MESSAGE — ONE PER LINE",
                value=config["messages"],
                height=180
            )

        st.info(
            "🔒 Safety mode: the cookie value is never "
            "injected into Facebook or used to access "
            "a third-party account."
        )

        if st.button(
            "💾 SAVE SETTINGS",
            use_container_width=True
        ):

            db.update_user_config(
                uid,
                chat_id,
                name_prefix,
                delay,
                cookies,
                messages
            )

            st.success(
                "✅ SAVED • Cookie fingerprint: "
                f"{cookie_fingerprint(cookies)}"
            )

    with tab2:

        config = db.get_user_config(uid)

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "TESTS COMPLETED",
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
            x.strip()
            for x in config["messages"].splitlines()
            if x.strip()
        ]

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "▶️ START TEST",
                disabled=st.session_state.running,
                use_container_width=True
            ):

                if not messages:

                    st.error(
                        "❌ ADD AT LEAST ONE TEST MESSAGE"
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
                    "Stopped by user."
                )

                st.rerun()

        if st.session_state.logs:

            st.markdown(
                "### 📊 LIVE CONSOLE"
            )

            html = (
                '<div class="console-output">'
            )

            for item in st.session_state.logs:

                safe = (
                    item
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                html += (
                    '<div class="console-line">'
                    f'{safe}'
                    '</div>'
                )

            html += "</div>"

            st.markdown(
                html,
                unsafe_allow_html=True
            )

            if st.button("🔄 REFRESH"):
                st.rerun()


# =========================================================
# START APP
# =========================================================

db.init_db()

if not st.session_state.logged_in:
    login_page()
else:
    main_app()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'MADE IN INDIA 🇮🇳 • PROFESSOR PANEL'
    '</div>',
    unsafe_allow_html=True
)
