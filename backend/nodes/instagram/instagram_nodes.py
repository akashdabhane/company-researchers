from graph.state import CompanyState
from tools.instagram.instagram_tools import get_instagram_profile, get_instagram_recent_posts
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm

tools = [get_instagram_profile, get_instagram_recent_posts]
memory = MemorySaver()

instagram_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are an expert Instagram Brand & Visual Strategy Agent.
    When given a company name:
    1. Fetch Instagram account details (followers, bio, posts count).
    2. Fetch recent Instagram posts, visual themes, captions, and engagement metrics.
    3. Synthesize visual brand identity, audience interaction, and hashtag usage.
    """,
    checkpointer=memory,
)


def instagram_node(state: CompanyState):
    company = state.get("company_name", "")
    print(f"[Node: Instagram Agent] Analyzing company '{company}'...")

    profile_data = get_instagram_profile.invoke(company)
    posts_data = get_instagram_recent_posts.invoke(company)

    summary_text = f"--- Instagram Account Profile ---\n{profile_data}\n\n--- Recent Instagram Posts & Reels ---\n{posts_data}"

    return {
        "instagram_data": summary_text,
        "instagram_research": summary_text,
    }