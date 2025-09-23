# Tokyo-Trip-Assistant
A conversational bot that helps visitors explore Tokyo — temples, views, neighborhoods, and cultural tips.


🗼 Project Title: Tokyo Trip Assistant – A Conversational AI Travel Guide
🧠 Summary

Tokyo Trip Assistant is a production-ready conversational AI that helps users explore Tokyo through natural dialogue — suggesting temples, skyline views, cultural spots, and local tips, while providing real-time weather, memory of user preferences, and context-aware answers.

It demonstrates key skills required for a Conversational AI Engineer role:

LLM app development (OpenAI + LangChain/LangGraph)

Prompt design

RAG (retrieval-augmented generation)

Context tracking and state handling

External API integration

Production Python backend (FastAPI)

Reusable templates and memory modules

This project is deployable, testable, and extendable — made to simulate a real-world user-facing AI product.

🎯 Goal

To simulate a smart, travel-savvy AI agent that visitors can interact with in real-time, asking questions such as:

“What are some temples near Asakusa?”

“Where can I get the best city view?”

“Can you help me plan a day in Shibuya?”

“What’s the weather like tomorrow in Tokyo?”

It answers with context-aware, grounded, natural-sounding responses, using a mix of preloaded knowledge (via RAG) and real-time API calls.

🔧 Core Features
Feature	Description
🔁 Natural conversation	Memory of previous messages for contextual replies
📖 RAG Knowledge Base	Retrieval from embedded travel guide (Pinecone) to reduce hallucinations
✍️ Prompt Templates	Custom prompt templates per category (views, temples, food, etc.)
🌐 Weather Integration	Real-time weather fetched from OpenWeather API
🛠️ Production Backend	FastAPI app with typed endpoints, Docker-ready
📜 Reusable Prompt System	YAML/JSON configs for easy scaling and modularity
🧠 LLM Orchestration	LangChain (or LangGraph for advanced logic)
🧪 Unit Test & Health Check	Integration tests + /health endpoint
🌍 Multilingual Extensibility	Future-ready for Japanese/English language support
👥 Example Conversation

User: I want to see some temples.
Bot: Sure! One of the most famous is Senso-ji in Asakusa. Would you like me to suggest nearby places too?

User: Yes, anything with a great view?
Bot: You’re in luck — Tokyo Skytree is nearby and offers stunning city views. For skyline photos, Shibuya Sky or Roppongi Hills are also great options.

User: What’s the weather like tomorrow?
Bot: It’s expected to be 26°C and sunny in Tokyo. Great for a walking tour!

🛠️ Tech Stack
Layer	Tool/Tech	Purpose
LLM Provider	OpenAI GPT-4 / GPT-3.5	Natural language understanding and generation
Orchestration	LangChain or LangGraph	Chain logic, memory, prompt flows
API Server	FastAPI	Production-ready Python web backend
Vector DB	Pinecone	RAG over travel guide data
Prompt Templates	YAML / JSON	Dynamic, modular system prompts
External APIs	OpenWeather (real) or Google Places (mocked)	Real-time information
Containerization	Docker + docker-compose	One-command deployment
Testing	Pytest + healthcheck	Reliability and test coverage
Frontend (optional)	Streamlit	For showing demo visually (if needed)
✅ MVP Project Structure: tokyo-trip-assistant/
tokyo-trip-assistant/
├── app/
│   ├── main.py                        # FastAPI entrypoint
│
│   ├── routes/
│   │   └── chat.py                    # /chat endpoint
│
│   ├── chains/
│   │   └── conversation_chain.py      # LangChain or LangGraph logic (LLM, memory, RAG)
│
│   ├── prompts/
│   │   └── sightseeing.yaml           # Prompt template for travel dialogue
│
│   ├── vectorstore/
│   │   ├── loader.py                  # Load and embed knowledge base
│   │   ├── search.py                  # Search/query Pinecone
│   │   └── # Pinecone index (cloud-hosted)
│
│   ├── services/
│   │   └── weather.py                 # Calls OpenWeather API
│
│   ├── data/
│   │   └── tokyo_guide.json           # Curated travel info: temples, views, areas
│
│   └── utils/
│       └── prompt_loader.py           # Load YAML prompt templates
│
├── tests/
│   └── test_chat_flow.py              # Test the /chat endpoint (basic flow)
│
├── .env.template                      # Example env vars (OpenAI key, API keys)
├── Dockerfile                         # Container config
├── docker-compose.yml                 # Easy dev environment spin-up
├── requirements.txt                   # Python dependencies
└── README.md                          # Project overview, features, setup instructions

🧠 Breakdown by Purpose
Folder	Why it matters
main.py	Starts FastAPI app, registers routes
routes/	Exposes endpoints (/chat, /health)
chains/	Contains the LangChain or LangGraph logic (LLM, memory, RAG)
prompts/	Reusable YAML templates to show prompt engineering
vectorstore/	Prepares and searches Pinecone over curated knowledge
services/	External APIs like weather or (later) maps, restaurant info
data/	Local JSON knowledge base: temples, shrines, neighborhoods, views
utils/	Loaders, helpers, logging
tests/	Basic test(s) to show production mindset
Dockerfile	Proves containerization and deployment skill
.env.template	Makes it easy to set up secrets and config

✅ Skills Demonstrated (Mapped to JD)
Job Skill	Demo Proof
✅ Python + production backend	FastAPI, Pydantic, Docker
✅ LLM applications	OpenAI + LangChain/LangGraph
✅ Prompt design	Custom YAML-based templates
✅ Conversational AI & state	LangChain memory and intent continuity
✅ RAG	Pinecone-based travel guide retrieval
✅ API integration	Weather + pluggable 3rd party APIs
✅ Reusability	Modular config-driven design
✅ Team-readiness	Clean repo structure, tests, docs
🚀 Deployment Notes

Deployable locally via:

docker-compose up --build


Environment variables set via .env

Optional: Deploy to Railway, Render, or fly.io for a hosted demo

🗣️ What to Say in Your Cover Letter

I’ve recently built a demo that reflects the exact skills listed in your role: a Tokyo Trip Assistant — a conversational AI that helps users explore the city’s temples, skyline views, and neighborhoods using LLMs, RAG, and real-time API integrations. It's built with FastAPI, LangChain, OpenAI, and Pinecone, includes prompt templates and memory handling, and is containerized for easy deployment. I’d be happy to share it or walk you through the code.

⚡ Optional Extensions (Post-Demo)

Already uses Pinecone for scalable vector search

Add LangGraph instead of LangChain for node-based orchestration

Add route planner / day trip agent

Add Japanese response mode with language switch

Expand knowledge base via real-time Google Places