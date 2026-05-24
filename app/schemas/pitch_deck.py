from pydantic import BaseModel, Field


class PitchDeckRequest(BaseModel):
    project_idea: str = Field(
        ..., min_length=15, max_length=2000,
        description="The project idea to generate a pitch deck for.",
    )
    currency: str = Field(
        default="INR", min_length=3, max_length=3, pattern=r"^[A-Z]{3}$",
    )


class PitchSlide(BaseModel):
    slide_number: int = Field(..., ge=1, description="Slide position in the deck.")
    title: str = Field(..., description="Slide title.")
    content: str = Field(..., description="Bullet-point content for the slide.")
    speaker_notes: str = Field(..., description="What the speaker should say on this slide.")


class PitchDeckResponse(BaseModel):
    slides: list[PitchSlide] = Field(..., min_length=8, description="Pitch deck slides (8-12 slides).")
    elevator_pitch: str = Field(..., description="30-second elevator pitch summary.")
    key_metrics: list[str] = Field(..., description="Metrics investors would want to see.")
    investor_questions: list[str] = Field(..., description="Questions investors are likely to ask.")
    funding_ask: str = Field(..., description="Suggested funding ask with justification.")
