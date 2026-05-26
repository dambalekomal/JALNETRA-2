import streamlit as st

st.title("Dashboard")

col1,col2,col3,col4 = st.columns(4)

cards = [
("Safe","3"),
("Semi-Critical","2"),
("Critical","2"),
("Over-Exploited","1")
]

for col,(title,value) in zip([col1,col2,col3,col4],cards):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-title'>{title}</div>
            <div class='metric-value'>{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left,right = st.columns([3,1])

with left:
    st.markdown("""
    <div class='chat-box'>
        <h2>🤖 AI ChatBot</h2>
        <p>Hello! I'm JALNETRA AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    msg = st.chat_input("Ask groundwater question")

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