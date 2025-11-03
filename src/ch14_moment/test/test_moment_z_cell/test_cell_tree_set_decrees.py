from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch11_bud._ref.ch11_path import (
    create_beliefspark_path,
    create_cell_dir_path as cell_dir,
)
from src.ch11_bud.bud_filehandler import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    save_belief_file,
)
from src.ch11_bud.cell_main import cellunit_shop
from src.ch14_moment.moment_cell import DecreeUnit, set_cell_trees_decrees
from src.ch14_moment.test._util.ch14_env import get_temp_dir, temp_dir_setup
from src.ch14_moment.test._util.ch14_examples import (
    example_casa_floor_clean_factunit,
    example_casa_floor_dirty_factunit,
    get_bob_mop_with_reason_beliefunit_example,
    get_bob_mop_without_reason_beliefunit_example,
)
from src.ref.keywords import ExampleStrs as exx


def test_DecreeUnit_Exists():
    # ESTABLISH / WHEN
    x_decreeunit = DecreeUnit()
    # THEN
    assert not x_decreeunit.parent_cell_dir
    assert not x_decreeunit.cell_dir
    assert not x_decreeunit.cell_ancestors
    assert not x_decreeunit.cell_mandate
    assert not x_decreeunit.cell_celldepth
    assert not x_decreeunit.root_cell_bool
    assert not x_decreeunit.cell_belief_name
    assert not x_decreeunit.spark_num


def test_DecreeUnit_get_child_cell_ancestors_ReturnsObj_Scenario0():
    # ESTABLISH
    x_decreeunit = DecreeUnit(cell_ancestors=[exx.yao])

    # WHEN
    child_cell_ancestors = x_decreeunit.get_child_cell_ancestors(exx.bob)

    # THEN
    assert child_cell_ancestors == [exx.yao, exx.bob]
    assert x_decreeunit.cell_ancestors != [exx.yao, exx.bob]
    assert x_decreeunit.cell_ancestors != child_cell_ancestors


# create a world with, cell.json, found facts and belief sparks
# for every found_fact change beliefspark to that fact
# create agenda (different than if found_fact was not applied)
def test_set_cell_trees_decrees_SetsRootAttr_Scenario0_Depth0NoFacts(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    das = []
    spark7 = 7
    # create cell file
    bob_cell = cellunit_shop(exx.bob, [], spark7, celldepth=0)
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, [])
    bob_bob_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, [exx.bob])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_bob_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}


def test_set_cell_trees_decrees_SetsRootAttr_Scenario1_Depth0AndOne_beliefspark_fact(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    das = []
    spark7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    # create cell file
    clean_fact = example_casa_floor_clean_factunit()
    clean_facts = {clean_fact.fact_context: clean_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        [],
        spark7,
        0,
        beliefadjust=bob_beliefadjust,
        beliefspark_facts=clean_facts,
    )
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, [])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsRootAttr_Scenario2_Depth0AndOne_found_fact(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    das = []
    spark7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    # create cell file
    clean_fact = example_casa_floor_clean_factunit()
    clean_facts = {clean_fact.fact_context: clean_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        [],
        spark7,
        celldepth=0,
        beliefadjust=bob_beliefadjust,
        found_facts=clean_facts,
    )
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, [])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario3_Depth1AndZero_boss_facts(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    bob_ancs = []
    bob_sue_ancs = [exx.sue]
    e7 = 7
    bob_beliefadjust = get_bob_mop_without_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(exx.sue, 1)
    bob_sue_beliefadjust = beliefunit_shop(exx.sue, exx.a23)
    # create cell file
    bob_cell = cellunit_shop(
        exx.bob, bob_ancs, spark_num=e7, celldepth=2, beliefadjust=bob_beliefadjust
    )
    bob_sue_cell = cellunit_shop(
        exx.bob,
        bob_sue_ancs,
        spark_num=e7,
        celldepth=0,
        beliefadjust=bob_sue_beliefadjust,
    )
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_sue_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}


def test_set_cell_trees_decrees_SetsChildCells_Scenario3_Depth1And_boss_facts(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    bob_ancs = []
    bob_sue_ancs = [exx.sue]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(exx.sue, 1)
    bob_sue_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_sue_beliefadjust.set_belief_name(exx.sue)
    # create cell file
    dirty_fact = example_casa_floor_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        bob_ancs,
        spark_num=e7,
        celldepth=2,
        beliefadjust=bob_beliefadjust,
        beliefspark_facts=dirty_facts,
    )
    bob_sue_cell = cellunit_shop(
        exx.bob,
        bob_sue_ancs,
        spark_num=e7,
        celldepth=0,
        beliefadjust=bob_sue_beliefadjust,
    )
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_sue_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario4_Depth3And_boss_facts(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    bob_ancs = []
    b_sue_ancs = [exx.sue]
    bs_yao_ancs = [exx.sue, exx.yao]
    bsy_zia_ancs = [exx.sue, exx.yao, exx.zia]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(exx.sue, 1)
    b_sue_ba = get_bob_mop_with_reason_beliefunit_example()
    b_sue_ba.set_belief_name(exx.sue)
    b_sue_ba.add_voiceunit(exx.yao, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(exx.yao)
    bs_yao_ba.add_voiceunit(exx.zia, 1)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(exx.zia)
    # create cell file
    dirty_fact = example_casa_floor_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        bob_ancs,
        spark_num=e7,
        celldepth=4,
        beliefadjust=bob_beliefadjust,
        beliefspark_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(exx.bob, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(exx.bob, bs_yao_ancs, e7, 0, beliefadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(exx.bob, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario5_Depth2And_boss_facts(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    bob_ancs = []
    b_sue_ancs = [exx.sue]
    bs_yao_ancs = [exx.sue, exx.yao]
    bsy_zia_ancs = [exx.sue, exx.yao, exx.zia]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(exx.sue, 1)
    b_sue_ba = get_bob_mop_with_reason_beliefunit_example()
    b_sue_ba.set_belief_name(exx.sue)
    b_sue_ba.add_voiceunit(exx.yao, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(exx.yao)
    bs_yao_ba.add_voiceunit(exx.zia, 1)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(exx.zia)
    # create cell file
    dirty_fact = example_casa_floor_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        bob_ancs,
        spark_num=e7,
        celldepth=2,
        beliefadjust=bob_beliefadjust,
        beliefspark_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(exx.bob, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(exx.bob, bs_yao_ancs, e7, 0, beliefadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(exx.bob, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}


def test_set_cell_trees_decrees_SetsChildCells_Scenario6_boss_facts_ResetAtEachCell(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    bob_ancs = []
    b_sue_ancs = [exx.sue]
    bs_yao_ancs = [exx.sue, exx.yao]
    bsy_zia_ancs = [exx.sue, exx.yao, exx.zia]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(exx.sue, 1)
    b_sue_ba = beliefunit_shop(exx.sue, exx.a23)
    b_sue_ba.set_belief_name(exx.sue)
    b_sue_ba.add_voiceunit(exx.yao, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(exx.yao)
    bs_yao_ba.add_voiceunit(exx.zia, 1)
    clean_fact = example_casa_floor_clean_factunit()
    bs_yao_ba.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(exx.zia)
    # create cell file
    dirty_fact = example_casa_floor_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        bob_ancs,
        spark_num=e7,
        celldepth=3,
        beliefadjust=bob_beliefadjust,
        beliefspark_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(exx.bob, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(exx.bob, bs_yao_ancs, e7, 0)
    bs_yao_cell.eval_beliefspark(bs_yao_ba)
    bsy_zia_cell = cellunit_shop(exx.bob, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    clean_facts = {clean_fact.fact_context: clean_fact}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == clean_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario7_NoCell_GetBeliefSpark(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    tp5 = 5
    bob_ancs = []
    b_sue_ancs = [exx.sue]
    bs_yao_ancs = [exx.sue, exx.yao]
    bsy_zia_ancs = [exx.sue, exx.yao, exx.zia]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(exx.sue, 1)
    b_sue_ba = get_bob_mop_with_reason_beliefunit_example()
    b_sue_ba.set_belief_name(exx.sue)
    b_sue_ba.add_voiceunit(exx.yao, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(exx.yao)
    bs_yao_ba.add_voiceunit(exx.zia, 1)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(exx.zia)
    # create cell file
    dirty_fact = example_casa_floor_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        exx.bob,
        bob_ancs,
        spark_num=e7,
        celldepth=4,
        beliefadjust=bob_beliefadjust,
        beliefspark_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(exx.bob, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    # bs_yao_cell = cellunit_shop(exx.bob, bs_yao_ancs, e7, 0, beliefadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(exx.bob, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, exx.a23, exx.bob, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    beliefspark_path = create_beliefspark_path(mstr_dir, exx.a23, exx.yao, e7)
    save_belief_file(beliefspark_path, None, bs_yao_ba)
    # cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert not cellunit_get_from_dir(bob_sue_yao_dir)
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, exx.a23)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts
