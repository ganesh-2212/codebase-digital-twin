import pickle
import networkx as nx


class CircularDependencyDetector:

    def __init__(self):

        graph_path = "data/dependency_graph.pkl"

        try:
            with open(graph_path, "rb") as f:
                self.graph = pickle.load(f)
        except Exception:
            self.graph = None

    def detect(self):

        if self.graph is None:
            return {
                "count": 0,
                "cycles": []
            }

        cycles = []

        try:
            # networkx cycle detection
            for cycle in nx.simple_cycles(self.graph):
                cycles.append(cycle)

        except Exception:
            cycles = []

        return {
            "count": len(cycles),
            "cycles": cycles
        }