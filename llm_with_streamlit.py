# pip install openai streamlit python-dotenv

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ---------- Load environment variables ----------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are a friendly assistant.

Rules:
- Answer all questions clearly.
- Use friendly, simple English.
- Plain text only.
"""

# ---------- Streamlit GUI ----------
st.set_page_config(page_title="Python Chat Assistant", page_icon="🤖")

st.title("🤖 Sam BotBuddy")
st.write("Ask me any question, I will try to answer.")

# ---------- Initialize session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---------- Display previous chat messages ----------
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ---------- Chat input ----------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response with full history
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
