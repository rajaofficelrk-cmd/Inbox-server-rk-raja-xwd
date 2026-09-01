import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import os
import base64

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

OWNER_USERNAME = os.getenv(
    "OWNER_USERNAME",
    "rkraja"
)

OWNER_LICENSE = os.getenv(
    "OWNER_LICENSE",
    "RKRAJA-PREMIUM-2026"
)

LICENSE_DAYS = 30

BG_IMAGE = Path("155933.png")
WELCOME_AUDIO = Path("welcome.mp3")


# =========================================================
# HACKER GREEN / BLACK CSS
# =========================================================

CUSTOM_CSS = """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Share+Tech+Mono&display=swap'
);


/* GLOBAL */

* {
    box-sizing: border-box;
}

html,
body,
[class*="css"] {
    font-family:
        'Share Tech Mono',
        monospace !important;
}


/* BLACK + GREEN BACKGROUND */

.stApp {

    background-color: #000000 !important;

    background-image:
        linear-gradient(
            rgba(0,0,0,.78),
            rgba(0,0,0,.82)
        ),
        url("155933.png");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    color: #00ff41 !important;
}


/* MATRIX LINES */

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


/* MAIN PANEL */

.main .block-container {

    position: relative;

    z-index: 1;

    background:
        rgba(0,0,0,.84);

    border:
        1px solid rgba(0,255,65,.38);

    border-radius:
        20px;

    padding:
        32px;

    box-shadow:
        0 0 25px rgba(0,255,65,.10),
        inset 0 0 25px rgba(0,255,65,.025);

    backdrop-filter:
        blur(8px);
}


/* HEADER */

.main-header {

    padding:
        36px 20px;

    text-align:
        center;

    border:
        1px solid #00ff41;

    border-radius:
        18px;

    background:
        rgba(0,0,0,.76);

    box-shadow:
        0 0 22px rgba(0,255,65,.18),
        inset 0 0 20px rgba(0,255,65,.04);
}


/* HACKER TITLE */

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

    color:
        #00ff41;

    text-shadow:
        0 0 5px #00ff41,
        0 0 15px #00ff41,
        0 0 35px rgba(0,255,65,.65);

    animation:
        hackerGlow 2s ease-in-out infinite alternate;
}


@keyframes hackerGlow {

    from {
        text-shadow:
            0 0 5px #00ff41,
            0 0 12px #00ff41;
    }

    to {
        text-shadow:
            0 0 8px #00ff41,
            0 0 25px #00ff41,
            0 0 45px #00ff41;
    }
}


.main-header p {

    color:
        #00ff41;

    font-family:
        'Share Tech Mono',
        monospace !important;

    letter-spacing:
        4px;

    text-shadow:
        0 0 8px #00ff41;
}


/* HEADINGS */

h1,
h2,
h3,
h4 {

    font-family:
        'Orbitron',
        monospace !important;

    color:
        #00ff41 !important;

    text-shadow:
        0 0 8px rgba(0,255,65,.55);

    letter-spacing:
        2px !important;
}


/* LABELS */

label {

    color:
        #00ff41 !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        800 !important;

    text-shadow:
        0 0 6px #00ff41;
}


/* INPUTS */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {

    background:
        #000000 !important;

    color:
        #00ff41 !important;

    border:
        1px solid #00ff41 !important;

    border-radius:
        8px !important;

    font-family:
        'Share Tech Mono',
        monospace !important;

    caret-color:
        #00ff41 !important;

    box-shadow:
        inset 0 0 8px rgba(0,255,65,.06);
}


.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {

    border-color:
        #00ff41 !important;

    box-shadow:
        0 0 12px rgba(0,255,65,.30) !important;
}


/* BUTTONS */

.stButton > button {

    min-height:
        46px;

    background:
        #000000 !important;

    color:
        #00ff41 !important;

    border:
        1px solid #00ff41 !important;

    border-radius:
        8px !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900 !important;

    letter-spacing:
        1px !important;

    text-shadow:
        0 0 5px #00ff41;

    box-shadow:
        0 0 10px rgba(0,255,65,.12);

    transition:
        .2s ease !important;
}


.stButton > button:hover {

    background:
        #00ff41 !important;

    color:
        #000000 !important;

    text-shadow:
        none;

    box-shadow:
        0 0 22px rgba(0,255,65,.60);

    transform:
        translateY(-2px);
}


/* TABS */

.stTabs [data-baseweb="tab-list"] {

    gap:
        5px;

    background:
        #000000;

    padding:
        7px;

    border:
        1px solid rgba(0,255,65,.30);

    border-radius:
        10px;
}


.stTabs [data-baseweb="tab"] {

    color:
        #00ff41 !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        800;
}


.stTabs [aria-selected="true"] {

    color:
        #000000 !important;

    background:
        #00ff41 !important;

    border-radius:
        7px;
}


/* METRICS */

[data-testid="stMetric"] {

    background:
        #000000;

    border:
        1px solid rgba(0,255,65,.38);

    border-radius:
        12px;

    padding:
        16px;

    box-shadow:
        0 0 12px rgba(0,255,65,.08);
}


[data-testid="stMetricLabel"] {

    color:
        #00ff41 !important;

    font-family:
        'Orbitron',
        monospace !important;
}


[data-testid="stMetricValue"] {

    color:
        #00ff41 !important;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900 !important;

    text-shadow:
        0 0 8px #00ff41;
}


/* VOICE */

.voice-box {

    margin:
        18px 0;

    padding:
        18px;

    border:
        1px solid #00ff41;

    border-radius:
        12px;

    text-align:
        center;

    background:
        rgba(0,0,0,.80);

    color:
        #00ff41;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900;

    letter-spacing:
        2px;

    text-shadow:
        0 0 10px #00ff41;

    box-shadow:
        0 0 18px rgba(0,255,65,.12);
}


/* CONSOLE */

.console-output {

    background:
        #000000;

    border:
        1px solid #00ff41;

    border-radius:
        10px;

    padding:
        16px;

    max-height:
        400px;

    overflow-y:
        auto;

    box-shadow:
        inset 0 0 15px rgba(0,255,65,.05);
}


.console-line {

    padding:
        8px 10px;

    margin-bottom:
        6px;

    background:
        rgba(0,255,65,.035);

    border-left:
        3px solid #00ff41;

    border-radius:
        4px;

    color:
        #00ff41;

    font-family:
        'Share Tech Mono',
        monospace !important;

    text-shadow:
        0 0 5px rgba(0,255,65,.45);
}


/* SUCCESS */

.success-box {

    background:
        rgba(0,255,65,.05);

    border:
        1px solid #00ff41;

    border-radius:
        8px;

    padding:
        12px;

    text-align:
        center;

    color:
        #00ff41;

    font-family:
        'Orbitron',
        monospace !important;

    font-weight:
        900;

    box-shadow:
        0 0 10px rgba(0,255,65,.10);
}


/* SIDEBAR */

section[data-testid="stSidebar"] {

    background:
        #000000 !important;

    border-right:
        1px solid rgba(0,255,65,.25);
}


/* INFO */

.stAlert {

    background:
        #000000 !important;

    border:
        1px solid rgba(0,255,65,.30) !important;

    color:
        #00ff41 !important;
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

    letter-spacing:
        3px;

    font-weight:
        900;

    color:
        #00ff41;

    text-shadow:
        0 0 8px #00ff41,
        0 0 20px rgba(0,255,65,.55);
}


/* HIDE STREAMLIT MENU */

#MainMenu {
    visibility:
        hidden;
}

footer {
    visibility:
        hidden;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# WELCOME AUDIO
# =========================================================

def get_audio_html():

    if not WELCOME_AUDIO.exists():

        return """
        <div class="voice-box">
            🔊 welcome.mp3 NOT FOUND
        </div>
        """

    try:

        audio_data = base64.b64encode(
            WELCOME_AUDIO.read_bytes()
        ).decode("utf-8")

        return f"""
        <div class="voice-box">

            🔊 RK RAJA XWD KE END TO END
            MEIN AAPKA WELCOME HAI

            <br><br>

            <audio
                id="rkWelcomeAudio"
                controls
                preload="auto"
                style="width:100%;"
            >

                <source
                    src="data:audio/mpeg;base64,{audio_data}"
                    type="audio/mpeg"
                >

            </audio>

        </div>

        <script>

        const audio =
            document.getElementById(
                "rkWelcomeAudio"
            );

        setTimeout(
            function () {

                audio.play()
                .catch(
                    function () {
                        console.log(
                            "Browser autoplay blocked. Tap play."
                        );
                    }
                );

            },
            1500
        );

        document.addEventListener(
            "click",
            function () {

                audio.play()
                .catch(
                    function () {}
                );

            },
            { once: true }
        );

        </script>
        """

    except Exception:

        return """
        <div class="voice-box">
            ⚠️ AUDIO LOAD ERROR
        </div>
        """


st.markdown(
    get_audio_html(),
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "logged_in": False,

    "user_id": None,

    "username": None,

    "license_ok": False,

    "license_expiry": None,

    "logs": [],

    "running": False,

    "message_count": 0,
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# HELPERS
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

    username = (
        st.session_state.username
    )

    return bool(
        username
        and username.lower()
        == OWNER_USERNAME.lower()
    )


def activate_license():

    st.session_state.license_ok = True

    st.session_state.license_expiry = (
        datetime.now()
        + timedelta(
            days=LICENSE_DAYS
        )
    )


def license_valid():

    if is_owner():

        return True

    if not st.session_state.license_ok:

        return False

    expiry = (
        st.session_state.license_expiry
    )

    if not expiry:

        return False

    return datetime.now() < expiry


# =========================================================
# LOCAL TEST
# =========================================================

def demo_worker(
    messages,
    delay
):

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
            + " : "
            + message[:60]
        )


def start_demo(
    messages,
    delay
):

    if st.session_state.running:

        return

    st.session_state.running = True

    st.session_state.message_count = 0

    st.session_state.logs = []

    add_log(
        "LOCAL TEST STARTED"
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
                "LOCAL TEST STOPPED"
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# =========================================================
# LOGIN
# =========================================================

def login_page():

    st.markdown(
        """
        <div class="main-header">

            <h1>☠ RK RAJA XWD ☠</h1>

            <p>
                // SECURE HACKER TERMINAL //
            </p>

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

            if not username or not password:

                st.warning(
                    "⚠ ENTER USERNAME AND PASSWORD"
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

            if (
                not username
                or not password
                or not confirm
            ):

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
# LICENSE
# =========================================================

def license_page():

    st.markdown(
        """
        <div class="main-header">

            <h1>💀 PREMIUM ACCESS</h1>

            <p>
                // 30 DAY LICENSE TERMINAL //
            </p>

        </div>
        """,
        unsafe_allow_html=True
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

    config = db.get_user_config(uid)


    st.markdown(
        """
        <div class="main-header">

            <h1>☠ RK RAJA XWD ☠</h1>

            <p>
                // HACKER TERMINAL ONLINE //
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


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

        expiry = (
            st.session_state.license_expiry
        )

        if expiry:

            remaining = (
                expiry - datetime.now()
            )

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

        st.rerun()


    tab1, tab2, tab3 = st.tabs(
        [
            "🍪 TEST SET-UP",
            "🚀 AUTOMATION",
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
                value=int(
                    config["delay"]
                )
            )


        with col2:

            # FIXED:
            # st.text_area DOES NOT have type=password

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
            "🔒 Safe test mode: cookie values are "
            "not used to access third-party accounts."
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
                "✅ SETTINGS SAVED • FINGERPRINT: "
                + cookie_fingerprint(
                    cookies
                )
            )


    # =====================================================
    # AUTOMATION
    # =====================================================

    with tab2:

        config = db.get_user_config(uid)


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

            x.strip()

            for x in
            config["messages"].splitlines()

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
                        "❌ ADD TEST MESSAGE"
                    )

                else:

                    start_demo(
                        messages,
                        int(
                            config["delay"]
                        )
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


        if st.session_state.logs:

            st.markdown(
                "### 💻 LIVE TERMINAL"
            )


            html = (
                '<div class="console-output">'
            )


            for item in (
                st.session_state.logs
            ):

                safe = (
                    item
                    .replace(
                        "&",
                        "&amp;"
                    )
                    .replace(
                        "<",
                        "&lt;"
                    )
                    .replace(
                        ">",
                        "&gt;"
                    )
                )


                html += (
                    '<div class="console-line">'
                    + safe
                    + '</div>'
                )


            html += (
                '</div>'
            )


            st.markdown(
                html,
                unsafe_allow_html=True
            )


            if st.button(
                "🔄 REFRESH"
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

            st.error(
                "❌ 155933.png NOT FOUND"
            )


# =========================================================
# RUN
# =========================================================

db.init_db()


if not st.session_state.logged_in:

    login_page()

else:

    if is_owner():

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
        ⚡ RK RAJA XWD • no 8368312643 • MADE IN INDIA 🇮🇳 ⚡
    </div>
    """,
    unsafe_allow_html=True
                )
