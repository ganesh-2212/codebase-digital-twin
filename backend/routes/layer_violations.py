from fastapi import APIRouter
import pickle
import os

router = APIRouter()


def load_layers():

    path = "data/architecture_layers.pkl"

    if not os.path.exists(path):
        return {}

    with open(path, "rb") as f:
        return pickle.load(f)


def build_layer_map(layers):

    layer_map = {}

    for layer, components in layers.items():

        for comp in components:

            file_path = (comp.get("file", "") or "").replace("\\", "/")

            if not file_path:
                continue

            layer_map[file_path] = layer
            layer_map[file_path.split("/")[-1]] = layer

    return layer_map


RULES = {
    "API": ["Service", "Data", "Domain"],
    "Service": ["Data", "Domain"],
    "Data": ["Domain"],
    "Domain": [],
    "Infrastructure": ["API", "Service", "Data", "Domain"]
}


NOISE = {
    "get", "post", "put", "delete", "patch",
    "fastapi", "pydantic", "starlette"
}


def is_violation(src, tgt):

    if src == "Unknown" or tgt == "Unknown":
        return False

    return tgt not in RULES.get(src, [])


@router.get("/layer-violations")
def get_layer_violations():

    layers = load_layers()
    layer_map = build_layer_map(layers)

    graph_path = "data/dependency_graph.pkl"

    if not os.path.exists(graph_path):
        return {"success": False, "message": "graph not found"}

    with open(graph_path, "rb") as f:
        graph = pickle.load(f)

    violations = []

    for source, target in graph.edges():

        source = str(source).replace("\\", "/")
        target = str(target).replace("\\", "/")

        if any(n in source.lower() for n in NOISE):
            continue

        if any(n in target.lower() for n in NOISE):
            continue

        src_layer = layer_map.get(source) or layer_map.get(source.split("/")[-1], "Unknown")
        tgt_layer = layer_map.get(target) or layer_map.get(target.split("/")[-1], "Unknown")

        if is_violation(src_layer, tgt_layer):

            violations.append({
                "source": source,
                "target": target,
                "source_layer": src_layer,
                "target_layer": tgt_layer,
                "severity": "high",
                "message": f"{src_layer} should not depend on {tgt_layer}"
            })

    return {
        "success": True,
        "count": len(violations),
        "violations": violations[:200]
    }