import os
import ast

from sentence_transformers import SentenceTransformer
import chromadb


class CodeChunkEmbedder:

    def __init__(self, repo_path):

        self.repo_path = repo_path

        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.chroma_client = chromadb.PersistentClient(
            path="data/chroma_db_chunks"
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="code_chunks"
        )

    # ==========================================
    # EXTRACT CHUNKS
    # ==========================================

    def extract_chunks(self, file_path):

        chunks = []

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                source_code = f.read()

            tree = ast.parse(source_code)

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):

                    chunk_code = ast.get_source_segment(
                        source_code,
                        node
                    )

                    chunks.append({
                        "type": "function",
                        "name": node.name,
                        "code": chunk_code
                    })

                elif isinstance(node, ast.AsyncFunctionDef):

                    chunk_code = ast.get_source_segment(
                        source_code,
                        node
                    )

                    chunks.append({
                        "type": "async_function",
                        "name": node.name,
                        "code": chunk_code
                    })

                elif isinstance(node, ast.ClassDef):

                    chunk_code = ast.get_source_segment(
                        source_code,
                        node
                    )

                    chunks.append({
                        "type": "class",
                        "name": node.name,
                        "code": chunk_code
                    })

        except Exception as e:

            print(f"Error parsing {file_path}: {e}")

        return chunks

    # ==========================================
    # GENERATE EMBEDDINGS
    # ==========================================

    def generate_embeddings(self):

        doc_id = 0

        for root, dirs, files in os.walk(self.repo_path):

            # Skip unnecessary folders
            dirs[:] = [
                d for d in dirs
                if d not in [
                    "venv",
                    ".git",
                    "__pycache__",
                    "node_modules",
                    "dist",
                    "build"
                ]
            ]

            for file in files:

                if file.endswith(".py"):

                    file_path = os.path.join(
                        root,
                        file
                    )

                    relative_path = os.path.relpath(
                        file_path,
                        self.repo_path
                    )

                    chunks = self.extract_chunks(
                        file_path
                    )

                    for chunk in chunks:

                        embedding_text = f"""
File: {relative_path}

Type: {chunk['type']}

Name: {chunk['name']}

Code:
{chunk['code']}
"""

                        embedding = self.embedding_model.encode(
                            embedding_text
                        ).tolist()

                        self.collection.add(
                            ids=[str(doc_id)],
                            embeddings=[embedding],
                            documents=[embedding_text],
                            metadatas=[{
                                "file": relative_path,
                                "chunk_type": chunk["type"],
                                "chunk_name": chunk["name"]
                            }]
                        )

                        print(
                            f"Embedded: {relative_path} -> {chunk['name']}"
                        )

                        doc_id += 1

        print(
            f"\nChunk embeddings generated successfully!"
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    repo_path = input(
        "Enter repository path: "
    )

    embedder = CodeChunkEmbedder(
        repo_path=repo_path
    )

    embedder.generate_embeddings()