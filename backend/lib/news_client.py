from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
news_client = NewsApiClient(api_key=NEWS_API_KEY)

