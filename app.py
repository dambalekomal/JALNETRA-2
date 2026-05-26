import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
import pandas as pd

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="JALNETRA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS LOAD ---------------- #

with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------- SESSION STATE ---------------- #

if "page" not in st.session_state:
    st.session_state.page = "home"

if "otp" not in st.session_state:
    st.session_state.otp = ""

if "verified" not in st.session_state:
    st.session_state.verified = False

# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero-section">

        <h1 class='main-title'>
            JALNETRA
        </h1>

        <p class='subtitle'>
            AI-Driven Virtual Assistant for Groundwater Management
        </p>

        <br>

        <p class='desc'>
            Intelligent groundwater management powered by AI.
        </p>

    </div>
    """,
      unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,1,1])

    with col2:

        if st.button(
            "Get Started",
            use_container_width=True
        ):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align:center'>
        Powerful Features
    </h1>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🤖 AI Chatbot</h3>
            <p>Query groundwater data instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📊 Visualizations</h3>
            <p>Interactive charts and graphs.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='feature-card'>
            <h3>🗂 Historical Data</h3>
            <p>Access historical groundwater records.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# LOGIN PAGE
# =========================================================

elif st.session_state.page == "login":

    st.markdown("""
    <div class='login-container'>

        <div class='login-card'>

            <h1 class='login-title'>
                Welcome to VARUNA
            </h1>

            <p class='login-subtitle'>
                Login with Email OTP
            </p>

        </div>

    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,1,1])

    with col2:

        email = st.text_input(
            "Email Address"
        )

        # SEND OTP

        if st.button(
            "Send OTP",
            use_container_width=True
        ):

            otp = str(
                random.randint(100000,999999)
            )

            st.session_state.otp = otp

            sender_email = "dambalekomal5@gmail.com"

            sender_password = "fjwguqhoqkdkfvwd"

            msg = MIMEText(
                f"Your VARUNA OTP is: {otp}"
            )

            msg['Subject'] = "VARUNA OTP"

            msg['From'] = sender_email

            msg['To'] = email

            try:

                server = smtplib.SMTP(
                    'smtp.gmail.com',
                    587
                )

                server.starttls()

                server.login(
                    sender_email,
                    sender_password
                )

                server.send_message(msg)

                server.quit()

                st.success(
                    "OTP Sent Successfully!"
                )

            except:

                st.error(
                    "Email Failed"
                )

        entered_otp = st.text_input(
            "Enter OTP"
        )

        # VERIFY OTP

        if st.button(
            "Verify OTP",
            use_container_width=True
        ):

            if entered_otp == st.session_state.otp:

                st.success(
                    "Login Successful!"
                )

                st.session_state.verified = True

                st.session_state.page = "dashboard"

                st.rerun()

            else:

                st.error(
                    "Invalid OTP"
                )

# =========================================================
# DASHBOARD
# =========================================================

elif st.session_state.page == "dashboard":

    st.sidebar.title("💧 VARUNA")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Assessments",
            "Visualizations",
            "AI Chatbot"
        ]
    )

    # ---------------- DASHBOARD ---------------- #

    if page == "Dashboard":

        st.title("Dashboard")

        col1,col2,col3,col4 = st.columns(4)

        cards = [
            ("Safe","3"),
            ("Semi-Critical","2"),
            ("Critical","2"),
            ("Over-Exploited","1")
        ]

        for col,(title,value) in zip(
            [col1,col2,col3,col4],
            cards
        ):

            with col:

                st.markdown(f"""
                <div class='metric-card'>

                    <div class='metric-title'>
                        {title}
                    </div>

                    <div class='metric-value'>
                        {value}
                    </div>

                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        left,right = st.columns([3,1])

        with left:

            st.markdown("""
            <div class='chat-box'>
                <h2>🤖 AI ChatBot</h2>
                <p>Hello! I'm VARUNA AI Assistant</p>
            </div>
            """, unsafe_allow_html=True)

            msg = st.chat_input(
                "Ask groundwater question"
            )

            if msg:

                st.chat_message("user").write(msg)

                st.chat_message("assistant").write(
                    "Groundwater analysis generated successfully."
                )

        with right:

            st.subheader("Quick Actions")

            st.button("Show Critical Areas")
            st.button("Compare Trends")
            st.button("Predict Future")
            st.button("Regional Distribution")

    # ---------------- ASSESSMENTS ---------------- #

    elif page == "Assessments":

        st.title("Assessment Units")

        data = {
            "Name":[
                "Aurangabad",
                "Paithan",
                "Vaijapur"
            ],

            "Status":[
                "Safe",
                "Critical",
                "Semi-Critical"
            ],

            "Extraction %":[
                70,
                95,
                88
            ],

            "Year":[
                2024,
                2024,
                2024
            ]
        }

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

    # ---------------- VISUALIZATIONS ---------------- #

    elif page == "Visualizations":

        st.title("Visualizations")

        data = pd.DataFrame({
            "Category":[
                "Safe",
                "Critical",
                "Semi-Critical"
            ],

            "Count":[
                5,
                2,
                3
            ]
        })

        st.bar_chart(
            data.set_index("Category")
        )

    # ---------------- CHATBOT ---------------- #

    elif page == "AI Chatbot":

        st.title("AI ChatBot")

        if "messages" not in st.session_state:

            st.session_state.messages=[]

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):

                st.write(msg["content"])

        prompt = st.chat_input(
            "Ask anything"
        )

        if prompt:

            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":prompt
                }
            )

            st.chat_message("user").write(
                prompt
            )

            response = f"""
            Analysis for: {prompt}
            """

            st.chat_message(
                "assistant"
            ).write(response)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":response
                }
            )