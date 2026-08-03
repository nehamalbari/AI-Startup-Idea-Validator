from typing import List, Optional
from pydantic import BaseModel, Field


class MVPRecommendation(BaseModel):
    
    core_problem: str = Field(
        description="The single most important problem this startup idea solves."
    )

    target_user: Optional[str] = Field(
        default=None,
        description="The primary user segment this MVP is built for."
    )

    must_have_features: List[str] = Field(
        description="Essential, specific MVP features required to validate the idea in 4-6 weeks."
    )

    nice_to_have_features: List[str] = Field(
        description="Useful but non-essential features that can wait until after validation."
    )

    future_enhancements: List[str] = Field(
        description="Features, integrations, and scale improvements that should come later."
    )

    development_priority: List[str] = Field(
        description="Ordered build steps for implementing the MVP."
    )

    validation_risks: List[str] = Field(
        default_factory=list,
        description="Key risks or assumptions that could invalidate the idea."
    )

    success_metrics: List[str] = Field(
        default_factory=list,
        description="Simple signals that indicate whether the MVP is working."
    )


class ValidatorState(BaseModel):
    startup_idea: str
    target_audience: Optional[str] = None
    industry: Optional[str] = None
    constraints: Optional[str] = None
    mvp_recommendation: Optional[MVPRecommendation] = None