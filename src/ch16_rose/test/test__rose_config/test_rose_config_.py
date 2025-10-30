from os import getcwd as os_getcwd
from src.ch01_py.file_toolbox import create_path
from src.ch16_rose.rose_config import (
    default_unknown_str,
    default_unknown_str_if_None,
    get_quick_roses_column_ref,
    get_rose_args_dimen_mapping,
    get_rose_config_dict,
    get_rose_dimens,
    get_rose_filename,
    rose_config_path,
)
from src.ref.keywords import Ch16Keywords as kw


def test_get_rose_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_rose_filename() == "rose.json"


def test_rose_config_path_ReturnsObj_Rose() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch16_rose")
    assert rose_config_path() == create_path(chapter_dir, "rose_config.json")


def test_get_rose_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    rose_config = get_rose_config_dict()

    # THEN
    assert rose_config
    rose_config_dimens = set(rose_config.keys())
    assert kw.rose_name in rose_config_dimens
    assert kw.rose_title in rose_config_dimens
    assert kw.rose_label in rose_config_dimens
    assert kw.rose_rope in rose_config_dimens
    assert kw.rose_epoch in rose_config_dimens
    assert len(rose_config) == 5

    _validate_rose_config(rose_config)
    rose_rope_dict = rose_config.get(kw.rose_rope)
    rose_label_dict = rose_config.get(kw.rose_label)
    assert len(rose_rope_dict.get(kw.jkeys)) == 1
    assert len(rose_label_dict.get(kw.jkeys)) == 1
    assert len(rose_rope_dict.get(kw.jvalues)) == 4
    assert len(rose_label_dict.get(kw.jvalues)) == 4


def _validate_rose_config(rose_config: dict):
    x_possible_args = {
        kw.inx_epoch_diff,
        kw.otx_epoch_length,
        kw.inx_knot,
        kw.otx_knot,
        kw.inx_title,
        kw.otx_title,
        kw.inx_name,
        kw.otx_name,
        kw.inx_label,
        kw.otx_label,
        kw.inx_rope,
        kw.otx_rope,
        kw.unknown_str,
    }

    # for every rose_format file there exists a unique rose_number with leading zeros to make 5 digits
    for rose_dimens, dimen_dict in rose_config.items():
        print(f"_validate_rose_config {rose_dimens=}")
        assert dimen_dict.get(kw.jkeys)
        assert dimen_dict.get(kw.jvalues)
        assert dimen_dict.get(kw.rose_category)
        assert dimen_dict.get(kw.UPDATE) is None
        assert dimen_dict.get(kw.INSERT) is None
        assert dimen_dict.get(kw.DELETE) is None
        assert dimen_dict.get(kw.normal_specs) is None
        assert len(dimen_dict) == 3

        assert dimen_dict.get(kw.rose_category) in {"number", "term"}
        rose_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
        for jkey_key in rose_jkeys_keys:
            print(f"_validate_rose_config {rose_dimens=} {jkey_key=} ")
            assert jkey_key in x_possible_args
        rose_jvalues_keys = set(dimen_dict.get(kw.jvalues).keys())
        for jvalue_key in rose_jvalues_keys:
            print(f"_validate_rose_config {rose_dimens=} {jvalue_key=} ")
            assert jvalue_key in x_possible_args


def test_get_rose_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    rose_config_dimens = get_rose_dimens()

    # THEN
    assert kw.rose_name in rose_config_dimens
    assert kw.rose_title in rose_config_dimens
    assert kw.rose_label in rose_config_dimens
    assert kw.rose_rope in rose_config_dimens
    assert kw.rose_epoch in rose_config_dimens
    assert len(rose_config_dimens) == 5


def test_get_rose_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_rose_args_dimen_mapping = get_rose_args_dimen_mapping()
    print(f"{x_rose_args_dimen_mapping=}")

    # THEN
    assert x_rose_args_dimen_mapping
    assert x_rose_args_dimen_mapping.get(kw.otx_rope)
    rope_dimens = {kw.rose_rope}
    assert x_rose_args_dimen_mapping.get(kw.otx_rope) == rope_dimens
    assert x_rose_args_dimen_mapping.get(kw.inx_knot)
    inx_knot_dimens = x_rose_args_dimen_mapping.get(kw.inx_knot)
    assert len(inx_knot_dimens) == 4
    assert len(x_rose_args_dimen_mapping) == 13


def _get_all_rose_config_attrs() -> dict[str, set[str]]:
    rose_config = get_rose_config_dict()
    x_rose_attrs = {}
    for rose_dimen, jkeys_jvalues_dict in rose_config.items():
        attrs_set = set(jkeys_jvalues_dict.get(kw.jkeys).keys())
        attrs_set.update(set(jkeys_jvalues_dict.get(kw.jvalues).keys()))
        x_rose_attrs[rose_dimen] = attrs_set
    return x_rose_attrs


def test_get_quick_roses_column_ref_ReturnsObj():
    # ESTABLISH
    all_rose_config_attrs = _get_all_rose_config_attrs()
    # print(f"{all_rose_config_attrs=}")

    # WHEN / THEN
    assert kw.rose_rope in set(get_quick_roses_column_ref().keys())
    assert kw.rose_epoch in set(get_quick_roses_column_ref().keys())
    assert len(get_quick_roses_column_ref().keys()) == 5
    assert get_quick_roses_column_ref() == all_rose_config_attrs


def test_default_unknown_str_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_str() == "UNKNOWN"


def test_default_unknown_str_if_None_ReturnsObj():
    # ESTABLISH
    unknown33_str = "unknown33"
    x_nan = float("nan")

    # WHEN / THEN
    assert default_unknown_str_if_None() == default_unknown_str()
    assert default_unknown_str_if_None(None) == default_unknown_str()
    assert default_unknown_str_if_None(unknown33_str) == unknown33_str
    assert default_unknown_str_if_None(x_nan) == default_unknown_str()
