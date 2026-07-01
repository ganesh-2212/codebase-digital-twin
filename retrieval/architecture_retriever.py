import os
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer


class ArchitectureRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        embeddings_path = (
            "data/architecture_embeddings.pkl"
        )

        if not os.path.exists(
            embeddings_path
        ):
            raise FileNotFoundError(
                f"{embeddings_path} not found."
            )

        with open(
            embeddings_path,
            "rb"
        ) as f:

            self.embeddings = pickle.load(f)

        print(
            f"Loaded {len(self.embeddings)} architecture embeddings"
        )

    # ==========================================
    # COSINE SIMILARITY
    # ==========================================

    def cosine_similarity(
        self,
        a,
        b
    ):

        return float(
            np.dot(a, b)
        )

    # ==========================================
    # RETRIEVE
    # ==========================================

    def retrieve(
        self,
        query,
        top_k=5,
        threshold=0.20
    ):

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        scored = []

        for item in self.embeddings:

            score = self.cosine_similarity(
                query_embedding,
                item["embedding"]
            )

            scored.append({

                "score": score,

                "summary":
                item["summary"]

            })

        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        print("\nTop Architecture Matches:\n")

        for result in scored[:10]:

            summary = result["summary"]

            print(
                f"{summary.get('name', 'Unknown')} "
                f"({summary.get('type', 'Unknown')}) "
                f"| Score = {round(result['score'], 4)}"
            )

        results = []

        for result in scored:

            if result["score"] < threshold:
                continue

            results.append({

                "score":
                round(
                    result["score"],
                    4
                ),

                "summary":
                result["summary"]

            })

            if len(results) >= top_k:
                break

        print(
            f"\nReturned {len(results)} architecture matches\n"
        )

        return results


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    retriever = ArchitectureRetriever()

    query = input(
        "Enter query: "
    )

    results = retriever.retrieve(
        query=query,
        top_k=5,
        threshold=0.20
    )

    print(
        "\nFinal Architecture Results:\n"
    )

    for result in results:

        print(
            f"Score: {result['score']}"
        )

        print(
            result["summary"]
        )

        print(
            "-" * 60
        )