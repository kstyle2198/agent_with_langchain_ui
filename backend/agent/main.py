from .LLM.llms import GPT_OSS_120B
from .utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

from .sub_agents.general_agent import general_agent
from .sub_agents.websearch_agent import websearch_agent
from typing import TypedDict, List, Dict, Any, cast

agent = websearch_agent


# class GraphState(TypedDict):
#     messages: List[Dict[str, Any]]
#     route: str

# def router(state: GraphState) -> GraphState:
#     last_message = state["messages"][-1]["content"]

#     # 간단한 룰 기반 라우팅
#     if any(keyword in last_message.lower() for keyword in ["요약", "번역", "코딩", "리팩토링"]):
#         state["route"] = "general"
#     else:
#         state["route"] = "websearch"

#     return state

# async def agent_node(state: GraphState):
#     if state["route"] == "websearch":
#         result = await websearch_agent.ainvoke(cast(Any, {
#             "messages": state["messages"]
#         }))
#     else:
#         result = await general_agent.ainvoke(cast(Any, {
#             "messages": state["messages"]
#         }))

#     # 결과를 messages에 추가
#     state["messages"].append(result["messages"][-1])
#     return state

# async def llm_router(state: GraphState) -> GraphState:
#     last_message = state["messages"][-1]["content"]

#     prompt = f"""
#     아래 사용자 질문을 보고 어떤 에이전트를 써야 하는지 선택하세요.

#     선택지:
#     - general: 일반 질문
#     - websearch: 최신 정보, 뉴스, 검색 필요

#     질문:
#     {last_message}

#     답변은 general 또는 websearch 중 하나만 출력하세요.
#     """

#     decision = await GPT_OSS_120B.ainvoke(prompt)
#     route = decision.content

#     state["route"] = route if route in ["general", "websearch"] else "general"
#     return state

# from langgraph.graph import StateGraph

# builder = StateGraph(GraphState)

# builder.add_node("router", llm_router)
# builder.add_node("agent", agent_node)

# builder.set_entry_point("router")

# builder.add_conditional_edges(
#     "router",
#     lambda state: state["route"],
#     {
#         "general": "agent",
#         "websearch": "agent",
#     }
# )

# builder.set_finish_point("agent")

# agent = builder.compile()