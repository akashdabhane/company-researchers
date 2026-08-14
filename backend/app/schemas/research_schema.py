from pydantic import BaseModel
from typing import Optional


class ResearchRequest(BaseModel):
    company_name: str
    website_url: str
    email: Optional[str] = None


class ResearchStreamRequest(BaseModel):
    company_name: str
    website_url: str


class PRGenerateRequest(BaseModel):
    company_name: str
    website_url: Optional[str] = ""
    platform: str = "LinkedIn"
    narrative_theme: str = "Product Launch & Major Announcement"
    human_feedback: Optional[str] = ""


class PRRefineRequest(BaseModel):
    company_name: str
    platform: str
    narrative_theme: str
    human_feedback: str
    current_content: Optional[str] = ""


class PitchGenerateRequest(BaseModel):
    company_name: str
    website_url: Optional[str] = ""
    prospect_url: str
    prospect_data: Optional[str] = ""