import pickle
import networkx as nx


def load_graph():

    with open("data/dependency_graph.pkl", "rb") as f:
        graph = pickle.load(f)

    return graph


def analyze_impact(graph, target_module):

    if target_module not in graph:
        print(f"\nModule '{target_module}' not found.")
        return

    affected_modules = list(nx.ancestors(graph, target_module))
    
    print(f"\nImpact Analysis for: {target_module}\n")

    if not affected_modules:
        print("No affected modules found.")

    else:

        print("Potentially Affected Modules:\n")

        for module in affected_modules:
            print(module)


if __name__ == "__main__":

    graph = load_graph()

    target_module = input(
        "Enter module to analyze impact: "
    )

    analyze_impact(graph, target_module)