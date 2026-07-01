from fastapi import APIRouter
from analysis.blast_radius_predictor import BlastRadiusPredictor

router = APIRouter()


@router.get("/blast-radius")
def blast_radius(
    component: str
):

    predictor = BlastRadiusPredictor()

    result = predictor.predict(
        component
    )

    return {
        "success": True,
        **result
    }