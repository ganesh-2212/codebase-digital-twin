import pickle
import os


class SmellDetector:

    def __init__(self):
        self.summaries = self.load_summaries()

    def load_summaries(self):

        path = "data/architecture_summaries.pkl"

        if not os.path.exists(path):
            return []

        with open(path, "rb") as f:
            return pickle.load(f)

    # ==========================================
    # STRICT NOISE FILTER (CRITICAL FIX)
    # ==========================================
    def is_noise(self, name):

        if not name:
            return True

        name = name.lower()

        if len(name) < 5:
            return True

        noise_words = {
            "get", "set", "run", "main",
            "__init__", "__call__", "__str__"
        }

        if name in noise_words:
            return True

        if name.startswith("test_"):
            return True

        return False

    # ==========================================
    # MAIN DETECTION (FIXED LOGIC)
    # ==========================================
    def detect(self):

        smells = []

        total_nodes = len(self.summaries)
        if total_nodes == 0:
            return []

        for component in self.summaries:

            name = component.get("name", "")

            if self.is_noise(name):
                continue

            methods = len(component.get("methods", []))
            calls = len(component.get("calls", []))
            inherits = len(component.get("inherits", []))

            complexity = methods + calls + inherits

            # =================================================
            # NORMALIZED THRESHOLDS (IMPORTANT FIX)
            # =================================================

            # GOD OBJECT (VERY STRICT)
            if complexity > 150:
                smells.append({
                    "name": name,
                    "type": "God Object",
                    "severity": "Critical",
                    "score": complexity
                })

            # HIGH COUPLING (NORMALIZED)
            elif calls > 50:
                smells.append({
                    "name": name,
                    "type": "High Coupling",
                    "severity": "High",
                    "score": calls
                })

            # LOW USAGE (REAL DEAD CODE SIGNAL)
            elif len(component.get("called_by", [])) == 0 and calls == 0:
                smells.append({
                    "name": name,
                    "type": "Dead Component",
                    "severity": "Low",
                    "score": 1
                })

        # ==========================================
        # HARD CAP (CRITICAL FIX)
        # Prevent explosion like 660 smells
        # ==========================================
        MAX_SMELLS = int(total_nodes * 0.15)

        smells = smells[:MAX_SMELLS]

        # ==========================================
        # DEDUPLICATION
        # ==========================================
        unique = []
        seen = set()

        for s in smells:
            key = (s["name"], s["type"])
            if key not in seen:
                seen.add(key)
                unique.append(s)

        return unique