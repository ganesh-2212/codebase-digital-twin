from fastapi import APIRouter
import pickle

router = APIRouter()


@router.get("/cluster/{cluster_id}")
def get_cluster(
    cluster_id: int
):

    with open(
        "data/architecture_clusters.pkl",
        "rb"
    ) as f:
        clusters = pickle.load(f)

    with open(
        "data/architecture_summaries.pkl",
        "rb"
    ) as f:
        summaries = pickle.load(f)

    cluster_components = clusters.get(
        cluster_id,
        []
    )

    nodes = []
    edges = []

    component_names = set(
        cluster_components
    )

    for component in summaries:

        if component["name"] in component_names:

            nodes.append({
                "id": component["name"],
                "label": component["name"],
                "type": component["type"]
            })

            for called in component.get(
                "calls",
                []
            ):

                if called in component_names:

                    edges.append({
                        "source":
                        component["name"],

                        "target":
                        called
                    })

    return {
        "nodes": nodes,
        "edges": edges
    }