import json
from langchain_core.tools import tool
from lib.apify_client import run_apify_actor
from tools.website.website_tools import search_web_via_firecrawl


@tool
def get_linkedin_company_profile(company_name: str) -> str:
    """
    Searches for and retrieves LinkedIn company profile data (tagline, follower count, employee count, industry, about text).
    Uses Apify scraper if APIFY_API_KEY is available, with web search fallback.
    """
    print(f"[LinkedIn Tool] Searching profile for '{company_name}'...")
    
    # 1. Try Apify LinkedIn Scraper
    apify_items = run_apify_actor(
        actor_id="apify/linkedin-company-scraper",
        run_input={
            "search": company_name,
            "maxResults": 1,
        },
        timeout_secs=60
    )
    
    if apify_items and len(apify_items) > 0:
        item = apify_items[0]
        profile_info = {
            "name": item.get("name", company_name),
            "tagline": item.get("tagline", ""),
            "description": item.get("description", ""),
            "industry": item.get("industry", ""),
            "company_size": item.get("companySize", ""),
            "followers": item.get("followerCount", "N/A"),
            "website": item.get("website", ""),
            "headquarters": item.get("headquarters", ""),
        }
        return json.dumps(profile_info, indent=2)

    # 2. Fallback via Firecrawl Search
    print(f"[LinkedIn Tool] Apify unavailable/empty. Falling back to web search...")
    search_res = search_web_via_firecrawl.invoke({"query": f"LinkedIn official company page profile {company_name}", "limit": 3})
    return str(search_res)


@tool
def get_linkedin_posts(company_name: str) -> str:
    """
    Retrieves recent LinkedIn company posts, announcements, and employee updates.
    """
    print(f"[LinkedIn Tool] Fetching posts for '{company_name}'...")
    
    apify_items = run_apify_actor(
        actor_id="apify/linkedin-post-scraper",
        run_input={
            "searchKeywords": company_name,
            "maxPosts": 5,
        },
        timeout_secs=60
    )
    
    if apify_items and len(apify_items) > 0:
        posts = []
        for item in apify_items[:5]:
            posts.append({
                "text": item.get("text", item.get("postText", "")),
                "likes": item.get("numLikes", item.get("likesCount", 0)),
                "comments": item.get("numComments", item.get("commentsCount", 0)),
                "posted_at": item.get("postedAt", item.get("time", "")),
                "url": item.get("postUrl", item.get("url", ""))
            })
        return json.dumps(posts, indent=2)
        
    # Fallback search
    search_res = search_web_via_firecrawl.invoke({"query": f"site:linkedin.com/posts OR site:linkedin.com/company {company_name} recent updates", "limit": 3})
    return str(search_res)
