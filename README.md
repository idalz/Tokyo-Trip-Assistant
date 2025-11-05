# Tokyo Trip Assistant

> **AI-Powered Conversational Travel Guide for Tokyo**

A modern, production-ready conversational AI application that leverages **GPT-4o-mini**, **LangGraph**, **Pinecone**, and **FastAPI** to help visitors explore Tokyo through natural dialogue. Get personalized recommendations for temples, skyline views, cultural spots, dining, entertainment, and real-time weather forecasts via **RAG** (Retrieval-Augmented Generation).

**🚀 [Live Demo](https://your-railway-app.railway.app)** *(Coming soon)*

---

## Key Features

✅ **Natural Conversation** - Context-aware dialogue with conversation memory
✅ **RAG Knowledge Base** - Retrieval from embedded Tokyo travel guide (Pinecone)
✅ **Smart Intent Classification** - Understands temples, views, food, entertainment, weather queries
✅ **Real-time Weather** - Live weather forecasts via OpenWeather API
✅ **Production-Ready** - FastAPI backend with CORS, health checks, structured logging
✅ **Modern Stack** - FastAPI, Streamlit, LangGraph, Pinecone, GPT-4o-mini

---

## Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
- [How to Install](#how-to-install)
- [Development](#development)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [License](#license)

---

## Features

- Use the power of **OpenAI LLMs** and **LangGraph** to:
    1. Understand user intent through natural conversation
    2. Retrieve relevant information from a curated Tokyo knowledge base
    3. Provide context-aware recommendations for temples, views, dining, and entertainment
    4. Fetch real-time weather forecasts for trip planning
- **RAG** using Pinecone Vector Store for grounded, accurate responses
- **Conversational Memory** - Remembers context within each session
- **Modular Prompt System** - YAML-based prompt templates for easy customization
- **Health Monitoring** - Built-in health and readiness checks
- Simple and user-friendly interface built with **Streamlit**
- **Dockerized** for fast and easy deployment

---

## Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **LangGraph** - Advanced LLM orchestration with state management
- **LangChain 1.0+** - LLM tooling and chains
- **Pydantic Settings** - Configuration management
- **Uvicorn** - ASGI server

### AI & ML
- **OpenAI GPT-4o-mini** - Latest, cost-effective LLM
- **Pinecone** - Vector database for semantic search over travel knowledge
- **LangGraph** - Stateful multi-agent orchestration
- **tiktoken** - Token counting for context management

### External APIs
- **OpenWeather API** - Real-time weather forecasts

### Frontend
- **Streamlit** - Interactive Python web UI
- **Requests** - HTTP client for API calls

### DevOps & Tools
- **Docker + Docker Compose** - Containerized deployment
- **Railway** - Cloud deployment platform *(configured)*
- **Python 3.13** - Latest Python version
- **pytest** - Testing framework

---

## Usage

### Example Conversations

**User:** "I want to see some temples."
**Bot:** "Sure! One of the most famous is Senso-ji in Asakusa. Would you like me to suggest nearby places too?"

**User:** "Yes, anything with a great view?"
**Bot:** "You're in luck — Tokyo Skytree is nearby and offers stunning city views. For skyline photos, Shibuya Sky or Roppongi Hills are also great options."

**User:** "What's the weather like tomorrow?"
**Bot:** "It's expected to be 26°C and sunny in Tokyo. Great for a walking tour!"

---

## How to Install

### Prerequisites
- **Python 3.13+**
- **Docker & Docker Compose** (optional, for containerized setup)
- API Keys: OpenAI, Pinecone, OpenWeather

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Tokyo-Trip-Assistant.git
cd Tokyo-Trip-Assistant
```

2. **Install dependencies**

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

3. **Set up environment variables**

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Environment: production or development
ENVIRONMENT=production

# OpenAI API Key for LLM responses
OPENAI_API_KEY=your_openai_api_key_here

# OpenWeather API Key for weather data
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Pinecone API Key for vector database
PINECONE_API_KEY=your_pinecone_api_key_here
# Pinecone environment/region
PINECONE_ENVIRONMENT=
# Pinecone index name
PINECONE_INDEX_NAME=
# Pinecone namespace
PINECONE_NAMESPACE=
```

4. **Initialize Pinecone Vector Store** (one-time setup)
```bash
python -m app.vectorstore.loader
```

5. **Start the backend** (terminal 1)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Start the frontend** (terminal 2)
```bash
streamlit run ui.py
```

7. **Access the application**
- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

### Docker Setup

Run the entire application with a single command:

```bash
docker-compose up --build
```

This starts both the FastAPI backend and Streamlit frontend in a single container.

**Access the application:**
- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000

---

## Development

### Project Structure

```
tokyo-trip-assistant/
├── app/
│   ├── main.py                        # FastAPI entrypoint
│   ├── routes/
│   │   └── chat.py                    # /chat endpoint
│   ├── chains/
│   │   └── conversation_chain.py      # LangGraph conversation logic
│   ├── prompts/
│   │   └── sightseeing.yaml           # Prompt template for travel dialogue
│   ├── vectorstore/
│   │   ├── loader.py                  # Load and embed knowledge base
│   │   └── search.py                  # Query Pinecone
│   ├── services/
│   │   └── weather.py                 # OpenWeather API integration
│   ├── data/
│   │   └── tokyo_guide.json           # Curated travel info
│   ├── core/
│   │   ├── config.py                  # Settings management
│   │   └── logger.py                  # Structured logging
│   └── utils/
│       └── prompt_loader.py           # YAML prompt loader
├── tests/
│   ├── test_chat_flow.py              # Integration tests
│   └── test_health.py                 # Health check tests
├── ui.py                              # Streamlit frontend
├── docker-compose.yml                 # Docker orchestration
├── Dockerfile                         # Container config
├── pyproject.toml                     # Python dependencies
├── start.sh                           # Container startup script
└── README.md                          # This file
```

### Adding Dependencies

Using uv (recommended):
```bash
uv add package-name
```

Or update `pyproject.toml` manually and sync:
```toml
[project]
dependencies = [
    "package-name>=1.0.0",
]
```
```bash
uv sync
```

### Customizing Prompts

Edit the YAML prompt templates in `app/prompts/`:

```yaml
# app/prompts/sightseeing.yaml
system_prompt: |
  You are a friendly Tokyo travel assistant.
  Help users discover temples, views, dining, and cultural experiences.
  Use the provided context to give accurate recommendations.
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_chat_flow.py
```

### Code Quality

```bash
# Format code (if using black)
black app/ tests/

# Lint (if using ruff)
ruff check app/

# Type checking (if using mypy)
mypy app/
```

---

## Deployment

### Railway Deployment

This application is configured for deployment on Railway.

#### Architecture
- **Unified Service**: Single container running both FastAPI backend and Streamlit frontend
- **Start Command**: `bash start.sh` (manages both processes)

#### Environment Variables (Set in Railway Dashboard)

```env
# API Keys
OPENAI_API_KEY=your-openai-key
PINECONE_API_KEY=your-pinecone-key
OPENWEATHER_API_KEY=your-weather-key

# Pinecone Configuration
PINECONE_INDEX_NAME=tokyo-travel-guide
PINECONE_NAMESPACE=tokyo

# App Configuration
ENVIRONMENT=production

# CORS (set to your Railway frontend URL)
CORS_ORIGINS=https://your-app.railway.app
```

#### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

2. **Create Railway Project**
   - Go to [Railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Select the repository

3. **Configure Service**
   - **Start Command**: `bash start.sh`
   - Add all environment variables (see above)
   - Deploy!

4. **Access Your Application**
   - Railway will provide a public URL
   - Both the Streamlit UI and FastAPI backend will be accessible

---

## Skills Demonstrated

This project showcases skills relevant for **Conversational AI Engineer** roles:

| Skill | Implementation |
|-------|----------------|
| **Python + Production Backend** | FastAPI with health checks, CORS, structured logging |
| **LLM Applications** | OpenAI GPT-4o-mini integration with LangChain/LangGraph |
| **Prompt Engineering** | Custom YAML-based prompt templates with intent classification |
| **Conversational AI & State** | LangGraph state management with conversation memory |
| **RAG (Retrieval-Augmented Generation)** | Pinecone vector search over curated travel knowledge |
| **API Integration** | Real-time weather data from OpenWeather API |
| **Modularity & Reusability** | Config-driven design, reusable components |
| **Production Readiness** | Docker, health checks, error handling, logging |
| **Testing** | Pytest integration and unit tests |

---

## Future Enhancements

- [ ] **Multi-language Support** - Add Japanese language responses
- [ ] **Advanced Planning** - Multi-day itinerary generation
- [ ] **Google Places Integration** - Real-time restaurant and attraction data
- [ ] **Image Support** - Show photos of recommended locations
- [ ] **User Preferences** - Persistent user profiles and saved favorites
- [ ] **Extended Coverage** - Support for Osaka, Kyoto, and other Japanese cities
- [ ] **Voice Interface** - Voice input/output for hands-free exploration

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

**Questions or feedback?** Feel free to open an issue or reach out!

Built with ❤️ for travelers exploring Tokyo.
