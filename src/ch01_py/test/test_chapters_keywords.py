from src.ch01_py._ref.ch01_path import create_keywords_classes_file_path
from src.ch01_py.chapter_desc_tools import get_chapter_desc_prefix
from src.ch01_py.file_toolbox import open_file, save_file
from src.ch01_py.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
    create_examplestrs_class_str,
    create_keywords_enum_class_file_str,
    get_chapter_descs,
    get_cumlative_ch_keywords_dict,
    get_example_strs_config,
    get_keywords_by_chapter,
    get_keywords_src_config,
)


def test_get_chapter_desc_prefix_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_chapter_desc_prefix("ch03_") == "ch03"
    assert get_chapter_desc_prefix("ch99") == "ch99"
    assert get_chapter_desc_prefix("ch03") == "ch03"
    assert get_chapter_desc_prefix("ch99") == "ch99"
    assert get_chapter_desc_prefix("chXX") == "chXX"
    assert get_chapter_desc_prefix("cha01") != "ch02"


def test_get_example_strs_config_ReturnsObj():
    # ESTABLISH / WHEN
    example_strs_config = get_example_strs_config()

    # THEN
    assert example_strs_config
    for key_str, key_value in example_strs_config.items():
        assert type(key_str) == type("")
        assert type(key_value) == type("")


def test_get_keywords_src_config_ReturnsObj():
    # ESTABLISH / WHEN
    keywords_config = get_keywords_src_config()

    # THEN
    assert keywords_config
    for keyword, ref_dict in keywords_config.items():
        # print(f"{keyword=} {ref_dict=}")
        assert set(ref_dict.keys()).issuperset({"init_chapter"}), keyword
    example_strs_keys = set(get_example_strs_config().keys())
    keys_in_both = example_strs_keys.intersection(set(keywords_config.keys()))
    assert not keys_in_both


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario0_Empty_keyword_set():
    # ESTABLISH
    ch03_str = "ch03"
    ch03_keywords = {}

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch03_str, ch03_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""

class Ch03{key_str}words(str, Enum):
    pass

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario1_NonEmpty_keyword_set():
    # ESTABLISH
    ch03_str = "ch03"
    keywordF = "Funny"
    keywordI = "INSET"
    keywordf = "funny"
    keywordG = "Guppies"
    keywordH = "Heath"
    keywordR = "Risto"
    ch03_keywords = {
        keywordF,
        keywordI,
        keywordf,
        keywordG,
        keywordH,
        keywordR,
    }

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch03_str, ch03_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""

class Ch03{key_str}words(str, Enum):
    {keywordF} = "{keywordF}"
    {keywordG} = "{keywordG}"
    {keywordH} = "{keywordH}"
    {keywordI} = "{keywordI}"
    {keywordR} = "{keywordR}"
    {keywordf} = "{keywordf}"

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_create_examplestrs_class_str_ReturnsObj():
    # ESTABLISH
    example_strs_dict = {"sue": "Sue", "yao": "Yao", "bob": "Bob"}

    # WHEN
    x_str = create_examplestrs_class_str(example_strs_dict)

    # THEN
    expected_str = """class ExampleStrs(str, Enum):
    bob = "Bob"
    sue = "Sue"
    yao = "Yao"

    def __str__(self):
        return self.value"""
    assert x_str == expected_str


def test_create_all_enum_keyword_classes_str_ReturnsObj():
    # ESTABLISH
    examples_strs = get_example_strs_config()

    #  WHEN
    classes_str = create_all_enum_keyword_classes_str()

    # THEN
    keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
    cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
    expected_classes_str = f"""from enum import Enum


{create_examplestrs_class_str(examples_strs)}
"""
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        ch_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_keywords = cumlative_keywords.get(ch_prefix)
        enum_class_str = create_keywords_enum_class_file_str(ch_prefix, ch_keywords)
        expected_classes_str += enum_class_str
    assert expected_classes_str == classes_str
    two_line_spacing_str = f"""from enum import Enum


{create_examplestrs_class_str(examples_strs)}


class Ch00Key"""
    print(classes_str[:100])
    assert classes_str.find(two_line_spacing_str) == 0


def test_SpecialTestThatBuildsKeywordEnumClasses():
    # ESTABLISH
    # save file for all Enum class references
    keywords_classes_file_path = create_keywords_classes_file_path("src")
    enum_classes_str = create_all_enum_keyword_classes_str()
    current_classes_file_str = open_file(keywords_classes_file_path)
    # print(enum_classes_str[:100])
    print(
        "Create and save Enum classes, fail test if there are any changes so changes can apply to next test run. "
    )
    save_file(keywords_classes_file_path, None, enum_classes_str)
    assertion_failure_str = "Special case: keywords.py was changed. Run test again."

    # WHEN / THEN
    prev_and_curr_classes_file_are_same = enum_classes_str == current_classes_file_str
    assert prev_and_curr_classes_file_are_same, assertion_failure_str
