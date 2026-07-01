from fastapi import APIRouter
import pickle

router = APIRouter()


@router.get("/architecture-graph")
def get_architecture_graph():

    # ======================================
    # LOAD CALL GRAPH
    # ======================================

    with open(
        "data/call_graph.pkl",
        "rb"
    ) as f:

        graph = pickle.load(f)

    raw_nodes = graph.get(
        "nodes",
        []
    )

    raw_edges = graph.get(
        "edges",
        []
    )

    nodes = []
    edges = []

    existing_ids = set()

    # ======================================
    # BUILD NODES
    # ======================================

    for node in raw_nodes:

        node_id = str(
            node["id"]
        )

        if node_id in existing_ids:
            continue

        existing_ids.add(
            node_id
        )

        nodes.append({

            "id": node_id,

            "label":
                node["name"],

            "full_name":
                node["name"],

            "type":
                node["type"],

            "file":
                node["file"]

        })

    # ======================================
    # BUILD EDGES
    # ======================================

    edge_set = set()

    for edge in raw_edges:

        source = str(
            edge["source"]
        )

        target = str(
            edge["target"]
        )

        # Ignore external library calls
        if (
            source not in existing_ids
            or target not in existing_ids
        ):
            continue

        edge_key = (
            source,
            target
        )

        # Remove duplicate edges
        if edge_key in edge_set:
            continue

        edge_set.add(
            edge_key
        )

        edges.append({

            "source": source,
            "target": target

        })

    # ======================================
    # DEBUG
    # ======================================

    print(
        "\n========== GRAPH API =========="
    )

    print(
        f"Nodes Returned: {len(nodes)}"
    )

    print(
        f"Edges Returned: {len(edges)}"
    )

    print(
        "===============================\n"
    )

    # ======================================
    # RESPONSE
    # ======================================

    return {

        "nodes": nodes,
        "edges": edges

    }