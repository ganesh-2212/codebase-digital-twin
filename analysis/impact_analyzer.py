import pickle


class ImpactAnalyzer:

    def __init__(self):

        self.graph_data = self.load_graph()

        self.nodes = set(
            self.graph_data["nodes"]
        )

        self.edges = (
            self.graph_data["edges"]
        )

        self.adjacency = (
            self.build_adjacency()
        )

    # ==========================================
    # LOAD GRAPH
    # ==========================================

    def load_graph(self):

        with open(
            "data/call_graph.pkl",
            "rb"
        ) as f:

            return pickle.load(f)

    # ==========================================
    # BUILD ADJACENCY LIST
    # ==========================================

    def build_adjacency(self):

        adjacency = {}

        for edge in self.edges:

            source = edge["source"]
            target = edge["target"]

            if source not in adjacency:

                adjacency[source] = []

            adjacency[source].append(
                target
            )

        return adjacency

    # ==========================================
    # SEARCH NODES
    # ==========================================

    def search_nodes(
        self,
        keyword
    ):

        keyword = keyword.lower()

        matches = []

        for node in self.nodes:

            if keyword in str(node).lower():

                matches.append(node)

        return sorted(matches)

    # ==========================================
    # IMPACT ANALYSIS
    # ==========================================

    def analyze(
        self,
        target_node,
        depth=2
    ):

        impacted = set()

        current = {target_node}

        for _ in range(depth):

            next_level = set()

            for node in current:

                neighbors = self.adjacency.get(
                    node,
                    []
                )

                next_level.update(
                    neighbors
                )

            impacted.update(
                next_level
            )

            current = next_level

        return sorted(
            impacted
        )

    # ==========================================
    # FIND + ANALYZE
    # ==========================================

    def analyze_keyword(
        self,
        keyword,
        depth=2
    ):

        matches = self.search_nodes(
            keyword
        )

        if not matches:

            print(
                "\nNo matching nodes found."
            )

            return

        print(
            "\nMatching Nodes:\n"
        )

        for i, node in enumerate(
            matches[:20]
        ):

            print(
                f"{i+1}. {node}"
            )

        target = matches[0]

        print(
            f"\nAnalyzing: {target}"
        )

        impacted = self.analyze(
            target,
            depth
        )

        print(
            f"\nImpacted Components ({len(impacted)}):\n"
        )

        for item in impacted:

            print(item)


if __name__ == "__main__":

    analyzer = ImpactAnalyzer()

    query = input(
        "Enter function/class name: "
    )

    analyzer.analyze_keyword(
        query,
        depth=2
    )