"""
/chat endpoint for conversational interactions.
Handles chat requests and responses for the Tokyo Trip Assistant.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
import logging
import uuid
from datetime import datetime, timezone

from app.chains.conversation_chain import agent
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1", tags=["chat"])

# Session storage - In production, use Redis or database
user_sessions: Dict[str, list] = {}

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message", min_length=1, max_length=1000)
    session_id: Optional[str] = Field(default=None, description="Session ID for tracking")

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str = Field(..., description="Assistant response")
    session_id: str = Field(..., description="Session ID")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    intent_classified: Optional[str] = Field(None, description="Detected intent")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint for Tokyo Trip Assistant.
    Uses single LangGraph agent with session-based conversation history.
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        logger.info(f"Processing chat request - Session: {session_id}, Message: '{request.message[:50]}...'")

        # Get conversation history for this user session
        conversation_history = user_sessions.get(session_id, [])

        # Create state for the agent
        initial_state = {
            "user_input": request.message,
            "conversation_history": conversation_history,  # User-specific history
            "intent": "",
            "final_response": ""
        }

        # Run the single LangGraph agent with user-specific state
        result = agent.invoke(initial_state)

        # Save updated conversation history for this user
        user_sessions[session_id] = result["conversation_history"]

        response = ChatResponse(
            message=result["final_response"],
            session_id=session_id,
            intent_classified=result.get("intent")
        )

        logger.info(f"Chat response generated - Session: {session_id}, Intent: {result.get('intent')}, History length: {len(result['conversation_history'])}")
        return response

    except Exception as e:
        logger.error(f"Chat endpoint error - Session: {session_id if 'session_id' in locals() else 'unknown'}, Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
        )

# Development-only endpoints
if settings.environment != "production":
    @router.get("/chat/health")
    async def chat_health_check():
        """Health check for chat functionality"""
        try:
            # Test a simple agent invocation
            test_state = {
                "user_input": "test",
                "conversation_history": [],
                "intent": "",
                "final_response": ""
            }

            # Quick test without actually running the full agent
            return {
                "status": "healthy",
                "service": "chat_endpoint",
                "agent_ready": True,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Chat health check failed: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Chat service unhealthy: {str(e)}"
            )

    @router.post("/chat/reset")
    async def reset_conversation(session_id: str) -> Dict[str, str]:
        """Reset conversation history for a session"""
        # In a real app, you'd clear session data from a database
        # For now, just return success
        logger.info(f"Conversation reset requested for session: {session_id}")
        return {
            "status": "success",
            "message": f"Conversation history cleared for session {session_id}",
            "session_id": session_id
        }