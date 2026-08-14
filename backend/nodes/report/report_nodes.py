from graph.state import CompanyState
from langchain_google_genai import ChatGoogleGenerativeAI  # ← only this changes
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm


memory = MemorySaver() # directory=os.path.join(os.getcwd(), "agent_memory")


# 3. Create the agent — this builds the full ReAct loop for you
agent = create_react_agent(
    model=llm,
    tools=[],
    prompt="""
    You are a company research assistant.
    When given a company name and all the data collected from Web scrapping, YouTube, Wikipedia, and NewsAPI, you will:
    1. Summarize the company's online presence and public perception based on the data provided
    2. Analyze how the company is performing in terms of audience engagement and media coverage
    3. Provide insights on the company's content strategy, public relations, and potential areas of improvement based on the YouTube channel analysis, Wikipedia information, and news articles
    4. Synthesize the information into a concise report that highlights key findings and actionable insights for the company
    5. Ensure that the report is well-structured, easy to understand, and provides a clear overview of the company's online presence and public perception.
    6. The report should be in a professional tone and format, suitable for presentation to stakeholders or decision-makers.
    7. Use the data provided to support your analysis and insights, and make sure to reference specific data points where relevant in your report.
    8. The final report should be comprehensive yet concise, providing a clear and insightful overview of the company's online presence and public perception based on the data collected.
    9. Ensure that the report is actionable, providing specific recommendations for improving the company's online presence and public perception based on the analysis of the data provided.
    10. The report should be structured in a way that highlights the key findings and insights, making it easy for stakeholders to understand the company's current position and potential areas for growth or improvement.
    """,
    checkpointer=memory,
)


def report_node(state: CompanyState):
    # print("\n\n\n\n Company State:", state)
    
    data = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                        Company Name: {state["company_name"]}

                        Website Data: {state.get("website_data", {})}

                        YouTube Data: {state.get("youtube_data", {})}

                        Wikipedia Data: {state.get("wikipedia_data", {})}

                        News Data: {state.get("news_data", {})}

                        LinkedIn Data: {state.get("linkedin_data", "")}

                        Instagram Data: {state.get("instagram_data", "")}

                        Twitter / X Data: {state.get("twitter_data", "")}

                        Competitor Analysis: {state.get("competitor_matrix", "")}

                        Location & Footprint Data: {state.get("location_data", "")}

                        Tech Stack & Infrastructure Audit: {state.get("tech_stack_data", "")}

                        Financials & Valuation Data: {state.get("financial_data", "")}
                        """,
                },
            ],
        }
    )

    print("\n\n\n data:", "*"*20, data)

    return {"final_report": data}

    