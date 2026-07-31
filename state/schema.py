
from pydantic import BaseModel, Field
from typing import List

class CustomerSegment(BaseModel):
    name: str
    description: str


class MarketAnalysis(BaseModel):
    location: str = Field(description="The target location this analysis is for")
    tam: str = Field(description="Total Addressable Market — largest figure")
    sam: str = Field(description="Serviceable Addressable Market — subset of TAM")
    som: str = Field(description="Serviceable Obtainable Market — subset of SAM")
    growth_rate: str = Field(description="e.g. '12% CAGR (2024-2029)'")
    customer_segments: List[CustomerSegment]
    market_maturity: str = Field(description="Emerging | Growing | Mature | Declining")
    key_trends: List[str]

    # -------------------- WEB SEARCH --------------------

class WebSearchReport(BaseModel):
    market_trends: List[str]
    customer_pain_points: List[str]
    latest_news: List[str]
    industry_insights: List[str]

