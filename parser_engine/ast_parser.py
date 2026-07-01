import ast
import os


class ASTParser:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def parse_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        tree = ast.parse(source_code)

        print(f"\nParsing: {file_path}")

        for node in ast.walk(tree):

            # Function Definitions
            if isinstance(node, ast.FunctionDef):
                print(f"Function: {node.name}")

            # Async Functions
            elif isinstance(node, ast.AsyncFunctionDef):
                print(f"Async Function: {node.name}")

            # Class Definitions
            elif isinstance(node, ast.ClassDef):
                print(f"Class: {node.name}")

            # Imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    print(f"Import: {alias.name}")

            # From Imports
            elif isinstance(node, ast.ImportFrom):
                module = node.module

                for alias in node.names:
                    print(f"From {module} import {alias.name}")

    def scan_repository(self):
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)

                    try:
                        self.parse_file(file_path)

                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")


if __name__ == "__main__":

    repo_path = input("Enter local repository path: ")

    parser = ASTParser(repo_path)

    parser.scan_repository()