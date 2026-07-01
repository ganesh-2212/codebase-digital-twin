import pickle
import networkx as nx

from networkx.algorithms.community import (
    greedy_modularity_communities
)


# ==========================================
# LOAD GRAPH
# ==========================================

def load_graph():

    with open(
        "data/dependency_graph.pkl",
        "rb"
    ) as f:

        graph = pickle.load(f)

    return graph


# ==========================================
# CLUSTER NAMING
# ==========================================

def generate_cluster_name(
    members
):

    text = (
        " ".join(members)
    ).lower()

    # API Layer
    if any(
        keyword in text
        for keyword in [
            "router",
            "request",
            "response",
            "endpoint",
            "fastapi",
            "route",
            "api"
        ]
    ):
        return "API Layer"

    # Testing Layer
    if any(
        keyword in text
        for keyword in [
            "test",
            "pytest",
            "mock",
            "fixture"
        ]
    ):
        return "Testing Layer"

    # Database Layer
    if any(
        keyword in text
        for keyword in [
            "database",
            "session",
            "engine",
            "sql",
            "model",
            "orm"
        ]
    ):
        return "Database Layer"

    # Authentication Layer
    if any(
        keyword in text
        for keyword in [
            "auth",
            "oauth",
            "jwt",
            "token",
            "security"
        ]
    ):
        return "Authentication Layer"

    # Dependency Injection Layer
    if any(
        keyword in text
        for keyword in [
            "depends",
            "dependency",
            "inject"
        ]
    ):
        return (
            "Dependency Injection Layer"
        )

    # CLI Layer
    if any(
        keyword in text
        for keyword in [
            "cli",
            "command",
            "terminal"
        ]
    ):
        return "CLI Layer"

    # Middleware Layer
    if any(
        keyword in text
        for keyword in [
            "middleware",
            "cors",
            "gzip"
        ]
    ):
        return "Middleware Layer"

    # Schema Layer
    if any(
        keyword in text
        for keyword in [
            "schema",
            "pydantic",
            "validator"
        ]
    ):
        return "Schema Layer"

    return "Core Architecture Layer"


# ==========================================
# DETECT COMMUNITIES
# ==========================================

def detect_communities(
    graph
):

    undirected_graph = (
        graph.to_undirected()
    )

    communities = (
        greedy_modularity_communities(
            undirected_graph
        )
    )

    cluster_data = []

    print(
        "\n========== COMMUNITIES ==========\n"
    )

    for index, community in enumerate(
        communities
    ):

        members = sorted(
            list(community)
        )

        cluster_name = (
            generate_cluster_name(
                members
            )
        )

        cluster_data.append({

            "cluster_id":
                index + 1,

            "cluster_name":
                cluster_name,

            "size":
                len(members),

            "members":
                members
        })

        print(
            f"{cluster_name} "
            f"({len(members)} nodes)"
        )

    return cluster_data


# ==========================================
# SAVE CLUSTERS
# ==========================================

def save_clusters(
    cluster_data
):

    with open(
        "data/architecture_clusters.pkl",
        "wb"
    ) as f:

        pickle.dump(
            cluster_data,
            f
        )

    print(
        "\nSaved clusters -> "
        "data/architecture_clusters.pkl"
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    graph = load_graph()

    clusters = (
        detect_communities(
            graph
        )
    )

    save_clusters(
        clusters
    )

    print(
        f"\nTotal Clusters: "
        f"{len(clusters)}"
    )