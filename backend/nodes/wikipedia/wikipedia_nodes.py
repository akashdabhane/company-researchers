from graph.state import CompanyState
from tools.wikipedia.wikipedia_tools import (
    search_wikipedia,
    wikipedia_search,
    wikipedia_summary,
    wikipedia_full_content,
    wikipedia_company_metadata,
    wikipedia_related_companies,
    wikipedia_page_url
)
                                            
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm



def wikipedia_node(state: CompanyState):

    company = state["company_name"]

    wiki_info = search_wikipedia.invoke(company)

    return {
        "wikipedia_data": wiki_info
    }



## wikipedia agent

# 2. Register all your tools in a list
tools = [
    search_wikipedia,
    wikipedia_search,
    wikipedia_summary,
    wikipedia_full_content,
    wikipedia_company_metadata,
    wikipedia_related_companies,
    wikipedia_page_url
]


memory = MemorySaver()

# 3. Create the agent — this builds the full ReAct loop for you
wikipedia_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are a wikipedia research assistant.
    When given a company or creator name, you will:
    1. Search for the company on Wikipedia and retrieve relevant information such as a summary, full content, metadata, related companies, and page URL.
    2. Analyze the retrieved information to provide insights about the company's background, industry, and related entities.
    3. Return the information in a structured format, avoiding technical details or code snippets in your response.

    If given a query or question related to a specific company, you will:
    1. Identify the relevant company using the appropriate tools.
    2. Fetch the necessary information or data related to the query.
    3. Analyze the information and provide a comprehensive answer to the user's question based on the company's Wikipedia content, metadata, and related entities.
    4. Return the answer in a clear and concise manner, avoiding technical jargon and code snippets in your response.

    Always use tools step by step. Never guess anything.
    """,
    checkpointer=memory,
)


def wikipedia_node2(state):
    result = wikipedia_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f""" Company Name: {state["company_name"]}""",
                },
            ],
        }
    )

    content = result["wikipedia_data"]

    return {
        "wikipedia_data": content,
    }

    