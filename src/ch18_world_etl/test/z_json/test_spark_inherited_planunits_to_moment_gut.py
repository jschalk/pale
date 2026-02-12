from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_json, save_json
from src.ch07_plan_logic.plan_main import get_planunit_from_dict, planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import create_gut_path
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import create_plan_spark_dir_path
from src.ch18_world_etl.etl_main import etl_spark_inherited_planunits_to_moment_gut
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import ExampleStrs as exx

# create test where spark create_plan_spark_dir_path()
# test that budunit with depth 0 is able to create
# test that budunit with depth 1 is able to create nested planunits directories and populate with spark relevant


def test_etl_spark_inherited_planunits_to_moment_gut_SetsFiles_Scenario0(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)
    a23_bob_e3_dir = create_plan_spark_dir_path(mstr_dir, a23_lasso, bob_inx, spark3)
    a23_bob_e7_dir = create_plan_spark_dir_path(mstr_dir, a23_lasso, bob_inx, spark7)
    plan_filename = "plan.json"
    e3_bob_plan = planunit_shop(bob_inx, exx.a23)
    e7_bob_plan = planunit_shop(bob_inx, exx.a23)
    e3_bob_plan.add_partnerunit(bob_inx, credit77)
    e3_bob_plan.add_partnerunit(yao_inx, credit44)
    e7_bob_plan.add_partnerunit(bob_inx, credit77)
    e7_bob_plan.add_partnerunit(sue_inx, credit88)
    e7_bob_plan.add_partnerunit(yao_inx, credit44)
    save_json(a23_bob_e3_dir, plan_filename, e3_bob_plan.to_dict())
    save_json(a23_bob_e7_dir, plan_filename, e7_bob_plan.to_dict())
    e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    e7_plan_path = create_path(a23_bob_e7_dir, plan_filename)
    assert os_path_exists(e3_plan_path)
    assert os_path_exists(e7_plan_path)
    print(e3_plan_path)
    print(e7_plan_path)
    a23_bob_gut_path = create_gut_path(mstr_dir, a23_lasso, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_spark_inherited_planunits_to_moment_gut(mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_plan = get_planunit_from_dict(open_json(a23_bob_gut_path))
    assert generated_gut_plan.partners == e7_bob_plan.partners
    assert generated_gut_plan == e7_bob_plan
    assert generated_gut_plan.to_dict() == e7_bob_plan.to_dict()
