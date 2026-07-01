import os
import pickle
import ollama
import numpy as np
from sentence_transformers import SentenceTransformer


class ChunkRetriever:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
            "BAAI/bge-small-en"
        )

        embeddings_path = os.path.join(
            "data",
            "chunk_embeddings.pkl"
        )

        with open(embeddings_path, "rb") as f:

            data = pickle.load(f)

        self.embeddings = data["embeddings"]
        self.documents = data["documents"]
        self.metadatas = data["metadatas"]

    # ======================================================
    # COSINE SIMILARITY
    # ======================================================

    def cosine_similarity(self, a, b):

        a = np.array(a)
        b = np.array(b)

        denominator = (
            np.linalg.norm(a)
            * np.linalg.norm(b)
        )

        if denominator == 0:
            return 0

        return np.dot(a, b) / denominator

    # ======================================================
    # BOOSTING LOGIC
    # ======================================================

    def calculate_boost(
        self,
        query,
        metadata
    ):

        query_lower = query.lower()

        file_path = metadata.get(
            "file",
            ""
        ).lower()

        chunk_name = metadata.get(
            "name",
            ""
        ).lower()

        chunk_type = metadata.get(
            "type",
            ""
        ).lower()

        boost = 0

        # ==================================================
        # ROUTING / APIRouter
        # ==================================================

        if any(
            word in query_lower
            for word in [
                "router",
                "routing",
                "route",
                "apirouter",
                "path operation"
            ]
        ):

            if "routing.py" in file_path:
                boost += 2.0

            if "applications.py" in file_path:
                boost += 1.0

            if chunk_name == "include_router":
                boost += 3.0

            if chunk_name == "apirouter":
                boost += 2.5

            if chunk_name == "add_api_route":
                boost += 2.0

            if chunk_name == "api_route":
                boost += 1.5

            if chunk_name == "route":
                boost += 1.0

            if chunk_type == "class":
                boost += 0.5

        # ==================================================
        # DEPENDENCIES
        # ==================================================

        if any(
            word in query_lower
            for word in [
                "dependency",
                "dependencies",
                "depends",
                "injection"
            ]
        ):

            if "dependencies" in file_path:
                boost += 2.0

            if "depends" in chunk_name:
                boost += 2.0

            if "dependency" in chunk_name:
                boost += 1.5

        # ==================================================
        # SECURITY
        # ==================================================

        if any(
            word in query_lower
            for word in [
                "security",
                "oauth",
                "jwt",
                "authentication",
                "authorization",
                "auth"
            ]
        ):

            if "security" in file_path:
                boost += 2.0

        # ==================================================
        # OPENAPI
        # ==================================================

        if any(
            word in query_lower
            for word in [
                "openapi",
                "swagger",
                "schema",
                "docs"
            ]
        ):

            if "openapi" in file_path:
                boost += 2.0

        # ==================================================
        # MIDDLEWARE
        # ==================================================

        if "middleware" in query_lower:

            if "middleware" in file_path:
                boost += 2.0

        # ==================================================
        # VALIDATION / EXCEPTIONS
        # ==================================================

        if any(
            word in query_lower
            for word in [
                "exception",
                "validation",
                "error"
            ]
        ):

            if "exception" in file_path:
                boost += 2.0

        # ==================================================
        # CORE ARCHITECTURE FILES
        # ==================================================

        important_modules = [
            "routing.py",
            "applications.py",
            "dependencies",
            "security",
            "openapi"
        ]

        if any(
            module in file_path
            for module in important_modules
        ):
            boost += 0.25

        return boost

    # ======================================================
    # RETRIEVAL
    # ======================================================

    def retrieve(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.embedding_model.encode(query)

        query_lower = query.lower()

        scored_results = []

        for idx, embedding in enumerate(self.embeddings):

            metadata = self.metadatas[idx]

            file_path = metadata.get(
                "file",
                ""
            ).lower()

            chunk_name = metadata.get(
                "name",
                ""
            ).lower()

            chunk_type = metadata.get(
                "type",
                ""
            ).lower()

            document = self.documents[idx]

            # ==================================================
            # SKIP TESTS + DOCS
            # ==================================================

            if (
                "docs_src" in file_path
                or "tests" in file_path
            ):
                continue

            # ==================================================
            # SKIP EMPTY CHUNKS
            # ==================================================

            if not document:
                continue

            # ==================================================
            # ROUTER FILTERING
            # ==================================================

            if any(
                word in query_lower
                for word in [
                    "router",
                    "routing",
                    "route",
                    "apirouter"
                ]
            ):

                allowed_files = [
                    "routing.py",
                    "applications.py"
                ]

                if not any(
                    allowed in file_path
                    for allowed in allowed_files
                ):
                    continue

            # ==================================================
            # DEPENDENCY FILTERING
            # ==================================================

            if any(
                word in query_lower
                for word in [
                    "dependency",
                    "dependencies",
                    "depends"
                ]
            ):

                if "dependencies" not in file_path:
                    continue

            # ==================================================
            # SECURITY FILTERING
            # ==================================================

            if any(
                word in query_lower
                for word in [
                    "security",
                    "oauth",
                    "jwt",
                    "auth"
                ]
            ):

                if "security" not in file_path:
                    continue

            # ==================================================
            # SEMANTIC SIMILARITY
            # ==================================================

            similarity = self.cosine_similarity(
                query_embedding,
                embedding
            )

            # ==================================================
            # ARCHITECTURE BOOST
            # ==================================================

            boost = self.calculate_boost(
                query,
                metadata
            )

            final_score = similarity + boost

            scored_results.append({
                "score": final_score,
                "chunk": document,
                "metadata": metadata
            })

        # ======================================================
        # SORT RESULTS
        # ======================================================

        scored_results = sorted(
            scored_results,
            key=lambda x: x["score"],
            reverse=True
        )

        semantic_results = scored_results[:top_k]

        # ======================================================
        # FINAL FILTERING
        # ======================================================

        filtered = []

        for result in semantic_results:

            file = result["metadata"].get(
                "file",
                ""
            )

            if "tests" in file.lower():
                continue

            filtered.append(result)

        return filtered