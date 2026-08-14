from graph.state import CompanyState
from tools.news.news_tools import (
    get_latest_news,
    get_company_news,
    get_company_news_summary,
    get_competitor_news,
    get_industry_news,
    get_top_headlines,
    detect_company_risks,
    get_funding_news,
    analyze_company_news
)
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm


def news_node(state: CompanyState):

    company = state["company_name"]

    latest_news = get_latest_news.invoke(company)

    return {
        "news_data": latest_news
    }



# 2. Register all your tools in a list
tools = [
    get_latest_news,
    get_company_news,
    get_company_news_summary,
    get_competitor_news,
    get_industry_news,
    get_top_headlines,
    detect_company_risks,
    get_funding_news,
    analyze_company_news
]


memory = MemorySaver()

# 3. Create the agent — this builds the full ReAct loop for you
news_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are a news research assistant.
    When given a company or creator name, you will:
    1. Search for the latest news articles related to the company using the appropriate tools.
    2. Analyze the retrieved news articles to identify key themes, trends, and insights about the company's recent activities, industry developments, and competitive landscape.
    3. Summarize the news information in a clear and concise manner, highlighting the most relevant and impactful news stories that could influence the company's reputation, market position, or strategic decisions.
    4. Return the information in a structured format, avoiding technical details or code snippets in your response.

    if given a query or question related to a specific aspect of the company's news, you will:
    1. Identify the relevant aspect using the appropriate tools. For example, if the query is about the company's funding news, you will use the get_funding_news tool to fetch relevant information.
    2. Fetch the necessary information or data related to the query.
    3. Analyze the information and provide a comprehensive answer to the user's question based on the company's news articles and related insights.
    4. Return the answer in a clear and concise manner, avoiding technical jargon and code snippets in your response.
    5. If the query is unrelated to the company's news or cannot be answered with the available information, inform the user and suggest alternative ways to obtain the required information.

    Always use tools step by step. Never guess anything.
    """,
    checkpointer=memory,
)


def news_node2(state):
    result = news_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f""" Company Name: {state["company_name"]}""",
                },
            ],
        }
    )

    content = result["news_data"]

    return {
        "news_data": content,
    }

    