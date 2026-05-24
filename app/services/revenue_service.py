import logging

from app.schemas.revenue import RevenueResponse
from app.services.gemini_service import gemini_service
from app.services.pricing_policy import preferred_currency

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a startup revenue analyst and monetization strategist. "
    "You analyze app ideas and forecast revenue potential, break-even timelines, "
    "and recommend monetization models. "
    "Always return valid JSON matching the requested schema. "
    "Do not include markdown or text outside the JSON."
)


class RevenueService:
    async def estimate_revenue(self, project_idea: str, currency: str) -> RevenueResponse:
        currency = preferred_currency(currency)
        user_prompt = (
            f"Analyze the revenue potential for this app idea:\n\n"
            f'"{project_idea}"\n\n'
            f"Currency: {currency}\n\n"
            f"Recommend the best monetization model, estimate MRR at month 6 and 12, "
            f"calculate break-even, and suggest a pricing strategy.\n\n"
            f"For INR, use India-market pricing assumptions and realistic consumer or SMB "
            f"willingness to pay. Avoid US SaaS pricing unless the idea targets global users.\n\n"
            f"The estimate.model field must be exactly one of: Freemium, Subscription, Ads, Marketplace, One-time Purchase, Hybrid.\n\n"
            f"Return JSON:\n"
            f'{{\n'
            f'  "estimate": {{\n'
            f'    "model": "Freemium",\n'
            f'    "model_description": "why this model",\n'
            f'    "monthly_users_estimate_year_1": 10000,\n'
            f'    "estimated_mrr_month_6": 5000,\n'
            f'    "estimated_mrr_month_12": 15000,\n'
            f'    "break_even_months": 12,\n'
            f'    "monetization_strategy": "detailed strategy with pricing tiers",\n'
            f'    "alternative_models": ["model1", "model2"],\n'
            f'    "currency": "{currency}"\n'
            f'  }},\n'
            f'  "assumptions": ["assumption1", ...],\n'
            f'  "risks": ["risk1", ...]\n'
            f'}}'
        )

        result = await gemini_service.structured_call(
            system_instruction=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=RevenueResponse,
            cache_type="revenue",
        )
        result.estimate.currency = currency
        return result


revenue_service = RevenueService()
