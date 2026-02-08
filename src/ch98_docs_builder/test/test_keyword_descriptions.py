from src.ch00_py._ref.ch00_path import create_keywords_classes_file_path
from src.ch00_py.chapter_desc_main import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
    valid_chapter_numbers,
)
from src.ch00_py.file_toolbox import open_file, save_file
from src.ch00_py.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
    create_examplestrs_class_str,
    create_keywords_enum_class_file_str,
    get_chapter_descs,
    get_cumlative_ch_keywords_dict,
    get_example_strs_config,
    get_keywords_by_chapter,
    get_keywords_src_config,
)
from src.ch98_docs_builder.keyword_description_builder import get_keywords_description


def test_get_keywords_description_ReturnsObj():
    # ESTABLISH / WHEN
    keywords_description = get_keywords_description()

    # THEN
    assert keywords_description
    keywords_config = get_keywords_src_config()
    assert keywords_description.keys() == keywords_config.keys()
    for keyword, description in keywords_description.items():
        assert description, keyword
