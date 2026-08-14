from tools.website.website_tools import search_web_via_firecrawl, crawl_website, filter_urls, scrape_pages
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from lib.llm import llm
from lib.firecrawl_client import firecrawl_client


IMPORTANT_KEYWORDS = [
    "about",
    "contact",
    "faq",
    "company",
    "team",
    "leadership",
    "careers",
    "products",
    "services",
    "solutions",
    "mission",
    "vision",
]
 

def website_scraper_node(state):
    urls = crawl_website.invoke(
        {"website_url": state["website_url"]}
    )

    all_urls = []

    for link in urls["all_urls"].links:
        all_urls.append(link.url)

    important_urls = filter_urls.invoke(
        {
            "all_urls": all_urls,
            "IMPORTANT_KEYWORDS": IMPORTANT_KEYWORDS
        }
    )

    important_urls.append(state["website_url"])

    print("\n\n\nimportant URLs:", important_urls)

    content = scrape_pages.invoke(
        {"important_urls": important_urls}
    )

    return {
        "website_data": content,
    }


def interact_with_website_scrapped_data_node(state):
    # 1. Scrape the page
    scrape = firecrawl_client.scrape_url("https://example.com")
    scrape_id = scrape.metadata.scrape_id

    # 2. Interact with a prompt
    result = firecrawl_client.interact(
        scrape_id,
        prompt="Click the login button and fill in the email field with test@example.com",
    )
    print("Output:", result.output)
    print("Live view:", result.live_view_url)

    # 3. Chain another interaction
    result2 = firecrawl_client.interact(
        scrape_id,
        prompt="Submit the form and tell me what happens",
    )

    # 4. Stop when done
    firecrawl_client.stop_interaction(scrape_id)


def web_search_node(state):

    return search_web_via_firecrawl(query=state['company_name'])



## wikipedia agent
# 2. Register all your tools in a list
tools = [
    search_web_via_firecrawl, 
    crawl_website, 
    filter_urls, 
    scrape_pages
]


memory = MemorySaver()

# 3. Create the agent — this builds the full ReAct loop for you
website_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are a website research assistant.
    When given a company or creator name, you will:
    1. Search for the company on the web and retrieve relevant URLs using the search_web_via_firecrawl tool.
    2. Crawl the company's official website using the crawl_website tool to gather all available URLs.
    3. Filter the gathered URLs to identify important pages such as About, Contact, Team, Leadership, Careers, Products, Services, Solutions, Mission, Vision, etc. using the filter_urls tool.
    4. Scrape the content of the important URLs using the scrape_pages tool to extract relevant information about the company.
    5. Analyze the retrieved information to provide insights about the company's background, industry, and related entities.
    6. Return the information in a structured format, avoiding technical details or code snippets in your response.

    if given a query or question related to a specific aspect of the company, you will:
    1. Identify the relevant aspect using the appropriate tools.
    2. Fetch the necessary information or data related to the query.
    3. Analyze the information and provide a comprehensive answer to the user's question based on the company's website content and related web data.
    4. Return the answer in a clear and concise manner, avoiding technical jargon and code snippets in your response.
    5. If the query is unrelated to the company or cannot be answered with the available information, inform the user and suggest alternative ways to obtain the required information.

    Always use tools step by step. Never guess anything.
    """,
    checkpointer=memory,
)


def website_scraper_node2(state):
    result = website_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f""" Company Name: {state["company_name"]}""",
                },
            ],
        }
    )

    content = result["website_data"]

    return {
        "website_data": content,
    }

    