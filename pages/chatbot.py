import streamlit as st

st.title("AI ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages=[]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything")

if prompt:
    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    st.chat_message("user").write(prompt)

    response = f"Analysis for: {prompt}"

    st.chat_message("assistant").write(response)

    st.session_state.messages.append(
        {"role":"assistant","content":response}
    )