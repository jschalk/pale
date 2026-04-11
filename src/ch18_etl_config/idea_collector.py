from dataclasses import dataclass
from pandas import read_excel as pandas_read_excel
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.idea_config import get_idea_types, get_quick_ideas_column_ref
from src.ch17_idea.idea_db_tool import get_all_excel_sheet_names


def get_all_excel_ideasheets(dir: str) -> set[tuple[str, str, str]]:
    return get_all_excel_sheet_names(dir, get_idea_types())


@dataclass
class IdeaFileRef:
    file_dir: str = None
    filename: str = None
    sheet_name: str = None
    idea_type: str = None

    def get_csv_filename(self) -> str:
        return "" if self.idea_type is None else f"{self.idea_type}.csv"


def get_all_idea_dataframes(dir: str) -> list[IdeaFileRef]:
    ideasheets = get_all_excel_ideasheets(dir)
    candidate_ideas = set()
    for dir, filename, sheet_name in ideasheets:
        for idea_type in get_idea_types():
            if sheet_name.find(idea_type) >= 0:
                candidate_ideas.add((dir, filename, sheet_name, idea_type))

    idea_dfs = []
    for dir, filename, sheet_name, idea_type in candidate_ideas:
        idea_columns = get_quick_ideas_column_ref().get(idea_type)
        file_path = create_path(dir, filename)
        df = pandas_read_excel(file_path, sheet_name=sheet_name)
        if idea_columns.issubset(set(df.columns)):
            idea_dfs.append(IdeaFileRef(dir, filename, sheet_name, idea_type))
    return idea_dfs
