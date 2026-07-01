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


@router.get("/impact-heatmap")
def impact_heatmap():

    summaries = load_summaries()

    nodes = []

    for component in summaries:

        impact_score = component.get(
            "impact_score",
            0
        )

        if impact_score >= 80:
            risk = "critical"

        elif impact_score >= 60:
            risk = "high"

        elif impact_score >= 40:
            risk = "medium"

        else:
            risk = "low"

        nodes.append({
            "name": component["name"],
            "impact_score": impact_score,
            "risk": risk,
            "cluster": component.get(
                "cluster",
                "Unknown"
            )
        })

    nodes = sorted(
        nodes,
        key=lambda x: x["impact_score"],
        reverse=True
    )

    return {
        "success": True,
        "components": nodes
    }