from langgraph.graph import (
    StateGraph,
    START,
    END
)
from langgraph.checkpoint.memory import MemorySaver
from graph.state import CompanyState

from nodes.website.website_scraper_nodes import website_scraper_node
from nodes.wikipedia.wikipedia_nodes import wikipedia_node
from nodes.youtube.youtube_nodes import youtube_node
from nodes.news.news_nodes import news_node
from nodes.competitors.competitor_nodes import competitor_discovery_node
from nodes.report.report_nodes import report_node
from nodes.pr.pr_nodes import pr_copywriter_node
from nodes.pitch.pitch_nodes import sales_pitch_node


builder = StateGraph(CompanyState)

## Add nodes to graph -----------------------------------------------------
builder.add_node("website", website_scraper_node)
builder.add_node("wikipedia", wikipedia_node)
builder.add_node("youtube", youtube_node)
builder.add_node("news", news_node)
builder.add_node("competitor", competitor_discovery_node)
builder.add_node("report", report_node)
builder.add_node("pr_copywriter", pr_copywriter_node)
builder.add_node("sales_pitch", sales_pitch_node)


## Add edges to graph ----------------------------------------------------
builder.add_edge(START, "website")
builder.add_edge(START, "wikipedia")
builder.add_edge(START, "youtube")
builder.add_edge(START, "news")

## Competitor discovery depends on initial website research
builder.add_edge("website", "competitor")

## Report node depends on all research & competitor nodes
builder.add_edge("website", "report")
builder.add_edge("wikipedia", "report")
builder.add_edge("youtube", "report")
builder.add_edge("news", "report")
builder.add_edge("competitor", "report")

## PR Copywriter & Sales Pitch nodes depend on report context
builder.add_edge("report", "pr_copywriter")
builder.add_edge("report", "sales_pitch")

builder.add_edge("pr_copywriter", END)
builder.add_edge("sales_pitch", END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
