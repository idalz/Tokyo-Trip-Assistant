# Tokyo Trip Assistant - Complete Development & Deployment Plan

## 🎯 Goal: Production-Ready Demo in 1-2 Days

### Phase 1: Foundation Setup (Day 1 - Morning)
**Priority: Critical Infrastructure**

1. **Environment Configuration** ~ DONE
   - Create `.env` file from template with real API keys
   - Set up Pinecone account and create index
   - Get OpenWeather API key
   - Test OpenAI API connection

2. **Dependencies & Requirements** ~ DONE
   - Implement `requirements.txt` with exact versions
   - Create virtual environment
   - Install and verify all packages work together

3. **Core FastAPI App Structure** ~ DONE
   - Implement `app/main.py` - FastAPI server with basic routes
   - Add health check endpoint
   - Add ready check endpoint
   - Configure CORS, logging, error handling
   - Test server starts successfully

### Phase 2: Data & Knowledge Base (Day 1 - Late Morning)
**Priority: RAG Foundation**

4. **Tokyo Travel Data** ~ DONE
   - Implement `app/data/tokyo_guide.json` with curated content:
     - Famous temples (Senso-ji, Meiji Shrine, etc.)
     - Best viewpoints (Tokyo Skytree, Shibuya Sky, etc.)
     - Neighborhoods (Shibuya, Harajuku, Asakusa, etc.)
     - Cultural tips and recommendations

5. **Vector Store Setup** ~ DONE
   - Implement `app/vectorstore/loader.py` - Load data to Pinecone
   - Implement `app/vectorstore/search.py` - Query Pinecone index
   - Test embedding and retrieval pipeline

### Phase 3: AI Conversation Engine (Day 1 - Afternoon)
**Priority: Core AI Functionality**

6. **Prompt Engineering**
   - Implement `app/prompts/sightseeing.yaml` with structured prompts
   - Implement `app/utils/prompt_loader.py` for YAML loading
   - Create prompts for different scenarios (temples, views, planning)

7. **LangChain Integration**
   - Implement `app/chains/conversation_chain.py`:
     - OpenAI integration with conversation memory
     - RAG chain combining Pinecone search + LLM
     - Context management for multi-turn conversations

### Phase 4: API Integration (Day 1 - Late Afternoon)
**Priority: External Data**

8. **Weather Service** ~ DONE
   - Implement `app/services/weather.py` for OpenWeather API
   - Handle API errors gracefully
   - Format weather data for conversational context

9. **Chat API Endpoint**
   - Implement `app/routes/chat.py`:
     - `/chat` POST endpoint with proper request/response models
     - Integration with conversation chain
     - Session/user management
     - Error handling and validation

### Phase 5: Testing & Quality (Day 2 - Morning)
**Priority: Reliability**

10. **Testing Suite**
    - Implement `tests/test_chat_flow.py`:
      - Test basic conversation flow
      - Test RAG retrieval accuracy
      - Test weather integration
      - Test error handling

11. **Integration Testing**
    - End-to-end conversation tests
    - API response validation
    - Performance testing with sample queries

### Phase 6: Containerization (Day 2 - Late Morning)
**Priority: Deployment Ready**

12. **Docker Setup**
    - Implement `Dockerfile` with Python app containerization
    - Implement `docker-compose.yml` for local development
    - Test container build and run process
    - Environment variable handling in containers

### Phase 7: Documentation & Demo Prep (Day 2 - Afternoon)
**Priority: Demo Success**

13. **Documentation**
    - Update README with setup instructions
    - Add API documentation
    - Create demo script with example conversations

14. **Demo Testing**
    - Test complete user journey
    - Prepare demo conversation examples
    - Test deployment process

### Phase 8: Deployment (Day 2 - Late Afternoon)
**Priority: Live Demo**

15. **Cloud Deployment** (Choose One)
    - **Option A**: Railway.app (easiest)
    - **Option B**: Render.com 
    - **Option C**: fly.io
    - Set up environment variables in cloud platform
    - Test live deployment

16. **Final Demo Prep**
    - Create demo conversation scripts
    - Test all features work in production
    - Prepare backup local demo if needed

## 📋 Implementation Order (Critical Path)

### **Start Here - Day 1:**
1. `requirements.txt` → `app/main.py` → `.env` setup
2. `app/data/tokyo_guide.json` → Pinecone setup
3. `app/vectorstore/loader.py` + `search.py` 
4. `app/prompts/sightseeing.yaml` + `app/utils/prompt_loader.py`
5. `app/chains/conversation_chain.py`
6. `app/services/weather.py`
7. `app/routes/chat.py`

### **Day 2 - Polish & Deploy:**
8. `tests/test_chat_flow.py`
9. `Dockerfile` + `docker-compose.yml`
10. Cloud deployment
11. Demo preparation

## 🚨 Critical Success Factors

- **Keep it simple**: Focus on core functionality first
- **Test early**: Verify each component works before moving on  
- **Have backups**: Local demo ready if cloud deployment fails
- **Real data**: Use actual Tokyo attractions, not placeholder data
- **Conversation flow**: Ensure natural, contextual responses

## 📝 Implementation Status
- [x] Project structure created
- [x] README updated with Pinecone
- [x] Requirements.txt implemented
- [x] FastAPI main.py created
- [x] Environment setup
- [x] Tokyo guide data created
- [x] Vector store implemented
- [x] Conversation chain built
- [x] Weather service added
- [x] Chat API endpoint
- [ ] Testing suite
- [ ] Docker containerization
- [ ] Cloud deployment
- [ ] Demo preparation

Agent part:
User Input]
    ↓
────────────────────────────────────────
|      LangGraph Agent Core Logic      |
────────────────────────────────────────
    ↓
[Step 1] 🧠 Classify Intent
    → Does user want...
        - Travel Info? → Use FAISS
        - Weather Info? → Use OpenWeather API
        - Mixed? → Both
        - Small Talk? → Direct LLM

    ↓
[Step 2] 🧰 Select Tool(s) to Use
    → Call FAISS for RAG results (if needed)
    → Call Weather API (if needed)

    ↓
[Step 3] 🧪 Assemble Prompt Context
    → System prompt: "You are a helpful Tokyo travel assistant..."
    → Add: memory + docs from FAISS + weather info

    ↓
[Step 4] 💬 Call OpenAI (GPT‑4)
    → Uses everything above to generate final reply

    ↓
[Step 5] 🗣️ Return Response to User
    → “You can visit Senso-ji in Asakusa. Tomorrow will be 26°C with light rain.”

    ↓
🧠 Add to memory for next round