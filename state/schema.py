from pydantic import BaseModel, Field
from typing import List


class CustomerSegment(BaseModel):
    name: str = Field(description="Name of the customer segment")
    description: str = Field(description="Brief description of this segment's needs and behavior")


class MarketAnalysisResult(BaseModel):
    location: str = Field(description="Target market location analyzed")
    tam: str = Field(description="Total Addressable Market size, with currency and value")
    sam: str = Field(description="Serviceable Addressable Market size, with currency and value")
    som: str = Field(description="Serviceable Obtainable Market size, with currency and value")
    growth_rate: str = Field(description="Estimated annual market growth rate, e.g. '12% CAGR'")
    market_maturity: str = Field(description="Market stage, e.g. 'Emerging', 'Growing', 'Mature', 'Saturated'")
    customer_segments: List[CustomerSegment] = Field(description="Key customer segments in this market")
    key_trends: List[str] = Field(description="Major trends currently shaping this market")