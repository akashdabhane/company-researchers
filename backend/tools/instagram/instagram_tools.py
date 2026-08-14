import json
from langchain_core.tools import tool
from lib.apify_client import run_apify_actor
from tools.website.website_tools import search_web_via_firecrawl


@tool
def get_instagram_profile(company_name: str) -> str:
    """
    Retrieves Instagram account information (username, bio, followers, following, total posts) for a company.
    Uses Apify scraper with web search fallback.
    """
    print(f"[Instagram Tool] Searching profile for '{company_name}'...")
    handle_candidate = company_name.lower().replace(" ", "").replace(".", "")
    
    # 1. Try Apify Instagram Profile Scraper
    apify_items = run_apify_actor(
        actor_id="apify/instagram-profile-scraper",
        run_input={
            "usernames": [handle_candidate],
        },
        timeout_secs=60
    )
    
    if apify_items and len(apify_items) > 0:
        item = apify_items[0]
        profile_info = {
            "username": item.get("username", handle_candidate),
            "fullName": item.get("fullName", company_name),
            "biography": item.get("biography", ""),
            "followersCount": item.get("followersCount", 0),
            "followsCount": item.get("followsCount", 0),
            "postsCount": item.get("postsCount", 0),
            "isVerified": item.get("isVerified", False),
            "externalUrl": item.get("externalUrl", ""),
        }
        return json.dumps(profile_info, indent=2)

    # 2. Fallback via Firecrawl Search
    print(f"[Instagram Tool] Apify unavailable/empty. Falling back to web search...")
    search_res = search_web_via_firecrawl.invoke({"query": f"site:instagram.com official account profile bio followers {company_name}", "limit": 3})
    return str(search_res)


@tool
def get_instagram_recent_posts(company_name: str) -> str:
    """
    Fetches recent Instagram posts, captions, hashtags, likes, and comment counts for a company.
    """
    print(f"[Instagram Tool] Fetching recent posts for '{company_name}'...")
    handle_candidate = company_name.lower().replace(" ", "").replace(".", "")
    
    apify_items = run_apify_actor(
        actor_id="apify/instagram-post-scraper",
        run_input={
            "username": [handle_candidate],
            "resultsLimit": 5,
        },
        timeout_secs=60
    )
    
    if apify_items and len(apify_items) > 0:
        posts = []
        for item in apify_items[:5]:
            posts.append({
                "caption": item.get("caption", ""),
                "likesCount": item.get("likesCount", 0),
                "commentsCount": item.get("commentsCount", 0),
                "timestamp": item.get("timestamp", ""),
                "url": item.get("url", ""),
                "type": item.get("type", "Image")
            })
        return json.dumps(posts, indent=2)

    # Fallback search
    search_res = search_web_via_firecrawl.invoke({"query": f"site:instagram.com {company_name} post caption updates", "limit": 3})
    return str(search_res)
