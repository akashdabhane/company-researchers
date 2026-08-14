import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp


load_dotenv()


firecrawl_client = FirecrawlApp(
    api_key=os.getenv("FIRECRAWL_API_KEY")
)
