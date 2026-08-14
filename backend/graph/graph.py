from langgraph.graph import (
    StateGraph,
    START,
    END
)
from langgraph.checkpoint.memory import MemorySaver
from graph.state import CompanyState

# from nodes.linkedin import linkedin_node
from nodes.website.website_scraper_nodes import website_scraper_node
from nodes.wikipedia.wikipedia_nodes import wikipedia_node
from nodes.youtube.youtube_nodes import youtube_node
from nodes.news.news_nodes import news_node
from nodes.report.report_nodes import report_node
# from nodes.database.database_nodes import database_node


builder = StateGraph(
    CompanyState
)

## add nodes to the graph -----------------------------------------------------
builder.add_node(
    "website",
    website_scraper_node
)

builder.add_node(
    "wikipedia",
    wikipedia_node
)

builder.add_node(
    "youtube",
    youtube_node
)

builder.add_node(
    "news",
    news_node
)

# builder.add_node(
#     "linkedin",
#     linkedin_node
# )


# builder.add_node(
#     "database",
#     database_node
# )

builder.add_node(
    "report",
    report_node
)


## add edges to the graph ----------------------------------------------------
builder.add_edge(
    START,
    "website"
)

builder.add_edge(
    START,
    "wikipedia"
)

builder.add_edge(
    START,
    "youtube"
)

builder.add_edge(
    START,
    "news"
)

# builder.add_edge(
#     START,
#     "linkedin"
# )



## the report node depends on all the other nodes 
builder.add_edge(
    "website",
    "report"
)

builder.add_edge(
    "wikipedia",
    "report"
)

builder.add_edge(
    "youtube",
    "report"
)

builder.add_edge(
    "news",
    "report"
)

# builder.add_edge(
#     "linkedin",
#     "report"
# )


builder.add_edge(
    "report",
    END
)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
