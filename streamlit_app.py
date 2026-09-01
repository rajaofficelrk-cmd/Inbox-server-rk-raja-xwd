import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import os
from datetime import datetime
from pathlib import Path
import database as db


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RK RAJA XWD",
    page_icon="😈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# FILES
# =========================================================

BG_IMAGE = Path("background.png")


# =========================================================
# OWNER / LICENSE
# =========================================================

OWNER_USERNAME = os.getenv(
    "OWNER_USERNAME",
    "rkraja"
)

OWNER_LICENSE = os.getenv(
    "OWNER_LICENSE",
    "RKRAJA-PREMIUM-2026"
)


# =========================================================
# HACKER CSS
# =========================================================

CUSTOM_CSS = """
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


/* MAIN BACKGROUND */

.stApp {

    background:
        linear-gradient(
            rgba(0,0,0,.73),
            rgba(0,0,0,.73)
        ),
        url("background.png");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    color: white !important;
}


/* SCAN LINES */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    background:
        repeating-linear-gradient(
            0deg,
            rgba(0,255,255,.025) 0px,
            rgba(0,255,255,.025) 1px,
            transparent 1px,
            transparent 4px
        );

    z-index: 0;
}


/* CONTAINER */

.main .block-container {

    position: relative;

    z-index: 1;

    background:
        linear-gradient(
            135deg,
            rgba(0,0,0,.84),
            rgba(2,15,28,.80),
            rgba(20,0,30,.80)
        );

    border:
        1px solid rgba(0,255,255,.35);

    border-radius:
        25px;

    padding:
        35px;

    box-shadow:
        0 0 25px rgba(0,255,255,.13),
        0 0 70px rgba(130,0,255,.10);

    backdrop-filter:
        blur(10px);
}


/* HEADER */

.main-header {

    padding:
        38px 20px;

    text-align:
        center;

    border-radius:
        22px;

    background:
        linear-gradient(
            120deg,
            rgba(0,255,255,.08),
            rgba(120,0,255,.10),
            rgba(255,0,170,.08)
        );

    border:
        1px solid rgba(0,255,255,.30);

    box-shadow:
        0 0 30px rgba(0,255,255,.12);
}


.main-header h1 {

    font-family:
        'Orbitron',
        monospace !important;

    font-size:
        3rem;

    font-weight:
        900;

    letter-spacing:
        5px;

    background:
        linear-gradient(
            90deg,
            #00ffff,
            #00ff88,
            #ffffff,
            #a855ff,
            #ff00aa,
            #00ffff
        );

    background-size:
        400% auto;

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;

    animation:
        rainbow 5s linear infinite;
}


.main-header p {

    color:
        #00ffff;

    font-family:
        'Share Tech Mono',
        monospace !important;

    letter-spacing:
        4px;

    text-shadow:
        0 0 8px #00ffff;
}


@keyframes rainbow {

    0% {
        background-position: 0% center;
    }

    100% {
        background-position: 400% center;
    }
}


/* ALL HEADINGS */

h1,
h2,
h3,
h4 {

    font-family:
        'Orbitron',
        monospace !important;

    letter-spacing:
        2px !important;
}


/* LABEL */

label {

    color:
        #00ffff !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        800 !important;

    letter-spacing:
        1px !important;

    text-shadow:
        0 0 7px #00ffff;
}


/* INPUT */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {

    background:
        rgba(0,0,0,.78) !important;

    color:
        #00ffcc !important;

    border:
        1px solid #00ffff !important;

    border-radius:
        10px !important;

    font-family:
        'Share Tech Mono',
        monospace !important;

    caret-color:
        #00ffff !important;
}


.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {

    border-color:
        #ff00ff !important;

    box-shadow:
        0 0 15px rgba(255,0,255,.30) !important;
}


/* BUTTON */

.stButton > button {

    min-height:
        48px;

    background:
        linear-gradient(
            90deg,
            #00c6ff,
            #0066ff,
            #8b00ff,
            #ff00aa,
            #00ff99
        ) !important;

    background-size:
        300% auto !important;

    color:
        white !important;

    border:
        1px solid rgba(255,255,255,.25) !important;

    border-radius:
        10px !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900 !important;

    letter-spacing:
        1px !important;

    box-shadow:
        0 0 18px rgba(0,255,255,.20);

    transition:
        .25s ease !important;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    background-position:
        right center !important;

    box-shadow:
        0 0 25px rgba(0,255,255,.45);
}


/* TABS */

.stTabs [data-baseweb="tab-list"] {

    gap:
        8px;

    background:
        rgba(0,0,0,.55);

    padding:
        8px;

    border-radius:
        14px;
}


.stTabs [data-baseweb="tab"] {

    color:
        #00ffff !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        800;
}


.stTabs [aria-selected="true"] {

    color:
        white !important;

    background:
        linear-gradient(
            90deg,
            #005eff,
            #8b00ff,
            #ff0099
        ) !important;

    border-radius:
        10px;
}


/* METRICS */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            rgba(0,255,255,.10),
            rgba(120,0,255,.10),
            rgba(255,0,170,.08)
        );

    border:
        1px solid rgba(0,255,255,.28);

    border-radius:
        16px;

    padding:
        18px;
}


[data-testid="stMetricLabel"] {

    color:
        #00ffff !important;

    font-family:
        'Orbitron',
        monospace !important;
}


[data-testid="stMetricValue"] {

    color:
        white !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900 !important;
}


/* VOICE BOX */

.voice-box {

    margin:
        18px 0;

    padding:
        18px;

    border:
        1px solid #00ffff;

    border-radius:
        15px;

    text-align:
        center;

    background:
        linear-gradient(
            90deg,
            rgba(0,255,255,.08),
            rgba(150,0,255,.10),
            rgba(255,0,150,.08)
        );

    color:
        #00ffff;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900;

    letter-spacing:
        2px;

    text-shadow:
        0 0 10px #00ffff;
}


/* CONSOLE */

.console-output {

    background:
        rgba(0,0,0,.88);

    border:
        1px solid #00ffff;

    border-radius:
        14px;

    padding:
        18px;

    max-height:
        400px;

    overflow-y:
        auto;
}


.console-line {

    padding:
        9px 12px;

    margin-bottom:
        7px;

    background:
        rgba(0,255,255,.06);

    border-left:
        3px solid #00ffff;

    border-radius:
        6px;

    color:
        #00ff99;

    font-family:
        'Share Tech Mono',
        monospace !important;

    text-shadow:
        0 0 5px rgba(0,255,120,.35);
}


/* SUCCESS */

.success-box {

    background:
        rgba(0,255,120,.08);

    border:
        1px solid #00ff99;

    border-radius:
        10px;

    padding:
        14px;

    text-align:
        center;

    color:
        #00ff99;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            160deg,
            #02060d,
            #071426,
            #13051c
        ) !important;
}


/* PHOTO PREVIEW */

.photo-card {

    border:
        1px solid #00ffff;

    border-radius:
        18px;

    padding:
        10px;

    background:
        rgba(0,0,0,.65);

    box-shadow:
        0 0 20px rgba(0,255,255,.15);

    text-align:
        center;
}


/* FOOTER */

.footer {

    text-align:
        center;

    margin-top:
        30px;

    padding:
        20px;

    font-family:
        'Orbitron',
        monospace !important;

    font-size:
        13px;

    letter-spacing:
        3px;

    font-weight:
        900;

    background:
        linear-gradient(
            90deg,
            #00ffff,
            #00ff88,
            #ffffff,
            #a855ff,
            #ff00aa,
            #00ffff
        );

    background-size:
        300% auto;

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;

    animation:
        rainbow 5s linear infinite;
}


/* STREAMLIT BRAND */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
"""

st.markdown(
    CUSTOM_CSS,
    unsafe_allow_html=True
)


# =========================================================
# WELCOME VOICE
# =========================================================

WELCOME_VOICE = """
<script>

(function () {

    const text =
        "RK RAJA XWD ke end to end mein aapka welcome hai.";

    function speak() {

        if (!("speechSynthesis" in window)) {
            return;
        }

        window.speechSynthesis.cancel();

        const msg =
            new SpeechSynthesisUtterance(text);

        msg.lang = "hi-IN";
        msg.rate = 0.88;
        msg.pitch = 1.0;
        msg.volume = 1.0;

        window.speechSynthesis.speak(msg);
    }


    setTimeout(
        speak,
        1200
    );


    document.addEventListener(
        "click",
        function () {

            if (
                !window.__rkWelcomePlayed
            ) {

                window.__rkWelcomePlayed = true;

                speak();
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

defaults = {
    "logged_in": False,
    "user_id": None,
    "username": None,
    "license_ok": False,
    "logs": [],
    "running": False,
    "message_count": 0,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# FUNCTIONS
# =========================================================

def add_log(message):

    stamp = datetime.now().strftime(
        "%H:%M:%S"
    )

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


def is_owner():

    username = st.session_state.username

    if not username:
        return False

    return (
        username.lower()
        == OWNER_USERNAME.lower()
    )


def demo_worker(messages, delay):

    for message in messages:

        if not st.session_state.running:
            break

        time.sleep(delay)

        st.session_state.message_count += 1

        add_log(
            "TEST #"
            + str(
                st.session_state.message_count
            )
            + ": "
            + message[:60]
        )


def start_demo(messages, delay):

    if st.session_state.running:
        return

    st.session_state.running = True
    st.session_state.message_count = 0
    st.session_state.logs = []

    add_log(
        "Local demo automation started."
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
                "Local demo automation stopped."
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# =========================================================
# LICENSE PAGE
# =========================================================

def license_page():

    st.markdown(
        """
        <div class="main-header">
            <h1>☠ PREMIUM ACCESS ☠</h1>
            <p>// LICENSE TERMINAL //</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="voice-box">
            🔐 PREMIUM LICENSE REQUIRED
        </div>
        """,
        unsafe_allow_html=True
    )

    license_key = st.text_input(
        "ENTER LICENSE KEY",
        type="password"
    )

    if st.button(
        "🔓 ACTIVATE PREMIUM",
        use_container_width=True
    ):

        if license_key == OWNER_LICENSE:

            st.session_state.license_ok = True

            st.success(
                "✅ PREMIUM ACCESS ACTIVATED"
            )

            st.rerun()

        else:

            st.error(
                "❌ INVALID LICENSE KEY"
            )


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        """
        <div class="main-header">

            <h1>☠ RK RAJA XWD ☠</h1>

            <p>
                // SECURE ACCESS TERMINAL //
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="voice-box">

            🔊 RK RAJA XWD KE END TO END
            MEIN AAPKA WELCOME HAI

        </div>
        """,
        unsafe_allow_html=True
    )


    login_tab, signup_tab = st.tabs(
        [
            "🔐 LOGIN",
            "➕ SIGN-UP"
        ]
    )


    # LOGIN

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
            "⚡ LOGIN TO SYSTEM",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "⚠ ENTER BOTH FIELDS"
                )

            else:

                uid = db.verify_user(
                    username,
                    password
                )

                if uid:

                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    st.session_state.username = username

                    if is_owner():
                        st.session_state.license_ok = True

                    st.rerun()

                else:

                    st.error(
                        "❌ ACCESS DENIED"
                    )


    # SIGN UP

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

            if not username or not password or not confirm:

                st.warning(
                    "⚠ FILL ALL FIELDS"
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

                if ok:
                    st.success(msg)
                else:
                    st.error(msg)


# =========================================================
# MAIN APP
# =========================================================

def main_app():

    uid = st.session_state.user_id

    config = db.get_user_config(uid)


    st.markdown(
        """
        <div class="main-header">

            <h1>☠ RK RAJA XWD ☠</h1>

            <p>
                // PREMIUM MULTI-COLOUR TERMINAL //
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # SIDEBAR

    st.sidebar.markdown(
        "## 👤 USER TERMINAL"
    )

    st.sidebar.write(
        "**USERNAME:** "
        + str(
            st.session_state.username
        )
    )

    st.sidebar.write(
        "**USER ID:** "
        + str(uid)
    )


    if is_owner():

        st.sidebar.markdown(
            '<div class="success-box">'
            '👑 OWNER • FREE ACCESS'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.sidebar.markdown(
            '<div class="success-box">'
            '💎 PREMIUM ACCESS'
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
        st.session_state.license_ok = False
        st.session_state.running = False

        st.rerun()


    tab1, tab2, tab3 = st.tabs(
        [
            "🍪 TEST SET-UP",
            "🚀 AUTOMATION",
            "🖼 PHOTO"
        ]
    )


    # =====================================================
    # TEST SETUP
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
                value=int(
                    config["delay"]
                )
            )


        with col2:

            cookies = st.text_area(
                "🍪 TEST COOKIE VALUE",
                value="",
                type="password",
                height=150,
                placeholder="Dummy/test data only"
            )

            messages = st.text_area(
                "TYPE TEST MESSAGE — ONE PER LINE",
                value=config["messages"],
                height=180
            )


        st.info(
            "🔒 Safety mode: cookie data is not "
            "used to access or control third-party accounts."
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
                "✅ SETTINGS SAVED • Fingerprint: "
                + cookie_fingerprint(cookies)
            )


    # =====================================================
    # AUTOMATION
    # =====================================================

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
                "▶️ START LOCAL TEST",
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
                "### 💻 LIVE TERMINAL"
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
                    + safe
                    + '</div>'
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
                🖼 AUTO PHOTO PREVIEW
            </div>
            """,
            unsafe_allow_html=True
        )


        uploaded = st.file_uploader(
            "SELECT PHOTO",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ]
        )


        if uploaded:

            st.image(
                uploaded,
                caption="RK RAJA XWD",
                use_container_width=True
            )

            st.success(
                "✅ PHOTO LOADED"
            )

        elif BG_IMAGE.exists():

            st.image(
                str(BG_IMAGE),
                caption="RK RAJA XWD",
                use_container_width=True
            )

            st.success(
                "✅ BACKGROUND PHOTO ACTIVE"
            )

        else:

            st.warning(
                "⚠ background.png project folder mein add karo."
            )


# =========================================================
# START
# =========================================================

db.init_db()


if not st.session_state.logged_in:

    login_page()

else:

    if is_owner():

        st.session_state.license_ok = True
        main_app()

    elif st.session_state.license_ok:

        main_app()

    else:

        license_page()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ⚡ RK RAJA XWD No 8368312643• MADE IN INDIA 🇮🇳 • SYSTEM ONLINE ⚡
    </div>
    """,
    unsafe_allow_html=True
)
