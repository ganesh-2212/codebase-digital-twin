import pickle
from fastapi import APIRouter

router = APIRouter()


@router.get("/clusters")
def get_clusters():

    try:

        with open(
            "data/architecture_clusters.pkl",
            "rb"
        ) as f:

            raw_clusters = pickle.load(f)

        clusters = []

        for cluster_id, members in raw_clusters.items():

            clusters.append({
                "cluster_id": cluster_id,
                "cluster_name": f"Cluster {cluster_id}",
                "size": len(members),
                "members": members
            })

        clusters.sort(
            key=lambda x: x["size"],
            reverse=True
        )

        return clusters

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }