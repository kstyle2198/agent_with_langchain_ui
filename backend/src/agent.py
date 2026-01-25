# import os
# from langchain.agents import create_agent
# from langchain_groq import ChatGroq

# def send_email(to: str, subject: str, body: str):
#     """Send an email"""
#     email = {
#         "to": to,
#         "subject": subject,
#         "body": body
#     }
#     # ... email sending logic

#     return f"Email sent to {to}"

# MODEL_NAME = os.getenv("BIG_MODEL")
# llm = ChatGroq(model=MODEL_NAME, temperature=0)

# agent = create_agent(
#     llm,
#     tools=[send_email],
#     system_prompt="You are an email assistant. Always use the send_email tool.",
# )

import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

load_dotenv()

def web_search_tool(query: str):
    """Search on web for given query using tavily search tool"""
    logger.info(f"Performing web search for question: {query}")
    try:
        web_search_tool = TavilySearch(
            max_results=3,
            include_answer=True,
            include_raw_content=False,
            include_images=False,
        )
        web_results = web_search_tool.invoke(query)
        logger.info(f"Web search completed. Found {len(web_results.get('results', []))} results.")
        return web_results
    except Exception as e:
        logger.exception("Error occurred during web search")
        raise


tools = [web_search_tool]

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]


from langgraph.graph import StateGraph
from dotenv import load_dotenv
import os
from langgraph.checkpoint.memory import MemorySaver

from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
BIG_MODEL = os.getenv("BIG_MODEL")
llm = ChatGroq(model_name=BIG_MODEL, temperature=0,max_tokens=3000,) 
# memory = MemorySaver()
llm_with_tools = llm.bind_tools(tools=tools)


# 프롬프트 정의
SYSTEM_PROMPT = """
You are the Smart AI Assistant in a company.
Based on the result of tool calling, Generate a consice and logical answer.
and if there is no relevant infomation in the tool calling result, Just say 'I don't know'.
Answer in Korean.
"""

async def agent_node(state: GraphState):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *state["messages"]
    ]
    result = await llm_with_tools.ainvoke(messages )
    return {"messages": [result],}

tool_node = ToolNode(tools=tools)

def get_graph():
    graph_builder = StateGraph(GraphState)

    graph_builder.add_node("agent", agent_node)
    graph_builder.add_node("tools", tool_node)

    graph_builder.set_entry_point("agent")

    graph_builder.add_conditional_edges("agent", tools_condition)
    graph_builder.add_edge("tools", "agent")

    return graph_builder.compile()

# Create Graph Object
agent = get_graph()
