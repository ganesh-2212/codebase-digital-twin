from fastapi import APIRouter
import pickle
import os

router = APIRouter()


# ==========================================
# LOAD CLUSTERS
# ==========================================

def load_clusters():

    path = "data/architecture_clusters.pkl"

    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


# ==========================================
# LOAD SUMMARIES
# ==========================================

def load_summaries():

    path = "data/architecture_summaries.pkl"

    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


# ==========================================
# BUILD COMPONENT -> CLUSTER MAP
# ==========================================

def build_component_cluster_map(clusters):

    mapping = {}

    # OLD FORMAT
    # {1:[a,b,c],2:[d,e,f]}
    if isinstance(clusters, dict):

        for cluster_id, members in clusters.items():

            for component in members:

                mapping[component] = cluster_id

        return mapping

    # NEW FORMAT
    # [{"cluster_id":1,"members":[...]}]
    if isinstance(clusters, list):

        for cluster in clusters:

            cid = cluster.get("cluster_id")

            for component in cluster.get(
                "members",
                []
            ):

                mapping[component] = cid

    return mapping


# ==========================================
# CLUSTER GRAPH
# ==========================================

@router.get("/cluster-relationships")
def get_cluster_relationships():

    clusters = load_clusters()
    summaries = load_summaries()

    if clusters is None:

        return {
            "success": False,
            "message": "No clusters found"
        }

    if summaries is None:

        return {
            "success": False,
            "message": "No summaries found"
        }

    component_cluster = (
        build_component_cluster_map(
            clusters
        )
    )

    relationship_weights = {}

    for component in summaries:

        source_component = component["name"]

        if source_component not in component_cluster:
            continue

        source_cluster = (
            component_cluster[source_component]
        )

        for dependency in component.get(
            "calls",
            []
        ):

            if dependency not in component_cluster:
                continue

            target_cluster = (
                component_cluster[dependency]
            )

            if source_cluster == target_cluster:
                continue

            key = (
                source_cluster,
                target_cluster
            )

            relationship_weights[key] = (
                relationship_weights.get(
                    key,
                    0
                ) + 1
            )

    # =====================================
    # NODES
    # =====================================

    nodes = []

    if isinstance(clusters, dict):

        for cluster_id, members in clusters.items():

            nodes.append({

                "id": str(cluster_id),

                "label":
                    f"Cluster {cluster_id}",

                "size":
                    len(members)
            })

    else:

        for cluster in clusters:

            nodes.append({

                "id":
                    str(
                        cluster["cluster_id"]
                    ),

                "label":
                    cluster["cluster_name"],

                "size":
                    cluster["size"]
            })

    # =====================================
    # EDGES
    # =====================================

    edges = []

    for (
        source,
        target
    ), weight in relationship_weights.items():

        edges.append({

            "source": str(source),

            "target": str(target),

            "weight": weight
        })

    print(
        f"Cluster Graph: "
        f"{len(nodes)} nodes "
        f"{len(edges)} edges"
    )

    return {

        "success": True,

        "nodes": nodes,

        "edges": edges
    }