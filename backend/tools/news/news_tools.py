from langchain_core.tools import tool
import os
from dotenv import load_dotenv
import requests
from newsapi import NewsApiClient

load_dotenv()  # Load environment variables from .env file

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
news_client = NewsApiClient(api_key=NEWS_API_KEY)


@tool
def get_latest_news(query: str) -> dict:
    """
    Fetch the latest news articles related to the company using NewsAPI.
    Returns a list of articles with their title, description, source, published date, and URL.
    """

    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            return {"error": "News API key not found in environment variables."}

        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=relevancy&language=en&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            return {"error": f"News API error: {data.get('message', 'Unknown error')}"}

        articles = data.get("articles", [])
        return {
            "articles": [
                {
                    "title": article["title"],
                    "description": article["description"],
                    "source": article["source"]["name"],
                    "publishedAt": article["publishedAt"],
                    "url": article["url"],
                }
                for article in articles
            ]
        }

    except Exception as e:
        return {"error": f"Failed to fetch latest news: {str(e)}"}


@tool
def get_company_news(company_name: str):
    """
    Fetch latest news articles about a specific company.
    Returns a list of articles with their title, source, published date, URL, and description.
    """

    result = news_client.get_everything(
        q=company_name, language="en", sort_by="publishedAt", page_size=10
    )

    articles = []

    for article in result["articles"]:
        articles.append(
            {
                "title": article["title"],
                "source": article["source"]["name"],
                "published_at": article["publishedAt"],
                "url": article["url"],
                "description": article["description"],
            }
        )

    return articles


@tool
def get_company_news_summary(company_name: str):
    """
    Returns summarized recent company news.
    Accepts a company name and returns a concise summary of the latest news articles about that company, including key themes and sentiment.
    """

    result = news_client.get_everything(
        q=company_name, language="en", sort_by="publishedAt", page_size=5
    )

    summaries = []

    for article in result["articles"]:
        summaries.append(f"""
            Title: {article['title']}
            Source: {article['source']['name']}
            Description: {article['description']}
            """)

    return "\n\n".join(summaries)


@tool
def get_competitor_news(company_names: list[str]):
    """
    Get latest news for a list of competitor companies.
    Accepts a list of company names and returns the latest news articles for each company, including title and source.
    """

    output = {}

    for company in company_names:

        result = news_client.get_everything(
            q=company, language="en", sort_by="publishedAt", page_size=5
        )

        output[company] = [
            {"title": article["title"], "source": article["source"]["name"]}
            for article in result["articles"]
        ]

    return output


@tool
def get_industry_news(industry: str):
    """
    Get latest news for a specific industry.
    Accepts an industry name and returns the latest news articles related to that industry, including title, source, and URL.
    """

    result = news_client.get_everything(
        q=industry, language="en", sort_by="publishedAt", page_size=15
    )

    return [
        {
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
        }
        for article in result["articles"]
    ]


@tool
def get_top_headlines(country: str = "us"):
    """
    Get top headlines for a specific country.
    Accepts a country code (e.g., 'us' for United States) and returns the top news headlines, including title and source.
    """

    result = news_client.get_top_headlines(country=country, page_size=20)

    return [
        {"title": article["title"], "source": article["source"]["name"]}
        for article in result["articles"]
    ]


RISK_KEYWORDS = [
    "lawsuit",
    "hack",
    "cyberattack",
    "breach",
    "fraud",
    "bankruptcy",
    "layoff",
    "fined",
    "investigation",
    "regulator",
]


@tool
def detect_company_risks(company_name: str):
    """
    Detect potential risks for a company based on recent news.
    Accepts a company name and returns news articles that mention potential risks, such as lawsuits, cyberattacks, or financial issues.
    """

    query = f"{company_name} AND ({' OR '.join(RISK_KEYWORDS)})"

    result = news_client.get_everything(
        q=query, language="en", sort_by="publishedAt", page_size=20
    )

    return [
        {
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
        }
        for article in result["articles"]
    ]


@tool
def get_funding_news(company_name: str):
    """
    Get recent funding news for a company.
    Accepts a company name and returns news articles related to funding, investment, acquisitions, or mergers, including title, source, and published date.
    """

    query = f"{company_name} AND " "(funding OR investment OR acquisition OR merger)"

    result = news_client.get_everything(
        q=query, language="en", sort_by="publishedAt", page_size=20
    )

    return [
        {
            "title": article["title"],
            "source": article["source"]["name"],
            "published_at": article["publishedAt"],
        }
        for article in result["articles"]
    ]


@tool
def analyze_company_news(company_name: str):
    """
    Analyze recent news articles about a company to identify trends, sentiment, and key topics.
    Accepts a company name and returns an analysis of the latest news articles, including sentiment and key topics.
    """

    result = news_client.get_everything(
        q=company_name, language="en", sort_by="publishedAt", page_size=25
    )

    articles = []

    for article in result["articles"]:

        articles.append(
            {
                "title": article["title"],
                "description": article["description"],
                "source": article["source"]["name"],
                "date": article["publishedAt"],
            }
        )

    return {
        "company": company_name,
        "article_count": len(articles),
        "articles": articles,
    }
