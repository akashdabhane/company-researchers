import json
from langchain_core.tools import tool
from lib.apify_client import run_apify_actor
from tools.website.website_tools import search_web_via_firecrawl


@tool
def get_twitter_profile(company_name: str) -> str:
    """
    Retrieves Twitter/X handle profile info (bio, followers, following, tweets count, verified status) for a company.
    Uses Apify scraper with web search fallback.
    """
    print(f"[Twitter Tool] Searching profile for '{company_name}'...")
    
    # 1. Try Apify Twitter Scraper
    apify_items = run_apify_actor(
        actor_id="apify/twitter-scraper",
        run_input={
            "searchTerms": [company_name],
            "maxItems": 1,
            "sort": "Top",
        },
        timeout_secs=60
    )
    
    if apify_items and len(apify_items) > 0:
        item = apify_items[0]
        user_info = item.get("user", item)
        profile_info = {
            "name": user_info.get("name", company_name),
            "username": user_info.get("screen_name", user_info.get("username", "")),
            "description": user_info.get("description", user_info.get("bio", "")),
            "followersCount": user_info.get("followers_count", user_info.get("followersCount", 0)),
            "followingCount": user_info.get("friends_count", user_info.get("followingCount", 0)),
            "statusesCount": user_info.get("statuses_count", user_info.get("tweetsCount", 0)),
            "isVerified": user_info.get("verified", False),
            "location": user_info.get("location", "")
        }
        return json.dumps(profile_info, indent=2)

    # 2. Fallback via Firecrawl Search
    print(f"[Twitter Tool] Apify unavailable/empty. Falling back to web search...")
    search_res = search_web_via_firecrawl.invoke({"query": f"site:x.com OR site:twitter.com official profile bio followers {company_name}", "limit": 3})
    return str(search_res)


@tool
def get_twitter_recent_tweets(company_name: str) -> str:
    """
    Fetches recent tweets, threads, retweets, and engagement counts for a company on Twitter / X.
    """
    print(f"[Twitter Tool] Fetching recent tweets for '{company_name}'...")
    
    apify_items = run_apify_actor(
        actor_id="apify/twitter-scraper",
        run_input={
            "searchTerms": [f"from:{company_name.lower().replace(' ', '')} OR {company_name}"],
            "maxItems": 5,
        },
        timeout_secs=60
    )
    
    if apify_items and len(apify_items) > 0:
        tweets = []
        for item in apify_items[:5]:
            tweets.append({
                "text": item.get("full_text", item.get("text", "")),
                "retweetCount": item.get("retweet_count", item.get("retweetCount", 0)),
                "replyCount": item.get("reply_count", item.get("replyCount", 0)),
                "likeCount": item.get("favorite_count", item.get("likeCount", 0)),
                "createdAt": item.get("created_at", item.get("createdAt", "")),
                "url": item.get("url", "")
            })
        return json.dumps(tweets, indent=2)

    # Fallback search
    search_res = search_web_via_firecrawl.invoke({"query": f"site:x.com OR site:twitter.com {company_name} recent tweets status", "limit": 3})
    return str(search_res)
