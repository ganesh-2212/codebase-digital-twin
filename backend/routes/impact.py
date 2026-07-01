from fastapi import APIRouter
from pydantic import BaseModel

import os

from analysis.change_impact_predictor import (
    ChangeImpactPredictor
)

router = APIRouter()

predictor = None


class ImpactRequest(BaseModel):
    component: str


@router.post("/impact")
def get_impact(request: ImpactRequest):

    global predictor

    required_files = [
        "data/architecture_summaries.pkl",
        "data/dependency_graph.pkl"
    ]

    missing = [
        f for f in required_files
        if not os.path.exists(f)
    ]

    if missing:
        return {
            "success": False,
            "error":
                "Repository analysis has not been performed yet.",
            "missing_files": missing
        }

    if predictor is None:
        predictor = ChangeImpactPredictor()

    try:

        result = predictor.predict(
            request.component
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }