from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    project_idea: str = Field(..., min_length=15, max_length=2000)
    project_name: str = Field(
        default="", max_length=200, description="Optional name for the project."
    )
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class ProjectOut(BaseModel):
    id: int
    project_name: str
    project_idea: str
    status: Literal["Exploring", "In Development", "Launched", "Archived"]
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(BaseModel):
    project_name: str | None = None
    status: Literal["Exploring", "In Development", "Launched", "Archived"] | None = None


class EstimateOut(BaseModel):
    id: int
    project_id: int
    estimate_type: str
    estimate_data: str  # JSON string
    created_at: datetime
