from langchain_core.tools import tool
from tools.website.website_tools import search_web_via_firecrawl
import requests


@tool
def search_tech_stack(company_name: str, website_url: str = "") -> dict:
    """
    Search for technology stack, frameworks, hosting providers, APIs, AI models, and analytics tools used by a company.
    """
    try:
        query = f"tech stack technologies frameworks cloud hosting infrastructure software tools {company_name} {website_url}"
        results = search_web_via_firecrawl.invoke({"query": query, "limit": 5})

        headers_detected = {}
        if website_url:
            target = website_url if website_url.startswith("http") else f"https://{website_url}"
            try:
                resp = requests.head(target, timeout=5, allow_redirects=True)
                headers_detected = {
                    "server": resp.headers.get("Server"),
                    "x-powered-by": resp.headers.get("X-Powered-By"),
                    "via": resp.headers.get("Via"),
                    "cf-ray": resp.headers.get("CF-RAY"),
                }
            except Exception:
                headers_detected = {"status": "Could not inspect headers directly"}

        return {
            "tech_search": results,
            "headers_detected": headers_detected
        }
    except Exception as e:
        return {"error": f"Tech stack audit failed: {str(e)}"}
