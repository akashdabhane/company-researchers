from graph.state import CompanyState
from tools.website.website_tools import search_web_via_firecrawl
from langchain_google_genai import ChatGoogleGenerativeAI   # ← only this changes
from langgraph.prebuilt import create_react_agent


def news_node(state: CompanyState):

    company = state["company_name"]

    scrapped_results = search_web_via_firecrawl.invoke(company)

    

    return {
        "instagram_data": instagram_data
    }


    