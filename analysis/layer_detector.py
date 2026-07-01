import pickle
import os


class LayerDetector:

    def __init__(self):
        self.summaries = self.load_summaries()

    def load_summaries(self):

        path = "data/architecture_summaries.pkl"

        if not os.path.exists(path):
            return []

        with open(path, "rb") as f:
            return pickle.load(f)

    # ==========================================
    # IMPROVED LAYER DETECTION (FIXED LOGIC)
    # ==========================================
    def detect_layer(self, component):

        file_path = (component.get("file", "") or "").lower().replace("\\", "/")

        name = (component.get("name", "") or "").lower()

        # -----------------------------
        # API LAYER (STRICT)
        # -----------------------------
        if any(x in file_path for x in [
            "router", "route", "api", "controller",
            "endpoint", "main", "app", "http"
        ]):
            return "API"

        # -----------------------------
        # SERVICE LAYER (ONLY BUSINESS LOGIC)
        # -----------------------------
        if "service" in file_path:
            return "Service"

        # scripts folder should NOT be Service (FIX)
        if "scripts" in file_path:
            return "Utility"

        # -----------------------------
        # DATA LAYER
        # -----------------------------
        if any(x in file_path for x in [
            "repo", "repository", "dao", "data_access"
        ]):
            return "Data"

        # -----------------------------
        # DOMAIN LAYER
        # -----------------------------
        if any(x in file_path for x in [
            "model", "schema", "entity", "domain"
        ]):
            return "Domain"

        # -----------------------------
        # INFRASTRUCTURE
        # -----------------------------
        if any(x in file_path for x in [
            "db", "database", "cache", "redis",
            "config", "settings", "logger"
        ]):
            return "Infrastructure"

        # -----------------------------
        # UTILITY LAYER (IMPORTANT FIX)
        # -----------------------------
        if any(x in file_path for x in [
            "utils", "util", "helper", "helpers",
            "scripts"
        ]):
            return "Utility"

        # -----------------------------
        # FINAL FALLBACK
        # -----------------------------
        return "Utility"

    def generate(self):

        layers = {}

        for c in self.summaries:

            layer = self.detect_layer(c)

            layers.setdefault(layer, []).append({
                "name": c.get("name", ""),
                "file": c.get("file", "")
            })

        return layers

    def save(self, layers):

        os.makedirs("data", exist_ok=True)

        with open("data/architecture_layers.pkl", "wb") as f:
            pickle.dump(layers, f)

        print(f"Saved {len(layers)} layers")


if __name__ == "__main__":

    detector = LayerDetector()
    layers = detector.generate()
    detector.save(layers)

    print("Layer detection completed")