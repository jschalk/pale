from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import create_cell_dir_path as cell_dir
from src.ch11_bud.bud_filehandler import cellunit_get_from_dir, cellunit_save_to_dir
from src.ch11_bud.cell_main import cellunit_shop
from src.ch14_moment.moment_cell import set_cell_trees_found_facts
from src.ch14_moment.test._util.ch14_env import get_temp_dir, temp_dir_setup
from src.ch14_moment.test._util.ch14_examples import example_casa_floor_clean_factunit
from src.ref.keywords import ExampleStrs as exx


def test_set_cell_trees_found_facts_Scenario0_RootOnly_NoFacts(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)
    time5 = 5
    das = []
    bob5_dir = cell_dir(moment_mstr_dir, a23_lasso, exx.bob, time5, das)
    bob5_cell = cellunit_shop(exx.bob, planspark_facts={})
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    assert bob5_cell.get_plansparks_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(moment_mstr_dir, a23_lasso)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}


def test_set_cell_trees_found_facts_Scenario1_ChildNode_NoFacts(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)
    time5 = 5
    das = []
    das_y = [exx.yao]
    das_ys = [exx.yao, exx.sue]
    bob5_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_ys)
    cellunit_save_to_dir(bob5_dir, cellunit_shop(exx.bob, das))
    cellunit_save_to_dir(bob5_yao_dir, cellunit_shop(exx.bob, das_y))
    cellunit_save_to_dir(bob5_yao_sue_dir, cellunit_shop(exx.bob, das_ys))
    cellunit_get_from_dir(bob5_dir).get_plansparks_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_dir).get_plansparks_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_sue_dir).get_plansparks_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(mstr_dir, a23_lasso)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}


def test_set_cell_trees_found_facts_Scenario2_ChildNodeWithOneFactIsAssignedToAncestors(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)
    time5 = 5
    clean_fact = example_casa_floor_clean_factunit()
    das = []
    das_y = [exx.yao]
    das_ys = [exx.yao, exx.sue]
    bob5_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_lasso, exx.bob, time5, das_ys)
    bob5_planspark = planunit_shop(exx.bob, exx.a23)
    bob5_yao_planspark = planunit_shop(exx.yao, exx.a23)
    bob5_yao_sue_planspark = planunit_shop(exx.sue, exx.a23)
    bob5_planspark.add_personunit(exx.yao)
    bob5_yao_planspark.add_personunit(exx.sue)
    bob5_yao_sue_planspark.add_personunit(exx.bob)
    bob5_yao_sue_planspark.add_keg(clean_fact.fact_state, 1)
    bob5_yao_sue_planspark.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    bob5_cell = cellunit_shop(exx.bob, das, planadjust=bob5_planspark)
    bob5_yao_cell = cellunit_shop(exx.bob, das_y, planadjust=bob5_yao_planspark)
    clean_facts = {clean_fact.fact_context: clean_fact}
    bob5_yao_sue_cell = cellunit_shop(
        exx.bob,
        das_ys,
        planadjust=bob5_yao_sue_planspark,
        planspark_facts=clean_facts,
    )
    assert bob5_cell.get_plansparks_quota_ledger() == {exx.yao: 1000}
    assert bob5_yao_cell.get_plansparks_quota_ledger() == {exx.sue: 1000}
    assert bob5_yao_sue_cell.get_plansparks_quota_ledger() == {exx.bob: 1000}
    assert bob5_cell.planspark_facts == {}
    assert bob5_yao_cell.planspark_facts == {}
    assert bob5_yao_sue_cell.planspark_facts == clean_facts
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    cellunit_save_to_dir(bob5_yao_dir, bob5_yao_cell)
    cellunit_save_to_dir(bob5_yao_sue_dir, bob5_yao_sue_cell)
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == {}
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(mstr_dir, a23_lasso)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == clean_facts
