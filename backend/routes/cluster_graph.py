from fastapi import APIRouter
import pickle

router = APIRouter()


@router.get("/cluster-graph")
def get_cluster_graph():

    with open(
        "data/architecture_clusters.pkl",
        "rb"
    ) as f:
        clusters = pickle.load(f)

    nodes = []
    edges = []

    for cluster_id, components in clusters.items():

        nodes.append({
            "id": str(cluster_id),
            "label": f"Cluster {cluster_id}",
            "size": len(components)
        })

    return {
        "nodes": nodes,
        "edges": edges
    }