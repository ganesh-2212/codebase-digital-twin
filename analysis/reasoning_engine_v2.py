from retrieval.graphrag_retrieval import (
    GraphRAGRetriever
)

from analysis.architecture_impact import (
    ArchitectureImpactAnalyzer
)


class ReasoningEngineV2:

    def __init__(self):

        self.retriever = GraphRAGRetriever()

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

        retrieved = self.retriever.retrieve(

            query,

            top_k=10

        )

        context = []

        for item in retrieved:

            name = item["metadata"].get(
                "name",
                ""
            )

            architecture = self.impact_analyzer.find_component(

                name

            )

            if architecture:

                context.append({

                    "name":
                    architecture["name"],

                    "type":
                    architecture["type"],

                    "file":
                    architecture["file"],

                    "impact":
                    architecture.get(
                        "impact_level",
                        "LOW"
                    ),

                    "methods":
                    architecture.get(
                        "methods",
                        []
                    ),

                    "calls":
                    architecture.get(
                        "calls",
                        []
                    )

                })

        return context

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

        print("\n" + "=" * 70)
        print("QUERY")
        print("=" * 70)

        print(query)

        print("\n" + "=" * 70)
        print("ARCHITECTURE ANALYSIS")
        print("=" * 70)

        for item in context[:10]:

            print(
                f"\nComponent: {item['name']}"
            )

            print(
                f"Type: {item['type']}"
            )

            print(
                f"Impact: {item['impact']}"
            )

            print(
                f"File: {item['file']}"
            )

            print(
                f"Methods: {len(item['methods'])}"
            )

            print(
                f"Calls: {len(item['calls'])}"
            )

        print("\n" + "=" * 70)
        print("DIGITAL TWIN REASONING")
        print("=" * 70)

        print("""

The system successfully:

1. Retrieved relevant code chunks.

2. Retrieved architectural entities.

3. Retrieved impact information.

4. Combined semantic retrieval +
   architecture retrieval +
   impact analysis.

5. Built a complete repository context.

This is the exact context that will
later be passed into an LLM for
architectural reasoning.

Current stage:
GraphRAG + Architecture Intelligence

Next stage:
LLM-Powered Repository Reasoning

Examples:
- Explain architecture
- Predict change impact
- Suggest refactoring
- Detect architectural smells
- Generate design summaries
- Repository Q&A

        """)


if __name__ == "__main__":

    engine = ReasoningEngineV2()

    query = input(
        "Enter query: "
    )

    engine.reason(
        query
    )