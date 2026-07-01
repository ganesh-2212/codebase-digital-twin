from fastapi import APIRouter
import pickle
import os

router = APIRouter()


def load_summaries():

    path = "data/architecture_summaries.pkl"

    if not os.path.exists(path):
        return []

    with open(path, "rb") as f:
        return pickle.load(f)


@router.get("/change-prediction/{component_path:path}")
def predict(component_path: str):

    summaries = load_summaries()

    component_path = (
        component_path
        .replace("\\", "/")
        .strip()
        .lower()
    )

    affected_components = []

    for component in summaries:

        file_path = (
            component.get("file", "")
            .replace("\\", "/")
            .strip()
            .lower()
        )

        if file_path == component_path:
            affected_components.append(component)

    if not affected_components:
        return {
            "success": False,
            "message": "Component not found",
            "component": component_path
        }

    impact_score = len(affected_components) * 5

    if impact_score >= 80:
        risk_level = "Critical"

    elif impact_score >= 60:
        risk_level = "High"

    elif impact_score >= 40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "success": True,
        "component": component_path,
        "risk_level": risk_level,
        "estimated_impact": impact_score,
        "architectural_elements": len(affected_components),
        "reason": (
            f"{len(affected_components)} architectural "
            f"elements exist inside this file."
        )
    }