from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import count_dirs_files, open_json, save_json
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import (
    create_moment_json_path,
    create_moment_plans_dir_path,
)
from src.ch11_bud._ref.ch11_path import create_planspark_path
from src.ch14_moment._ref.ch14_path import (
    create_bud_person_mandate_ledger_path as bud_mandate_path,
)
from src.ch14_moment.moment_main import get_momentunit_from_dict, momentunit_shop
from src.ch14_moment.test._util.ch14_examples import example_casa_floor_clean_factunit
from src.ch18_world_etl._ref.ch18_path import create_moment_ote1_json_path
from src.ch20_world_logic.test._util.ch20_env import (
    get_temp_dir as worlds_dir,
    temp_dir_setup,
)
from src.ch20_world_logic.test._util.ch20_examples import (
    get_bob_mop_reason_planunit_example,
)
from src.ch20_world_logic.world import worldunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_WorldUnit_calc_moment_bud_person_mandate_net_ledgers_Scenaro0_BudEmpty(
    temp_dir_setup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    moment_mstr_dir = fay_world._moment_mstr_dir
    amy23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_json_path = create_moment_json_path(fay_world._moment_mstr_dir, exx.a23)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    print(f"{a23_json_path=}")
    a23_plans_path = create_moment_plans_dir_path(fay_world._moment_mstr_dir, exx.a23)
    assert count_dirs_files(a23_plans_path) == 0

    # WHEN
    fay_world.calc_moment_bud_person_mandate_net_ledgers()

    # THEN
    assert count_dirs_files(a23_plans_path) == 0


def test_WorldUnit_calc_moment_bud_person_mandate_net_ledgers_Scenaro1_SimpleBud(
    temp_dir_setup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    mstr_dir = fay_world._moment_mstr_dir
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_moment.add_budunit(exx.bob, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, exx.a23)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    # Create empty ote1 file
    a23_ote1_json_path = create_moment_ote1_json_path(mstr_dir, exx.a23)
    save_json(a23_ote1_json_path, None, {})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, exx.a23, exx.bob, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fay_world.calc_moment_bud_person_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_person_nets = {exx.bob: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_person_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(exx.bob, tp37)
    assert gen_bob37_budunit._bud_person_nets == expected_bud_person_nets


def test_WorldUnit_calc_moment_bud_person_mandate_net_ledgers_Scenaro2_BudExists(
    temp_dir_setup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    mstr_dir = fay_world._moment_mstr_dir

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(exx.a23, mstr_dir)
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_moment.add_budunit(exx.bob, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, exx.a23)
    save_json(a23_json_path, None, amy23_moment.to_dict())

    # Create spark time mapping plan_time_agg for time 37
    spark33 = 33
    spark44 = 44
    spark55 = 55
    bob55_planspark = get_bob_mop_reason_planunit_example()
    bob55_planspark.add_personunit(exx.sue, 1)
    sue44_planspark = planunit_shop(exx.sue, exx.a23)
    sue44_planspark.set_plan_name(exx.sue)
    sue44_planspark.add_personunit(exx.yao, 1)
    yao44_planspark = get_bob_mop_reason_planunit_example()
    yao44_planspark.set_plan_name(exx.yao)
    yao44_planspark.add_personunit(exx.zia, 1)
    clean_fact = example_casa_floor_clean_factunit()
    yao44_planspark.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    zia33_planspark = get_bob_mop_reason_planunit_example()
    zia33_planspark.set_plan_name(exx.zia)
    bob55_path = create_planspark_path(mstr_dir, exx.a23, exx.bob, spark55)
    sue44_path = create_planspark_path(mstr_dir, exx.a23, exx.sue, spark44)
    yao44_path = create_planspark_path(mstr_dir, exx.a23, exx.yao, spark44)
    zia33_path = create_planspark_path(mstr_dir, exx.a23, exx.zia, spark33)
    save_json(bob55_path, None, bob55_planspark.to_dict())
    save_json(sue44_path, None, sue44_planspark.to_dict())
    save_json(yao44_path, None, yao44_planspark.to_dict())
    save_json(zia33_path, None, zia33_planspark.to_dict())

    # Create empty ote1 file
    a23_ote1_dict = {
        exx.bob: {str(tp37): spark55},
        exx.sue: {str(tp37): spark44},
        exx.yao: {str(tp37): spark44},
        exx.zia: {str(tp37): spark33},
    }
    a23_ote1_json_path = create_moment_ote1_json_path(mstr_dir, exx.a23)
    save_json(a23_ote1_json_path, None, a23_ote1_dict)

    # create result bud_person_mandate_ledger file
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, exx.a23, exx.bob, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fay_world.calc_moment_bud_person_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_person_nets = {exx.zia: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_person_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(exx.bob, tp37)
    assert gen_bob37_budunit._bud_person_nets == expected_bud_person_nets
