import logging

from app.schemas.estimation import (
    EstimateRequest,
    EstimateResponse,
    ScopeBreakdownItem,
    TimelineEstimate,
    DeepCostEstimate,
    MinimumViableCost,
)
from app.services.gemini_service import gemini_service
from app.services.pricing_policy import normalize_estimate_for_value, preferred_currency

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a senior software solution architect and pricing analyst. "
    "You analyze project ideas and produce detailed, realistic cost estimates "
    "for the 2026 software development market. "
    "Always return valid JSON matching the requested schema exactly. "
    "Do not include markdown, explanations, or any text outside the JSON."
)


class EstimationService:
    """Service for generating project cost estimates using Gemini."""

    async def estimate_cost(self, payload: EstimateRequest) -> EstimateResponse:
        currency = preferred_currency(payload.currency)
        user_prompt = (
            f"Analyze this project idea and provide a detailed cost estimate:\n\n"
            f"Project: {payload.project_idea}\n"
            f"Currency: {currency}\n\n"
            f"Return JSON with this exact structure:\n"
            f"{{\n"
            f'  "project_summary": "string",\n'
            f'  "assumptions": ["string"],\n'
            f'  "scope_breakdown": [\n'
            f'    {{\n'
            f'      "module": "string",\n'
            f'      "description": "string",\n'
            f'      "estimated_hours": number,\n'
            f'      "complexity": "Low" | "Medium" | "High"\n'
            f'    }}\n'
            f'  ],\n'
            f'  "timeline_estimate_weeks": {{\n'
            f'    "minimum": number,\n'
            f'    "expected": number,\n'
            f'    "maximum": number\n'
            f'  }},\n'
            f'  "team_recommendation": ["string"],\n'
            f'  "deep_cost_estimate": {{\n'
            f'    "development": number,\n'
            f'    "infrastructure": number,\n'
            f'    "testing_and_qa": number,\n'
            f'    "project_management": number,\n'
            f'    "contingency": number,\n'
            f'    "total": number,\n'
            f'    "currency": "{currency}"\n'
            f'  }},\n'
            f'  "minimum_viable_cost": {{\n'
            f'    "total": number,\n'
            f'    "currency": "{currency}",\n'
            f'    "what_is_included": ["string"]\n'
            f'  }},\n'
            f'  "minimum_scope_notes": ["string"],\n'
            f'  "risks": ["string"],\n'
            f'  "confidence": "Low" | "Medium" | "High"\n'
            f'}}\n\n'
            f"Rules:\n"
            f"- Keep estimates realistic for 2026 software market, calibrated for India when currency is INR.\n"
            f"- Prefer a lean MVP-first estimate unless the user explicitly asks for an enterprise, studio-grade, or large-scale launch.\n"
            f"- For simple games, landing pages, CRUD dashboards, and small apps, do not include enterprise/studio overhead.\n"
            f"- Show the value of open-source and reusable tools through a much lower minimum viable cost.\n"
            f"- Explain tradeoffs in minimum scope notes.\n"
            f"- Ensure totals are internally consistent.\n"
            f"- Use {currency} only.\n"
            f"- All cost values must be non-negative numbers.\n"
            f"- timeline_estimate_weeks must satisfy: minimum <= expected <= maximum.\n"
        )

        result = await gemini_service.structured_call(
            system_instruction=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=EstimateResponse,
            cache_type="estimation",
        )
        return normalize_estimate_for_value(result, payload.project_idea, currency)


# Singleton
estimation_service = EstimationService()
