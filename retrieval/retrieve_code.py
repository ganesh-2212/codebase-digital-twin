from sentence_transformers import SentenceTransformer
import chromadb


class CodeRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.chroma_client = chromadb.PersistentClient(
            path="data/vector_db"
        )

        self.collection = self.chroma_client.get_collection(
            name="codebase_embeddings"
        )

    def retrieve(self, query, top_k=5):

        query_embedding = self.model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results


if __name__ == "__main__":

    retriever = CodeRetriever()

    query = input("Enter your query: ")

    results = retriever.retrieve(query)

    print("\nTop Relevant Files:\n")

    for idx, file_id in enumerate(results["ids"][0]):

        print(f"{idx + 1}. {file_id}")