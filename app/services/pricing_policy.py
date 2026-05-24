from dataclasses import dataclass

from app.schemas.estimation import EstimateResponse
from app.schemas.roadmap import RoadmapResponse
from app.schemas.team import TeamResponse
from app.schemas.tech_stack import TechStackResponse


DEFAULT_CURRENCY = "INR"


@dataclass(frozen=True)
class ProjectPricingProfile:
    name: str
    mvp_min: float
    mvp_max: float
    full_min: float
    full_max: float
    max_hours: float
    hourly_rate: float
    infra_max: float
    note: str


SIMPLE_GAME_PROFILE = ProjectPricingProfile(
    name="simple_game",
    mvp_min=35_000,
    mvp_max=150_000,
    full_min=150_000,
    full_max=500_000,
    max_hours=320,
    hourly_rate=900,
    infra_max=30_000,
    note=(
        "Simple 2D games should be estimated as lean MVPs first, using open-source "
        "game engines, reusable UI/audio assets, and lightweight analytics unless a "
        "studio-grade multiplayer/live-ops scope is explicitly requested."
    ),
)

LANDING_PAGE_PROFILE = ProjectPricingProfile(
    name="landing_page",
    mvp_min=15_000,
    mvp_max=80_000,
    full_min=50_000,
    full_max=180_000,
    max_hours=140,
    hourly_rate=800,
    infra_max=12_000,
    note=(
        "Marketing and portfolio sites should stay lean by using open-source UI kits, "
        "static hosting, and a small CMS only when content editing is required."
    ),
)

CRUD_APP_PROFILE = ProjectPricingProfile(
    name="crud_app",
    mvp_min=80_000,
    mvp_max=300_000,
    full_min=250_000,
    full_max=900_000,
    max_hours=520,
    hourly_rate=1_000,
    infra_max=60_000,
    note=(
        "Standard dashboards and CRUD apps should reuse proven open-source frameworks, "
        "authentication libraries, admin templates, and managed database free tiers."
    ),
)


def preferred_currency(currency: str | None) -> str:
    """Use INR as the product default while keeping non-USD explicit currencies usable."""
    normalized = (currency or DEFAULT_CURRENCY).strip().upper()
    if not normalized or normalized == "USD":
        return DEFAULT_CURRENCY
    return normalized


def detect_pricing_profile(project_idea: str) -> ProjectPricingProfile | None:
    idea = project_idea.lower()
    simple_game_terms = (
        "brick game",
        "bricks game",
        "bricks",
        "brick breaker",
        "breakout",
        "snake game",
        "flappy",
        "tic tac toe",
        "simple game",
        "2d game",
        "arcade game",
    )
    landing_terms = (
        "landing page",
        "portfolio",
        "brochure website",
        "company website",
        "static website",
    )
    crud_terms = (
        "admin panel",
        "dashboard",
        "crm",
        "inventory",
        "booking system",
        "management system",
    )

    if any(term in idea for term in simple_game_terms):
        return SIMPLE_GAME_PROFILE
    if any(term in idea for term in landing_terms):
        return LANDING_PAGE_PROFILE
    if any(term in idea for term in crud_terms):
        return CRUD_APP_PROFILE
    return None


def normalize_estimate_for_value(
    estimate: EstimateResponse,
    project_idea: str,
    currency: str,
) -> EstimateResponse:
    estimate.deep_cost_estimate.currency = currency
    estimate.minimum_viable_cost.currency = currency

    profile = detect_pricing_profile(project_idea)
    if currency != DEFAULT_CURRENCY or profile is None:
        _add_unique(estimate.assumptions, f"Costs are shown in {currency}.")
        return estimate

    total_hours = sum(item.estimated_hours for item in estimate.scope_breakdown)
    if total_hours > profile.max_hours and total_hours > 0:
        scale = profile.max_hours / total_hours
        for item in estimate.scope_breakdown:
            item.estimated_hours = round(item.estimated_hours * scale, 1)
        total_hours = profile.max_hours

    if total_hours <= 0:
        total_hours = min(profile.max_hours, 120)

    development = total_hours * profile.hourly_rate
    infrastructure = min(
        max(estimate.deep_cost_estimate.infrastructure, profile.infra_max * 0.25),
        profile.infra_max,
    )
    testing_and_qa = development * 0.18
    project_management = development * 0.12
    contingency = (development + infrastructure + testing_and_qa + project_management) * 0.10
    full_total = development + infrastructure + testing_and_qa + project_management + contingency

    if full_total > profile.full_max:
        scale = profile.full_max / full_total
        development *= scale
        infrastructure *= scale
        testing_and_qa *= scale
        project_management *= scale
        contingency *= scale
        full_total = profile.full_max
    elif full_total < profile.full_min:
        scale = profile.full_min / max(full_total, 1)
        development *= scale
        infrastructure *= scale
        testing_and_qa *= scale
        project_management *= scale
        contingency *= scale
        full_total = profile.full_min

    mvp_total = min(max(full_total * 0.32, profile.mvp_min), profile.mvp_max)

    estimate.deep_cost_estimate.development = round(development)
    estimate.deep_cost_estimate.infrastructure = round(infrastructure)
    estimate.deep_cost_estimate.testing_and_qa = round(testing_and_qa)
    estimate.deep_cost_estimate.project_management = round(project_management)
    estimate.deep_cost_estimate.contingency = round(contingency)
    estimate.deep_cost_estimate.total = round(
        estimate.deep_cost_estimate.development
        + estimate.deep_cost_estimate.infrastructure
        + estimate.deep_cost_estimate.testing_and_qa
        + estimate.deep_cost_estimate.project_management
        + estimate.deep_cost_estimate.contingency
    )
    estimate.minimum_viable_cost.total = round(mvp_total)

    savings = max(0, estimate.deep_cost_estimate.total - estimate.minimum_viable_cost.total)
    savings_percent = round((savings / estimate.deep_cost_estimate.total) * 100) if estimate.deep_cost_estimate.total else 0

    _add_unique(estimate.assumptions, "Costs are calibrated for the Indian INR market.")
    _add_unique(estimate.assumptions, profile.note)
    _add_unique(
        estimate.minimum_scope_notes,
        (
            f"Lean open-source MVP path saves about {savings_percent}% versus a fuller "
            "custom build by limiting scope, reusing proven libraries, and avoiding "
            "paid tools until traction justifies them."
        ),
    )
    _add_unique(
        estimate.team_recommendation,
        "Start with a compact team: 1 full-stack/mobile developer, part-time UI/UX, and QA near release.",
    )
    _add_unique(
        estimate.minimum_viable_cost.what_is_included,
        "Open-source/reusable implementation path focused on playable core flow, basic polish, and launch readiness.",
    )

    return estimate


def normalize_roadmap_for_value(
    roadmap: RoadmapResponse,
    project_idea: str,
    currency: str,
) -> RoadmapResponse:
    roadmap.currency = currency
    for phase in roadmap.phases:
        phase.currency = currency

    profile = detect_pricing_profile(project_idea)
    if currency != DEFAULT_CURRENCY or profile is None:
        return roadmap

    if roadmap.total_cost > profile.full_max and roadmap.total_cost > 0:
        scale = profile.full_max / roadmap.total_cost
        for phase in roadmap.phases:
            phase.estimated_cost = round(phase.estimated_cost * scale)
        roadmap.total_cost = round(sum(phase.estimated_cost for phase in roadmap.phases))

    if roadmap.mvp_cost > profile.mvp_max:
        roadmap.mvp_cost = profile.mvp_max
    if roadmap.phases:
        roadmap.phases[0].estimated_cost = min(roadmap.phases[0].estimated_cost, profile.mvp_max)
        roadmap.mvp_cost = min(roadmap.mvp_cost, roadmap.phases[0].estimated_cost)
        roadmap.total_cost = round(sum(phase.estimated_cost for phase in roadmap.phases))

    return roadmap


def normalize_team_for_value(
    team: TeamResponse,
    project_idea: str,
    currency: str,
) -> TeamResponse:
    team.currency = currency

    profile = detect_pricing_profile(project_idea)
    if currency != DEFAULT_CURRENCY or profile is None:
        return team

    computed_total = sum(member.estimated_monthly_rate * member.duration_months for member in team.team)
    if computed_total > profile.full_max and computed_total > 0:
        scale = profile.full_max / computed_total
        for member in team.team:
            member.estimated_monthly_rate = round(member.estimated_monthly_rate * scale)

    team.total_monthly_cost = round(sum(member.estimated_monthly_rate for member in team.team))
    team.total_project_cost = round(
        sum(member.estimated_monthly_rate * member.duration_months for member in team.team)
    )
    team.hiring_strategy = (
        "Use a lean India-based MVP team and open-source tooling first; add specialist "
        "roles only after the core product proves traction."
    )
    return team


def normalize_tech_stack_for_value(
    tech_stack: TechStackResponse,
    project_idea: str,
    currency: str,
) -> TechStackResponse:
    tech_stack.currency = currency

    profile = detect_pricing_profile(project_idea)
    if currency != DEFAULT_CURRENCY or profile is None:
        return tech_stack

    paid_monthly_total = 0.0
    open_source_monthly_total = 0.0
    for comparison in tech_stack.comparisons:
        comparison.open_source.cost_per_month = min(comparison.open_source.cost_per_month, 2_000)
        comparison.paid.cost_per_month = max(comparison.paid.cost_per_month, comparison.open_source.cost_per_month)
        paid_monthly_total += comparison.paid.cost_per_month
        open_source_monthly_total += comparison.open_source.cost_per_month

    monthly_savings = max(0, paid_monthly_total - open_source_monthly_total)
    if monthly_savings > 0:
        tech_stack.estimated_savings_vs_paid = round(monthly_savings)

    return tech_stack


def _add_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)
