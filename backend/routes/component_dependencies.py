from fastapi import APIRouter
import pickle

router = APIRouter()

@router.get("/component-dependencies/{name}")
def component_dependencies(name: str):

    with open(
        "data/architecture_summaries.pkl",
        "rb"
    ) as f:
        summaries = pickle.load(f)

    for item in summaries:

        if item["name"] == name:

            return {
                "success": True,
                "name": name,
                "calls": item.get("calls", []),
                "called_by": item.get("called_by", [])
            }

    return {
        "success": False
    }