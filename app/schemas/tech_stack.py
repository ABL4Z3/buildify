from typing import Any

from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="before")
    @classmethod
    def fill_missing_summary_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        # Some JSON-mode providers occasionally return a schema-shaped object.
        # If useful data is nested under properties, unwrap it before validation.
        properties = data.get("properties")
        if isinstance(properties, dict) and "comparisons" in properties:
            data = {**properties, **{key: value for key, value in data.items() if key != "properties"}}

        comparisons = data.get("comparisons")
        if not isinstance(comparisons, list):
            return data

        if not data.get("recommended_combo"):
            open_source_names = []
            for comparison in comparisons:
                if not isinstance(comparison, dict):
                    continue
                open_source = comparison.get("open_source")
                if isinstance(open_source, dict) and open_source.get("name"):
                    open_source_names.append(str(open_source["name"]))
            data["recommended_combo"] = " + ".join(open_source_names[:5]) or "Open-source MVP stack"

        if "estimated_savings_vs_paid" not in data:
            open_source_total = 0.0
            paid_total = 0.0
            for comparison in comparisons:
                if not isinstance(comparison, dict):
                    continue
                open_source = comparison.get("open_source")
                paid = comparison.get("paid")
                if isinstance(open_source, dict):
                    open_source_total += _as_non_negative_float(open_source.get("cost_per_month"))
                if isinstance(paid, dict):
                    paid_total += _as_non_negative_float(paid.get("cost_per_month"))
            data["estimated_savings_vs_paid"] = max(0.0, paid_total - open_source_total)

        if not data.get("currency"):
            data["currency"] = "INR"

        return data


def _as_non_negative_float(value: Any) -> float:
    try:
        return max(0.0, float(value or 0))
    except (TypeError, ValueError):
        return 0.0
