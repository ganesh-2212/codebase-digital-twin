import os
import ast
import json
from git import Repo


class RepoParser:

    def __init__(self, repo_url):

        self.repo_url = repo_url

        repo_name = repo_url.split("/")[-1].replace(".git", "")

        self.local_path = os.path.join(
            "data",
            "repos",
            repo_name
        )

        self.output_file = os.path.join(
            "data",
            "parsed_chunks.json"
        )

        # ======================================================
        # STRICT EXCLUSION LIST (SAFE FOR ALL REPOS)
        # ======================================================
        self.EXCLUDED_DIRS = {
            "venv",
            "site-packages",
            "node_modules",
            "__pycache__",
            ".git",
            "docs_src",
            "tests"
        }

    # ======================================================
    # CLONE REPOSITORY
    # ======================================================

    def clone_repository(self):

        if os.path.exists(self.local_path):
            print(f"Repository exists: {self.local_path}")
            return

        print("Cloning repository...")

        Repo.clone_from(
            self.repo_url,
            self.local_path
        )

        print("Clone complete")

    # ======================================================
    # EXTRACT AST CHUNKS
    # ======================================================

    def extract_chunks(self, file_path, relative_path):

        chunks = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

        except Exception:
            return chunks

        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                start = node.lineno
                end = getattr(node, "end_lineno", start)

                code = "\n".join(
                    source.splitlines()[start - 1:end]
                )

                chunks.append({
                    "chunk": code,
                    "metadata": {
                        "file": relative_path,
                        "type": "function",
                        "name": node.name
                    }
                })

            elif isinstance(node, ast.ClassDef):

                start = node.lineno
                end = getattr(node, "end_lineno", start)

                code = "\n".join(
                    source.splitlines()[start - 1:end]
                )

                chunks.append({
                    "chunk": code,
                    "metadata": {
                        "file": relative_path,
                        "type": "class",
                        "name": node.name
                    }
                })

        return chunks

    # ======================================================
    # DIRECTORY FILTER (CORRECT VERSION)
    # ======================================================

    def is_valid_dir(self, dirname: str):

        return dirname not in self.EXCLUDED_DIRS

    # ======================================================
    # PARSE REPOSITORY
    # ======================================================

    def parse_repository(self):

        all_chunks = []

        for root, dirs, files in os.walk(self.local_path):

            # ==================================================
            # FILTER DIRECTORIES PROPERLY
            # ==================================================
            dirs[:] = [d for d in dirs if self.is_valid_dir(d)]

            for file in files:

                if not file.endswith(".py"):
                    continue

                # Optional: skip test files (clean architecture focus)
                if file.startswith("test_"):
                    continue

                file_path = os.path.join(root, file)

                relative_path = os.path.relpath(
                    file_path,
                    self.local_path
                )

                chunks = self.extract_chunks(
                    file_path,
                    relative_path
                )

                all_chunks.extend(chunks)

        os.makedirs("data", exist_ok=True)

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2)

        print(f"\nSaved {len(all_chunks)} chunks")


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":

    repo_url = input("Enter GitHub Repository URL: ")

    parser = RepoParser(repo_url)

    parser.clone_repository()

    parser.parse_repository()