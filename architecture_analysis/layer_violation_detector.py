import pickle


class LayerViolationDetector:

    ALLOWED_DEPENDENCIES = {
        "API": ["Service"],
        "Service": ["Data", "Utils"],
        "Data": [],
        "Utils": []
    }

    def load_layers(self):
        with open("data/architecture_layers.pkl", "rb") as f:
            return pickle.load(f)

    def load_summaries(self):
        with open("data/architecture_summaries.pkl", "rb") as f:
            return pickle.load(f)

    def get_severity(
        self,
        source_layer,
        target_layer
    ):

        if target_layer == source_layer:
            return "low"

        if target_layer not in self.ALLOWED_DEPENDENCIES.get(
            source_layer,
            []
        ):
            return "high"

        return "low"

    def detect(self):

        layers = self.load_layers()
        summaries = self.load_summaries()

        component_layer = {}

        for layer, members in layers.items():
            for member in members:
                component_layer[member] = layer

        violations = []

        for component in summaries:

            source = component["name"]

            source_layer = component_layer.get(source)

            if not source_layer:
                continue

            for dependency in component.get(
                "calls",
                []
            ):

                target_layer = component_layer.get(
                    dependency
                )

                if not target_layer:
                    continue

                allowed = self.ALLOWED_DEPENDENCIES.get(
                    source_layer,
                    []
                )

                if target_layer not in allowed and target_layer != source_layer:

                    violations.append({
                        "source": source,
                        "target": dependency,
                        "source_layer": source_layer,
                        "target_layer": target_layer,
                        "severity": self.get_severity(
                            source_layer,
                            target_layer
                        ),
                        "message":
                            f"{source_layer} should not depend on {target_layer}"
                    })

        return violations