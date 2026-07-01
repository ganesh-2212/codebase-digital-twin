import pickle
import os


class LayerDetector:

    def __init__(self):
        self.summaries = self.load_summaries()

    # ======================================================
    # LOAD SUMMARIES
    # ======================================================
    def load_summaries(self):

        path = "data/architecture_summaries.pkl"

        if not os.path.exists(path):
            print("No architecture summaries found. Run parser first.")
            return []

        with open(path, "rb") as f:
            return pickle.load(f)

    # ======================================================
    # CLASSIFY LAYER (FIXED + CLEAN ARCHITECTURE LOGIC)
    # ======================================================
    def classify(self, name, file_path):

        path = (file_path or "").lower()
        name = (name or "").lower()

        # =========================
        # API LAYER
        # =========================
        if any(x in path for x in [
            "route", "routes", "api", "controller", "main", "app"
        ]):
            return "API"

        # =========================
        # SERVICE LAYER
        # =========================
        if any(x in path for x in [
            "service", "services", "business", "logic"
        ]):
            return "Service"

        # =========================
        # DATA LAYER
        # =========================
        if any(x in path for x in [
            "repository", "repo", "dao", "data_access"
        ]):
            return "Data"

        # =========================
        # DOMAIN LAYER
        # =========================
        if any(x in path for x in [
            "model", "models", "schema", "entity", "domain"
        ]):
            return "Domain"

        # =========================
        # INFRASTRUCTURE LAYER
        # =========================
        if any(x in path for x in [
            "database", "db", "cache", "redis",
            "client", "config", "settings",
            "util", "utils"
        ]):
            return "Infrastructure"

        # =========================
        # EXTERNAL / THIRD-PARTY (IMPORTANT FIX)
        # =========================
        if any(x in path for x in [
            "fastapi",
            "pydantic",
            "starlette",
            "typing",
            "contextlib",
            "docs_src",
            "tests"
        ]):
            return "External"

        # =========================
        # FALLBACK (IMPORTANT FIX)
        # =========================
        return "Domain"

    # ======================================================
    # BUILD LAYERS
    # ======================================================
    def detect(self):

        layers = {}

        for component in self.summaries:

            file_path = component.get("file", "")
            name = component.get("name", "")

            layer = self.classify(name, file_path)

            layers.setdefault(layer, []).append({
                "name": name,
                "file": file_path
            })

        return layers

    # ======================================================
    # SAVE RESULT
    # ======================================================
    def save(self, layers):

        os.makedirs("data", exist_ok=True)

        with open("data/architecture_layers.pkl", "wb") as f:
            pickle.dump(layers, f)


# ======================================================
# MAIN ENTRY
# ======================================================
if __name__ == "__main__":

    detector = LayerDetector()

    print("\nRunning Layer Detection...\n")

    layers = detector.detect()

    detector.save(layers)

    print("\nLayer detection completed successfully!")
    print(f"Total layers found: {len(layers)}")

    for k, v in layers.items():
        print(f" - {k}: {len(v)} components")