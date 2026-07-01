import os
import ast
import pickle

from sentence_transformers import SentenceTransformer


class ChunkEmbeddingGenerator:

    def __init__(self, repo_path):

        self.repo_path = repo_path

        self.model = SentenceTransformer(
            "BAAI/bge-small-en"
        )

        self.documents = []
        self.embeddings = []
        self.metadatas = []

    # =====================================================
    # EXTRACT CHUNKS
    # =====================================================

    def extract_chunks(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source_code = f.read()

        try:

            tree = ast.parse(
                source_code
            )

        except Exception:

            return []

        chunks = []

        lines = source_code.splitlines()

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ClassDef
            ):

                start = node.lineno - 1

                end = min(

                    start + 80,

                    len(lines)

                )

                chunk_code = "\n".join(

                    lines[start:end]

                )

                chunks.append({

                    "type": "class",

                    "name": node.name,

                    "code": chunk_code

                })

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            ):

                start = node.lineno - 1

                end = min(

                    start + 80,

                    len(lines)

                )

                chunk_code = "\n".join(

                    lines[start:end]

                )

                chunks.append({

                    "type": "function",

                    "name": node.name,

                    "code": chunk_code

                })

        return chunks

    # =====================================================
    # GENERATE EMBEDDINGS
    # =====================================================

    def generate_embeddings(self):

        skip_dirs = [
    "tests",
    "docs",
    "docs_src",
    "__pycache__",
    ".github",
    "benchmarks",
    "venv",
    ".git",
    "node_modules",
    "data/repos",
    "data/vector_db",
    "data/chroma_db_chunks",
    "dist",
    "build"
]

        for root, _, files in os.walk(
            self.repo_path
        ):

            for file in files:

                if not file.endswith(".py"):

                    continue

                file_path = os.path.join(
                    root,
                    file
                )

                normalized = file_path.replace(
                    "\\",
                    "/"
                )

                if any(

                    d in normalized

                    for d in skip_dirs

                ):

                    continue

                relative_path = os.path.relpath(
                    file_path,
                    self.repo_path
                )

                chunks = self.extract_chunks(
                    file_path
                )

                for chunk in chunks:

                    if not chunk["code"]:

                        continue

                    embedding = self.model.encode(
                        chunk["code"]
                    )

                    self.documents.append(
                        chunk["code"]
                    )

                    self.embeddings.append(
                        embedding
                    )

                    self.metadatas.append({

                        "file": relative_path,

                        "type": chunk["type"],

                        "name": chunk["name"]

                    })

                    print(

                        f"Embedded: "

                        f"{relative_path}"

                        f" -> "

                        f"{chunk['type']} "

                        f"{chunk['name']}"

                    )

    # =====================================================
    # SAVE
    # =====================================================

    def save_embeddings(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            "data/chunk_embeddings.pkl",
            "wb"
        ) as f:

            pickle.dump({

                "documents":
                    self.documents,

                "embeddings":
                    self.embeddings,

                "metadatas":
                    self.metadatas

            }, f)

        print(

            "\nSaved",

            len(self.documents),

            "chunks"

        )


if __name__ == "__main__":

    repo_path = input(
        "Enter repository path: "
    )

    generator = ChunkEmbeddingGenerator(
        repo_path=repo_path
    )

    generator.generate_embeddings()

    generator.save_embeddings()