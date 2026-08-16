import os
import json

import requests
import streamlit as st


DEFAULT_API_URL = os.getenv("AI_ASSISTANT_API_URL", "http://ai_assistant_server:8000")


def initialise_session() -> None:
    st.session_state.setdefault("chat_id", None)
    st.session_state.setdefault("messages", [])


def reset_chat() -> None:
    st.session_state.chat_id = None
    st.session_state.messages = []


def stream_message(api_url: str, message: str):
    payload = {"message": message}
    if st.session_state.chat_id:
        payload["chat_id"] = st.session_state.chat_id

    response = requests.post(
        f"{api_url.rstrip('/')}/api/chat/stream",
        json=payload,
        timeout=120,
        stream=True,
    )
    response.raise_for_status()
    for line in response.iter_lines(decode_unicode=True):
        if line:
            yield json.loads(line)


st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
initialise_session()

st.title("AI Assistant")
st.caption("Chat with your FastAPI and LangGraph assistant.")

with st.sidebar:
    st.header("Connection")
    api_url = st.text_input("FastAPI URL", value=DEFAULT_API_URL)

    if st.button("New chat", use_container_width=True):
        reset_chat()
        st.rerun()

    if st.session_state.chat_id:
        st.caption("Current chat ID")
        st.code(st.session_state.chat_id, language=None)

for saved_message in st.session_state.messages:
    with st.chat_message(saved_message["role"]):
        st.markdown(saved_message["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        planning_placeholder = st.empty()
        try:
            for event in stream_message(api_url, prompt):
                if event["event"] == "chat_started":
                    st.session_state.chat_id = event["chat_id"]
                elif event["event"] == "plan":
                    # Reuse one placeholder so the previous plan is hidden.
                    planning_placeholder.info(f"Thinking: {event['content']}")
                elif event["event"] == "output":
                    planning_placeholder.empty()
                    answer = event["response"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                elif event["event"] == "error":
                    planning_placeholder.empty()
                    st.error(f"API error ({event['status']}): {event['detail']}")
        except requests.HTTPError as error:
            st.error(f"API error ({error.response.status_code}): {error.response.text}")
        except requests.RequestException:
            st.error(
                "Cannot reach the FastAPI server. Start it first and check the URL in the sidebar."
            )
