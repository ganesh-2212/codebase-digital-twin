import pickle

from sentence_transformers import SentenceTransformer


class ArchitectureEmbeddingGenerator:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    # ==========================================
    # LOAD SUMMARIES
    # ==========================================

    def load_summaries(self):

        with open(
            "data/architecture_summaries.pkl",
            "rb"
        ) as f:

            return pickle.load(f)

    # ==========================================
    # BUILD TEXT FOR EMBEDDING
    # ==========================================

    def create_text(
        self,
        summary
    ):

        text = f"""
Name: {summary.get('name')}
Type: {summary.get('type')}
File: {summary.get('file')}
"""

        methods = summary.get(
            "methods",
            []
        )

        if methods:

            text += "\nMethods:\n"

            text += "\n".join(
                methods
            )

        return text

    # ==========================================
    # GENERATE EMBEDDINGS
    # ==========================================

    def generate(self):

        summaries = self.load_summaries()

        embeddings = []

        for summary in summaries:

            text = self.create_text(
                summary
            )

            vector = self.model.encode(

                text,

                normalize_embeddings=True

            )

            embeddings.append({

                "summary": summary,

                "embedding": vector

            })

        with open(
            "data/architecture_embeddings.pkl",
            "wb"
        ) as f:

            pickle.dump(
                embeddings,
                f
            )

        print(
            f"Saved {len(embeddings)} architecture embeddings"
        )


if __name__ == "__main__":

    generator = ArchitectureEmbeddingGenerator()

    generator.generate()