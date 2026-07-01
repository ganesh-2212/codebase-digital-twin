from fastapi import APIRouter
from architecture_analysis.architecture_health_score import ArchitectureHealthScore

router = APIRouter()


@router.get("/architecture-health")
def architecture_health():

    engine = ArchitectureHealthScore()

    result = engine.calculate()

    return {
        "success": True,
        **result
    }