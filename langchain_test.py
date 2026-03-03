import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek

from lerobot.scripts.lerobot_find_port import (
    find_port as real_find_port,
)
# Load API keys from .env file
load_dotenv()

# -----------------------------------------------------------------------------
# 1. DEFINE ROBOT TOOLS
# These functions represent actions the robot arm can physically perform.
# -----------------------------------------------------------------------------

@tool("pickAndPlaceItem")
def pick_item() -> str:
    """Initiates the robot arm to pick up an item and place it in the box."""
    msg = "The robot is starting to move!"
    print(f"[ROBOT ACTION] {msg}")
    return msg

@tool("resumePickUp")
def resume_pickup() -> str:
    """Restarts the pickup process after an item has been dropped."""
    msg = "The robot is restarting to pick up the dropped item!"
    print(f"[ROBOT ACTION] {msg}")
    return msg

@tool("identifyPort")
def identify_port_tool() -> str:
    """Run the interactive port‑finding routine and report completion.

    Errors raised by the underlying helper are caught and returned as a
    human-readable message so the agent can handle failures gracefully.
    """
    try:
        real_find_port()
        return "port‑finding routine executed"
    except Exception as exc:  # pragma: no cover - depends on hardware
        # any exception becomes a tool output rather than crashing the agent
        return f"Error during port identification: {exc}"

# -----------------------------------------------------------------------------
# 2. INITIALIZE AI AGENT
# -----------------------------------------------------------------------------

llm = ChatDeepSeek(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-chat",
    temperature=0,  # Deterministic output for reliable tool calling
)

agent = create_agent(
    model=llm,
    tools=[pick_item, resume_pickup, identify_port_tool],
)
# Create a lightweight LLM instance just for intent classification
# Using a simple prompt is cheaper/faster than creating another agent
intent_llm = ChatDeepSeek(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-chat",
    temperature=0,
)

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def print_ai_response(messages):
    """Extracts and prints the latest response from the AI."""
    ai_messages = [m for m in messages if isinstance(m, AIMessage)]
    if ai_messages:
        print('-' * 100)
        print(f"Assistant: {ai_messages[-1].content}")
        print('-' * 100)

def classify_intent(user_reply: str) -> bool:
    """
    Uses the LLM to interpret if a user's natural language reply 
    implies 'yes' (True) or 'no' (False) to resuming the task.
    
    Handles variations like: "yeah", "sure", "go ahead", "nope", "stop", etc.
    """
    prompt = f"""
    You are a binary classifier. The user is responding to the question: 
    "Would you like to resume the robot task after dropping an item?"
    
    User reply: "{user_reply}"
    
    Reply with ONLY one word: "YES" or "NO".
    - If the reply implies agreement, confirmation, or willingness to continue → YES
    - If the reply implies refusal, cancellation, or stopping → NO
    - If unclear, default to NO for safety.
    """
    
    response = intent_llm.invoke([HumanMessage(content=prompt)])
    decision = response.content.strip().upper()
    
    # Debug: Show how the LLM interpreted the input
    print(f"[INTENT CLASSIFIER] Input: '{user_reply}' → Classified as: {decision}")
    
    return decision == "YES"

# -----------------------------------------------------------------------------
# 4. MAIN EXECUTION FLOW
# -----------------------------------------------------------------------------

def main():
    messages = []

    # --- Step 1: Initial Task ---
    user_input = input("How can I help you today?: ")
    messages.append(HumanMessage(content=user_input))

    try:
        result = agent.invoke({"messages": messages})
    except Exception as err:  # catch unexpected agent errors
        print(f"[AGENT ERROR] {err}")
        return
    messages.extend(result["messages"])
    print_ai_response(messages)

    # --- Step 2: Simulate Hardware Failure ---
    print("\n[SYSTEM ALERT] The robot arm dropped the item!\n")
    print('-' * 100)

    # --- Step 3: LLM-Powered Recovery Logic ---
    user_reply = input("It looks like the item has been dropped, would you like to resume? ")

    # Use LLM to interpret natural language intent instead of rigid string matching
    if classify_intent(user_reply):
        # User wants to resume → add context and re-invoke agent
        messages.append(HumanMessage(
            content="The item was accidentally dropped. The user has confirmed they want to resume. Please restart the pickup process."
        ))
        
        result = agent.invoke({"messages": messages})
        messages.extend(result["messages"])
        print_ai_response(messages)
    else:
        # User wants to stop → add context and let AI acknowledge cancellation
        messages.append(HumanMessage(
            content="The item was dropped. The user has decided NOT to resume. Please acknowledge and stop the task."
        ))
        
        result = agent.invoke({"messages": messages})
        messages.extend(result["messages"])
        print_ai_response(messages)
        print("Operation stopped by user.")

if __name__ == "__main__":
    main()