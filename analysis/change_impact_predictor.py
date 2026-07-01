from analysis.architecture_impact import (
    ArchitectureImpactAnalyzer
)


class ChangeImpactPredictor:

    def __init__(self):

        self.analyzer = (
            ArchitectureImpactAnalyzer()
        )

    # ==========================================
    # PREDICT CHANGE IMPACT
    # ==========================================

    def predict(
        self,
        component_name
    ):

        component = (
            self.analyzer.analyze(
                component_name
            )
        )

        if not component:

            return {

                "error":
                "Component not found"

            }

        impact_score = component[
            "impact_score"
        ]

        impact_level = component[
            "impact_level"
        ]

        risk = "LOW"

        if impact_score > 50:

            risk = "HIGH"

        elif impact_score > 20:

            risk = "MEDIUM"

        direct_dependencies = (
            component["calls"][:15]
        )

        affected_modules = (
            component["calls"][:10]
        )

        return {

            "component":
            component["name"],

            "type":
            component["type"],

            "file":
            component["file"],

            "impact_score":
            impact_score,

            "impact_level":
            impact_level,

            "risk":
            risk,

            "direct_dependencies":
            direct_dependencies,

            "affected_modules":
            affected_modules,

            "methods":
            component["methods"],

            "calls":
            component["calls"][:15]

        }


if __name__ == "__main__":

    predictor = (
        ChangeImpactPredictor()
    )

    name = input(
        "Component: "
    )

    result = predictor.predict(
        name
    )

    print("\n")

    for k, v in result.items():

        print(
            f"{k}: {v}"
        )