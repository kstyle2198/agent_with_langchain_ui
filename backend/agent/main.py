from .LLM.llms import GPT_OSS_120B
from .utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

from .sub_agents.general_agent import general_agent
from .sub_agents.search_agent import search_agent
from typing import TypedDict, List, Dict, Any, cast

# agent = search_agent

from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

supervisor = create_supervisor(
    model=GPT_OSS_120B,
    agents=[general_agent, search_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a general agent. Assign general tasks to summarize, translate that does not need searching\n"
        "- a search agent. Assign web/wiki/arxiv search-needed tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile(name="multi_agent_supervisor")