from typing import Literal

from pydantic import BaseModel, Field, model_validator


class EstimateRequest(BaseModel):
    project_idea: str = Field(
        ...,
        min_length=15,
        max_length=2000,
        description="Client's project idea and requirements.",
    )
    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
        description="3-letter ISO 4217 currency code.",
    )


# ── Typed sub-models (replacing dict[str, Any]) ──


class ScopeBreakdownItem(BaseModel):
    module: str = Field(..., description="Module or feature area name.")
    description: str = Field(..., description="What this module includes.")
    estimated_hours: float = Field(..., ge=0, description="Estimated development hours.")
    complexity: Literal["Low", "Medium", "High"] = Field(
        ..., description="Complexity level."
    )


class TimelineEstimate(BaseModel):
    minimum: int = Field(..., ge=1, description="Minimum weeks to deliver.")
    expected: int = Field(..., ge=1, description="Expected weeks to deliver.")
    maximum: int = Field(..., ge=1, description="Maximum weeks to deliver.")

    @model_validator(mode="after")
    def validate_order(self) -> "TimelineEstimate":
        if not (self.minimum <= self.expected <= self.maximum):
            raise ValueError(
                "Timeline must satisfy: minimum <= expected <= maximum"
            )
        return self


class DeepCostEstimate(BaseModel):
    development: float = Field(..., ge=0)
    infrastructure: float = Field(..., ge=0)
    testing_and_qa: float = Field(..., ge=0)
    project_management: float = Field(..., ge=0)
    contingency: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")

    @model_validator(mode="after")
    def validate_total(self) -> "DeepCostEstimate":
        component_sum = (
            self.development
            + self.infrastructure
            + self.testing_and_qa
            + self.project_management
            + self.contingency
        )
        # Normalize the total to the computed component sum so small math drift
        # from the LLM does not fail the whole analysis.
        if component_sum > 0:
            self.total = round(component_sum, 2)
        return self


class MinimumViableCost(BaseModel):
    total: float = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    what_is_included: list[str] = Field(..., min_length=1)


class EstimateResponse(BaseModel):
    project_summary: str
    assumptions: list[str]
    scope_breakdown: list[ScopeBreakdownItem]
    timeline_estimate_weeks: TimelineEstimate
    team_recommendation: list[str]
    deep_cost_estimate: DeepCostEstimate
    minimum_viable_cost: MinimumViableCost
    minimum_scope_notes: list[str]
    risks: list[str]
    confidence: Literal["Low", "Medium", "High"]
