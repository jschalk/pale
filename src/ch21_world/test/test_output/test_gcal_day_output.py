from datetime import datetime
from os.path import exists as os_path_exists
from pandas import DataFrame as pandas_DataFrame
from pytest import fixture as pytest_fixture
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch04_rope.rope import create_rope, create_rope_from_labels as init_rope
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch10_person_listen._ref.ch10_path import create_job_path
from src.ch10_person_listen.keep_tool import save_job_file
from src.ch13_time.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch14_moment.moment_main import momentunit_shop, save_moment_file
from src.ch17_idea.idea_db_tool import save_sheet
from src.ch20_kpi._ref.ch20_path import create_day_punch_txt_path as day_punch_path
from src.ch21_world.test._util.ch21_examples import br00013_example
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


# # TODO get this going
# def test_sheets_to_gcal_day_punchs_SavesFiles_Scenario1_TwoSueReports(temp3_fs):
#     # ESTABLISH
#     here_wdir = worlddir_shop("HereNow", str(temp3_fs))
#     br00013_example_path = create_path(here_wdir.input_dir, "example.xlsx")
#     h1_mop = init_rope(["herenow1", "family", exx.casa, exx.clean, exx.mop])
#     h1_tools = init_rope(["herenow1", "family", exx.casa, exx.clean, exx.scrub])
#     h7_mop = init_rope(["herenow7", "family", exx.casa, exx.clean, exx.mop])
#     h7_grocery = init_rope(["herenow7", "family", exx.casa, exx.clean, "grocery"])
#     h7_brush = init_rope(["herenow7", "family", exx.casa, exx.clean, "brush"])

#     data = [
#         (0, exx.sue, exx.zia, exx.hn1, h1_mop, 1, True),
#         (0, exx.sue, exx.yao, exx.hn1, h1_tools, 2, True),
#         (2, exx.yao, exx.yao, exx.hn7, h7_mop, 8, True),
#         (3, exx.sue, exx.sue, exx.hn7, h7_grocery, 3, True),
#         (4, exx.zia, exx.xio, exx.hn7, h7_brush, 1, True),
#     ]
#     cols = [
#         kw.spark_num,
#         kw.face_name,
#         kw.person_name,
#         kw.moment_rope,
#         kw.plan_rope,
#         kw.star,
#         kw.pledge,
#     ]
#     br00013_example = pandas_DataFrame(data, columns=cols)
#     save_sheet(br00013_example_path, "br00013_ex1", br00013_example)
#     mmt_dir = here_wdir.moment_mstr_dir
#     hn1_lasso = lassounit_shop(exx.hn1)
#     hn7_lasso = lassounit_shop(exx.hn7)
#     hn1_mmt_json_path = create_moment_json_path(mmt_dir, hn1_lasso)
#     hn7_mmt_json_path = create_moment_json_path(mmt_dir, hn7_lasso)
#     hn1_zia_job_path = create_job_path(mmt_dir, hn1_lasso, exx.zia)
#     hn7_yao_job_path = create_job_path(mmt_dir, hn7_lasso, exx.yao)
#     hn7_sue_job_path = create_job_path(mmt_dir, hn7_lasso, exx.sue)
#     hn7_xio_job_path = create_job_path(mmt_dir, hn7_lasso, exx.xio)
#     assert not os_path_exists(hn1_mmt_json_path)
#     assert not os_path_exists(hn7_mmt_json_path)
#     assert not os_path_exists(hn1_zia_job_path)
#     assert not os_path_exists(hn7_yao_job_path)
#     assert not os_path_exists(hn7_sue_job_path)
#     assert not os_path_exists(hn7_xio_job_path)
#     sue_hn1_day_punch_path = day_punch_path(mmt_dir, hn1_lasso, exx.sue)
#     sue_hn7_day_punch_path = day_punch_path(mmt_dir, hn7_lasso, exx.sue)
#     assert not os_path_exists(sue_hn1_day_punch_path)
#     assert not os_path_exists(sue_hn7_day_punch_path)

#     # WHEN
#     apr7 = datetime(2010, 5, 7)
#     sheets_to_gcal_day_punchs(worlddir=here_wdir, person_name=exx.sue, day=apr7)

#     # THEN
#     assert os_path_exists(hn1_mmt_json_path)
#     assert os_path_exists(hn7_mmt_json_path)
#     assert os_path_exists(hn1_zia_job_path)
#     assert os_path_exists(hn7_yao_job_path)
#     assert os_path_exists(hn7_sue_job_path)
#     assert os_path_exists(hn7_xio_job_path)
#     sue_hn1_day_punch_path = day_punch_path(mmt_dir, hn1_lasso, exx.sue)
#     sue_hn7_day_punch_path = day_punch_path(mmt_dir, hn7_lasso, exx.sue)
#     assert os_path_exists(sue_hn1_day_punch_path)
#     assert os_path_exists(sue_hn7_day_punch_path)
#     print(open_file(sue_hn1_day_punch_path))
#     assert 1 == 2
