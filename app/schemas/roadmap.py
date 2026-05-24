from pydantic import BaseModel, Field


class RoadmapPhase(BaseModel):
    phase: str = Field(..., description="Phase name, e.g. MVP, V2, Full Vision.")
    features: list[str] = Field(..., description="Features included in this phase.")
    estimated_weeks: int = Field(..., ge=1, description="Estimated timeline in weeks.")
    estimated_cost: float = Field(..., ge=0, description="Estimated cost for this phase.")
    currency: str = Field(..., min_length=3, max_length=3)
    tech_stack: list[str] = Field(
        ..., description="Recommended tech stack for this phase."
    )


class RoadmapRequest(BaseModel):
    project_idea: str = Field(..., min_length=15, max_length=2000)
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class RoadmapResponse(BaseModel):
    phases: list[RoadmapPhase] = Field(
        ..., min_length=2, description="Phased development roadmap."
    )
    total_cost: float = Field(..., ge=0, description="Total cost across all phases.")
    currency: str = Field(..., min_length=3, max_length=3)
    mvp_cost: float = Field(..., ge=0, description="Cost of the MVP phase only.")
    total_timeline_weeks: int = Field(..., ge=1)
    recommendation: str = Field(
        ..., description="Strategic recommendation on how to proceed."
    )
