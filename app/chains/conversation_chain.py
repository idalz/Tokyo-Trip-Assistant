"""
LangChain or LangGraph logic (LLM, memory, RAG).
Contains the conversation chain with memory and RAG integration.
"""

from typing import TypedDict, List, Optional, Union, Dict
from langgraph.graph import StateGraph, START, END
from app.core.config import settings
from openai import OpenAI
import json
import logging
import tiktoken

# Disable OpenAI HTTP debug logs - keep only our workflow prints
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)

# Initialize OpenAI client and tokenizer
client = OpenAI(api_key=settings.OPENAI_API_KEY)
tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    user_input: str
    intent: str
    conversation_history: List[Dict]
    final_response: str

def generate_response(state: AgentState) -> AgentState:
      """Generate a response using OpenAI with conversation memory"""

      # Build the conversation context
      messages = []

      # Add system prompt
      messages.append({
          "role": "system",
          "content": "You are a helpful Tokyo travel assistant. Be friendly and conversational."
      })

      # Add conversation history
      for msg in state["conversation_history"]:
          messages.append(msg)

      # Add current user input
      messages.append({
          "role": "user",
          "content": state["user_input"]
      })

      response = client.responses.create(
          model="gpt-4o-mini",
          input=messages
      )

      state["final_response"] = response.output_text
      return state

def count_conversation_tokens(conversation_history: List[Dict]) -> int:
    """Count total tokens in conversation history"""
    total_tokens = 0
    for message in conversation_history:
        content = message.get("content", "")
        role = message.get("role", "")
        # Count tokens for both role and content
        total_tokens += len(tokenizer.encode(f"{role}: {content}"))
    return total_tokens

def update_memory(state: AgentState) -> AgentState:
    """Add the conversation to memory with token-based summarization"""

    # Add user message
    state["conversation_history"].append({"role": "user", "content": state["user_input"]})

    # Add assistant response
    state["conversation_history"].append({"role": "assistant", "content": state["final_response"]})

    # Count tokens in conversation history
    current_tokens = count_conversation_tokens(state["conversation_history"])
    MAX_TOKENS = 12000  # Adjust based on your model's context window

    # Check if we need to summarize based on token count
    if current_tokens > MAX_TOKENS:
        logger.info(f"Summarizing conversation: {current_tokens} tokens exceeds {MAX_TOKENS} limit")

        # Create conversation text for summarization
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in state["conversation_history"]
        ])

        try:
            # Use LLM to summarize the entire conversation
            summary_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"""Summarize this conversation, keep it concise and to the point (essentials).
{conversation_text}

Summary:"""
                }]
            )

            summary = summary_response.choices[0].message.content.strip()

            # Replace entire history with just the summary
            state["conversation_history"] = [
                {"role": "system", "content": f"Previous conversation summary: {summary}"}
            ]

            new_tokens = count_conversation_tokens(state["conversation_history"])
            logger.info(f"Conversation compressed from {current_tokens} to {new_tokens} tokens")

        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            # Fallback: keep only last 10 messages if summarization fails
            state["conversation_history"] = state["conversation_history"][-10:]
            logger.warning("Using fallback: kept last 10 messages")

    return state

def classify_intent(state: AgentState) -> AgentState:
    """Step 1: Classify what the user wants"""

    classification_prompt = """You are an intent classifier for a Tokyo travel assistant.

Classify this user input into exactly ONE category:
- travel_info: asking about temples, shrines, views, neighborhoods, places to visit in Tokyo
- weather_info: asking about weather, forecast, temperature, rain in Tokyo
- mixed: asking about BOTH travel places AND weather (even if one is primary)
- small_talk: greetings, general conversation, unrelated topics

Respond with ONLY the category name (no explanation)."""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": classification_prompt},
            {"role": "user", "content": state["user_input"]}
        ]
    )

    state["intent"] = response.output_text.strip()
    return state

# Tool Functions
def search_tokyo_info(query: str) -> str:
    """Tool function for searching Tokyo travel information"""
    try:
        from app.vectorstore.search import VectorStoreSearcher
        searcher = VectorStoreSearcher()
        results = searcher.search(query, top_k=5)

        if not results:
            return "No travel information found for this query."

        # Format results for LLM
        formatted_results = []
        for result in results:
            formatted_results.append(
                f"• {result['title']}\n"
                f"  {result['content']}\n"
                f"  Location: {result['area']} | Category: {result['category']}\n"
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Error searching travel information: {str(e)}"

def get_weather_info(location: str = "Tokyo") -> str:
    """Tool function for getting real weather information"""
    try:
        from app.services.weather import WeatherService

        weather_service = WeatherService()
        weather_data = weather_service.get_weather(location)

        # Return raw JSON for LLM to parse - much simpler!
        return json.dumps(weather_data, indent=2)

    except Exception as e:
        logger.error(f"Weather API error: {e}")
        # Fallback to mock data if API fails
        return json.dumps({
            "error": f"Weather service temporarily unavailable for {location}",
            "fallback": {
                "location": location,
                "current": {"temp": 295.15, "description": "partly cloudy"},
                "message": "Using fallback data"
            }
        }, indent=2)

# Tools Schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_tokyo_info",
            "description": "Search for information about Tokyo temples, shrines, views, neighborhoods, and attractions",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for Tokyo attractions (e.g. 'temples in Asakusa', 'best views')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_info",
            "description": "Get current weather and 5-day forecast for Tokyo. Returns multi-day forecast data including today, tomorrow, and up to 5 days ahead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to get weather for (defaults to Tokyo if not specified)"
                    }
                },
                "required": []
            }
        }
    }
]

def smart_agent_with_tools(state: AgentState) -> AgentState:
    """Intelligent agent that can use tools to answer queries"""

    # Build conversation with intent-based hints
    intent = state["intent"]

    # Create context hints based on classified intent
    intent_hints = {
        "travel_info": "HINT: This appears to be a travel question - you'll likely need the search_tokyo_info tool.",
        "weather_info": "HINT: This appears to be a weather question - you'll likely need the get_weather_info tool.",
        "mixed": "HINT: This query involves both travel and weather - you'll likely need BOTH search_tokyo_info and get_weather_info tools.",
        "small_talk": "HINT: This appears to be casual conversation - you probably won't need any tools."
    }

    system_content = f"""You are a Tokyo travel assistant. You EXCLUSIVELY provide information about Tokyo, Japan. NO OTHER CITIES ALLOWED.

{intent_hints.get(intent, "")}

If user asks about ANY other location = Respond: "I can only help you with Tokyo information."
Use your tools to find answers to the user's question.
In case of not finding relevant informations after using your tools, specify the response includes information from your own knowledge.
"""
    messages = [
        {
            "role": "system",
            "content": system_content
        }
    ]

    # Add conversation history
    for msg in state["conversation_history"]:
        messages.append(msg)

    # Add current user input
    messages.append({"role": "user", "content": state["user_input"]})

    try:
        # First LLM call with tools
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Handle tool calls if any
        if message.tool_calls:
            # Add assistant's message with tool calls
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in message.tool_calls
                ]
            })

            # Execute each tool call
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "search_tokyo_info":
                    result = search_tokyo_info(function_args["query"])
                elif function_name == "get_weather_info":
                    result = get_weather_info(function_args.get("location", "Tokyo"))
                else:
                    result = "Unknown function"

                # Add tool result
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Get final response with tool results
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            state["final_response"] = final_response.choices[0].message.content
        else:
            # No tools needed, direct response
            state["final_response"] = message.content

    except Exception as e:
        logger.error(f"Agent error: {e}")
        state["final_response"] = "I'm sorry, I'm having trouble processing your request right now."

    return state

# Create the LangGraph workflow
graph = StateGraph(AgentState)

# Add our 3 nodes - much simpler now!
graph.add_node("classify_intent", classify_intent)
graph.add_node("smart_agent", smart_agent_with_tools)
graph.add_node("update_memory", update_memory)

# Simple linear flow: START → classify → smart_agent → memory → END
graph.add_edge(START, "classify_intent")
graph.add_edge("classify_intent", "smart_agent")
graph.add_edge("smart_agent", "update_memory")
graph.add_edge("update_memory", END)

# Compile the agent
agent = graph.compile()

def chat_cli():
    """Interactive CLI for chatting with the Tokyo Travel Assistant"""

    print("🗼 Tokyo Travel Assistant")
    print("Type 'quit' to exit\n")

    # Initialize conversation state
    conversation_history = []

    while True:
        # Get user input
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Create initial state
            initial_state = {
                "user_input": user_input,
                "conversation_history": conversation_history.copy(),
                "intent": "",
                "final_response": ""
            }

            # Run the agent
            result = agent.invoke(initial_state)

            # Display response
            print(f"Assistant: {result['final_response']}\n")

            # Update conversation history for next turn
            conversation_history = result["conversation_history"]

        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    chat_cli()