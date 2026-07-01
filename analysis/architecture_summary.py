import os
import ast
import pickle


class ArchitectureSummaryGenerator:

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.summaries = []

    # ==========================================
    # EXTRACT FUNCTION CALLS (IMPROVED)
    # ==========================================
    def extract_calls(self, node):

        calls = set()

        for child in ast.walk(node):

            if isinstance(child, ast.Call):

                if isinstance(child.func, ast.Name):
                    calls.add(child.func.id)

                elif isinstance(child.func, ast.Attribute):
                    calls.add(child.func.attr)

        return list(calls)

    # ==========================================
    # EXTRACT FILE STRUCTURE
    # ==========================================
    def extract_architecture(self, file_path, relative_path):

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read(), filename=file_path)

        except Exception:
            return []

        results = []

        for node in ast.walk(tree):

            # ----------------------------------
            # CLASS DETECTION
            # ----------------------------------
            if isinstance(node, ast.ClassDef):

                methods = []
                inherits = []

                for child in node.body:

                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(child.name)

                for base in node.bases:
                    if isinstance(base, ast.Name):
                        inherits.append(base.id)

                results.append({
                    "name": node.name,
                    "type": "class",
                    "file": relative_path.replace("\\", "/"),
                    "methods": methods,
                    "inherits": inherits,
                    "calls": self.extract_calls(node)
                })

            # ----------------------------------
            # FUNCTION DETECTION
            # ----------------------------------
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                # skip class methods (already included)
                if isinstance(getattr(node, "parent", None), ast.ClassDef):
                    continue

                results.append({
                    "name": node.name,
                    "type": "function",
                    "file": relative_path.replace("\\", "/"),
                    "methods": [],
                    "inherits": [],
                    "calls": self.extract_calls(node)
                })

        return results

    # ==========================================
    # GENERATE SUMMARIES
    # ==========================================
    def generate(self):

        excluded_dirs = {
            "venv", "__pycache__", ".git",
            "node_modules", "dist", "build",
            "tests", "docs", ".pytest_cache"
        }

        for root, dirs, files in os.walk(self.repo_path):

            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for file in files:

                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(root, file)

                relative_path = os.path.relpath(
                    file_path,
                    self.repo_path
                ).replace("\\", "/")

                items = self.extract_architecture(
                    file_path,
                    relative_path
                )

                self.summaries.extend(items)

        return self.summaries

    # ==========================================
    # SAVE
    # ==========================================
    def save(self):

        os.makedirs("data", exist_ok=True)

        with open("data/architecture_summaries.pkl", "wb") as f:
            pickle.dump(self.summaries, f)

        print(f"Saved {len(self.summaries)} architecture summaries")