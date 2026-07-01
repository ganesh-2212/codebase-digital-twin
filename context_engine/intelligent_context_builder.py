import ast
import os


class IntelligentContextBuilder:

    def __init__(self, repo_path):

        self.repo_path = repo_path

    def extract_code_context(self, relative_file_path):

        full_path = os.path.join(
            self.repo_path,
            relative_file_path
        )

        if not os.path.exists(full_path):
            return None

        try:

            with open(full_path, "r", encoding="utf-8") as file:
                source_code = file.read()

            tree = ast.parse(source_code)

            imports = []
            classes = []
            functions = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:
                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:
                        imports.append(node.module)

                elif isinstance(node, ast.ClassDef):

                    classes.append(node.name)

                elif isinstance(node, ast.FunctionDef):

                    functions.append(node.name)

            context = {
                "file": relative_file_path,
                "imports": imports[:10],
                "classes": classes[:10],
                "functions": functions[:20],
                "code_preview": source_code[:2000]
            }

            return context

        except Exception as e:

            print(f"Error processing {relative_file_path}: {e}")

            return None