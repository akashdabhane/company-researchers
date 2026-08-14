from langgraph.graph import (
    StateGraph,
    START,
    END
)
from langgraph.checkpoint.memory import MemorySaver
from graph.state import CompanyState

from nodes.supervisor.supervisor_node import supervisor_node
from nodes.website.website_scraper_nodes import website_scraper_node
from nodes.wikipedia.wikipedia_nodes import wikipedia_node
from nodes.youtube.youtube_nodes import youtube_node
from nodes.news.news_nodes import news_node
from nodes.linkedin.linkedin_nodes import linkedin_node
from nodes.instagram.instagram_nodes import instagram_node
from nodes.twitter.twitter_nodes import twitter_node
from nodes.competitors.competitor_nodes import competitor_discovery_node
from nodes.location.location_nodes import location_node
from nodes.tech.tech_nodes import tech_stack_node
from nodes.financial.financial_nodes import financial_node
from nodes.report.report_nodes import report_node
from nodes.pr.pr_nodes import pr_copywriter_node
from nodes.pitch.pitch_nodes import sales_pitch_node

# Wrapper to track completed agents in CompanyState
def make_worker(agent_name: str, fn):
    def wrapped_node(state: CompanyState):
        res = fn(state) or {}
        completed = list(state.get("completed_agents") or [])
        if agent_name not in completed:
            completed.append(agent_name)
        res["completed_agents"] = completed
        return res
    return wrapped_node

builder = StateGraph(CompanyState)

## Add Supervisor and Worker nodes ----------------------------------------
builder.add_node("supervisor", supervisor_node)
builder.add_node("website", make_worker("website", website_scraper_node))
builder.add_node("wikipedia", make_worker("wikipedia", wikipedia_node))
builder.add_node("youtube", make_worker("youtube", youtube_node))
builder.add_node("news", make_worker("news", news_node))
builder.add_node("linkedin", make_worker("linkedin", linkedin_node))
builder.add_node("instagram", make_worker("instagram", instagram_node))
builder.add_node("twitter", make_worker("twitter", twitter_node))
builder.add_node("competitor", make_worker("competitor", competitor_discovery_node))
builder.add_node("location", make_worker("location", location_node))
builder.add_node("tech_stack", make_worker("tech_stack", tech_stack_node))
builder.add_node("financial", make_worker("financial", financial_node))
builder.add_node("report", make_worker("report", report_node))
builder.add_node("pr_copywriter", make_worker("pr_copywriter", pr_copywriter_node))
builder.add_node("sales_pitch", make_worker("sales_pitch", sales_pitch_node))

## Set Entry Point --------------------------------------------------------
builder.add_edge(START, "supervisor")

## Router logic based on supervisor's next_agent decision ----------------
def route_supervisor(state: CompanyState) -> str:
    next_node = state.get("next_agent", "FINISH")
    if next_node == "FINISH":
        return END
    return next_node

builder.add_conditional_edges(
    "supervisor",
    route_supervisor,
    {
        "website": "website",
        "wikipedia": "wikipedia",
        "youtube": "youtube",
        "news": "news",
        "linkedin": "linkedin",
        "instagram": "instagram",
        "twitter": "twitter",
        "competitor": "competitor",
        "location": "location",
        "tech_stack": "tech_stack",
        "financial": "financial",
        "report": "report",
        "pr_copywriter": "pr_copywriter",
        "sales_pitch": "sales_pitch",
        END: END,
    }
)

## Worker nodes loop back to supervisor -----------------------------------
builder.add_edge("website", "supervisor")
builder.add_edge("wikipedia", "supervisor")
builder.add_edge("youtube", "supervisor")
builder.add_edge("news", "supervisor")
builder.add_edge("linkedin", "supervisor")
builder.add_edge("instagram", "supervisor")
builder.add_edge("twitter", "supervisor")
builder.add_edge("competitor", "supervisor")
builder.add_edge("location", "supervisor")
builder.add_edge("tech_stack", "supervisor")
builder.add_edge("financial", "supervisor")
builder.add_edge("report", "supervisor")
builder.add_edge("pr_copywriter", "supervisor")
builder.add_edge("sales_pitch", "supervisor")

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
