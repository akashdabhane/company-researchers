from typing import TypedDict


class CompanyState(TypedDict):
    company_name: str
    website_url: str

    website_data: str
    wikipedia_data: str
    youtube_data: str
    linkedin_data: str
    news_data: str
    twitter_data: str

    # competitors: [
    #     {
    #         company_name: str,
    #         website_url: str,

    #         website_data: str,
    #         wikipedia_data: str,
    #         youtube_data: str,
    #         linkedin_data: str,
    #         news_data: str,
    #         twitter_data: str,
    #     }
    # ]

    website_research: str
    wikipedia_research: str
    youtube_research: str
    linkedin_research: str
    news_research: str
    twitter_research: str

    final_report: str

