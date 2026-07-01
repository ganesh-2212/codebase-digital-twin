import os
import pickle

import networkx as nx


class CriticalComponentsAnalyzer:

    def __init__(self):
        self.graph = self.load_graph()

    def load_graph(self):
        path = "data/dependency_graph.pkl"

        if not os.path.exists(path):
            return nx.DiGraph()

        with open(path, "rb") as f:
            return pickle.load(f)

    def analyze(self):

        if len(self.graph.nodes()) == 0:
            return []

        centrality = nx.degree_centrality(self.graph)

        ranked = sorted(
            centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for node, score in ranked[:20]:

            if score > 0.10:
                risk = "Critical"
            elif score > 0.05:
                risk = "High"
            elif score > 0.02:
                risk = "Medium"
            else:
                risk = "Low"

            results.append(
                {
                    "component": node,
                    "score": round(score, 4),
                    "risk": risk
                }
            )

        return results