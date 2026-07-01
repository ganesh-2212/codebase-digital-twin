import os
import ast
import chromadb

from sentence_transformers import SentenceTransformer


class CodeEmbeddingGenerator:

    def __init__(self, repo_path):

        self.repo_path = repo_path

        self.model = SentenceTransformer(
            "BAAI/bge-small-en"
        )

        self.chroma_client = chromadb.PersistentClient(
            path="data/vector_db"
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="codebase_embeddings"
        )

    # ======================================================
    # READ FILE
    # ======================================================

    def read_code_file(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return file.read()

        except Exception as e:

            print(f"Error reading {file_path}: {e}")

            return None

    # ======================================================
    # EXTRACT CHUNKS
    # ======================================================

    def extract_chunks(
        self,
        code_content
    ):

        chunks = []

        try:

            tree = ast.parse(code_content)

            for node in ast.walk(tree):

                # ==========================================
                # CLASS
                # ==========================================

                if isinstance(node, ast.ClassDef):

                    chunk_code = ast.get_source_segment(
                        code_content,
                        node
                    )

                    chunks.append({

                        "type": "class",

                        "name": node.name,

                        "content": chunk_code
                    })

                # ==========================================
                # FUNCTION
                # ==========================================

                elif isinstance(
                    node,
                    ast.FunctionDef
                ):

                    chunk_code = ast.get_source_segment(
                        code_content,
                        node
                    )

                    chunks.append({

                        "type": "function",

                        "name": node.name,

                        "content": chunk_code
                    })

        except Exception as e:

            print(f"AST parsing failed: {e}")

        return chunks

    # ======================================================
    # GENERATE EMBEDDINGS
    # ======================================================

    def generate_embeddings(self):

        doc_id = 0

        for root, dirs, files in os.walk(self.repo_path):

            for file in files:

                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(
                    root,
                    file
                )

                relative_path = os.path.relpath(
                    file_path,
                    self.repo_path
                )

                print(f"\nProcessing: {relative_path}")

                code_content = self.read_code_file(
                    file_path
                )

                if not code_content:
                    continue

                chunks = self.extract_chunks(
                    code_content
                )

                for chunk in chunks:

                    chunk_content = chunk["content"]

                    if not chunk_content:
                        continue

                    embedding = self.model.encode(
                        chunk_content
                    ).tolist()

                    self.collection.add(

                        documents=[chunk_content],

                        embeddings=[embedding],

                        ids=[f"doc_{doc_id}"],

                        metadatas=[{

                            "file": relative_path,

                            "type": chunk["type"],

                            "name": chunk["name"]
                        }]
                    )

                    print(
                        f"Embedded -> "
                        f"{chunk['type']} : "
                        f"{chunk['name']}"
                    )

                    doc_id += 1


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    repo_path = input(
        "Enter repository path: "
    )

    generator = CodeEmbeddingGenerator(
        repo_path
    )

    generator.generate_embeddings()

    print(
        "\nEmbeddings generated successfully!"
    )