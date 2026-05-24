import logging

from app.schemas.team import TeamResponse
from app.services.gemini_service import gemini_service
from app.services.pricing_policy import normalize_team_for_value, preferred_currency

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a technical recruiter and team-building consultant for software projects. "
    "You determine the exact roles, skills, and duration needed to build an app. "
    "Always return valid JSON matching the requested schema. "
    "Do not include markdown or text outside the JSON."
)


class TeamService:
    async def generate_team(self, project_idea: str, currency: str) -> TeamResponse:
        currency = preferred_currency(currency)
        user_prompt = (
            f"Determine the team needed to build this app:\n\n"
            f'"{project_idea}"\n\n'
            f"Currency: {currency}\n\n"
            f"For each role, specify: title, duration in months, employment type, "
            f"monthly rate, required skills, and responsibilities.\n\n"
            f"For INR, use lean India-market monthly rates and prefer a compact MVP team. "
            f"Do not recommend a large full-time team for simple games, landing pages, "
            f"or small CRUD apps.\n\n"
            f"Return ONLY valid JSON. Do not include markdown, comments, or explanations.\n"
            f"Do not omit any top-level fields.\n\n"
            f"Return JSON:\n"
            f'{{\n'
            f'  "team": [\n'
            f'    {{\n'
            f'      "role": "Flutter Developer",\n'
            f'      "duration_months": 3,\n'
            f'      "employment_type": "Full-time",\n'
            f'      "estimated_monthly_rate": 5000,\n'
            f'      "skills_required": ["Flutter", "Dart", "Firebase"],\n'
            f'      "responsibilities": ["Build mobile UI", "Integrate APIs"]\n'
            f'    }}\n'
            f'  ],\n'
            f'  "total_monthly_cost": 15000,\n'
            f'  "total_project_cost": 45000,\n'
            f'  "currency": "{currency}",\n'
            f'  "hiring_strategy": "Recommendation on in-house vs outsource"\n'
            f'}}'
        )

        result = await gemini_service.structured_call(
            system_instruction=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=TeamResponse,
            cache_type="team",
        )
        return normalize_team_for_value(result, project_idea, currency)


team_service = TeamService()
