from datetime import datetime
from os.path import exists as os_path_exists
from pandas import DataFrame as pandas_DataFrame
from pytest import fixture as pytest_fixture
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch04_rope.rope import create_rope, create_rope_from_labels as init_rope
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch10_person_listen.keep_tool import save_job_file
from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch14_moment.moment_main import momentunit_shop, save_moment_file
from src.ch17_idea.idea_db_tool import save_sheet
from src.ch20_kpi._ref.ch20_path import create_day_punch_txt_path as day_punch_path
from src.ch21_world.world import sheets_to_gcal_day_punchs, worlddir_shop
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


def test_sheets_to_gcal_day_punchs_SavesFiles_Scenario0_TwoSueReports(
    temp3_fs,
):
    # ESTABLISH
    apr7 = datetime(2010, 4, 7)
    mmt_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    ep8_lasso = lassounit_shop(exx.ep8)
    sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
    sue_ep8_day_punch_path = day_punch_path(mmt_mstr_dir, ep8_lasso, exx.sue)
    worlddir = worlddir_shop("HereNow", str(temp3_fs))
    assert not os_path_exists(sue_a23_day_punch_path)
    assert not os_path_exists(sue_ep8_day_punch_path)

    # WHEN
    sheets_to_gcal_day_punchs(worlddir, exx.sue, apr7)

    # THEN
    assert not os_path_exists(sue_a23_day_punch_path)
    assert not os_path_exists(sue_ep8_day_punch_path)


@pytest_fixture
def br00013_example() -> pandas_DataFrame:
    """All rows valid. pledge=True throughout. Covers varied names."""
    # sue_person = personunit_shop(exx.sue, exx.a23)
    # add_epoch_planunit(sue_person)
    # sue_person.add_partnerunit(exx.bob, 2)
    # sue_person.add_partnerunit(exx.sue, 1)
    # casa_rope = sue_person.make_l1_rope(exx.casa)
    # clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    # sue_person.add_plan(clean_rope, 1, pledge=True)
    # sue_person.get_partner(exx.sue).add_membership(exx.run)

    h1_mop = init_rope([exx.hn1, "family", exx.casa, exx.clean, exx.mop])
    h1_tools = init_rope([exx.hn1, "family", exx.casa, exx.clean, exx.scrub])
    h7_mop = init_rope([exx.hn7, "family", exx.casa, exx.clean, exx.mop])
    h7_grocery = init_rope([exx.hn7, "family", exx.casa, exx.clean, "grocery"])
    h7_brush = init_rope([exx.hn7, "family", exx.casa, exx.clean, "brush"])

    data = [
        (0, exx.bob, exx.zia, exx.hn1, h1_mop, 1.0, True),
        (1, exx.sue, exx.yao, exx.hn1, h1_tools, 2.5, True),
        (2, exx.yao, exx.bob, exx.hn7, h7_mop, 0.8, True),
        (3, exx.xio, exx.sue, exx.hn7, h7_grocery, 3.3, True),
        (4, exx.zia, exx.xio, exx.hn7, h7_brush, 1.1, True),
    ]
    cols = [
        kw.spark_num,
        kw.face_name,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    return pandas_DataFrame(data, columns=cols)


# # TODO get this going
# def test_sheets_to_gcal_day_punchs_SavesFiles_Scenario1_TwoSueReports(
#     temp3_fs, br00013_example
# ):
#     # ESTABLISH
#     herenow_worlddir = worlddir_shop("HereNow", str(temp3_fs))
#     # WHEN
#     br00013_example_path = create_path(herenow_worlddir.input_dir, "example.xlsx")
#     save_sheet(br00013_example_path, "")
#     print(br00013_example)
#     # THEN
#     assert 1 == 2


#     # TODO convert this to dataframe
#     # sue_a23_person = get_a23_sue_clean_example()
#     # sue_ep8_person = get_ep8_sue_clean_example()
#     # yao_ep8_person = get_ep8_yao_clean_example()
#     # TODO save dataframes as sheets
#     epoch_config = get_default_epoch_config_dict()
#     x_epoch_label = epoch_config.get("epoch_label")
#     # add_epoch_planunit(sue_a23_person, epoch_config)
#     # add_epoch_planunit(sue_ep8_person, epoch_config)
#     # add_epoch_planunit(yao_ep8_person, epoch_config)
#     apr7 = datetime(2010, 4, 7)
#     # save momentunit json
#     mmt_mstr_dir = str(temp3_fs)
#     a23_lasso = lassounit_shop(exx.a23)
#     ep8_lasso = lassounit_shop(exx.ep8)
#     # assert exists moment_file(a23_moment, a23_lasso)
#     # assert exists moment_file(ep8_moment, ep8_lasso)
#     # assert exists job_file(mmt_mstr_dir, sue_a23_person)
#     # assert exists job_file(mmt_mstr_dir, sue_ep8_person)
#     # assert exists job_file(mmt_mstr_dir, yao_ep8_person)
#     sue_a23_day_punch_path = day_punch_path(mmt_mstr_dir, a23_lasso, exx.sue)
#     sue_ep8_day_punch_path = day_punch_path(mmt_mstr_dir, ep8_lasso, exx.sue)
#     assert not os_path_exists(sue_a23_day_punch_path)
#     assert not os_path_exists(sue_ep8_day_punch_path)

#     # WHEN
#     sheets_to_gcal_day_punchs(moment_mstr_dir=mmt_mstr_dir)

#     # THEN
#     assert os_path_exists(sue_a23_day_punch_path)
#     assert os_path_exists(sue_ep8_day_punch_path)
#     sue_a23_day_punch_str = open_file(sue_a23_day_punch_path)
#     sue_ep8_day_punch_str = open_file(sue_ep8_day_punch_path)
#     assert "Schedule Priorities" in sue_ep8_day_punch_str
#     assert f"Day Report for {exx.sue}" in sue_a23_day_punch_str
#     assert f"Day Report for {exx.sue}" in sue_ep8_day_punch_str
