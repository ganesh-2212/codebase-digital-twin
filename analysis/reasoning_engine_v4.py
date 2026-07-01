import os

from dotenv import load_dotenv
import google.generativeai as genai

from retrieval.graphrag_retrieval import GraphRAGRetriever
from analysis.architecture_impact import ArchitectureImpactAnalyzer


class ReasoningEngineV4:

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

        context_parts = []

        print("\nRetrieved Results:")
        print(len(retrieval_results))

        for item in retrieval_results:

            print("\nITEM:")
            print(item)

            metadata = item.get(
                "metadata",
                {}
            )

            # support both formats
            name = metadata.get(
                "name",
                ""
            )

            if not name:

                name = item.get(
                    "name",
                    ""
                )

            component = None

            if name:

                component = (
                    self.impact_analyzer.analyze(
                        name
                    )
                )

            if component:

                context_parts.append(
                    f"""
COMPONENT:
{component['name']}

TYPE:
{component['type']}

FILE:
{component['file']}

METHODS:
{component.get('methods', [])}

CALLS:
{component.get('calls', [])}

IMPACT SCORE:
{component.get('impact_score', 0)}

IMPACT LEVEL:
{component.get('impact_level', 'LOW')}
"""
                )

            chunk_text = item.get(
                "chunk",
                ""
            )

            if chunk_text:

                context_parts.append(
                    f"""
CODE CHUNK:

{chunk_text}
"""
                )

        final_context = "\n".join(
            context_parts
        )

        print("\n========== CONTEXT ==========\n")
        print(final_context[:5000])
        print("\n=============================\n")

        return final_context

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

You are analyzing a software repository.

Repository Context:

{context}

Question:

{query}

Instructions:

1. Explain the architecture involved.
2. Explain important classes and functions.
3. Explain how the code works internally.
4. Explain dependencies.
5. Explain what may break if modified.
6. Explain architectural risks.
7. Use only repository evidence.
8. Be detailed and technical.
"""

        try:

            response = (
                self.model.generate_content(
                    prompt
                )
            )

            answer = response.text

        except Exception as e:

            answer = (
                f"Gemini Error: {e}"
            )

        print("\n")
        print("=" * 80)
        print("DIGITAL TWIN REASONING")
        print("=" * 80)
        print("\n")

        print(answer)

        return answer