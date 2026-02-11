from pytest import raises as pytest_raises
from src.ch03_labor.labor import laborunit_shop, partyunit_shop
from src.ch04_rope.rope import default_knot_if_None
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import (
    get_dict_of_plan_from_dict,
    get_planunit_from_dict,
    planunit_shop,
)
from src.ch07_plan_logic.test._util.ch07_examples import (
    get_planunit_laundry_example1,
    get_planunit_reason_context_ziet_example,
    get_planunit_x1_3levels_1reason_1facts,
    planunit_v001,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PlanUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_plan = get_planunit_laundry_example1()
    yao_fund_pool = 23000
    yao_plan.fund_pool = yao_fund_pool
    yao_fund_grain = 23
    yao_plan.fund_grain = yao_fund_grain
    x_last_lesson_id = 77
    yao_plan.set_last_lesson_id(x_last_lesson_id)

    # WHEN
    plan_dict = yao_plan.to_dict()

    # THEN
    assert plan_dict is not None
    assert str(type(plan_dict)) == "<class 'dict'>"
    assert plan_dict[kw.plan_name] == yao_plan.plan_name
    assert plan_dict[kw.fund_pool] == yao_fund_pool
    assert plan_dict[kw.fund_grain] == yao_fund_grain
    assert plan_dict[kw.max_tree_traverse] == yao_plan.max_tree_traverse
    assert plan_dict[kw.knot] == yao_plan.knot
    assert plan_dict[kw.credor_respect] == yao_plan.credor_respect
    assert plan_dict[kw.debtor_respect] == yao_plan.debtor_respect
    assert plan_dict[kw.last_lesson_id] == yao_plan.last_lesson_id
    assert len(plan_dict[kw.persons]) == len(yao_plan.persons)
    assert len(plan_dict[kw.persons]) != 12

    x_kegroot = yao_plan.kegroot
    kegroot_dict = plan_dict[kw.kegroot]
    assert kegroot_dict[kw.keg_label] == x_kegroot.keg_label
    assert kegroot_dict[kw.star] == x_kegroot.star
    assert len(kegroot_dict[kw.kids]) == len(x_kegroot.kids)


def test_PlanUnit_to_dict_ReturnsObj_Scenario1_kegroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_plan = planunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.add_party(party_title=run_str)
    root_rope = sue_plan.kegroot.get_keg_rope()
    sue_plan.edit_keg_attr(root_rope, laborunit=x_laborunit)
    root_keg = sue_plan.get_keg_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_keg.gogo_want = x_gogo_want
    root_keg.stop_want = x_stop_want

    # WHEN
    plan_dict = sue_plan.to_dict()
    kegroot_dict = plan_dict.get(kw.kegroot)

    # THEN
    assert kegroot_dict[kw.laborunit] == x_laborunit.to_dict()
    run_partyunit = partyunit_shop(run_str)
    assert kegroot_dict[kw.laborunit] == {"partys": {run_str: run_partyunit.to_dict()}}
    assert kegroot_dict.get(kw.gogo_want) == x_gogo_want
    assert kegroot_dict.get(kw.stop_want) == x_stop_want


def test_PlanUnit_to_dict_ReturnsObj_Scenario2_With_kegroot_healerunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    yao_personunit = sue_plan.get_person(exx.yao)
    yao_personunit.add_membership(exx.run)
    run_healerunit = healerunit_shop()
    run_healerunit.set_healer_name(x_healer_name=exx.run)
    root_rope = sue_plan.kegroot.get_keg_rope()
    sue_plan.edit_keg_attr(root_rope, healerunit=run_healerunit)

    # WHEN
    plan_dict = sue_plan.to_dict()
    kegroot_dict = plan_dict.get(kw.kegroot)

    # THEN
    assert kegroot_dict[kw.healerunit] == run_healerunit.to_dict()


def test_PlanUnit_to_dict_ReturnsObj_Scenario3_kegkid_LaborUnit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    yao_personunit = sue_plan.get_person(exx.yao)
    yao_personunit.add_membership(exx.run)

    morn_str = "morning"
    morn_rope = sue_plan.make_l1_rope(morn_str)
    sue_plan.set_l1_keg(kegunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.add_party(party_title=exx.run)
    sue_plan.edit_keg_attr(morn_rope, laborunit=x_laborunit)

    # WHEN
    plan_dict = sue_plan.to_dict()
    kegroot_dict = plan_dict.get(kw.kegroot)

    # THEN
    labor_dict_x = kegroot_dict[kw.kids][morn_str][kw.laborunit]
    assert labor_dict_x == x_laborunit.to_dict()
    run_partyunit = partyunit_shop(exx.run)
    assert labor_dict_x == {"partys": {exx.run: run_partyunit.to_dict()}}


def test_PlanUnit_to_dict_ReturnsObj_Scenario4_kegunit_WithLevels():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_plan = get_planunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_plan.fund_pool = x_fund_pool
    x_fund_grain = 66
    zia_plan.fund_grain = x_fund_grain
    x_respect_grain = 7
    zia_plan.respect_grain = x_respect_grain
    x_mana_grain = 0.3
    zia_plan.mana_grain = x_mana_grain
    override_str = "override"
    zia_plan.add_personunit(exx.yao)
    yao_personunit = zia_plan.get_person(exx.yao)
    yao_personunit.add_membership(exx.run)
    run_healerunit = healerunit_shop({exx.run})
    root_rope = zia_plan.kegroot.get_keg_rope()
    zia_plan.edit_keg_attr(root_rope, healerunit=run_healerunit)
    zia_plan.edit_keg_attr(root_rope, problem_bool=True)

    # WHEN
    plan_dict = zia_plan.to_dict()

    # THEN
    assert plan_dict is not None
    assert plan_dict[kw.plan_name] == zia_plan.plan_name
    assert plan_dict[kw.fund_pool] == zia_plan.fund_pool
    assert plan_dict[kw.fund_grain] == zia_plan.fund_grain
    assert plan_dict[kw.respect_grain] == zia_plan.respect_grain
    assert plan_dict[kw.mana_grain] == zia_plan.mana_grain
    assert plan_dict[kw.credor_respect] == zia_plan.credor_respect
    assert plan_dict[kw.debtor_respect] == zia_plan.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     plan_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     plan_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        plan_dict[kw.last_lesson_id]

    x_kegroot = zia_plan.kegroot
    kegroot_dict = plan_dict.get(kw.kegroot)

    assert len(kegroot_dict[kw.kids]) == len(x_kegroot.kids)

    shave_str = "shave"
    shave_dict = kegroot_dict[kw.kids][shave_str]
    shave_factunits = shave_dict[kw.factunits]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_kegroot.kids[shave_str].factunits)
    kegroot_healerunit = kegroot_dict[kw.healerunit]
    print(f"{kegroot_healerunit=}")
    assert len(kegroot_healerunit) == 1
    assert x_kegroot.healerunit.any_healer_name_exists()
    assert x_kegroot.problem_bool


def test_PlanUnit_to_dict_ReturnsJSON_Scenario5_BigExample():
    # ESTABLISH
    yao_plan = planunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_plan.make_l1_rope(hr_number_str)
    yao_plan.add_fact(
        fact_context=hr_number_rope,
        fact_state=hr_number_rope,
        fact_lower=0,
        fact_upper=23,
    )
    jour_min_str = "jour_minute"
    jour_min_rope = yao_plan.make_l1_rope(jour_min_str)
    yao_plan.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=59,
    )
    x_factunit = factunit_shop(jour_min_rope, jour_min_rope, 5, 59)
    yao_plan.edit_keg_attr(x_factunit.fact_context, factunit=x_factunit)
    yao_plan.set_max_tree_traverse(2)

    # WHEN
    plan_dict = yao_plan.to_dict()

    # THEN
    assert plan_dict[kw.plan_name] == yao_plan.plan_name
    assert plan_dict[kw.max_tree_traverse] == 2
    assert plan_dict[kw.max_tree_traverse] == yao_plan.max_tree_traverse
    assert plan_dict[kw.knot] == yao_plan.knot

    x_kegroot = yao_plan.kegroot
    kegroot_dict = plan_dict.get(kw.kegroot)
    assert len(kegroot_dict[kw.kids]) == len(x_kegroot.kids)

    kids_dict = kegroot_dict[kw.kids]
    jour_min_dict = kids_dict[jour_min_str]
    jour_min_factunits_dict = jour_min_dict[kw.factunits]
    jour_min_keg_x = yao_plan.get_keg_obj(jour_min_rope)
    print(f"{jour_min_factunits_dict=}")
    assert len(jour_min_factunits_dict) == 1
    assert len(jour_min_factunits_dict) == len(jour_min_keg_x.factunits)

    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_plan.make_l1_rope(cont_str)
    ulti_rope = yao_plan.make_l1_rope(ulti_str)
    cont_keg = yao_plan.get_keg_obj(cont_rope)
    ulti_keg = yao_plan.get_keg_obj(ulti_rope)
    cont_reasonunits_dict = kegroot_dict[kw.kids][cont_str][kw.reasonunits]
    ulti_reasonunits_dict = kegroot_dict[kw.kids][ulti_str][kw.reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_keg.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_keg.reasonunits)

    anna_str = "Anna"
    anna_personunit = yao_plan.get_person(anna_str)
    assert anna_personunit.get_membership(";Family").group_cred_lumen == 6.2
    assert yao_plan.persons is not None
    assert len(yao_plan.persons) == 22


def test_get_planunit_from_dict_ReturnsKegRoot():
    # ESTABLISH
    zia_plan = get_planunit_x1_3levels_1reason_1facts()
    zia_plan.set_max_tree_traverse(23)
    root_keg = zia_plan.kegroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_keg.gogo_want = zia_gogo_want
    root_keg.stop_want = zia_stop_want

    # WHEN
    json_plan = get_planunit_from_dict(zia_plan.to_dict())

    # THEN
    json_kegroot = json_plan.get_keg_obj(zia_plan.kegroot.get_keg_rope())
    assert json_kegroot.gogo_want == zia_gogo_want
    assert json_kegroot.stop_want == zia_stop_want


def test_get_planunit_from_dict_ReturnsObj_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_plan = planunit_shop("Bob", knot=slash_knot)
    assert before_bob_plan.knot != default_knot_if_None()

    # WHEN
    after_bob_plan = get_planunit_from_dict(before_bob_plan.to_dict())

    # THEN
    assert after_bob_plan.knot != default_knot_if_None()
    assert after_bob_plan.knot == slash_knot
    assert after_bob_plan.knot == before_bob_plan.knot


def test_get_planunit_from_dict_ReturnsObj_knot_PersonExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_plan = planunit_shop("Bob", knot=slash_knot)
    bob_comma_str = ",Bob"
    before_bob_plan.add_personunit(bob_comma_str)
    assert before_bob_plan.person_exists(bob_comma_str)

    # WHEN
    after_bob_plan = get_planunit_from_dict(before_bob_plan.to_dict())

    # THEN
    after_bob_personunit = after_bob_plan.get_person(bob_comma_str)
    assert after_bob_personunit.groupmark == slash_knot


def test_get_planunit_from_dict_ReturnsObj_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_plan = planunit_shop("Bob", knot=slash_knot)
    swim_str = f"{slash_knot}Swimmers"
    before_bob_plan.add_personunit(exx.yao)
    yao_personunit = before_bob_plan.get_person(exx.yao)
    yao_personunit.add_membership(swim_str)

    # WHEN
    after_bob_plan = get_planunit_from_dict(before_bob_plan.to_dict())

    # THEN
    after_yao_personunit = after_bob_plan.get_person(exx.yao)
    assert after_yao_personunit.groupmark == slash_knot


def test_get_planunit_from_dict_ReturnsObj_Scenario7_kegroot_knot_IsApplied():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_plan = planunit_shop("Sue", knot=exx.slash)
    root_rope = sue_plan.kegroot.get_keg_rope()
    hr_number_str = "hr_number"
    hr_number_rope = sue_plan.make_l1_rope(hr_number_str)
    sue_plan.add_keg(hr_number_rope)
    assert sue_plan.knot == exx.slash
    assert sue_plan.get_keg_obj(root_rope).knot == exx.slash
    assert sue_plan.get_keg_obj(hr_number_rope).knot == exx.slash

    # WHEN
    after_bob_plan = get_planunit_from_dict(sue_plan.to_dict())

    # THEN
    assert after_bob_plan.knot == exx.slash
    assert after_bob_plan.get_keg_obj(root_rope).knot == exx.slash
    assert after_bob_plan.get_keg_obj(hr_number_rope).knot == exx.slash


def test_get_planunit_from_dict_ExportsPlanUnit_star():
    # ESTABLISH
    x1_plan = planunit_v001()
    assert x1_plan.kegroot.star == 1

    # WHEN
    x2_plan = get_planunit_from_dict(x1_plan.to_dict())

    # THEN
    assert x1_plan.kegroot.star == 1
    assert x1_plan.kegroot.star == x2_plan.kegroot.star
    assert x1_plan.kegroot.kids == x2_plan.kegroot.kids


def test_get_dict_of_plan_from_dict_ReturnsDictOfPlanUnits():
    # ESTABLISH
    x1_plan = planunit_v001()
    x2_plan = get_planunit_x1_3levels_1reason_1facts()
    x3_plan = get_planunit_reason_context_ziet_example()
    print(f"{x1_plan.plan_name}")
    print(f"{x2_plan.plan_name}")
    print(f"{x3_plan.plan_name}")

    cn_dict_of_dicts = {
        x1_plan.plan_name: x1_plan.to_dict(),
        x2_plan.plan_name: x2_plan.to_dict(),
        x3_plan.plan_name: x3_plan.to_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_plan_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_plan.plan_name) is not None
    assert ccn_dict_of_obj.get(x2_plan.plan_name) is not None
    assert ccn_dict_of_obj.get(x3_plan.plan_name) is not None

    ccn2_plan = ccn_dict_of_obj.get(x2_plan.plan_name)
    assert ccn2_plan.kegroot.keg_label == x2_plan.kegroot.keg_label
    assert ccn2_plan.kegroot.parent_rope == x2_plan.kegroot.parent_rope
    assert ccn2_plan.kegroot.fund_grain == x2_plan.kegroot.fund_grain
    shave_rope = ccn2_plan.make_l1_rope("shave")
    wk_rope = ccn2_plan.make_l1_rope("sem_jours")
    # assert ccn2_plan.get_keg_obj(shave_rope) == x2_plan.get_keg_obj(shave_rope)
    # assert ccn2_plan.get_keg_obj(wk_rope) == x2_plan.get_keg_obj(wk_rope)
    # assert ccn2_plan.kegroot == x2_plan.kegroot
    assert ccn2_plan.to_dict() == x2_plan.to_dict()

    ccn_plan3 = ccn_dict_of_obj.get(x3_plan.plan_name)
    assert ccn_plan3.to_dict() == x3_plan.to_dict()

    cc1_keg_root = ccn_dict_of_obj.get(x1_plan.plan_name).kegroot
    ccn_plan1 = ccn_dict_of_obj.get(x1_plan.plan_name)
    assert ccn_plan1._keg_dict == x1_plan._keg_dict
    philipa_str = "Philipa"
    ccn_philipa_personunit = ccn_plan1.get_person(philipa_str)
    x1_philipa_personunit = x1_plan.get_person(philipa_str)
    assert ccn_philipa_personunit.memberships == x1_philipa_personunit.memberships
    assert ccn_plan1 == x1_plan
    assert ccn_dict_of_obj.get(x1_plan.plan_name) == x1_plan
