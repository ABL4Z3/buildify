from typing import Literal

from pydantic import BaseModel, Field, model_validator


class TeamRequest(BaseModel):
    project_idea: str = Field(..., min_length=15, max_length=2000)
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class TeamMember(BaseModel):
    role: str = Field(..., description="Job title (e.g. Flutter Developer, UI/UX Designer).")
    duration_months: int = Field(..., ge=1, description="How many months this role is needed.")
    employment_type: Literal["Full-time", "Part-time", "Freelance", "Contract"] = Field(
        ..., description="Recommended employment arrangement."
    )
    estimated_monthly_rate: float = Field(
        ..., ge=0, description="Estimated monthly rate for this role."
    )
    skills_required: list[str] = Field(
        ..., description="Key skills needed for this role."
    )
    responsibilities: list[str] = Field(
        ..., description="What this person will be responsible for."
    )


class TeamResponse(BaseModel):
    team: list[TeamMember] = Field(..., min_length=1)
    total_monthly_cost: float = Field(default=0, ge=0)
    total_project_cost: float = Field(default=0, ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    hiring_strategy: str = Field(
        default="Start with a lean cross-functional MVP team, then scale selectively.",
        description="Recommended approach to hiring (in-house vs outsource)."
    )

    @model_validator(mode="after")
    def populate_costs_if_missing(self) -> "TeamResponse":
        if self.total_monthly_cost == 0:
            self.total_monthly_cost = round(
                sum(member.estimated_monthly_rate for member in self.team),
                2,
            )

        if self.total_project_cost == 0:
            self.total_project_cost = round(
                sum(member.estimated_monthly_rate * member.duration_months for member in self.team),
                2,
            )

        return self
