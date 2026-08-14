from graph.state import CompanyState
from tools.twitter.twitter_tools import get_twitter_profile, get_twitter_recent_tweets
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm

tools = [get_twitter_profile, get_twitter_recent_tweets]
memory = MemorySaver()

twitter_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are an expert Twitter / X Social Listening & PR Sentiment Agent.
    When given a company name:
    1. Fetch Twitter/X profile information (bio, follower count, handle).
    2. Fetch recent tweets, thread discussions, retweets, and likes.
    3. Analyze public sentiment, community chatter, product announcements, and viral reach.
    """,
    checkpointer=memory,
)


def twitter_node(state: CompanyState):
    company = state.get("company_name", "")
    print(f"[Node: Twitter Agent] Analyzing company '{company}'...")

    profile_data = get_twitter_profile.invoke(company)
    tweets_data = get_twitter_recent_tweets.invoke(company)

    summary_text = f"--- Twitter / X Profile Info ---\n{profile_data}\n\n--- Recent Tweets & Threads ---\n{tweets_data}"

    return {
        "twitter_data": summary_text,
        "twitter_research": summary_text,
    }
