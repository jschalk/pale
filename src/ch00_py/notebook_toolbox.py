import ast
from pathlib import Path
from src.ch00_py.file_toolbox import open_file
from typing import List


def get_imports_from_source(source: str) -> List[str]:
    """
    Return all import statements found in Python source code.

    Parameters
    ----------
    source : str
        Full Python file contents.

    Returns
    -------
    List[str]
        Import statements reconstructed as strings.
    """
    tree = ast.parse(source)
    imports: list[str] = []

    for node in ast.walk(tree):

        # import x, import x as y
        if isinstance(node, ast.Import):
            parts = []
            for alias in node.names:
                if alias.asname:
                    parts.append(f"{alias.name} as {alias.asname}")
                else:
                    parts.append(alias.name)
            imports.append(f"import {', '.join(parts)}")

        # from x import y
        elif isinstance(node, ast.ImportFrom):
            module = "." * node.level + (node.module or "")

            parts = []
            for alias in node.names:
                if alias.asname:
                    parts.append(f"{alias.name} as {alias.asname}")
                else:
                    parts.append(alias.name)

            imports.append(f"from {module} import {', '.join(parts)}")

    return imports


def create_marimo_notebook_from_test(test_file_path: Path, func_name: str) -> str:
    test_file_str = open_file(test_file_path)
    # p rint(f"{len(test_file_str)=}")
    imports_list = get_imports_from_source(test_file_str)
    # p rint("")
    marimo_str = """import marimo

app = marimo.App()


with app.setup:
    import marimo as mo"""
    for import_line in imports_list:
        marimo_str += f"\n    {import_line}"
    return marimo_str
