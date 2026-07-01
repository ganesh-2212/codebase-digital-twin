from analysis.architecture_smell_detector import (
    ArchitectureSmellDetector
)


class RefactoringAdvisor:

    def __init__(self):

        self.detector = (
            ArchitectureSmellDetector()
        )

    # ==========================================
    # ADVICE
    # ==========================================

    def generate_advice(self):

        smells = self.detector.detect()

        recommendations = []

        for item in smells:

            advice = []

            if "God Class" in item["smells"]:

                advice.append(

                    "Split into smaller "
                    "specialized classes"

                )

            if "High Coupling" in item["smells"]:

                advice.append(

                    "Reduce dependencies "
                    "and introduce interfaces"

                )

            recommendations.append({

                "component":
                item["name"],

                "smells":
                item["smells"],

                "advice":
                advice

            })

        return recommendations


if __name__ == "__main__":

    advisor = RefactoringAdvisor()

    recommendations = (
        advisor.generate_advice()
    )

    for item in recommendations:

        print(
            "\n===================="
        )

        print(
            item["component"]
        )

        print(
            "Smells:",
            item["smells"]
        )

        print(
            "Advice:",
            item["advice"]
        )