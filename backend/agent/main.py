from .utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")
from .sub_agents.websearch_agent import websearch_agent

agent = websearch_agent