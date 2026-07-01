import os

from dotenv import load_dotenv
import google.generativeai as genai

from retrieval.graphrag_retrieval import GraphRAGRetriever
from analysis.architecture_impact import ArchitectureImpactAnalyzer


class ReasoningEngineV3:

    def __init__(self):

        load_dotenv()

        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        self.retriever = GraphRAGRetriever()

        self.impact_analyzer = (
            ArchitectureImpactAnalyzer()
        )

    # ==========================================
    # BUILD CONTEXT
    # ==========================================

    def build_context(
        self,
        query,
        top_k=10
    ):

        retrieval_results = self.retriever.retrieve(
            query,
            top_k=top_k
        )

        context = []

        for item in retrieval_results:

            metadata = item["metadata"]

            name = metadata.get(
                "name",
                "unknown"
            )

            component = (
                self.impact_analyzer.find_component(
                    name
                )
            )

            if component:

                context.append(
                    str(component)
                )

        return "\n\n".join(context)

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

        prompt = f"""
You are an expert software architect.

Repository Context:

{context}

Question:

{query}

Instructions:

1. Explain the architecture.
2. Explain important classes/functions.
3. Explain relationships.
4. Mention likely impact of changes.
5. Give a detailed engineering answer.
"""

        response = self.model.generate_content(
            prompt
        )

        print("\n")
        print("=" * 70)
        print("AI REASONING")
        print("=" * 70)
        print("\n")

        print(
            response.text
        )

        return response.text