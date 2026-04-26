from langchain_tavily import TavilySearch
from ..utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

def build_ui_events(query: str, result: dict) -> list[dict]:
    return [
        {
            "type": "web_search_start",
            "query": query
        },
        {
            "type": "web_search_result",
            "query": query,
            "result_count": len(result.get("results", [])),
            "top_results": [
                {
                    "title": r.get("title"),
                    "url": r.get("url")
                }
                for r in result.get("results", [])[:3]
            ]
        }
    ]

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

        extracted_ui_events = build_ui_events(query, result)

        return {
            "result": result,              # LLM용
            "ui_events": extracted_ui_events  # UI용
        }
    except Exception as e:
        logger.exception(f"Error occurred during web search - {e}")
        raise