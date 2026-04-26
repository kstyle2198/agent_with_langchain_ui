import os
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch

from ..LLM.llms import GPT_OSS_120B, LLAMA_70B, QWEN3_32B
from ..tools.web import web_search_tool
from ..tools.wiki import wiki_search_tool
from ..tools.arxiv import arxiv_search_tool
from ..utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

from langchain.agents import create_agent
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# 🔥 핵심: Message 객체 그대로 사용
from langchain_core.messages import BaseMessage


# -------------------
# 1. Tool 정의
# -------------------
tools = [web_search_tool, wiki_search_tool, arxiv_search_tool]


# -------------------
# 2. Agent 생성
# -------------------
SYSTEM_PROMPT = """
You are the Smart AI Assistant in a company.
Based on the result of tool calling, generate a concise and logical answer.
If there is no relevant information, say 'I don't know'.
Answer in Korean.
"""

from langchain.agents.middleware import SummarizationMiddleware
summary_middleware = SummarizationMiddleware(
            model=LLAMA_70B,
            trigger=("tokens", 4000),
            keep=("messages", 10),
        ),

from langchain.agents.middleware import ModelFallbackMiddleware
model_fallback = ModelFallbackMiddleware(
            GPT_OSS_120B,
            LLAMA_70B,
        )

agent = create_agent(
    model=GPT_OSS_120B,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    middleware=[
        # summary_middleware, 
        model_fallback]
)


# -------------------
# 3. Graph State
# -------------------
class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# -------------------
# 4. Agent Node (🔥 완전 안정 구조)
# -------------------
async def agent_node(state: GraphState):
    """
    핵심 포인트:
    - 변환 없음
    - Message 객체 그대로 전달
    - tool_call_id 자동 유지
    - LangGraph / DB / UI 완전 호환
    """

    result = await agent.ainvoke({"messages": state["messages"]})

    # 🔥 기존 + 새로운 메시지 자동 merge
    return {"messages": result["messages"]}

# -------------------
# 5. Graph 구성
# -------------------
def get_graph():
    builder = StateGraph(GraphState)

    builder.add_node("agent", agent_node)
    builder.set_entry_point("agent")

    return builder.compile()


# -------------------
# 6. export
# -------------------
websearch_agent = get_graph()