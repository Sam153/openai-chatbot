# pip install openai streamlit

import streamlit as st
from openai import OpenAI

# ---------- Page Config ----------
st.set_page_config(page_title="Python Chat Assistant", page_icon="🤖")

# ---------- Load API Key from Streamlit Secrets ----------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found in Streamlit secrets.")
    st.stop()

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# ---------- System Prompt ----------
SYSTEM_PROMPT = """
You are a friendly assistant.

Rules:
- Answer all questions clearly.
- Use friendly, simple English.
- Plain text only.
"""

# ---------- UI ----------
st.title("🤖 Sam BotBuddy")
st.write("Ask me any question, I will try to answer.")

# ---------- Initialize Chat History ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---------- Display Previous Messages ----------
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ---------- Chat Input ----------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7
    )

    ai_response = response.choices[0].message.content

    # Add assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_response}
    )

    with st.chat_message("assistant"):
        st.markdown(ai_response)
