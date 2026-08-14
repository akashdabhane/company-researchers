from langchain.tools import tool
from tools.website.website_tools import search_web_via_firecrawl


@tool
def search_competitors_via_web(company_name: str, industry_keywords: str = "") -> list:
    """
    Search the web for top direct and indirect competitors of a given company.
    Args:
        company_name (str): Name of the company.
        industry_keywords (str): Optional industry or product category keywords.
    Returns:
        list: Search results containing potential competitors.
    """
    query = f"top competitors and alternatives to {company_name} {industry_keywords}".strip()
    try:
        results = search_web_via_firecrawl.invoke({"query": query, "limit": 5})
        return results
    except Exception as e:
        print(f"Competitor web search fallback due to error: {e}")
        return []
