from os import getcwd as os_getcwd
from src.ch01_py.file_toolbox import create_path
from src.ch15_nabu.nabu_config import (
    get_nabu_config_dict,
    get_nabu_dimens,
    get_quick_nabus_column_ref,
    nabu_config_path,
)
from src.ref.keywords import Ch15Keywords as kw


def test_nabu_config_path_ReturnsObj_Nabu() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch15_nabu")
    assert nabu_config_path() == create_path(chapter_dir, "nabu_config.json")


def test_get_nabu_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config = get_nabu_config_dict()

    # THEN
    assert nabu_config
    nabu_config_dimens = set(nabu_config.keys())
    assert "nabu_epochtime" in nabu_config_dimens
    assert len(nabu_config) == 1


#     _validate_nabu_config(nabu_config)
#     nabu_rope_dict = nabu_config.get(kw.nabu_rope)
#     nabu_label_dict = nabu_config.get(kw.nabu_label)
#     assert len(nabu_rope_dict.get(kw.jkeys)) == 1
#     assert len(nabu_label_dict.get(kw.jkeys)) == 1
#     assert len(nabu_rope_dict.get(kw.jvalues)) == 4
#     assert len(nabu_label_dict.get(kw.jvalues)) == 4


# def _validate_nabu_config(nabu_config: dict):
#     x_possible_args = {}

#     # for every nabu_format file there exists a unique nabu_number with leading zeros to make 5 digits
#     for nabu_dimens, dimen_dict in nabu_config.items():
#         print(f"_validate_nabu_config {nabu_dimens=}")
#         assert dimen_dict.get(kw.jkeys)
#         assert dimen_dict.get(kw.jvalues)
#         assert dimen_dict.get(kw.UPDATE) is None
#         assert dimen_dict.get(kw.INSERT) is None
#         assert dimen_dict.get(kw.DELETE) is None
#         assert dimen_dict.get(kw.normal_specs) is None
#         assert len(dimen_dict) == 2

#         nabu_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
#         for jkey_key in nabu_jkeys_keys:
#             print(f"_validate_nabu_config {nabu_dimens=} {jkey_key=} ")
#             assert jkey_key in x_possible_args
#         nabu_jvalues_keys = set(dimen_dict.get(kw.jvalues).keys())
#         for jvalue_key in nabu_jvalues_keys:
#             print(f"_validate_nabu_config {nabu_dimens=} {jvalue_key=} ")
#             assert jvalue_key in x_possible_args


def test_get_nabu_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    nabu_config_dimens = get_nabu_dimens()

    # THEN
    assert "nabu_epochtime" in nabu_config_dimens
    assert len(nabu_config_dimens) == 1
    gen_nabu_dimens = set(get_nabu_config_dict().keys())
    assert gen_nabu_dimens == get_nabu_dimens()
