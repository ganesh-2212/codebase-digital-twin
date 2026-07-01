import pickle


class ArchitectureImpactAnalyzer:

    def __init__(self):

        self.summaries = self.load_summaries()

    # ==========================================
    # LOAD ARCHITECTURE SUMMARIES
    # ==========================================

    def load_summaries(self):

        with open(
            "data/architecture_summaries.pkl",
            "rb"
        ) as f:

            return pickle.load(f)

    # ==========================================
    # FIND COMPONENT
    # ==========================================

    def find_component(
        self,
        component_name
    ):

        component_name = component_name.lower()

        for item in self.summaries:

            if item["name"].lower() == component_name:

                return item

        return None

    # ==========================================
    # FIND CALLERS
    # ==========================================

    def find_callers(
        self,
        component_name
    ):

        callers = []

        for item in self.summaries:

            calls = item.get(
                "calls",
                []
            )

            for call in calls:

                if call.lower() == component_name.lower():

                    callers.append(
                        item["name"]
                    )

        return callers

    # ==========================================
    # CALCULATE IMPACT SCORE
    # ==========================================

    def calculate_impact_score(
        self,
        methods,
        calls,
        callers
    ):

        return (
            len(methods)
            +
            len(calls)
            +
            len(callers)
        )

    # ==========================================
    # IMPACT ANALYSIS
    # ==========================================

    def analyze(
        self,
        component_name
    ):

        component = self.find_component(
            component_name
        )

        if component is None:

            return None

        methods = component.get(
            "methods",
            []
        )

        calls = component.get(
            "calls",
            []
        )

        callers = self.find_callers(
            component_name
        )

        impact_score = self.calculate_impact_score(

            methods,
            calls,
            callers

        )

        if impact_score > 40:

            impact_level = "HIGH"

        elif impact_score > 15:

            impact_level = "MEDIUM"

        else:

            impact_level = "LOW"

        return {

            "name":
            component["name"],

            "type":
            component["type"],

            "file":
            component["file"],

            "methods":
            methods,

            "calls":
            calls,

            "called_by":
            callers,

            "impact_score":
            impact_score,

            "impact_level":
            impact_level

        }


if __name__ == "__main__":

    analyzer = ArchitectureImpactAnalyzer()

    query = input(
        "Enter component: "
    )

    result = analyzer.analyze(
        query
    )

    print("\nResult:\n")

    print(result)