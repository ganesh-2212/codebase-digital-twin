import networkx as nx
import pickle
import os


class CircularDependencyDetector:

    def __init__(
        self,
        graph_path="data/dependency_graph.pkl"
    ):
        self.graph_path = graph_path
        self.graph = self.load_graph()

    # =====================================================
    # LOAD GRAPH
    # =====================================================

    def load_graph(self):

        if not os.path.exists(self.graph_path):
            return nx.DiGraph()

        with open(
            self.graph_path,
            "rb"
        ) as f:
            return pickle.load(f)

    # =====================================================
    # CYCLE DETECTION
    # =====================================================

    def detect_cycles(self):

        if (
            self.graph is None or
            len(self.graph.nodes()) == 0
        ):
            return {
                "count": 0,
                "cycles": []
            }

        strongly_connected_components = list(
            nx.strongly_connected_components(
                self.graph
            )
        )

        cycles = []

        for component in strongly_connected_components:

            # -----------------------------------------
            # Multi-node cycle
            # -----------------------------------------
            if len(component) > 1:

                subgraph = self.graph.subgraph(
                    component
                )

                try:
                    cycle_path = list(
                        nx.find_cycle(
                            subgraph,
                            orientation="original"
                        )
                    )
                except Exception:
                    cycle_path = []

                cycles.append({
                    "type": "cycle_group",
                    "nodes": sorted(
                        list(component)
                    ),
                    "path": cycle_path
                })

            # -----------------------------------------
            # Self-loop cycle
            # -----------------------------------------
            else:

                node = list(component)[0]

                if self.graph.has_edge(
                    node,
                    node
                ):
                    cycles.append({
                        "type": "self_loop",
                        "nodes": [node],
                        "path": [
                            (node, node)
                        ]
                    })

        return {
            "count": len(cycles),
            "cycles": cycles
        }

    # =====================================================
    # BACKWARD COMPATIBILITY
    # =====================================================

    def detect(self):
        return self.detect_cycles()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    detector = CircularDependencyDetector()

    result = detector.detect_cycles()

    print(
        "Circular Dependency Detection Complete"
    )

    print(
        "Cycle Count:",
        result["count"]
    )

    for cycle in result["cycles"]:

        print("\nCycle Type:", cycle["type"])

        print(
            "Nodes:",
            cycle["nodes"]
        )