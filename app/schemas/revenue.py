from typing import Literal

from pydantic import BaseModel, Field


class RevenueRequest(BaseModel):
    project_idea: str = Field(..., min_length=15, max_length=2000)
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class RevenueEstimate(BaseModel):
    model: Literal["Freemium", "Subscription", "Ads", "Marketplace", "One-time Purchase", "Hybrid"] = Field(
        ..., description="Recommended monetization model."
    )
    model_description: str = Field(
        ..., description="Explanation of why this model fits the app."
    )
    monthly_users_estimate_year_1: int = Field(
        ..., ge=0, description="Estimated monthly active users by end of year 1."
    )
    estimated_mrr_month_6: float = Field(
        ..., ge=0, description="Estimated monthly recurring revenue at month 6."
    )
    estimated_mrr_month_12: float = Field(
        ..., ge=0, description="Estimated monthly recurring revenue at month 12."
    )
    break_even_months: int = Field(
        ..., ge=1, description="Months until break-even on development cost."
    )
    monetization_strategy: str = Field(
        ..., description="Detailed monetization strategy and pricing tiers."
    )
    alternative_models: list[str] = Field(
        ..., description="Alternative monetization models to consider."
    )
    currency: str = Field(..., min_length=3, max_length=3)


class RevenueResponse(BaseModel):
    estimate: RevenueEstimate
    assumptions: list[str]
    risks: list[str]
