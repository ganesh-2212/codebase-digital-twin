from retrieval.graphrag_retrieval import (
    GraphRAGRetriever
)

from analysis.architecture_impact import (
    ArchitectureImpactAnalyzer
)


class ReasoningEngine:

    def __init__(self):

        self.retriever = (
            GraphRAGRetriever()
        )

        self.impact_analyzer = (
            ArchitectureImpactAnalyzer()
        )

    # ==========================================
    # BUILD CONTEXT
    # ==========================================

    def build_context(
        self,
        query
    ):

        retrieval_context = (

            self.retriever.retrieve(
                query,
                top_k=10
            )

        )

        architecture_context = []

        for item in retrieval_context:

            name = item["metadata"].get(
                "name"
            )

            if not name:

                continue

            impact = (

                self.impact_analyzer.analyze(
                    name
                )

            )

            if impact:

                architecture_context.append(
                    impact
                )

        return {

            "retrieval":
            retrieval_context,

            "architecture":
            architecture_context

        }

    # ==========================================
    # REASON
    # ==========================================

    def reason(
        self,
        query
    ):

        context = self.build_context(
            query
        )

        print("\n" + "=" * 60)
        print("QUERY")
        print("=" * 60)

        print(query)

        print("\n" + "=" * 60)
        print("ARCHITECTURE CONTEXT")
        print("=" * 60)

        for item in context["architecture"][:5]:

            print()

            print(
                f"Component: "
                f"{item['name']}"
            )

            print(
                f"Type: "
                f"{item['type']}"
            )

            print(
                f"Impact Level: "
                f"{item['impact_level']}"
            )

            print(
                f"Methods: "
                f"{len(item['methods'])}"
            )

            print(
                f"Calls: "
                f"{len(item['calls'])}"
            )

        print("\n" + "=" * 60)
        print("REASONING")
        print("=" * 60)

        print(
            "\nThe query is related to "
            "the retrieved architectural "
            "components above."
        )

        print(
            "These components have been "
            "identified through semantic "
            "retrieval and architecture "
            "analysis."
        )

        print(
            "The next step is connecting "
            "an LLM to generate natural "
            "language explanations."
        )

        return context


if __name__ == "__main__":

    engine = ReasoningEngine()

    query = input(
        "Enter query: "
    )

    engine.reason(
        query
    )