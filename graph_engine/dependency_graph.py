import ast
import os
import pickle
import networkx as nx


class DependencyGraphGenerator:

    def __init__(self, repo_path):

        self.repo_path = repo_path
        self.graph = nx.DiGraph()

        self.external_packages = {
            "fastapi",
            "pydantic",
            "starlette",
            "typing",
            "asyncio",
            "json",
            "os",
            "sys",
            "logging",
            "datetime",
            "sqlalchemy",
            "numpy",
            "pandas",
            "requests",
            "matplotlib",
            "networkx",
            "collections",
            "functools",
            "inspect",
            "uuid",
            "decimal",
            "pathlib",
            "contextlib",
            "warnings",
            "re",
            "types",
            "email",
            "dataclasses",
            "itertools",
            "enum",
            "ipaddress",
            "copy",
            "time",
            "math",
            "statistics",
            "abc",
            "hashlib",
            "subprocess"
        }

    def normalize(self, value):

        return str(value).replace("\\", "/").strip()

    def extract_imports(self, file_path):

        imports = []

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                tree = ast.parse(
                    f.read(),
                    filename=file_path
                )

            current_module = (
                os.path.relpath(
                    file_path,
                    self.repo_path
                )
                .replace("\\", "/")
                .replace(".py", "")
                .replace("/", ".")
            )

            current_parts = current_module.split(".")

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:
                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    # normal imports
                    if node.level == 0:

                        if node.module:
                            imports.append(node.module)

                    # relative imports
                    else:

                        parent_parts = current_parts[:-node.level]

                        if node.module:
                            resolved = ".".join(
                                parent_parts + [node.module]
                            )
                        else:
                            resolved = ".".join(parent_parts)

                        if resolved:
                            imports.append(resolved)

        except Exception:
            pass

        return imports

    def is_internal(self, module):

        if not module:
            return False

        root = module.split(".")[0]

        return root not in self.external_packages

    def resolve_internal_module(self, module):

        module_path = module.replace(".", "/")

        possible_paths = [
            module_path + ".py",
            module_path + "/__init__.py"
        ]

        for path in possible_paths:

            absolute_path = os.path.join(
                self.repo_path,
                path
            )

            if os.path.exists(absolute_path):

                if path.endswith("/__init__.py"):
                    return self.normalize(
                        path.replace("/__init__.py", ".py")
                    )

                return self.normalize(path)

        return None

    def build_graph(self):

        excluded = {
            "venv",
            ".git",
            "__pycache__",
            "node_modules",
            "dist",
            "build",
            "tests",
            "docs_src",
            ".pytest_cache",
            ".mypy_cache"
        }

        for root, dirs, files in os.walk(
            self.repo_path
        ):

            dirs[:] = [
                d for d in dirs
                if d not in excluded
            ]

            for file in files:

                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(
                    root,
                    file
                )

                source_file = self.normalize(
                    os.path.relpath(
                        file_path,
                        self.repo_path
                    )
                )

                self.graph.add_node(source_file)

                imports = self.extract_imports(
                    file_path
                )

                for imported_module in imports:

                    if not self.is_internal(
                        imported_module
                    ):
                        continue

                    resolved_target = (
                        self.resolve_internal_module(
                            imported_module
                        )
                    )

                    if not resolved_target:
                        continue

                    self.graph.add_node(
                        resolved_target
                    )

                    self.graph.add_edge(
                        source_file,
                        resolved_target
                    )

    def save_graph(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            "data/dependency_graph.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.graph,
                f
            )

        print(
            "Graph saved successfully!"
        )


if __name__ == "__main__":

    repo_path = input(
        "Enter local repository path: "
    ).strip()

    if not os.path.exists(repo_path):

        print(
            "Invalid repository path"
        )

        exit()

    generator = DependencyGraphGenerator(
        repo_path
    )

    generator.build_graph()

    print(
        "\nDependency Graph Built Successfully!"
    )

    print(
        "Nodes:",
        len(generator.graph.nodes())
    )

    print(
        "Edges:",
        len(generator.graph.edges())
    )

    generator.save_graph()