from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch11_bud.cell import cellunit_get_from_dict, cellunit_shop
from src.ch11_bud.test._util.ch11_examples import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)
from src.ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_CellUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    bob_sue_ancestors = [exx.bob, exx.sue]
    bob_sue_spark7 = 7
    bob_sue_bud_belief = exx.yao
    bob_sue_celldepth3 = 3
    bob_sue_mana_grain2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate444 = 444
    x_cellunit = cellunit_shop(
        bob_sue_bud_belief,
        bob_sue_ancestors,
        bob_sue_spark7,
        bob_sue_celldepth3,
        bob_sue_mana_grain2,
        bob_sue_quota300,
        mandate=bob_sue_mandate444,
    )

    # WHEN
    x_cell_dict = x_cellunit.to_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        kw.ancestors,
        kw.spark_num,
        kw.celldepth,
        kw.bud_belief_name,
        kw.mana_grain,
        kw.quota,
        kw.mandate,
        kw.beliefadjust,
        kw.beliefspark_facts,
        kw.found_facts,
        kw.boss_facts,
    ]
    assert x_cell_dict.get(kw.ancestors) == bob_sue_ancestors
    assert x_cell_dict.get(kw.spark_num) == bob_sue_spark7
    assert x_cell_dict.get(kw.celldepth) == bob_sue_celldepth3
    assert x_cell_dict.get(kw.bud_belief_name) == bob_sue_bud_belief
    assert x_cell_dict.get(kw.mana_grain) == bob_sue_mana_grain2
    assert x_cell_dict.get(kw.quota) == bob_sue_quota300
    assert x_cell_dict.get(kw.mandate) == bob_sue_mandate444
    bob_sue_belief = beliefunit_shop(bob_sue_bud_belief)
    assert x_cell_dict.get(kw.beliefadjust) == bob_sue_belief.to_dict()
    assert x_cell_dict.get(kw.beliefspark_facts) == {}
    assert x_cell_dict.get(kw.found_facts) == {}
    assert x_cell_dict.get(kw.boss_facts) == {}


def test_CellUnit_to_dict_ReturnsObj_Scenario1_EmptyBeliefAdjust():
    # ESTABLISH
    bob_sue_ancestors = [exx.bob, exx.sue]
    bob_sue_spark7 = 7
    bob_sue_celldepth3 = 3
    bob_sue_mana_grain2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate444 = 444
    x_cellunit = cellunit_shop(
        exx.yao,
        bob_sue_ancestors,
        bob_sue_spark7,
        bob_sue_celldepth3,
        bob_sue_mana_grain2,
        bob_sue_quota300,
        mandate=bob_sue_mandate444,
    )
    x_cellunit.beliefadjust = None

    # WHEN
    x_cell_dict = x_cellunit.to_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        kw.ancestors,
        kw.spark_num,
        kw.celldepth,
        kw.bud_belief_name,
        kw.mana_grain,
        kw.quota,
        kw.mandate,
        kw.beliefadjust,
        kw.beliefspark_facts,
        kw.found_facts,
        kw.boss_facts,
    ]
    assert x_cell_dict.get(kw.ancestors) == bob_sue_ancestors
    assert x_cell_dict.get(kw.spark_num) == bob_sue_spark7
    assert x_cell_dict.get(kw.celldepth) == bob_sue_celldepth3
    assert x_cell_dict.get(kw.bud_belief_name) == exx.yao
    assert x_cell_dict.get(kw.mana_grain) == bob_sue_mana_grain2
    assert x_cell_dict.get(kw.quota) == bob_sue_quota300
    assert x_cell_dict.get(kw.mandate) == bob_sue_mandate444
    bob_sue_belief = beliefunit_shop(exx.sue)
    assert x_cell_dict.get(kw.beliefadjust) == bob_sue_belief.to_dict()
    assert x_cell_dict.get(kw.beliefspark_facts) == {}
    assert x_cell_dict.get(kw.found_facts) == {}
    assert x_cell_dict.get(kw.boss_facts) == {}


def test_CellUnit_to_dict_ReturnsObj_Scenario1_WithMoreParameters():
    # ESTABLISH
    bob_sue_ancestors = [exx.bob, exx.sue]
    bob_sue_spark7 = 7
    bob_sue_bud_belief = exx.yao
    bob_sue_celldepth3 = 3
    bob_sue_mana_grain2 = 2
    bob_sue_quota300 = 300
    bob_sue_mandate444 = 444
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    x_cellunit = cellunit_shop(
        bob_sue_bud_belief,
        bob_sue_ancestors,
        bob_sue_spark7,
        bob_sue_celldepth3,
        bob_sue_mana_grain2,
        bob_sue_quota300,
        None,
        bob_sue_beliefspark_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
        mandate=bob_sue_mandate444,
    )

    # WHEN
    x_cell_dict = x_cellunit.to_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        kw.ancestors,
        kw.spark_num,
        kw.celldepth,
        kw.bud_belief_name,
        kw.mana_grain,
        kw.quota,
        kw.mandate,
        kw.beliefadjust,
        kw.beliefspark_facts,
        kw.found_facts,
        kw.boss_facts,
    ]
    assert x_cell_dict.get(kw.ancestors) == bob_sue_ancestors
    assert x_cell_dict.get(kw.spark_num) == bob_sue_spark7
    assert x_cell_dict.get(kw.celldepth) == bob_sue_celldepth3
    assert x_cell_dict.get(kw.bud_belief_name) == bob_sue_bud_belief
    assert x_cell_dict.get(kw.mana_grain) == bob_sue_mana_grain2
    assert x_cell_dict.get(kw.quota) == bob_sue_quota300
    assert x_cell_dict.get(kw.mandate) == bob_sue_mandate444
    assert (
        x_cell_dict.get(kw.beliefadjust)
        == beliefunit_shop(bob_sue_bud_belief).to_dict()
    )
    bob_sue_beliefspark_fact_dicts = {clean_fact.fact_context: clean_fact.to_dict()}
    bob_sue_found_fact_dicts = {dirty_fact.fact_context: dirty_fact.to_dict()}
    bob_sue_boss_fact_dicts = {sky_blue_fact.fact_context: sky_blue_fact.to_dict()}
    assert x_cell_dict.get(kw.beliefspark_facts) == bob_sue_beliefspark_fact_dicts
    assert x_cell_dict.get(kw.found_facts) == bob_sue_found_fact_dicts
    assert x_cell_dict.get(kw.boss_facts) == bob_sue_boss_fact_dicts
    assert len(x_cell_dict) == 11


def test_cellunit_get_from_dict_ReturnsObj_Scenario0_NoParameters():
    # ESTABLISH
    x_dict = {kw.bud_belief_name: exx.yao}

    # WHEN
    gen_cellunit = cellunit_get_from_dict(x_dict)

    # THEN
    assert gen_cellunit == cellunit_shop(exx.yao)


def test_cellunit_get_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    bob_sue_ancestors = [exx.bob, exx.sue]
    bob_sue_spark7 = 7
    bob_sue_bud_belief = exx.yao
    bob_sue_celldepth3 = 3
    bob_sue_mana_grain2 = 2
    bob_sue_quota300 = 300
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_beliefspark_factunits = {clean_fact.fact_context: clean_fact}
    bob_sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    bob_sue_belief = beliefunit_shop(bob_sue_bud_belief)
    bob_sue_belief.add_voiceunit(exx.sue)
    bob_sue_cellunit = cellunit_shop(
        bob_sue_bud_belief,
        bob_sue_ancestors,
        bob_sue_spark7,
        bob_sue_celldepth3,
        bob_sue_mana_grain2,
        bob_sue_quota300,
        bob_sue_belief,
        bob_sue_beliefspark_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
    )
    x_cell_dict = bob_sue_cellunit.to_dict()

    # WHEN
    gen_cellunit = cellunit_get_from_dict(x_cell_dict)

    # THEN
    assert gen_cellunit == bob_sue_cellunit
