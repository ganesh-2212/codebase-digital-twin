import ast
import pickle
import os


class CallGraphGenerator:

    def __init__(self, repo_path):

        self.repo_path = repo_path

        self.nodes = []
        self.edges = []

    # =====================================
    # BUILD GRAPH
    # =====================================

    def build(self):

        for root, _, files in os.walk(self.repo_path):

            for file in files:

                if not file.endswith(".py"):
                    continue

                path = os.path.join(
                    root,
                    file
                )

                self.process_file(path)

    # =====================================
    # PROCESS FILE
    # =====================================

    def process_file(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

            tree = ast.parse(source)

            visitor = CallVisitor(
                file_path,
                self.nodes,
                self.edges
            )

            visitor.visit(tree)

        except Exception as e:

            print(
                f"Failed parsing {file_path}"
            )

            print(e)

    # =====================================
    # SAVE
    # =====================================

    def save(self):

        graph = {

            "nodes": self.nodes,
            "edges": self.edges

        }

        with open(
            "data/call_graph.pkl",
            "wb"
        ) as f:

            pickle.dump(
                graph,
                f
            )

        print(
            "Call graph saved."
        )


# ==========================================
# AST VISITOR
# ==========================================

class CallVisitor(ast.NodeVisitor):

    def __init__(
        self,
        file_path,
        nodes,
        edges
    ):

        self.file_path = file_path

        self.nodes = nodes
        self.edges = edges

        self.current_function = None

    def visit_FunctionDef(self, node):

        self.current_function = node.name

        self.nodes.append({

            "id": node.name,
            "name": node.name,
            "type": "function",
            "file": self.file_path

        })

        self.generic_visit(node)

    def visit_ClassDef(self, node):

        self.nodes.append({

            "id": node.name,
            "name": node.name,
            "type": "class",
            "file": self.file_path

        })

        self.generic_visit(node)

    def visit_Call(self, node):

        if self.current_function:

            if isinstance(
                node.func,
                ast.Name
            ):

                target = node.func.id

                self.edges.append({

                    "source":
                    self.current_function,

                    "target":
                    target,

                    "type":
                    "calls"

                })

        self.generic_visit(node)