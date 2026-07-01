import pickle
import os


class ChangePredictor:

    def __init__(self):

        graph_path = "data/dependency_graph.pkl"

        if os.path.exists(graph_path):

            with open(graph_path, "rb") as f:
                self.graph = pickle.load(f)

        else:
            self.graph = None

    # ======================================================
    # NORMALIZATION (CRITICAL FIX)
    # ======================================================

    def normalize(self, component_name: str):

        """
        Supports:
        - fastapi/applications.py
        - fastapi.applications
        - fastapi%2Fapplications.py (encoded URLs)
        """

        # Handle URL encoded slashes
        component_name = component_name.replace("%2F", "/")

        # Convert dot format → path format
        component_name = component_name.replace(".", "/")

        # Ensure .py exists
        if not component_name.endswith(".py"):
            component_name += ".py"

        return component_name

    # ======================================================
    # PREDICTION ENGINE
    # ======================================================

    def predict(self, component_name):

        if self.graph is None:
            return {
                "success": False,
                "message": "Dependency graph not found"
            }

        # 🔥 Normalize input
        component_name = self.normalize(component_name)

        # -------------------------
        # SAFE LOOKUP (EXACT + FALLBACK)
        # -------------------------

        if component_name not in self.graph:

            # fallback: partial match
            matches = [
                node for node in self.graph.nodes
                if component_name.replace(".py", "") in node
            ]

            if matches:
                component_name = matches[0]
            else:
                return {
                    "success": False,
                    "message": f"{component_name} not found in graph"
                }

        # ======================================================
        # DIRECT DEPENDENCIES
        # ======================================================

        try:
            direct = list(self.graph.successors(component_name))
        except Exception:
            direct = []

        # ======================================================
        # INDIRECT DEPENDENCIES
        # ======================================================

        indirect = set()

        for dep in direct:
            try:
                for second in self.graph.successors(dep):
                    indirect.add(second)
            except Exception:
                continue

        # ======================================================
        # BLAST RADIUS + RISK
        # ======================================================

        blast_radius = len(direct) + len(indirect)

        if blast_radius > 20:
            risk = "HIGH"
        elif blast_radius > 10:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # ======================================================
        # RESPONSE
        # ======================================================

        return {
            "success": True,
            "component": component_name,
            "direct_impact": direct,
            "indirect_impact": list(indirect),
            "blast_radius": blast_radius,
            "risk": risk
        }