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
    page_title="Tokyo Trip Assistant",
    page_icon="🗼",
    layout="centered"
)

# API Configuration
import os
from dotenv import load_dotenv
load_dotenv()
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
        st.markdown("### 💡 Try asking:")
        st.markdown("- What temples are worth visiting in Tokyo?")
        st.markdown("- Where can I listen to live music?")
        st.markdown("- What's the weather like tomorrow?")
        st.markdown("- Plan an ideal day exploring Shibuya!")

        st.markdown("---")
        st.markdown("### 🎯 Demo Scope")
        st.markdown("Smart travel assistant for Tokyo exploration. Get recommendations for temples, scenic viewpoints, dining, entertainment venues, cultural experiences, and weather forecasts.")

        st.markdown("### ⚠️ Current Limitations")
        st.markdown("- Weather forecasts limited to 3-day period")
        st.markdown("- Knowledge base contains curated sample data")
        st.markdown("- Conversation memory resets with each session")

        st.markdown("### 🚀 Planned Enhancements")
        st.markdown("- Expanded knowledge base with comprehensive Tokyo data")
        st.markdown("- Advanced reasoning and multi-step trip planning")
        st.markdown("- Extended coverage beyond Tokyo to major Japanese cities")

        if not IS_PRODUCTION:
            st.markdown("---")
            st.text(f"Session ID: {st.session_state.session_id[:8]}...")

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