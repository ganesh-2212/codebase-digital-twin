import pickle

from fastapi import APIRouter

router = APIRouter()


@router.get("/component-impact/{component}")
def component_impact(component: str):

    with open(
        "data/dependency_graph.pkl",
        "rb"
    ) as f:

        graph = pickle.load(f)

    impacted = []

    if component in graph:

        impacted.extend(
            list(graph.successors(component))
        )

        impacted.extend(
            list(graph.predecessors(component))
        )

    return {
        "component": component,
        "impacted_components": list(
            set(impacted)
        )
    }