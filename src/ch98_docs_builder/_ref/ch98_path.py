from src.ch00_py.file_toolbox import create_path


def create_src_keywords_description_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keywords_description.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keywords_description.json")
