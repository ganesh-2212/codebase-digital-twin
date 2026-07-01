import pickle

from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
def get_stats():

    clusters = pickle.load(
        open(
            "data/architecture_clusters.pkl",
            "rb"
        )
    )

    return {

        "clusters":
        len(clusters),

        "components":
        sum(
            len(c)
            for c in clusters.values()
        )

    }