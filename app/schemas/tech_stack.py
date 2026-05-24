from pydantic import BaseModel, Field


class TechStackRequest(BaseModel):
    project_idea: str = Field(..., min_length=15, max_length=2000)
    currency: str = Field(default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class TechOption(BaseModel):
    category: str = Field(
        ..., description="Category (Frontend, Backend, Database, Hosting, Payments, etc.)."
    )


class TechDetail(BaseModel):
    name: str = Field(default="Unknown", description="Technology name.")
    pros: list[str] = Field(default_factory=list, description="Advantages of this technology.")
    cons: list[str] = Field(default_factory=list, description="Disadvantages of this technology.")
    cost_per_month: float = Field(default=0, ge=0, description="Estimated monthly cost.")
    setup_difficulty: str = Field(
        default="Medium", description="How hard to set up: Easy, Medium, or Hard."
    )
    scalability: str = Field(
        default="Medium", description="Scalability rating: Low, Medium, High."
    )


class TechCategoryComparison(BaseModel):
    category: str
    open_source: TechDetail
    paid: TechDetail


class TechStackResponse(BaseModel):
    comparisons: list[TechCategoryComparison] = Field(
        ..., description="Comparison per technology category."
    )
    recommended_combo: str = Field(
        ..., description="The recommended combination of technologies."
    )
    estimated_savings_vs_paid: float = Field(
        ..., ge=0, description="Monthly savings using open-source vs paid."
    )
    currency: str = Field(..., min_length=3, max_length=3)
