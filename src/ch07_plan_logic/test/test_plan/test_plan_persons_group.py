from src.ch02_person.group import groupunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_get_personunit_group_titles_dict_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob)
    bob_plan.add_personunit(exx.yao)
    bob_plan.add_personunit(exx.sue)
    bob_plan.add_personunit(exx.zia)
    sue_personunit = bob_plan.get_person(exx.sue)
    zia_personunit = bob_plan.get_person(exx.zia)
    swim_group_str = ";Swim"
    sue_personunit.add_membership(exx.run)
    zia_personunit.add_membership(exx.run)
    zia_personunit.add_membership(swim_group_str)

    # WHEN
    group_titles_dict = bob_plan.get_personunit_group_titles_dict()

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


def test_PlanUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob)
    assert not bob_plan.groupunits.get(exx.run)

    # WHEN
    bob_plan.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_plan.groupunits.get(exx.run)


def test_PlanUnit_set_groupunit_Sets_rope_fund_grain():
    # ESTABLISH
    x_fund_grain = 5
    bob_plan = planunit_shop(exx.bob, fund_grain=x_fund_grain)
    assert not bob_plan.groupunits.get(exx.run)

    # WHEN
    bob_plan.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_plan.groupunits.get(exx.run).fund_grain == x_fund_grain


def test_PlanUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob)
    assert not bob_plan.groupunit_exists(exx.run)

    # WHEN
    bob_plan.set_groupunit(groupunit_shop(exx.run))

    # THEN
    assert bob_plan.groupunit_exists(exx.run)


def test_PlanUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob)
    x_run_groupunit = groupunit_shop(exx.run)
    bob_plan.set_groupunit(x_run_groupunit)
    assert bob_plan.groupunits.get(exx.run)

    # WHEN / THEN
    assert bob_plan.get_groupunit(exx.run) == groupunit_shop(exx.run)


def test_PlanUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    yao_group_cred_lumen = 3
    yao_group_debt_lumen = 2
    zia_group_cred_lumen = 4
    zia_group_debt_lumen = 5
    yao_plan.add_personunit(exx.yao, yao_group_cred_lumen, yao_group_debt_lumen)
    yao_plan.add_personunit(exx.zia, zia_group_cred_lumen, zia_group_debt_lumen)

    # WHEN
    xio_groupunit = yao_plan.create_symmetry_groupunit(exx.xio)

    # THEN
    assert xio_groupunit.group_title == exx.xio
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert len(xio_groupunit.memberships) == 2
    yao_groupunit = xio_groupunit.get_person_membership(exx.yao)
    zia_groupunit = xio_groupunit.get_person_membership(exx.zia)
    assert yao_groupunit.group_cred_lumen == yao_group_cred_lumen
    assert zia_groupunit.group_cred_lumen == zia_group_cred_lumen
    assert yao_groupunit.group_debt_lumen == yao_group_debt_lumen
    assert zia_groupunit.group_debt_lumen == zia_group_debt_lumen
