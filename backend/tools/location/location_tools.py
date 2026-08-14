from langchain_core.tools import tool
import requests



@tool
def get_location_info() -> dict:
    """
    Get location information based on IP address.
    Returns the country, region, city, latitude, and longitude.
    """
    try:
        response = requests.get("http://ip-api.com/json/")
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
    