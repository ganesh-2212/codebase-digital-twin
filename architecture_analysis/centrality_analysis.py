import networkx as nx
from graph_engine_loader import load_graph


def analyze_centrality(graph):

    centrality = nx.degree_centrality(graph)

    sorted_nodes = sorted(
        centrality.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\nTop Critical Modules:\n")

    for node, score in sorted_nodes[:20]:
        print(f"{node} --> Centrality Score: {score:.4f}")


if __name__ == "__main__":

    graph = load_graph()

    analyze_centrality(graph)