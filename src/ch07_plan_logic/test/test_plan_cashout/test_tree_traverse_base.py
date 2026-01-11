from pytest import raises as pytest_raises
from src.ch02_person.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factheir_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import (
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
)
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_clear_keg_dict_and_plan_obj_settle_attrs_SetsAttrs_Scenario0():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_keg_dict = {1: 2, 2: 4}
    sue_plan.rational = x_rational
    sue_plan.tree_traverse_count = x_tree_traverse_count
    sue_plan._keg_dict = x_keg_dict
    sue_plan.offtrack_kids_star_set = "example"
    sue_plan.reason_contexts = {"example2"}
    sue_plan.range_inheritors = {"example2": 1}
    assert sue_plan.rational == x_rational
    assert sue_plan.tree_traverse_count == x_tree_traverse_count
    assert sue_plan._keg_dict == x_keg_dict
    assert sue_plan.offtrack_kids_star_set != set()
    assert sue_plan.reason_contexts != set()
    assert sue_plan.range_inheritors != {}

    # WHEN
    sue_plan._clear_keg_dict_and_plan_obj_settle_attrs()

    # THEN
    assert sue_plan.rational != x_rational
    assert not sue_plan.rational
    assert sue_plan.tree_traverse_count != x_tree_traverse_count
    assert sue_plan.tree_traverse_count == 0
    assert sue_plan._keg_dict != x_keg_dict
    assert sue_plan._keg_dict == {sue_plan.kegroot.get_keg_rope(): sue_plan.kegroot}
    assert sue_plan.offtrack_kids_star_set == set()
    assert not sue_plan.reason_contexts
    assert not sue_plan.range_inheritors


def test_PlanUnit_clear_keg_dict_and_plan_obj_settle_attrs_SetsAttrs_Scenario1():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    x_keep_justifed = False
    x_sum_healerunit_kegs_fund_total = 140
    sue_plan.keeps_justified = x_keep_justifed
    sue_plan.keeps_buildable = "swimmers"
    sue_plan.sum_healerunit_kegs_fund_total = x_sum_healerunit_kegs_fund_total
    sue_plan._keep_dict = {"run": "run"}
    sue_plan._healers_dict = {"run": "run"}
    assert sue_plan.keeps_justified == x_keep_justifed
    assert sue_plan.keeps_buildable
    assert sue_plan.sum_healerunit_kegs_fund_total == x_sum_healerunit_kegs_fund_total
    assert sue_plan._keep_dict != {}
    assert sue_plan._healers_dict != {}

    # WHEN
    sue_plan._clear_keg_dict_and_plan_obj_settle_attrs()

    # THEN
    assert sue_plan.keeps_justified != x_keep_justifed
    assert sue_plan.keeps_justified
    assert sue_plan.keeps_buildable is False
    assert sue_plan.sum_healerunit_kegs_fund_total == 0
    assert not sue_plan._keep_dict
    assert not sue_plan._healers_dict


def test_PlanUnit_cashout_ClearsDescendantAttributes():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = sue_plan.make_rope(wk_rope, mon_str)
    mon_keg = sue_plan.get_keg_obj(mon_rope)
    assert sue_plan.kegroot.descendant_pledge_count is None
    assert sue_plan.kegroot.all_person_cred is None
    assert sue_plan.kegroot.all_person_debt is None
    assert casa_keg.descendant_pledge_count is None
    assert casa_keg.all_person_cred is None
    assert casa_keg.all_person_debt is None
    assert mon_keg.descendant_pledge_count is None
    assert mon_keg.all_person_cred is None
    assert mon_keg.all_person_debt is None

    sue_plan.kegroot.descendant_pledge_count = -2
    sue_plan.kegroot.all_person_cred = -2
    sue_plan.kegroot.all_person_debt = -2
    casa_keg.descendant_pledge_count = -2
    casa_keg.all_person_cred = -2
    casa_keg.all_person_debt = -2
    mon_keg.descendant_pledge_count = -2
    mon_keg.all_person_cred = -2
    mon_keg.all_person_debt = -2

    assert sue_plan.kegroot.descendant_pledge_count == -2
    assert sue_plan.kegroot.all_person_cred == -2
    assert sue_plan.kegroot.all_person_debt == -2
    assert casa_keg.descendant_pledge_count == -2
    assert casa_keg.all_person_cred == -2
    assert casa_keg.all_person_debt == -2
    assert mon_keg.descendant_pledge_count == -2
    assert mon_keg.all_person_cred == -2
    assert mon_keg.all_person_debt == -2

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.kegroot.descendant_pledge_count == 2
    assert casa_keg.descendant_pledge_count == 0
    assert mon_keg.descendant_pledge_count == 0

    assert mon_keg.all_person_cred is True
    assert mon_keg.all_person_debt is True
    assert casa_keg.all_person_cred is True
    assert casa_keg.all_person_debt is True
    assert sue_plan.kegroot.all_person_cred is True
    assert sue_plan.kegroot.all_person_debt is True


def test_PlanUnit_cashout_RootOnlySetsDescendantAttributes():
    # ESTABLISH
    yao_plan = planunit_shop(plan_name="Yao")
    assert yao_plan.kegroot.descendant_pledge_count is None
    assert yao_plan.kegroot.all_person_cred is None
    assert yao_plan.kegroot.all_person_debt is None

    # WHEN
    yao_plan.cashout()

    # THEN
    assert yao_plan.kegroot.descendant_pledge_count == 0
    assert yao_plan.kegroot.all_person_cred is True
    assert yao_plan.kegroot.all_person_debt is True


def test_PlanUnit_cashout_NLevelSetsDescendantAttributes_1():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wk_keg = sue_plan.get_keg_obj(wk_rope)
    mon_str = "Mon"
    mon_rope = sue_plan.make_rope(wk_rope, mon_str)
    mon_keg = sue_plan.get_keg_obj(mon_rope)

    email_str = "email"
    email_keg = kegunit_shop(email_str, pledge=True)
    sue_plan.set_keg_obj(email_keg, parent_rope=casa_rope)

    root_rope = sue_plan.kegroot.get_keg_rope()
    x_kegroot = sue_plan.get_keg_obj(root_rope)
    assert x_kegroot.descendant_pledge_count is None
    assert x_kegroot.all_person_cred is None
    assert x_kegroot.all_person_debt is None
    assert casa_keg.descendant_pledge_count is None
    assert casa_keg.all_person_cred is None
    assert casa_keg.all_person_debt is None
    assert mon_keg.descendant_pledge_count is None
    assert mon_keg.all_person_cred is None
    assert mon_keg.all_person_debt is None

    # WHEN
    sue_plan.cashout()

    # THEN
    assert x_kegroot.descendant_pledge_count == 3
    assert casa_keg.descendant_pledge_count == 1
    assert casa_keg.kids[email_str].descendant_pledge_count == 0
    assert mon_keg.descendant_pledge_count == 0
    assert x_kegroot.all_person_cred is True
    assert x_kegroot.all_person_debt is True
    assert casa_keg.all_person_cred is True
    assert casa_keg.all_person_debt is True
    assert mon_keg.all_person_cred is True
    assert mon_keg.all_person_debt is True


def test_PlanUnit_cashout_NLevelSetsDescendantAttributes_2():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    email_str = "email"
    wk_str = "sem_jours"
    mon_str = "Mon"
    tue_str = "Tue"
    vacuum_str = "vacuum"

    casa_rope = sue_plan.make_l1_rope(exx.casa)
    email_keg = kegunit_shop(email_str, pledge=True)
    sue_plan.set_keg_obj(email_keg, parent_rope=casa_rope)
    vacuum_keg = kegunit_shop(vacuum_str, pledge=True)
    sue_plan.set_keg_obj(vacuum_keg, parent_rope=casa_rope)

    sue_plan.add_personunit(person_name=exx.sue)
    x_awardunit = awardunit_shop(awardee_title=exx.sue)

    sue_plan.kegroot.kids[exx.casa].kids[email_str].set_awardunit(awardunit=x_awardunit)
    # print(sue_plan.kids[exx.casa].kids[email_str])
    # print(sue_plan.kids[exx.casa].kids[email_str].awardunit)

    # WHEN
    sue_plan.cashout()
    # print(sue_plan.kids[exx.casa].kids[email_str])
    # print(sue_plan.kids[exx.casa].kids[email_str].awardunit)

    # THEN
    assert sue_plan.kegroot.all_person_cred is False
    assert sue_plan.kegroot.all_person_debt is False
    casa_keg = sue_plan.kegroot.kids[exx.casa]
    assert casa_keg.all_person_cred is False
    assert casa_keg.all_person_debt is False
    assert casa_keg.kids[email_str].all_person_cred is False
    assert casa_keg.kids[email_str].all_person_debt is False
    assert casa_keg.kids[vacuum_str].all_person_cred is True
    assert casa_keg.kids[vacuum_str].all_person_debt is True
    wk_keg = sue_plan.kegroot.kids[wk_str]
    assert wk_keg.all_person_cred is True
    assert wk_keg.all_person_debt is True
    assert wk_keg.kids[mon_str].all_person_cred is True
    assert wk_keg.kids[mon_str].all_person_debt is True
    assert wk_keg.kids[tue_str].all_person_cred is True
    assert wk_keg.kids[tue_str].all_person_debt is True


def test_PlanUnit_cashout_SetsKegUnitAttr_awardunits():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    sue_plan.add_personunit(exx.yao)
    sue_plan.add_personunit(exx.zia)
    sue_plan.add_personunit(exx.xio)

    assert len(sue_plan.persons) == 3
    assert len(sue_plan.get_personunit_group_titles_dict()) == 3
    sue_plan.set_l1_keg(kegunit_shop(exx.swim))
    awardunit_yao = awardunit_shop(exx.yao, give_force=10)
    awardunit_zia = awardunit_shop(exx.zia, give_force=10)
    awardunit_Xio = awardunit_shop(exx.xio, give_force=10)
    swim_rope = sue_plan.make_l1_rope(exx.swim)
    sue_plan.edit_keg_attr(swim_rope, awardunit=awardunit_yao)
    sue_plan.edit_keg_attr(swim_rope, awardunit=awardunit_zia)
    sue_plan.edit_keg_attr(swim_rope, awardunit=awardunit_Xio)

    street_str = "streets"
    sue_plan.set_keg_obj(kegunit_shop(street_str), parent_rope=swim_rope)
    assert sue_plan.kegroot.awardunits in (None, {})
    assert len(sue_plan.kegroot.kids[exx.swim].awardunits) == 3

    # WHEN
    sue_plan.cashout()

    # THEN
    print(f"{sue_plan._keg_dict.keys()=} ")
    swim_keg = sue_plan._keg_dict.get(swim_rope)
    street_keg = sue_plan._keg_dict.get(sue_plan.make_rope(swim_rope, street_str))

    assert len(swim_keg.awardunits) == 3
    assert len(swim_keg.awardheirs) == 3
    assert street_keg.awardunits in (None, {})
    assert len(street_keg.awardheirs) == 3

    print(f"{len(sue_plan._keg_dict)}")
    print(f"{swim_keg.awardunits}")
    print(f"{swim_keg.awardheirs}")
    print(f"{swim_keg.awardheirs}")
    assert len(sue_plan.kegroot.kids["swim"].awardheirs) == 3


def test_PlanUnit_cashout_TreeTraverseSetsClearsAwardLineestors():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    sue_plan.cashout()
    # keg tree has no awardunits
    assert sue_plan.kegroot.awardlines == {}
    sue_plan.kegroot.awardlines = {1: "testtest"}
    assert sue_plan.kegroot.awardlines != {}

    # WHEN
    sue_plan.cashout()

    # THEN
    assert not sue_plan.kegroot.awardlines

    # WHEN
    # test for level 1 and level n
    casa_keg = sue_plan.kegroot.kids[exx.casa]
    casa_keg.awardlines = {1: "testtest"}
    assert casa_keg.awardlines != {}
    sue_plan.cashout()

    # THEN
    assert not sue_plan.kegroot.kids[exx.casa].awardlines


def test_PlanUnit_cashout_DoesNotKeepNonRequired_awardheirs():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    yao_plan.add_personunit(exx.yao)
    yao_plan.add_personunit(exx.zia)
    yao_plan.add_personunit(exx.xio)

    swim_rope = yao_plan.make_l1_rope(exx.swim)

    yao_plan.set_l1_keg(kegunit_shop(exx.swim))
    awardunit_yao = awardunit_shop(exx.yao, give_force=10)
    awardunit_zia = awardunit_shop(exx.zia, give_force=10)
    awardunit_Xio = awardunit_shop(exx.xio, give_force=10)

    swim_keg = yao_plan.get_keg_obj(swim_rope)
    yao_plan.edit_keg_attr(swim_rope, awardunit=awardunit_yao)
    yao_plan.edit_keg_attr(swim_rope, awardunit=awardunit_zia)
    yao_plan.edit_keg_attr(swim_rope, awardunit=awardunit_Xio)

    assert len(swim_keg.awardunits) == 3
    assert len(swim_keg.awardheirs) == 0

    # WHEN
    yao_plan.cashout()

    # THEN
    assert len(swim_keg.awardunits) == 3
    assert len(swim_keg.awardheirs) == 3
    yao_plan.edit_keg_attr(swim_rope, awardunit_del=exx.yao)
    assert len(swim_keg.awardunits) == 2
    assert len(swim_keg.awardheirs) == 3

    # WHEN
    yao_plan.cashout()

    # THEN
    assert len(swim_keg.awardunits) == 2
    assert len(swim_keg.awardheirs) == 2


def test_PlanUnit_get_keg_tree_ordered_rope_list_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wk_str = "sem_jours"
    assert sue_plan.get_keg_tree_ordered_rope_list()

    # WHEN
    ordered_label_list = sue_plan.get_keg_tree_ordered_rope_list()

    # THEN
    assert len(ordered_label_list) == 17
    x_1st_rope_in_ordered_list = sue_plan.get_keg_tree_ordered_rope_list()[0]
    root_rope = sue_plan.kegroot.get_keg_rope()
    assert x_1st_rope_in_ordered_list == root_rope
    x_8th_rope_in_ordered_list = sue_plan.get_keg_tree_ordered_rope_list()[9]
    assert x_8th_rope_in_ordered_list == sue_plan.make_l1_rope(wk_str)


def test_PlanUnit_get_keg_tree_ordered_rope_list_ReturnsObj_Scenario1():
    # ESTABLISH
    y_plan = planunit_shop("Bob", exx.a23)
    root_rope = y_plan.kegroot.get_keg_rope()

    # WHEN
    y_1st_rope_in_ordered_list = y_plan.get_keg_tree_ordered_rope_list()[0]
    # THEN
    assert y_1st_rope_in_ordered_list == root_rope


def test_PlanUnit_get_keg_tree_ordered_rope_list_Scenario2_CleansRangedKegRopeTerms():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")

    # WHEN
    ziet_str = "zietline"
    ziet_rope = yao_plan.make_l1_rope(ziet_str)
    yao_plan.set_l1_keg(kegunit_shop(ziet_str, begin=0, close=700))
    wks_str = "wks"
    yao_plan.set_keg_obj(kegunit_shop(wks_str, denom=7), ziet_rope)

    # THEN
    assert len(yao_plan.get_keg_tree_ordered_rope_list()) == 3
    assert len(yao_plan.get_keg_tree_ordered_rope_list(no_range_descendants=True)) == 2


def test_PlanUnit_get_keg_dict_ReturnsObjWhenSingle():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    texas_str = "Texas"
    sue_plan.set_l1_keg(kegunit_shop(texas_str, problem_bool=True))
    sue_plan.set_l1_keg(kegunit_shop(exx.casa))

    # WHEN
    problems_dict = sue_plan.get_keg_dict(problem=True)

    # THEN
    assert sue_plan.keeps_justified
    texas_rope = sue_plan.make_l1_rope(texas_str)
    texas_keg = sue_plan.get_keg_obj(texas_rope)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_rope: texas_keg}


def test_PlanUnit_cashout_CreatesFullyPopulated_keg_dict():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()

    # WHEN
    sue_planunit.cashout()

    # THEN
    assert len(sue_planunit._keg_dict) == 17


def test_PlanUnit_cashout_Resets_offtrack_kids_star_set():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    sue_planunit.offtrack_kids_star_set = set("YY")
    x_set = set()

    assert sue_planunit.offtrack_kids_star_set != x_set

    # WHEN
    sue_planunit.cashout()

    # THEN
    assert sue_planunit.offtrack_kids_star_set == x_set


def test_PlanUnit_cashout_WhenKegRootHas_starButAll_kidsHaveZero_starAddTo_offtrack_kids_star_set_Scenario0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    casa_keg = kegunit_shop(exx.casa, star=0)
    sue_planunit.set_l1_keg(casa_keg)
    assert sue_planunit.offtrack_kids_star_set == set()

    # WHEN
    sue_planunit.cashout()

    # THEN
    root_rope = sue_planunit.kegroot.get_keg_rope()
    assert sue_planunit.offtrack_kids_star_set == {root_rope}

    # WHEN
    sue_planunit.edit_keg_attr(casa_rope, star=2)
    sue_planunit.cashout()

    # THEN
    assert sue_planunit.offtrack_kids_star_set == set()


def test_PlanUnit_cashout_WhenKegUnitHas_starButAll_kidsHaveZero_starAddTo_offtrack_kids_star_set():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    casa_keg = kegunit_shop(exx.casa, star=1)

    swim_rope = sue_planunit.make_rope(casa_rope, exx.swim)
    swim_keg = kegunit_shop(exx.swim, star=8)

    clean_str = "cleaning"
    clean_rope = sue_planunit.make_rope(casa_rope, clean_str)
    clean_keg = kegunit_shop(clean_str, star=2)
    sue_planunit.set_keg_obj(kegunit_shop(clean_str), casa_rope)

    sweep_str = "sweep"
    sweep_rope = sue_planunit.make_rope(clean_rope, sweep_str)
    sweep_keg = kegunit_shop(sweep_str, star=0)
    vacuum_str = "vacuum"
    vacuum_rope = sue_planunit.make_rope(clean_rope, vacuum_str)
    vacuum_keg = kegunit_shop(vacuum_str, star=0)

    sue_planunit.set_l1_keg(casa_keg)
    sue_planunit.set_keg_obj(swim_keg, casa_rope)
    sue_planunit.set_keg_obj(clean_keg, casa_rope)
    sue_planunit.set_keg_obj(sweep_keg, clean_rope)  # _star=0
    sue_planunit.set_keg_obj(vacuum_keg, clean_rope)  # _star=0

    assert sue_planunit.offtrack_kids_star_set == set()

    # WHEN
    sue_planunit.cashout()

    # THEN
    assert sue_planunit.offtrack_kids_star_set == {clean_rope}


def test_PlanUnit_cashout_CreatesNewGroupUnits_Scenario0():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    yao_person_cred_lumen = 3
    yao_person_debt_lumen = 2
    zia_person_cred_lumen = 4
    zia_person_debt_lumen = 5
    yao_plan.add_personunit(exx.yao, yao_person_cred_lumen, yao_person_debt_lumen)
    yao_plan.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    root_rope = yao_plan.kegroot.get_keg_rope()
    x_kegroot = yao_plan.get_keg_obj(root_rope)
    x_kegroot.set_awardunit(awardunit_shop(exx.yao))
    x_kegroot.set_awardunit(awardunit_shop(exx.zia))
    x_kegroot.set_awardunit(awardunit_shop(exx.xio))
    assert len(yao_plan.get_personunit_group_titles_dict()) == 2
    assert not yao_plan.groupunit_exists(exx.yao)
    assert not yao_plan.groupunit_exists(exx.zia)
    assert not yao_plan.groupunit_exists(exx.xio)

    # WHEN
    yao_plan.cashout()

    # THEN
    assert yao_plan.groupunit_exists(exx.yao)
    assert yao_plan.groupunit_exists(exx.zia)
    assert yao_plan.groupunit_exists(exx.xio)
    assert len(yao_plan.get_personunit_group_titles_dict()) == 2
    assert len(yao_plan.get_personunit_group_titles_dict()) != len(yao_plan.groupunits)
    assert len(yao_plan.groupunits) == 3
    xio_groupunit = yao_plan.get_groupunit(exx.xio)
    xio_symmerty_groupunit = yao_plan.create_symmetry_groupunit(exx.xio)
    assert xio_groupunit.memberships.keys() == xio_symmerty_groupunit.memberships.keys()
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert not xio_groupunit.group_membership_exists(exx.xio)
    yao_membership = xio_groupunit.get_person_membership(exx.yao)
    zia_membership = xio_groupunit.get_person_membership(exx.zia)
    assert yao_membership.group_cred_lumen == yao_person_cred_lumen
    assert zia_membership.group_cred_lumen == zia_person_cred_lumen
    assert yao_membership.group_debt_lumen == yao_person_debt_lumen
    assert zia_membership.group_debt_lumen == zia_person_debt_lumen


def test_PlanUnit_cashout_CreatesNewGroupUnits_Scenario1():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    swim_rope = yao_plan.make_l1_rope(exx.swim)
    yao_plan.set_l1_keg(kegunit_shop(exx.swim))
    yao_plan.add_personunit(exx.yao)
    yao_plan.add_personunit(exx.zia)
    swim_keg = yao_plan.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(awardunit_shop(exx.yao))
    swim_keg.set_awardunit(awardunit_shop(exx.zia))
    swim_keg.set_awardunit(awardunit_shop(exx.xio))
    assert len(yao_plan.get_personunit_group_titles_dict()) == 2
    assert not yao_plan.groupunit_exists(exx.yao)
    assert not yao_plan.groupunit_exists(exx.zia)
    assert not yao_plan.groupunit_exists(exx.xio)

    # WHEN
    yao_plan.cashout()

    # THEN
    assert yao_plan.groupunit_exists(exx.yao)
    assert yao_plan.groupunit_exists(exx.zia)
    assert yao_plan.groupunit_exists(exx.xio)
    assert len(yao_plan.get_personunit_group_titles_dict()) == 2
    assert len(yao_plan.get_personunit_group_titles_dict()) != len(yao_plan.groupunits)
    assert len(yao_plan.groupunits) == 3
    xio_groupunit = yao_plan.get_groupunit(exx.xio)
    xio_symmerty_groupunit = yao_plan.create_symmetry_groupunit(exx.xio)
    assert xio_groupunit.memberships.keys() == xio_symmerty_groupunit.memberships.keys()
    assert xio_groupunit.group_membership_exists(exx.yao)
    assert xio_groupunit.group_membership_exists(exx.zia)
    assert not xio_groupunit.group_membership_exists(exx.xio)


def test_PlanUnit_get_tree_traverse_generated_groupunits_ReturnsObj():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    swim_rope = yao_plan.make_l1_rope(exx.swim)
    yao_plan.set_l1_keg(kegunit_shop(exx.swim))
    yao_plan.add_personunit(exx.yao)
    yao_plan.add_personunit(exx.zia)
    swim_keg = yao_plan.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(awardunit_shop(exx.yao))
    swim_keg.set_awardunit(awardunit_shop(exx.zia))
    swim_keg.set_awardunit(awardunit_shop(exx.xio))
    yao_plan.cashout()
    assert yao_plan.groupunit_exists(exx.yao)
    assert yao_plan.groupunit_exists(exx.zia)
    assert yao_plan.groupunit_exists(exx.xio)
    assert len(yao_plan.get_personunit_group_titles_dict()) == 2
    assert len(yao_plan.get_personunit_group_titles_dict()) != len(yao_plan.groupunits)

    # WHEN
    symmerty_group_titles = yao_plan.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 1
    assert symmerty_group_titles == {exx.xio}

    # ESTABLISH
    swim_keg.set_awardunit(awardunit_shop(exx.run))
    assert not yao_plan.groupunit_exists(exx.run)
    yao_plan.cashout()
    assert yao_plan.groupunit_exists(exx.run)

    # WHEN
    symmerty_group_titles = yao_plan.get_tree_traverse_generated_groupunits()

    # THEN
    assert len(symmerty_group_titles) == 2
    assert symmerty_group_titles == {exx.xio, exx.run}


def test_PlanUnit_cashout_Sets_kegroot_factheir_With_range_factheirs():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    wk_rope = yao_plan.make_l1_rope(exx.wk)
    wk_addin = 10
    wk_keg = kegunit_shop(exx.wk, begin=10, close=15, addin=wk_addin)
    yao_plan.set_l1_keg(wk_keg)
    tue_str = "Tue"
    tue_rope = yao_plan.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_plan.set_keg_obj(kegunit_shop(tue_str, addin=tue_addin), wk_rope)
    root_rope = yao_plan.kegroot.get_keg_rope()
    yao_plan.edit_keg_attr(root_rope, reason_context=tue_rope, reason_case=tue_rope)

    wk_reason_lower = 3
    wk_reason_upper = 7
    yao_plan.add_fact(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # assert len(ball_keg.reasonheirs) == 1
    # assert ball_keg.factheirs == {wk_rope: wk_factheir}
    # assert ball_keg.factheirs.get(wk_rope)
    # assert len(ball_keg.factheirs) == 1
    # assert ball_keg.factheirs.get(tue_rope) is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_plan.cashout()

    # THEN
    exception_str = f"Cannot have fact for range inheritor '{tue_rope}'. A ranged fact keg must have _begin, _close"
    assert str(excinfo.value) == exception_str

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_plan_keg_dict = {wk_keg.get_keg_rope(): wk_keg, tue_keg.get_keg_rope(): tue_keg}
    # ball_keg.set_reasonheirs(x_plan_keg_dict, tue_reasonheirs)
    # x_range_inheritors = {tue_rope: wk_rope}
    # wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # tue_reason_lower = 113
    # tue_reason_upper = 117
    # tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    # root_keg = yao_plan.get_keg_obj(root_rope)
    # print(f"{wk_rope=} {root_keg.factheirs.keys()=}")
    # assert root_keg.factheirs.get(wk_rope) == wk_factheir
    # assert len(root_keg.factheirs) == 2
    # assert root_keg.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_PlanUnit_cashout_SetsKegUnit_factheir_With_range_factheirs():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    wk_rope = yao_plan.make_l1_rope(exx.wk)
    wk_addin = 10
    wk_keg = kegunit_shop(exx.wk, begin=10, close=15, addin=wk_addin)
    yao_plan.set_l1_keg(wk_keg)
    tue_str = "Tue"
    tue_rope = yao_plan.make_rope(wk_rope, tue_str)
    tue_addin = 100
    yao_plan.set_keg_obj(kegunit_shop(tue_str, addin=tue_addin), wk_rope)
    ball_str = "ball"
    ball_rope = yao_plan.make_l1_rope(ball_str)
    yao_plan.set_l1_keg(kegunit_shop(ball_str))
    yao_plan.edit_keg_attr(ball_rope, reason_context=tue_rope, reason_case=tue_rope)

    wk_reason_lower = 3
    wk_reason_upper = 7
    yao_plan.add_fact(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    # assert len(ball_keg.reasonheirs) == 1
    # assert ball_keg.factheirs == {wk_rope: wk_factheir}
    # assert ball_keg.factheirs.get(wk_rope)
    # assert len(ball_keg.factheirs) == 1
    # assert ball_keg.factheirs.get(tue_rope) is None

    # WHEN
    yao_plan.cashout()

    # THEN
    # wk_factunit = factunit_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    # tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    # x_plan_keg_dict = {wk_keg.get_keg_rope(): wk_keg, tue_keg.get_keg_rope(): tue_keg}
    # ball_keg.set_reasonheirs(x_plan_keg_dict, tue_reasonheirs)
    x_range_inheritors = {tue_rope: wk_rope}
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)

    tue_reason_lower = 113
    tue_reason_upper = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    ball_keg = yao_plan.get_keg_obj(ball_rope)
    print(f"{wk_rope=} {ball_keg.factheirs.keys()=}")
    assert ball_keg.factheirs.get(wk_rope) == wk_factheir
    assert len(ball_keg.factheirs) == 2
    assert ball_keg.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}
