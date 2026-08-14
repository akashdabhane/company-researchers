from pydantic import BaseModel
from typing import Optional


class ResearchRequest(BaseModel):
    company_name: str
    website_url: str
    email: Optional[str] = None


class ResearchStreamRequest(BaseModel):
    company_name: str
    website_url: str


    