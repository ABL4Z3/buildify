import logging

from app.schemas.roadmap import RoadmapResponse
from app.services.gemini_service import gemini_service
from app.services.pricing_policy import normalize_roadmap_for_value, preferred_currency

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a senior software architect and project planner. "
    "You break down software projects into phased development roadmaps "
    "(MVP, V2, Full Vision) with realistic timelines and costs. "
    "Always return valid JSON matching the requested schema. "
    "Do not include markdown or text outside the JSON."
)


class RoadmapService:
    async def generate_roadmap(self, project_idea: str, currency: str) -> RoadmapResponse:
        currency = preferred_currency(currency)
        user_prompt = (
            f"Create a phased development roadmap for this project:\n\n"
            f'"{project_idea}"\n\n'
            f"Currency: {currency}\n\n"
            f"Break it into at least 3 phases: MVP, V2, Full Vision.\n"
            f"For each phase include: features, weeks, cost, and tech stack.\n\n"
            f"Use an MVP-first India-market pricing style for INR. Keep simple apps lean, "
            f"show open-source/reusable tooling in the tech stack, and avoid enterprise "
            f"overhead unless the request clearly requires it.\n\n"
            f"Return JSON:\n"
            f'{{\n'
            f'  "phases": [\n'
            f'    {{\n'
            f'      "phase": "MVP",\n'
            f'      "features": ["feature1", ...],\n'
            f'      "estimated_weeks": 8,\n'
            f'      "estimated_cost": 5000,\n'
            f'      "currency": "{currency}",\n'
            f'      "tech_stack": ["React Native", "Node.js", ...]\n'
            f'    }}\n'
            f'  ],\n'
            f'  "total_cost": 25000,\n'
            f'  "currency": "{currency}",\n'
            f'  "mvp_cost": 5000,\n'
            f'  "total_timeline_weeks": 24,\n'
            f'  "recommendation": "Strategic advice on how to proceed"\n'
            f'}}'
        )

        result = await gemini_service.structured_call(
            system_instruction=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=RoadmapResponse,
            cache_type="roadmap",
        )
        return normalize_roadmap_for_value(result, project_idea, currency)


roadmap_service = RoadmapService()
