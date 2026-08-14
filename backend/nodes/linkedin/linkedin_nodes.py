from graph.state import CompanyState
from tools.linkedin.linkedin_tools import get_linkedin_company_profile, get_linkedin_posts
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm

tools = [get_linkedin_company_profile, get_linkedin_posts]
memory = MemorySaver()

linkedin_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are an expert LinkedIn Corporate Intelligence Agent.
    When given a company name:
    1. Fetch official LinkedIn company profile data (followers, industry, company size, bio).
    2. Fetch recent LinkedIn company updates and posts.
    3. Synthesize brand positioning, content strategy, corporate announcements, and engagement metrics.
    """,
    checkpointer=memory,
)


def linkedin_node(state: CompanyState):
    company = state.get("company_name", "")
    print(f"[Node: LinkedIn Agent] Analyzing company '{company}'...")

    profile_data = get_linkedin_company_profile.invoke(company)
    posts_data = get_linkedin_posts.invoke(company)

    summary_text = f"--- LinkedIn Company Profile ---\n{profile_data}\n\n--- Recent Company Posts ---\n{posts_data}"

    return {
        "linkedin_data": summary_text,
        "linkedin_research": summary_text,
    }
