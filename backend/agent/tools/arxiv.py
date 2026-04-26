from langchain_community.utilities import ArxivAPIWrapper
from ..utils.setlogger import setup_logger
logger = setup_logger(f"{__name__}")



def parse_paper_info(text: str) -> dict:
    lines = text.strip().split('\n')
    result = {}
    current_key = None
    summary_lines = []

    for line in lines:
        if line.startswith('Published:'):
            result['Published'] = line[len('Published:'):].strip()
            current_key = None
        elif line.startswith('Title:'):
            result['Title'] = line[len('Title:'):].strip()
            current_key = None
        elif line.startswith('Authors:'):
            result['Authors'] = line[len('Authors:'):].strip()
            current_key = None
        elif line.startswith('Summary:'):
            current_key = 'Summary'
            summary_lines.append(line[len('Summary:'):].strip())
        elif current_key == 'Summary':
            summary_lines.append(line.strip())

    if summary_lines:
        result['Summary'] = ' '.join(summary_lines)

    return result

def arxiv_search_tool(question:str):
    """Search the Arxiv for relevant information regarding academic research and papers."""
    logger.info(f"Performing arxiv search for question: {question}")
    try:
        arxiv = ArxivAPIWrapper(top_k_results=5)
        arxiv_results = arxiv.run(question)
        arxiv_results = arxiv_results.split("\n\n")    
        refined_results = []
        for d in arxiv_results:
            refined_d = parse_paper_info(d)
            refined_results.append(refined_d)
        print(f">>> Arxiv Search Result: {refined_results}")
        logger.info(f"Arxiv search completed. Found {len(refined_results)} results.")
        return refined_results
    except Exception as e:
        logger.exception("Error occurred during arxiv search")
        raise