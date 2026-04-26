from langchain_tavily import TavilySearch
from ..utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

def web_search_tool(query: str) -> dict:
    """Search the web for relevant information using Tavily."""
    logger.info(f"Performing web search for question: {query}")
    try:
        tavily = TavilySearch(
            max_results=3,
            include_answer=True,
            include_raw_content=False,
            include_images=False,
        )
        result = tavily.invoke(query)
        print(f">>> Web Search Result: {result}")
        return result
    except Exception as e:
        logger.exception(f"Error occurred during web search - {e}")
        raise