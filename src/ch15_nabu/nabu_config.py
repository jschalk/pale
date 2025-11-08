from os import getcwd as os_getcwd
from src.ch01_py.dict_toolbox import get_from_nested_dict
from src.ch01_py.file_toolbox import create_path, open_json


def nabu_config_path():
    "Returns path: c15_nabu/nabu_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch15_nabu")
    return create_path(chapter_dir, "nabu_config.json")


def get_nabu_config_dict():
    return open_json(nabu_config_path())


def get_quick_nabus_column_ref():
    pass


def get_nabu_dimens() -> set:
    return {"nabu_epochtime"}


def get_nabu_args() -> set:
    return {"otx_time", "inx_time", "moment_label"}


def get_nabuable_args() -> set:
    return {
        "tran_time",
        "bud_time",
        "offi_time",
        "reason_lower",
        "fact_lower",
        "fact_upper",
        "reason_upper",
    }
