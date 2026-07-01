import os
import ast
import pickle
import builtins


class CallGraphBuilder:

    def __init__(self, repo_path):

        self.repo_path = repo_path

        self.nodes = set()
        self.edges = []

        self.project_functions = set()
        self.project_classes = set()

        self.ignore_calls = set(dir(builtins))

    # ==========================================
    # PASS 1 — COLLECT DEFINITIONS
    # ==========================================

    def collect_definitions(self):

        for root, dirs, files in os.walk(self.repo_path):

            dirs[:] = [
                d for d in dirs
                if d not in [
                    "venv",
                    ".git",
                    "__pycache__",
                    "node_modules",
                    "dist",
                    "build",
                    "repos",
                    "tests",
                    ".github"
                ]
            ]

            for file in files:

                if not file.endswith(".py"):
                    continue

                path = os.path.join(root, file)

                try:

                    with open(
                        path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        tree = ast.parse(f.read())

                except Exception:
                    continue

                for node in ast.walk(tree):

                    if isinstance(node, ast.ClassDef):

                        self.project_classes.add(
                            node.name
                        )

                    elif isinstance(
                        node,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef
                        )
                    ):

                        self.project_functions.add(
                            node.name
                        )

    # ==========================================
    # EXTRACT CALLS
    # ==========================================

    def extract_call_name(self, call):

        if isinstance(call.func, ast.Name):

            return call.func.id

        if isinstance(call.func, ast.Attribute):

            return call.func.attr

        return None

    # ==========================================
    # ANALYZE FILE
    # ==========================================

    def analyze_file(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                source = f.read()

            tree = ast.parse(source)

        except Exception:
            return

        for node in tree.body:

            # ==================================
            # CLASS
            # ==================================

            if isinstance(node, ast.ClassDef):

                class_name = node.name

                self.nodes.add(class_name)

                for child in node.body:

                    if not isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef
                        )
                    ):
                        continue

                    method_name = (
                        f"{class_name}.{child.name}"
                    )

                    self.nodes.add(
                        method_name
                    )

                    self.edges.append({

                        "source": class_name,
                        "target": method_name,
                        "relation": "contains"

                    })

                    for call in ast.walk(child):

                        if not isinstance(
                            call,
                            ast.Call
                        ):
                            continue

                        called = self.extract_call_name(
                            call
                        )

                        if not called:
                            continue

                        if called in self.ignore_calls:
                            continue

                        if (
                            called
                            not in self.project_functions
                            and
                            called
                            not in self.project_classes
                        ):
                            continue

                        self.edges.append({

                            "source": method_name,
                            "target": called,
                            "relation": "calls"

                        })

            # ==================================
            # FUNCTION
            # ==================================

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            ):

                function_name = node.name

                self.nodes.add(
                    function_name
                )

                for call in ast.walk(node):

                    if not isinstance(
                        call,
                        ast.Call
                    ):
                        continue

                    called = self.extract_call_name(
                        call
                    )

                    if not called:
                        continue

                    if called in self.ignore_calls:
                        continue

                    if (
                        called
                        not in self.project_functions
                        and
                        called
                        not in self.project_classes
                    ):
                        continue

                    self.edges.append({

                        "source": function_name,
                        "target": called,
                        "relation": "calls"

                    })

    # ==========================================
    # BUILD GRAPH
    # ==========================================

    def build(self):

        self.collect_definitions()

        for root, dirs, files in os.walk(
            self.repo_path
        ):

            dirs[:] = [
                d for d in dirs
                if d not in [
                    "venv",
                    ".git",
                    "__pycache__",
                    "node_modules",
                    "dist",
                    "build",
                    "repos",
                    "tests",
                    ".github"
                ]
            ]

            for file in files:

                if file.endswith(".py"):

                    self.analyze_file(
                        os.path.join(root, file)
                    )

    # ==========================================
    # SAVE
    # ==========================================

    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            "data/call_graph.pkl",
            "wb"
        ) as f:

            pickle.dump({

                "nodes": list(self.nodes),
                "edges": self.edges

            }, f)

        print(
            f"\nSaved {len(self.nodes)} nodes"
        )

        print(
            f"Saved {len(self.edges)} relationships"
        )

        print(
            "\ncall_graph.pkl generated successfully!"
        )


if __name__ == "__main__":

    repo_path = input(
        "Enter repository path: "
    )

    builder = CallGraphBuilder(
        repo_path
    )

    builder.build()

    builder.save()