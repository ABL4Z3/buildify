from pydantic import BaseModel, Field

from app.schemas.estimation import EstimateResponse
from app.schemas.roadmap import RoadmapResponse
from app.schemas.revenue import RevenueResponse
from app.schemas.competitor import CompetitorResponse
from app.schemas.risk import RiskResponse
from app.schemas.team import TeamResponse
from app.schemas.tech_stack import TechStackResponse


class FullAnalysisRequest(BaseModel):
    project_idea: str = Field(..., min_length=15, max_length=2000)
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class FullAnalysisResponse(BaseModel):
    estimate: EstimateResponse
    roadmap: RoadmapResponse
    revenue: RevenueResponse
    competitors: CompetitorResponse
    risk: RiskResponse
    team: TeamResponse
    tech_stack: TechStackResponse
