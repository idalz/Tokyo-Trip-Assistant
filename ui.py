"""
Simple Streamlit UI for Tokyo Trip Assistant
"""

import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="🗼 Tokyo Trip Assistant",
    page_icon="🗼",
    layout="centered"
)

# API Configuration
import os
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development").lower() == "production"

# Simple API URL - backend runs on localhost:8000 in same container
API_BASE_URL = "http://localhost:8000/api/v1"

def call_chat_api(message: str, session_id: str) -> dict:
    """Call the FastAPI chat endpoint"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def main():
    # App Header
    st.title("🗼 Tokyo Trip Assistant")
    st.markdown("*Your AI guide to exploring Tokyo's temples, views, and neighborhoods*")

    # Initialize session state
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar with session info
    with st.sidebar:
        if not IS_PRODUCTION:
            st.header("Session Info")
            st.text(f"Session ID: {st.session_state.session_id[:8]}...")

        if st.button("🔄 New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("### 💡 Try asking:")
        st.markdown("- What temples are in Asakusa?")
        st.markdown("- Where can I get the best city view?")
        st.markdown("- What's the weather like today?")
        st.markdown("- Plan a day in Shibuya")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "timestamp" in message and not IS_PRODUCTION:
                st.caption(f"🕐 {message['timestamp']}")

    # Chat input
    if prompt := st.chat_input("Ask me about Tokyo..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = call_chat_api(prompt, st.session_state.session_id)

            if response:
                assistant_message = response["message"]
                st.markdown(assistant_message)

                # Show additional info in expander (development only)
                if not IS_PRODUCTION:
                    with st.expander("🔍 Response Details"):
                        st.json({
                            "Intent Classified": response.get("intent_classified"),
                            "Session ID": response["session_id"],
                            "Timestamp": response["timestamp"]
                        })

                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message,
                    "timestamp": response["timestamp"],
                    "intent": response.get("intent_classified")
                })
            else:
                st.error("Failed to get response from the assistant.")

    # Footer
    st.markdown("---")
    st.markdown("*Powered by FastAPI + LangGraph + OpenAI GPT-4o-mini*")

if __name__ == "__main__":
    main()