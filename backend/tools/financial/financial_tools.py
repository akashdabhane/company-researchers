from langchain_core.tools import tool
from tools.website.website_tools import search_web_via_firecrawl


@tool
def search_financial_info(company_name: str, website_url: str = "") -> dict:
    """
    Search for company funding rounds, investor backing, revenue model, pricing tiers, and valuation estimates.
    """
    try:
        query = f"funding investors venture capital valuation revenue model pricing {company_name} {website_url}"
        results = search_web_via_firecrawl.invoke({"query": query, "limit": 5})

        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        return {"error": f"Financial search failed: {str(e)}"}
