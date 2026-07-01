import os
import pickle
import networkx as nx
import chromadb

from sentence_transformers import SentenceTransformer

from retrieval.architecture_retriever import (
    ArchitectureRetriever
)


class GraphRAGRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="data/vector_db"
        )

        self.collection = self.client.get_collection(
            name="codebase_embeddings"
        )

        self.graph = self.load_graph()

        self.architecture_retriever = (
            ArchitectureRetriever()
        )

    # ==========================================
    # LOAD GRAPH SAFELY
    # ==========================================

    def load_graph(self):

        graph_path = "data/call_graph.pkl"

        if not os.path.exists(graph_path):

            print(
                "\ncall_graph.pkl not found."
            )

            print(
                "Starting with empty graph."
            )

            return nx.DiGraph()

        try:

            with open(
                graph_path,
                "rb"
            ) as f:

                graph = pickle.load(f)

            print(
                f"Loaded graph with "
                f"{len(graph.nodes())} nodes "
                f"and "
                f"{len(graph.edges())} edges"
            )

            return graph

        except Exception as e:

            print(
                f"Failed loading graph: {e}"
            )

            return nx.DiGraph()

    # ==========================================
    # SEMANTIC SEARCH
    # ==========================================

    def semantic_search(
        self,
        query,
        top_k=15
    ):

        embedding = self.model.encode(
            query
        ).tolist()

        results = self.collection.query(

            query_embeddings=[embedding],

            n_results=top_k,

            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        chunks = []

        print(
            "\nTop Semantic Chunks:\n"
        )

        for doc, meta, dist in zip(

            results["documents"][0],

            results["metadatas"][0],

            results["distances"][0]

        ):

            print(
                f"{meta.get('name')} "
                f"({meta.get('type')}) "
                f"| Distance={round(dist,4)}"
            )

            chunks.append({

                "chunk": doc,

                "metadata": meta,

                "distance": dist

            })

        return chunks

    # ==========================================
    # ARCHITECTURE SEARCH
    # ==========================================

    def architecture_search(
        self,
        query
    ):

        results = self.architecture_retriever.retrieve(
            query
        )

        print(
            "\nArchitecture Results:\n"
        )

        for result in results:

            item = result["summary"]

            print(
                f"{item.get('name')} "
                f"({item.get('type')}) "
                f"-> "
                f"{item.get('file')}"
            )

        return results

    # ==========================================
    # GRAPH EXPANSION
    # ==========================================

    def expand_graph_context(
        self,
        chunks
    ):

        expanded = list(chunks)

        return expanded

    # ==========================================
    # ADD ARCHITECTURE CONTEXT
    # ==========================================

    def add_architecture_context(
        self,
        full_context,
        architecture_results
    ):

        for result in architecture_results:

            item = result["summary"]

            architecture_text = f"""
Architecture Component

Name: {item.get('name')}
Type: {item.get('type')}
File: {item.get('file')}

Methods:
{', '.join(item.get('methods', []))}

Calls:
{', '.join(item.get('calls', []))}
"""

            full_context.append({

                "chunk":
                architecture_text,

                "metadata": {

                    "file":
                    item.get("file"),

                    "type":
                    "architecture",

                    "name":
                    item.get("name"),

                    "score":
                    result["score"]

                }

            })

        return full_context

    # ==========================================
    # RETRIEVE
    # ==========================================

    def retrieve(
        self,
        query,
        top_k=15
    ):

        semantic_results = self.semantic_search(

            query,

            top_k=top_k

        )

        architecture_results = (

            self.architecture_search(
                query
            )

        )

        full_context = self.expand_graph_context(

            semantic_results

        )

        full_context = self.add_architecture_context(

            full_context,

            architecture_results

        )

        print(
            f"\nRetrieved "
            f"{len(semantic_results)} semantic chunks"
        )

        print(
            f"Architecture matches: "
            f"{len(architecture_results)}"
        )

        print(
            f"Final context size: "
            f"{len(full_context)}"
        )

        return full_context


if __name__ == "__main__":

    retriever = GraphRAGRetriever()

    query = input(
        "Enter query: "
    )

    results = retriever.retrieve(

        query,

        top_k=15

    )

    print(
        "\nFinal Results:\n"
    )

    for r in results:

        print(
            r["metadata"]
        )