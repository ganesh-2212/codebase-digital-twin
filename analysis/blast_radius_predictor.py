import pickle
import os
import networkx as nx


class BlastRadiusPredictor:

    def __init__(
        self,
        graph_path="data/dependency_graph.pkl"
    ):

        self.graph_path = graph_path
        self.graph = self.load_graph()

    # ==========================================
    # LOAD GRAPH
    # ==========================================

    def load_graph(self):

        if not os.path.exists(
            self.graph_path
        ):
            return nx.DiGraph()

        with open(
            self.graph_path,
            "rb"
        ) as f:

            return pickle.load(f)

    # ==========================================
    # NORMALIZE PATH
    # ==========================================

    def normalize(
        self,
        value
    ):

        return (
            str(value)
            .replace("\\", "/")
            .strip()
            .lower()
        )

    # ==========================================
    # FIND COMPONENT IN GRAPH
    # ==========================================

    def find_node(
        self,
        component
    ):

        component = self.normalize(
            component
        )

        # Exact match
        for node in self.graph.nodes():

            if self.normalize(node) == component:
                return node

        # Full filename match
        filename = component.split("/")[-1]

        for node in self.graph.nodes():

            node_name = self.normalize(node)

            if node_name.endswith(filename):
                return node

        # Partial match
        for node in self.graph.nodes():

            node_name = self.normalize(node)

            if filename in node_name:
                return node

        return None

    # ==========================================
    # BLAST RADIUS PREDICTION
    # ==========================================

    def predict(
        self,
        component
    ):

        resolved_node = self.find_node(
            component
        )

        if resolved_node is None:

            print("\nComponent not found:", component)

            print("\nFirst 50 nodes in graph:\n")

            for node in list(
                self.graph.nodes()
            )[:50]:

                print(node)

            return {
                "component": component,
                "resolved_component": None,
                "direct_impact": [],
                "indirect_impact": [],
                "direct_count": 0,
                "indirect_count": 0,
                "blast_radius": 0,
                "risk": "Unknown"
            }

        # Files that depend directly on this component
        direct_impact = list(
            self.graph.predecessors(
                resolved_node
            )
        )

        # Files that depend indirectly on this component
        indirect_impact = set()

        for node in direct_impact:

            try:

                parents = nx.ancestors(
                    self.graph,
                    node
                )

                indirect_impact.update(
                    parents
                )

            except Exception:
                pass

        indirect_impact = list(
            indirect_impact
            - set(direct_impact)
            - {resolved_node}
        )

        blast_radius = (
            len(direct_impact)
            + len(indirect_impact)
        )

        # ======================================
        # RISK LEVEL
        # ======================================

        if blast_radius >= 100:
            risk = "Critical"

        elif blast_radius >= 50:
            risk = "High"

        elif blast_radius >= 20:
            risk = "Medium"

        elif blast_radius > 0:
            risk = "Low"

        else:
            risk = "Minimal"

        return {

            "component": component,

            "resolved_component": resolved_node,

            "direct_impact": sorted(
                direct_impact
            ),

            "indirect_impact": sorted(
                indirect_impact
            ),

            "direct_count": len(
                direct_impact
            ),

            "indirect_count": len(
                indirect_impact
            ),

            "blast_radius": blast_radius,

            "risk": risk
        }


if __name__ == "__main__":

    predictor = BlastRadiusPredictor()

    component = input(
        "Enter component name: "
    ).strip()

    result = predictor.predict(
        component
    )

    print("\nResult\n")

    for key, value in result.items():
        print(f"{key}: {value}")