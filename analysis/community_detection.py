import pickle
import networkx as nx
import community as community_louvain


class CommunityDetector:

    def __init__(self):

        self.summaries = self.load_summaries()

    # ==========================================
    # LOAD SUMMARIES
    # ==========================================

    def load_summaries(self):

        with open(
            "data/architecture_summaries.pkl",
            "rb"
        ) as f:

            return pickle.load(f)

    # ==========================================
    # DETECT COMMUNITIES
    # ==========================================

    def detect(self):

        G = nx.Graph()

        # --------------------------------------
        # Build graph
        # --------------------------------------

        for item in self.summaries:

            component = item["name"]

            G.add_node(component)

            for dependency in item["calls"]:

                G.add_edge(
                    component,
                    dependency
                )

        print(
            f"\nCommunity Detection Graph:"
        )

        print(
            f"Nodes: {G.number_of_nodes()}"
        )

        print(
            f"Edges: {G.number_of_edges()}"
        )

        # --------------------------------------
        # Louvain
        # --------------------------------------

        partition = (
            community_louvain
            .best_partition(
                G,
                resolution=0.5,
                random_state=42
            )
        )

        clusters = {}

        for node, cluster_id in partition.items():

            clusters.setdefault(
                cluster_id,
                []
            ).append(node)

        # --------------------------------------
        # Merge tiny clusters
        # --------------------------------------

        merged_clusters = {}
        small_nodes = []

        new_cluster_id = 0

        for cluster_id, members in clusters.items():

            if len(members) < 5:

                small_nodes.extend(
                    members
                )

            else:

                merged_clusters[
                    new_cluster_id
                ] = members

                new_cluster_id += 1

        if small_nodes:

            merged_clusters[
                new_cluster_id
            ] = small_nodes

        # --------------------------------------
        # Statistics
        # --------------------------------------

        print("\nCluster Sizes\n")

        sorted_clusters = sorted(
            merged_clusters.items(),
            key=lambda x:
                len(x[1]),
            reverse=True
        )

        for cluster_id, members in sorted_clusters:

            print(
                f"Cluster {cluster_id}: "
                f"{len(members)} nodes"
            )

        print(
            f"\nFinal Clusters: "
            f"{len(merged_clusters)}"
        )

        return merged_clusters

    # ==========================================
    # SAVE
    # ==========================================

    def save(self, clusters):

        with open(
            "data/architecture_clusters.pkl",
            "wb"
        ) as f:

            pickle.dump(
                clusters,
                f
            )

        print(
            f"\nSaved "
            f"{len(clusters)} clusters"
        )