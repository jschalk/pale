from src.linter.style import function_name_style_is_correct


def test_function_name_style_is_correct_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert function_name_style_is_correct("get_label")
    assert not function_name_style_is_correct("get_label_No")
    assert function_name_style_is_correct("get_label_None")
    assert not function_name_style_is_correct("Get_label")
    assert not function_name_style_is_correct("test_get_label")
    assert function_name_style_is_correct("test_get_label_ReturnsObj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj_scenari")
    assert not function_name_style_is_correct("test_get_label_ReturnObj_scenario")
    assert not function_name_style_is_correct("test_GetLabel_exists")
    assert function_name_style_is_correct("test_GetLabel_Exists")
    assert not function_name_style_is_correct("test_get_label_Returnsobj")
    assert not function_name_style_is_correct("test_get_label_returnsobj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj")
    assert not function_name_style_is_correct("test_get_label_ReturnObj")
    assert function_name_style_is_correct("test_get_label_ReturnsObj_correctly")
