from ..LLM.llms import GPT_OSS_120B
from ..utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")


from langchain.agents import create_agent

SYSTEM_PROMPT = """
You are the Smart AI Assistant in a company.
Answer in Korean.
"""

agent = create_agent(
    model=GPT_OSS_120B,
    system_prompt=SYSTEM_PROMPT,
)

import uuid
from typing import TypedDict, List, Dict

class GraphState(TypedDict):
    messages: List[Dict[str, str]]

from typing import cast, Any

def dedupe_messages(messages):
    seen = set()
    unique = []
    for m in messages:
        mid = m.get("id") if isinstance(m, dict) else m.id
        if mid and mid not in seen:
            seen.add(mid)
            unique.append(m)
    return unique

async def agent_node(state: GraphState):
    result = await agent.ainvoke(cast(Any, {
            "messages": state["messages"]
        }))

    new_messages = []

    if isinstance(result, dict) and "messages" in result:
        new_messages = result["messages"]
    else:
        content = result.get("output") if isinstance(result, dict) else result
        new_messages = [
            {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": content
            }
        ]

    merged = state["messages"] + new_messages

    return {
        "messages": dedupe_messages(merged)
    }

from langgraph.graph import StateGraph

def get_graph():
    builder = StateGraph(GraphState)

    builder.add_node("agent", agent_node)

    builder.set_entry_point("agent")
    builder.set_finish_point("agent")

    return builder.compile()

# Create Graph Object
general_agent = get_graph()