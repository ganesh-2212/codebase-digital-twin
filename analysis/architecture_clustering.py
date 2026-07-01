import pickle
import networkx as nx

from networkx.algorithms.community import (
    greedy_modularity_communities
)


class ArchitectureClustering:

    def __init__(self):

        self.graph = self.load_graph()

    # ==========================================
    # LOAD GRAPH
    # ==========================================

    def load_graph(self):

        with open(
            "data/call_graph.pkl",
            "rb"
        ) as f:

            data = pickle.load(f)

        graph = nx.Graph()

        for edge in data["edges"]:

            graph.add_edge(
                edge["source"],
                edge["target"]
            )

        return graph

    # ==========================================
    # CLUSTER
    # ==========================================

    def cluster(self):

        communities = greedy_modularity_communities(
            self.graph
        )

        clusters = []

        for idx, community in enumerate(
            communities
        ):

            clusters.append({

                "cluster_id": idx,

                "size": len(
                    community
                ),

                "nodes": list(
                    community
                )

            })

        return clusters


if __name__ == "__main__":

    clustering = ArchitectureClustering()

    clusters = clustering.cluster()

    print(
        f"\nFound {len(clusters)} clusters\n"
    )

    for cluster in clusters[:10]:

        print(
            f"\nCluster "
            f"{cluster['cluster_id']}"
        )

        print(
            f"Size: "
            f"{cluster['size']}"
        )

        print(
            cluster["nodes"][:20]
        )