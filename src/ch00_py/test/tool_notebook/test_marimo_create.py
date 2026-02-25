from src.ch00_py.file_toolbox import create_path, save_file
from src.ch00_py.notebook_toolbox import create_marimo_notebook_from_test
from src.ch00_py.test._util.ch00_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch00Keywords as kw, ExampleStrs as exx


def test_create_marimo_notebook_from_test_func_ReturnsObj_Scenario1(temp_dir_setup):
    # ESTABLISH
    test_function_str = """
def test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1(
    cursor0: Cursor,
):
    # ESTABLISH
    casa_color_tblname = "casa_color"
    insert_into_clause = f"INSERT INTO {casa_color_tblname} (casa_id, color)"
    values_clause = f"VALUES (1, 'Red'), (2, 'Blue'), (3, 'Blue');"
    cursor0.execute(f"{insert_into_clause} {values_clause}")
    assert get_row_count(cursor0, casa_color_tblname) == 3
    # Confirm destination table is empty
    casa_agg_tblname = "casa_agg"
    assert get_row_count(cursor0, casa_agg_tblname) == 0

    # WHEN
    insert_color_casa_into_casa_agg(cursor0)

    # THEN
    assert get_row_count(cursor0, casa_agg_tblname) == 2

    select_agg_sqlstr = f"SELECT * FROM {casa_agg_tblname};"
    cursor0.execute(select_agg_sqlstr)
    rows = cursor0.fetchall()
    print(rows)
    assert rows == [("Blue", 2), ("Red", 1)]
"""
    # create test file so that imports and be collected
    example_import_str = "from src.color import insert_color_casa_into_casa_agg"
    test_file_str = f"{example_import_str}\n\n\n{test_function_str}"
    test_file_path = create_path(get_temp_dir(), "test_color_sql.py")
    save_file(test_file_path, None, test_file_str)
    test_name = "test_insert_color_casa_into_casa_agg_PopulatesTable_Scenario1"

    # WHEN
    marimo_file_str = create_marimo_notebook_from_test(test_file_path, test_name)

    # THEN
    assert marimo_file_str
    print(marimo_file_str)
    expected_front = """import marimo

app = marimo.App()


with app.setup:
    import marimo as mo"""
    assert marimo_file_str.find(expected_front) == 0
    assert f"    {example_import_str}" in marimo_file_str
    # TODO complete this test
    # assert 1 == 2
