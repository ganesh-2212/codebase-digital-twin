import pickle


class ArchitectureSmellDetector:

    def __init__(self):

        with open(
            "data/architecture_summaries.pkl",
            "rb"
        ) as f:

            self.components = pickle.load(f)

    # ==========================================
    # DETECT SMELLS
    # ==========================================

    def detect(self):

        smells = []

        for component in self.components:

            methods = component.get(
                "methods",
                []
            )

            calls = component.get(
                "calls",
                []
            )

            findings = []

            if len(methods) > 15:

                findings.append(
                    "God Class"
                )

            if len(calls) > 30:

                findings.append(
                    "High Coupling"
                )

            if findings:

                smells.append({

                    "name":
                    component["name"],

                    "file":
                    component["file"],

                    "smells":
                    findings,

                    "methods":
                    len(methods),

                    "calls":
                    len(calls)

                })

        return smells


if __name__ == "__main__":

    detector = (
        ArchitectureSmellDetector()
    )

    results = detector.detect()

    print(
        f"\nDetected "
        f"{len(results)} smells\n"
    )

    for item in results:

        print(
            f"\n{item['name']}"
        )

        print(
            f"Smells: "
            f"{item['smells']}"
        )

        print(
            f"Methods: "
            f"{item['methods']}"
        )

        print(
            f"Calls: "
            f"{item['calls']}"
        )