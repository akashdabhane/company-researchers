from langchain_core.tools import tool
import requests
from tools.website.website_tools import search_web_via_firecrawl


@tool
def get_location_info() -> dict:
    """
    Get location information based on IP address.
    Returns the country, region, city, latitude, and longitude.
    """
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()

        return {
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon")
        }

    except Exception as e:
        return {"error": f"Location retrieval failed: {str(e)}"}


@tool
def search_company_location(company_name: str, website_url: str = "") -> dict:
    """
    Search web data to identify company headquarters address, global offices, and operating footprint.
    """
    try:
        query = f"corporate headquarters address office locations global footprint {company_name} {website_url}"
        results = search_web_via_firecrawl.invoke({"query": query, "limit": 5})
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        return {"error": f"Company location search failed: {str(e)}"}