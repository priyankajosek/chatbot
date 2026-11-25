import time

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")
st.title("Gemini Chatbot")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "client" not in st.session_state:
    st.session_state.client = genai.Client()


def chat(user_message):
    st.session_state.conversation.append(
        {"role": "user", "parts": [{"text": user_message}]}
    )

    for attempt in range(3):
        try:
            response = st.session_state.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=st.session_state.conversation,
            )
            if not getattr(response, "text", None):
                raise RuntimeError("The model returned an empty response.")
            reply = response.text
            break
        except Exception as error:
            is_service_unavailable = (
                getattr(error, "status_code", None) == 503
                or "503" in str(error)
                or "high demand" in str(error).lower()
            )
            if not is_service_unavailable:
                raise
            if attempt == 2:
                raise RuntimeError(
                    "Gemini is still unavailable due to high demand. "
                    "Please try again later."
                ) from error
            time.sleep(2**attempt)

    st.session_state.conversation.append(
        {"role": "assistant", "parts": [{"text": reply}]}
    )
    return reply


for message in st.session_state.conversation:
    role = "assistant" if message["role"] == "assistant" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

if prompt := st.chat_input("Ask Gemini..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat(prompt)
            st.markdown(reply)
    except Exception as error:
        st.session_state.conversation.pop()
        st.error(str(error))
