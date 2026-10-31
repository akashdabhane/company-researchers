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
        actor_id="johnvc/linkedin-company-api",
        run_input={
            "companyNames": [company_name],
        },
        timeout_secs=60
    )
    
    # Skip error rows (they carry error_message instead of company data)
    company_items = [i for i in (apify_items or []) if not i.get("error_message")]
    if company_items:
        item = company_items[0]
        industries = item.get("industries", "")
        if isinstance(industries, list):
            industries = ", ".join(str(i) for i in industries)
        profile_info = {
            "name": item.get("name", company_name),
            "tagline": item.get("slogan", ""),
            "description": item.get("description", ""),
            "industry": industries,
            "company_size": item.get("companySize", ""),
            "followers": item.get("followers", "N/A"),
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
        actor_id="johnvc/linkedin-post-search-api",
        run_input={
            "keywords": [company_name],
            "maxPostsPerKeyword": 5,
        },
        timeout_secs=60
    )
    
    # Skip error rows (they carry errorMessage instead of post data)
    post_items = [i for i in (apify_items or []) if not i.get("errorMessage")]
    if post_items:
        posts = []
        for item in post_items[:5]:
            posts.append({
                "text": item.get("text", item.get("postText", "")),
                "likes": item.get("numLikes", item.get("likesCount", 0)),
                "comments": item.get("numComments", item.get("commentsCount", 0)),
                "posted_at": item.get("datePosted", item.get("postedAt", item.get("time", ""))),
                "url": item.get("postUrl", item.get("url", ""))
            })
        return json.dumps(posts, indent=2)
        
    # Fallback search
    search_res = search_web_via_firecrawl.invoke({"query": f"site:linkedin.com/posts OR site:linkedin.com/company {company_name} recent updates", "limit": 3})
    return str(search_res)
