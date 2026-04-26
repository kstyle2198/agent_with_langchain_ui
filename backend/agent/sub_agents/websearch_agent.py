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
tools = [web_search_tool]#, wiki_search_tool, arxiv_search_tool]


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
        SummarizationMiddleware(
            model=LLAMA_70B,
            trigger=("tokens", 4000),
            keep=("messages", 10),
        ),
        model_fallback]
)


# -------------------
# 3. Graph State
# -------------------
import operator
class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    ui_events: Annotated[list[dict], operator.add] 


# -------------------
# 4. Agent Node (🔥 완전 안정 구조)
# -------------------
# async def agent_node(state: GraphState):
#     """
#     핵심 포인트:
#     - 변환 없음
#     - Message 객체 그대로 전달
#     - tool_call_id 자동 유지
#     - LangGraph / DB / UI 완전 호환
#     """

#     result = await agent.ainvoke({"messages": state["messages"]})

#     # 🔥 기존 + 새로운 메시지 자동 merge
#     return {
#         "messages": result["messages"],
#         }

async def agent_node(state: GraphState):
    """
    - LLM 실행
    - tool + agent UI 이벤트 merge
    - append 기반 구조 유지
    """
    # 1. 실행
    # 만약 agent가 단순히 메시지 리스트만 반환하는 구조라면:
    response = await agent.ainvoke({"messages": state["messages"]})

    # 2. 결과 정규화 (Response가 리스트인 경우와 dict인 경우 대응)
    if isinstance(response, list):
        # response가 [BaseMessage, ...] 형태일 때
        new_messages = response
        tool_ui_events = []
    elif isinstance(response, dict):
        # response가 {"messages": [...], "ui_events": ...} 형태일 때
        new_messages = response.get("messages", [])
        tool_ui_events = response.get("ui_events", [])
    else:
        # 단일 메시지 객체일 때
        new_messages = [response]
        tool_ui_events = []

    # 3. 반환 (반드시 GraphState의 키들을 가진 dict여야 함)
    # 중요: 이전 state의 ui_events를 더하지 마세요 (operator.add가 해결함)
    return {
        "messages": new_messages,
        "ui_events": [
            {"type": "agent_run", "status": "completed"},
            *tool_ui_events
        ]
    }

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