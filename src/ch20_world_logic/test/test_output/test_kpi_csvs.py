from os.path import exists as os_path_exists
from pandas import DataFrame
from src.ch00_py.file_toolbox import create_path
from src.ch17_idea.idea_db_tool import upsert_sheet
from src.ch20_world_logic.test._util.ch20_env import (
    get_temp_dir as worlds_dir,
    temp_dir_setup,
)
from src.ch20_world_logic.world import worldunit_shop
from src.ref.keywords import Ch20Keywords as kw, ExampleStrs as exx


def test_WorldUnit_create_kpi_csvs_Senario0_EmptyWorld_CreatesFile(
    temp_dir_setup,
):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    fay_world.sheets_input_to_clarity_mstr()
    kpi001_csv_path = create_path(output_dir, f"{kw.moment_kpi001_person_nets}.csv")
    assert not os_path_exists(kpi001_csv_path)

    # WHEN
    fay_world.create_world_kpi_csvs()

    # THEN
    assert os_path_exists(kpi001_csv_path)


def test_WorldUnit_create_kpi_csvs_Senario1_Add_CreatesFile(temp_dir_setup):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    spark2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00011_columns = [
        kw.spark_num,
        kw.face_name,
        kw.moment_rope,
        kw.plan_name,
        kw.person_name,
    ]
    br00011_rows = [[spark2, exx.sue, exx.a23, exx.sue, exx.sue]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    fay_world.sheets_input_to_clarity_mstr()
    kpi001_csv_path = create_path(output_dir, f"{kw.moment_kpi001_person_nets}.csv")
    print(f"         {kpi001_csv_path=}")
    assert not os_path_exists(kpi001_csv_path)

    # WHEN
    fay_world.create_world_kpi_csvs()

    # THEN
    assert os_path_exists(kpi001_csv_path)
    expected_csv_str = f"{kw.moment_rope},{kw.plan_name},{kw.bnet_funds},{kw.fund_rank},{kw.pledges_count}\n"
    assert open(kpi001_csv_path).read() == expected_csv_str
