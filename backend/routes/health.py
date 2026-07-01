from fastapi import APIRouter
from analysis.health_score import HealthScore

router = APIRouter()


@router.get("/health")
def health():

    engine = HealthScore()

    result = engine.evaluate(
        smells=0,
        cycles=0,
        violations=0,
        high_risk_components=0
    )

    return {
        "success": True,
        **result
    }