from src.ch03_voice.group import groupunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_BeliefUnit_get_voiceunit_group_titles_dict_ReturnsObj():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob)
    bob_belief.add_voiceunit(exx.yao)
    bob_belief.add_voiceunit(exx.sue)
    bob_belief.add_voiceunit(exx.zia)
    sue_voiceunit = bob_belief.get_voice(exx.sue)
    zia_voiceunit = bob_belief.get_voice(exx.zia)
    swim_group_str = ";Swim"
    sue_voiceunit.add_membership(exx.run)
    zia_voiceunit.add_membership(exx.run)
    zia_voiceunit.add_membership(swim_group_str)

    # WHEN
    group_titles_dict = bob_belief.get_voiceunit_group_titles_dict()

    # THEN
    print(f"{group_titles_dict=}")
    all_group_titles = {exx.yao, exx.sue, exx.zia, exx.run, swim_group_str}
    assert set(group_titles_dict.keys()) == all_group_titles
    assert set(group_titles_dict.keys()) != {swim_group_str, exx.run}
    assert group_titles_dict.get(swim_group_str) == {exx.zia}
    assert group_titles_dict.get(exx.run) == {exx.zia, exx.sue}
    assert group_titles_dict.get(exx.yao) == {exx.yao}
    assert group_titles_dict.get(exx.sue) == {exx.sue}
    assert group_titles_dict.get(exx.zia) == {exx.zia}


def test_BeliefUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob)
    assert not bob_belief.groupunits.get(exx.run)

    # WHEN
    bob_belief.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_belief.groupunits.get(exx.run)


def test_BeliefUnit_set_groupunit_Sets_rope_fund_grain():
    # ESTABLISH
    x_fund_grain = 5
    bob_belief = beliefunit_shop(exx.bob, fund_grain=x_fund_grain)
    assert not bob_belief.groupunits.get(exx.run)

    # WHEN
    bob_belief.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_belief.groupunits.get(exx.run).fund_grain == x_fund_grain


def test_BeliefUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob)
    assert not bob_belief.groupunit_exists(exx.run)

    # WHEN
    bob_belief.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_belief.groupunit_exists(exx.run)


def test_BeliefUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob)
    x_run_groupunit = groupunit_shop(exx.run)
    bob_belief.set_groupunit(x_run_groupunit)
    assert bob_belief.groupunits.get(exx.run)

    # WHEN / THEN
    assert bob_belief.get_groupunit(exx.run) == groupunit_shop(exx.run)


def test_BeliefUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_belief = beliefunit_shop(exx.yao)
    yao_group_cred_lumen = 3
    yao_group_debt_lumen = 2
    zia_group_cred_lumen = 4
    zia_group_debt_lumen = 5
    yao_belief.add_voiceunit(exx.yao, yao_group_cred_lumen, yao_group_debt_lumen)
    yao_belief.add_voiceunit(exx.zia, zia_group_cred_lumen, zia_group_debt_lumen)

    # WHEN
    xio_groupunit = yao_belief.create_symmetry_groupunit(exx.xio)

    # THEN
    assert xio_groupunit.group_title == exx.xio
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert len(xio_groupunit.memberships) == 2
    yao_groupunit = xio_groupunit.get_voice_membership(exx.yao)
    zia_groupunit = xio_groupunit.get_voice_membership(exx.zia)
    assert yao_groupunit.group_cred_lumen == yao_group_cred_lumen
    assert zia_groupunit.group_cred_lumen == zia_group_cred_lumen
    assert yao_groupunit.group_debt_lumen == yao_group_debt_lumen
    assert zia_groupunit.group_debt_lumen == zia_group_debt_lumen
