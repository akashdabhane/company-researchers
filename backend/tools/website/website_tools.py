import os
from firecrawl import Firecrawl
from langchain.tools import tool
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file


firecrawl = Firecrawl(
    api_key=os.getenv("FIRECRAWL_API_KEY")
)


@tool
def search_web_via_firecrawl(query: str, limit: int = 5, location: str = None):
    """
    Search the web using Firecrawl's search API.
    Args:
        query (str): The search query.
        limit (int): The maximum number of search results to return. Default is 3.
        location (str): Optional location parameter to refine search results.
    Returns:
        list: A list of search results, where each result is a dictionary containing 'title', 'url', and 'snippet'.
    """

    results = firecrawl.search(
        query=query, limit=limit, location=location if location else None
    )

    return results


@tool
def interact_with_website_scrapped_data(scrape_id: str, prompt: str):
    """
    Interact with the scraped website data using Firecrawl's interaction API.
    input: scrape_id (str): The ID of the scraped website.
    prompt (str): The prompt to interact with.
    output: The result of the interaction.
    """
    # 1. Scrape the page
    # scrape = firecrawl.scrape_url("https://example.com")
    # scrape_id = scrape.metadata.scrape_id

    # 2. Interact with a prompt
    result = firecrawl.interact(
        scrape_id,
        prompt=prompt,
    )
    # print("Output:", result.output)
    # print("Live view:", result.live_view_url)

    # 3. Stop when done
    firecrawl.stop_interaction(scrape_id)

    return {"output": result.output}


# ------------------ seprate  for crawling, filtering imp pages, and scraping ------------------
@tool
def crawl_website(website_url: str):
    """
    Crawl a website and return all the URLs found on the website.
    input: website_url (str): The URL of the website to crawl.
    output: A list of URLs found on the website.
    """

    result = firecrawl.map_url(website_url)
    print("\n\n\ncrawled URLs:", result)

    return {"all_urls": result}


@tool
def filter_urls(all_urls: list, IMPORTANT_KEYWORDS: list):
    """
    Filter the URLs based on the presence of important keywords.
    input: all_urls (list): A list of URLs to filter.
    IMPORTANT_KEYWORDS (list): A list of keywords to look for in the URLs.
    """

    urls = all_urls

    important_urls = [
        url
        for url in urls
        if any(keyword in url.lower() for keyword in IMPORTANT_KEYWORDS)
    ]

    return important_urls


@tool
def scrape_pages(important_urls: list):
    """
    Scrape the content of the important URLs and return the content in markdown format.
    input: important_urls (list): A list of important URLs to scrape.
    output: A dictionary containing the scraped content of the important URLs in markdown format.
    """

    content = []

    for url in important_urls[:15]:

        result = firecrawl.scrape_url(url, formats=["markdown"])
        content.append(f"\n\nPAGE: {url}\n" f"{result.markdown}")

    return {"website_content": "\n".join(content)}
