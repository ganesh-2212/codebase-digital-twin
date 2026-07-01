import pickle
from fastapi import APIRouter

router = APIRouter()


@router.get("/architecture")
def get_architecture():

    with open(
        "data/dependency_graph.pkl",
        "rb"
    ) as f:

        graph = pickle.load(f)

    nodes = []
    edges = []

    # -----------------------------
    # FILTER USELESS NODES
    # -----------------------------

    excluded_keywords = [

        "venv",
        "site-packages",
        "__pycache__",
        ".git",
        "tests",
        "docs"

    ]

    valid_nodes = set()

    for node in graph.nodes():

        node_str = str(node)

        if any(
            keyword in node_str
            for keyword in excluded_keywords
        ):
            continue

        valid_nodes.add(node_str)

        nodes.append({

            "id": node_str,
            "label": node_str

        })

    # -----------------------------
    # FILTER EDGES
    # -----------------------------

    for source, target in graph.edges():

        source = str(source)
        target = str(target)

        if source not in valid_nodes:
            continue

        if target not in valid_nodes:
            continue

        edges.append({

            "source": source,
            "target": target

        })

    print(
        f"Architecture Graph -> Nodes: {len(nodes)} | Edges: {len(edges)}"
    )

    return {

        "nodes": nodes,
        "edges": edges

    }