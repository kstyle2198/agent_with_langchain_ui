from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# 로거 설정
from ..utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")

def parse_paper_info(text: str) -> dict:
    lines = text.strip().split('\n')
    result = {}
    current_key = None
    summary_lines = []

    for line in lines:
        if line.startswith('Page:'):
            result['Page'] = line[len('Page:'):].strip()
            current_key = None
        elif line.startswith('Summary:'):
            current_key = 'Summary'
            summary_lines.append(line[len('Summary:'):].strip())
        elif current_key == 'Summary':
            summary_lines.append(line.strip())

    if summary_lines:
        result['Summary'] = ' '.join(summary_lines)

    return result


def wiki_search_tool(query:str):
    """Search the Wikipedia for relevant information that is not required wed search"""
    logger.info(f"Performing wiki search for query: {query}")
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=3, lang="ko"))
    wiki_results = wikipedia.run(query)
    wiki_results = wiki_results.split("\n\n")
    wiki_results = [wiki_result for wiki_result in wiki_results if wiki_result != '']
    refined_results = []
    for d in wiki_results:
        refined_d = parse_paper_info(d)
        refined_results.append(refined_d)
    print(f">>> Wiki Search Result: {refined_results}")
    logger.info(f"Wiki search completed. Found {len(refined_results)} results.")
    return refined_results





