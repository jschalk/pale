from src.ch30_etl_app.etl_gui_tool import (
    create_elpaso_time_config_file,
    create_emmanuel_belief_file,
    create_example_moment_budget_file,
    create_example_moment_ledger_file,
    create_five_time_config_file,
    get_option_table_options,
)


def test_get_option_table_options_ReturnsObj():
    # ESTABLISH / WHEN
    result = get_option_table_options()
    # THEN
    # func_desc00 = "Create TeamFive Moment Time Config File"
    # func_desc01 = "Create El Paso Moment Time Config File"
    # func_desc02 = "create_emmanuel_belief_file"
    # func_desc03 = "create_example_moment_ledger_file"
    # func_desc04 = "create_example_moment_budget_file"
    # expected_keys = {func_desc00, func_desc01, func_desc02, func_desc03, func_desc04}
    # assert set(result.keys()) == expected_keys
    expected_func_objs = {
        create_five_time_config_file,
        create_elpaso_time_config_file,
        create_emmanuel_belief_file,
        create_example_moment_ledger_file,
        create_example_moment_budget_file,
    }

    for func_desc, func_obj in result.values():
        assert callable(func_obj)
        assert len(func_desc) > 0
        assert func_obj in expected_func_objs

    # assert result[func_desc00] is create_five_time_config_file
    # assert result[func_desc01] is create_elpaso_time_config_file
    # assert result[func_desc02] is create_emmanuel_belief_file
    # assert result[func_desc03] is create_example_moment_ledger_file
    # assert result[func_desc04] is create_example_moment_budget_file
