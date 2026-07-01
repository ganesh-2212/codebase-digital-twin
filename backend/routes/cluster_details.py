import pickle
import os
from fastapi import APIRouter

router = APIRouter()


def load_clusters():

    path = "data/architecture_clusters.pkl"

    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


@router.get("/clusters")
def get_clusters():

    clusters = load_clusters()

    if clusters is None:
        return {
            "success": False,
            "message": "No clusters found"
        }

    result = []

    for cluster_id, members in clusters.items():

        result.append({
            "id": str(cluster_id),
            "name": f"Cluster {cluster_id}",
            "size": len(members)
        })

    return {
        "success": True,
        "clusters": result
    }


@router.get("/cluster-details/{cluster_id}")
def get_cluster_details(cluster_id: int):

    clusters = load_clusters()

    if clusters is None:
        return {
            "success": False,
            "message": "No clusters found"
        }

    if cluster_id not in clusters:
        return {
            "success": False,
            "message": f"Cluster {cluster_id} not found"
        }

    members = clusters[cluster_id]

    return {
        "success": True,
        "cluster_id": cluster_id,
        "cluster_name": f"Cluster {cluster_id}",
        "size": len(members),
        "components": members
    }