import logging

from app.schemas.pitch_deck import PitchDeckResponse
from app.services.gemini_service import gemini_service
from app.services.pricing_policy import preferred_currency

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a startup pitch coach and presentation expert. "
    "You create compelling investor pitch decks that follow the standard "
    "Sequoia/YC format: Problem, Solution, Market, Product, Business Model, "
    "Traction, Team, Competition, Financials, Ask. "
    "Always return valid JSON matching the requested schema. "
    "Do not include markdown or text outside the JSON."
)


class PitchDeckService:
    async def generate_pitch_deck(self, project_idea: str, currency: str) -> PitchDeckResponse:
        currency = preferred_currency(currency)
        user_prompt = (
            f"Create an investor pitch deck for this app idea:\n\n"
            f'"{project_idea}"\n\n'
            f"Currency: {currency}\n\n"
            f"Generate 8-12 slides following standard investor deck format. "
            f"Include speaker notes, elevator pitch, key metrics, "
            f"likely investor questions, and a funding ask.\n\n"
            f"For INR, express funding asks and financial references in rupees/lakhs/crores, "
            f"not dollars.\n\n"
            f"Return JSON:\n"
            f'{{\n'
            f'  "slides": [\n'
            f'    {{\n'
            f'      "slide_number": 1,\n'
            f'      "title": "The Problem",\n'
            f'      "content": "Bullet points describing the problem",\n'
            f'      "speaker_notes": "What to say on this slide"\n'
            f'    }}\n'
            f'  ],\n'
            f'  "elevator_pitch": "30-second pitch",\n'
            f'  "key_metrics": ["DAU", "MRR", ...],\n'
            f'  "investor_questions": ["How will you acquire users?", ...],\n'
            f'  "funding_ask": "Seeking INR 50 lakh seed round for ..."\n'
            f'}}'
        )

        return await gemini_service.structured_call(
            system_instruction=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=PitchDeckResponse,
            cache_type="pitch_deck",
        )


pitch_deck_service = PitchDeckService()
