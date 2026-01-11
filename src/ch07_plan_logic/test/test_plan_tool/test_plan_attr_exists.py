from src.ch02_person.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_tool import (
    plan_attr_exists,
    plan_keg_awardunit_exists,
    plan_keg_factunit_exists,
    plan_keg_healerunit_exists,
    plan_keg_partyunit_exists,
    plan_keg_reason_caseunit_exists as caseunit_exists,
    plan_keg_reasonunit_exists,
    plan_kegunit_exists,
    plan_person_membership_exists,
    plan_personunit_exists,
    planunit_exists,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_planunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not planunit_exists(None)
    assert planunit_exists(planunit_shop("Sue"))


def test_plan_personunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao}

    # WHEN / THEN
    assert not plan_personunit_exists(None, {})
    assert not plan_personunit_exists(sue_plan, jkeys)

    # WHEN
    sue_plan.add_personunit(exx.yao)

    # THEN
    assert plan_personunit_exists(sue_plan, jkeys)


def test_plan_person_membership_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao, kw.group_title: swim_str}

    # WHEN / THEN
    assert not plan_person_membership_exists(None, {})
    assert not plan_person_membership_exists(sue_plan, jkeys)

    # WHEN
    sue_plan.add_personunit(exx.yao)
    # THEN
    assert not plan_person_membership_exists(sue_plan, jkeys)

    # WHEN
    yao_keg = sue_plan.get_person(exx.yao)
    yao_keg.add_membership(";run")
    # THEN
    assert not plan_person_membership_exists(sue_plan, jkeys)

    # WHEN
    yao_keg = sue_plan.get_person(exx.yao)
    yao_keg.add_membership(swim_str)
    # THEN
    assert plan_person_membership_exists(sue_plan, jkeys)


def test_plan_kegunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_plan.make_rope(clean_rope, "sweep")
    root_rope = sue_plan.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope}
    casa_jkeys = {kw.keg_rope: casa_rope}
    clean_jkeys = {kw.keg_rope: clean_rope}
    sweep_jkeys = {kw.keg_rope: sweep_rope}

    # WHEN / THEN
    assert not plan_kegunit_exists(None, {})
    assert not plan_kegunit_exists(sue_plan, {})
    assert plan_kegunit_exists(sue_plan, root_jkeys)
    assert not plan_kegunit_exists(sue_plan, casa_jkeys)
    assert not plan_kegunit_exists(sue_plan, clean_jkeys)
    assert not plan_kegunit_exists(sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_keg(casa_rope)
    # THEN
    assert not plan_kegunit_exists(sue_plan, {})
    assert plan_kegunit_exists(sue_plan, root_jkeys)
    assert plan_kegunit_exists(sue_plan, casa_jkeys)
    assert not plan_kegunit_exists(sue_plan, clean_jkeys)
    assert not plan_kegunit_exists(sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_keg(clean_rope)
    # THEN
    assert not plan_kegunit_exists(sue_plan, {})
    assert plan_kegunit_exists(sue_plan, root_jkeys)
    assert plan_kegunit_exists(sue_plan, casa_jkeys)
    assert plan_kegunit_exists(sue_plan, clean_jkeys)
    assert not plan_kegunit_exists(sue_plan, sweep_jkeys)


def test_plan_keg_awardunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    root_rope = sue_plan.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.awardee_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.awardee_title: exx.swim}

    # WHEN / THEN
    assert not plan_keg_awardunit_exists(None, {})
    assert not plan_keg_awardunit_exists(sue_plan, {})
    assert not plan_keg_awardunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_awardunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_awardunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.kegroot.set_awardunit(awardunit_shop(exx.swim))

    # THEN
    assert not plan_keg_awardunit_exists(sue_plan, {})
    assert plan_keg_awardunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_awardunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_awardunit_exists(sue_plan, clean_jkeys)


def test_plan_keg_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    root_jkeys = {kw.keg_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not plan_keg_reasonunit_exists(None, {})
    assert not plan_keg_reasonunit_exists(sue_plan, {})
    assert not plan_keg_reasonunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_reasonunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_reasonunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(wk_rope)
    sue_plan.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not plan_keg_reasonunit_exists(sue_plan, {})
    assert plan_keg_reasonunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_reasonunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_reasonunit_exists(sue_plan, clean_jkeys)


def test_plan_keg_reason_caseunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    thur_rope = sue_plan.make_rope(wk_rope, "thur")
    root_jkeys = {
        kw.keg_rope: root_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    clean_jkeys = {
        kw.keg_rope: clean_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }

    # WHEN / THEN
    assert not caseunit_exists(None, {})
    assert not caseunit_exists(sue_plan, {})
    assert not caseunit_exists(sue_plan, root_jkeys)
    assert not caseunit_exists(sue_plan, casa_jkeys)
    assert not caseunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(wk_rope)
    sue_plan.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not caseunit_exists(sue_plan, {})
    assert not caseunit_exists(sue_plan, root_jkeys)
    assert not caseunit_exists(sue_plan, casa_jkeys)
    assert not caseunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(thur_rope)
    sue_plan.kegroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not caseunit_exists(sue_plan, {})
    assert caseunit_exists(sue_plan, root_jkeys)
    assert not caseunit_exists(sue_plan, casa_jkeys)
    assert not caseunit_exists(sue_plan, clean_jkeys)


def test_plan_keg_partyunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.party_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.party_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.party_title: exx.swim}

    # WHEN / THEN
    assert not plan_keg_partyunit_exists(None, {})
    assert not plan_keg_partyunit_exists(sue_plan, {})
    assert not plan_keg_partyunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_partyunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_partyunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.kegroot.laborunit.add_party(exx.swim)

    # THEN
    assert not plan_keg_partyunit_exists(sue_plan, {})
    assert plan_keg_partyunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_partyunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_partyunit_exists(sue_plan, clean_jkeys)


def test_plan_keg_healerunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.healer_name: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.healer_name: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.healer_name: exx.swim}

    # WHEN / THEN
    assert not plan_keg_healerunit_exists(None, {})
    assert not plan_keg_healerunit_exists(sue_plan, {})
    assert not plan_keg_healerunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_healerunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_healerunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.kegroot.healerunit.set_healer_name(exx.swim)

    # THEN
    assert not plan_keg_healerunit_exists(sue_plan, {})
    assert plan_keg_healerunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_healerunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_healerunit_exists(sue_plan, clean_jkeys)


def test_plan_keg_factunit_exists_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    root_jkeys = {kw.keg_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not plan_keg_factunit_exists(None, {})
    assert not plan_keg_factunit_exists(sue_plan, {})
    assert not plan_keg_factunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_factunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_factunit_exists(sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(wk_rope)
    sue_plan.kegroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not plan_keg_factunit_exists(sue_plan, {})
    assert plan_keg_factunit_exists(sue_plan, root_jkeys)
    assert not plan_keg_factunit_exists(sue_plan, casa_jkeys)
    assert not plan_keg_factunit_exists(sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_planunit():
    # ESTABLISH / WHEN / THEN
    assert not plan_attr_exists(kw.planunit, None, {})
    assert plan_attr_exists(kw.planunit, planunit_shop("Sue"), {})


def test_plan_attr_exists_ReturnsObj_plan_personunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    x_jkeys = {kw.person_name: exx.yao}

    # WHEN / THEN
    assert not plan_attr_exists(kw.plan_personunit, None, {})
    assert not plan_attr_exists(kw.plan_personunit, sue_plan, x_jkeys)

    # WHEN
    sue_plan.add_personunit(exx.yao)

    # THEN
    assert plan_attr_exists(kw.plan_personunit, sue_plan, x_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_person_membership():
    # ESTABLISH
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    x_jkeys = {kw.person_name: exx.yao, kw.group_title: swim_str}
    x_dimen = kw.plan_person_membership

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, x_jkeys)

    # WHEN
    sue_plan.add_personunit(exx.yao)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, x_jkeys)

    # WHEN
    yao_keg = sue_plan.get_person(exx.yao)
    yao_keg.add_membership(";run")
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, x_jkeys)

    # WHEN
    yao_keg = sue_plan.get_person(exx.yao)
    yao_keg.add_membership(swim_str)
    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, x_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_kegunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_plan.make_rope(clean_rope, "sweep")
    x_parent_rope = sue_plan.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: x_parent_rope}
    casa_jkeys = {kw.keg_rope: casa_rope}
    clean_jkeys = {kw.keg_rope: clean_rope}
    sweep_jkeys = {kw.keg_rope: sweep_rope}
    x_dimen = kw.plan_kegunit

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_keg(casa_rope)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)

    # WHEN
    sue_plan.add_keg(clean_rope)
    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, sweep_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_keg_awardunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    x_dimen = kw.plan_keg_awardunit
    root_jkeys = {kw.keg_rope: root_rope, kw.awardee_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.awardee_title: exx.swim}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.kegroot.set_awardunit(awardunit_shop(exx.swim))

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_keg_reasonunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    x_dimen = kw.plan_keg_reasonunit
    root_jkeys = {kw.keg_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(wk_rope)
    sue_plan.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_keg_reason_caseunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    thur_rope = sue_plan.make_rope(wk_rope, "thur")
    x_dimen = kw.plan_keg_reason_caseunit
    root_jkeys = {
        kw.keg_rope: root_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    clean_jkeys = {
        kw.keg_rope: clean_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(wk_rope)
    sue_plan.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(thur_rope)
    sue_plan.kegroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_keg_partyunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    x_dimen = kw.plan_keg_partyunit
    root_jkeys = {kw.keg_rope: root_rope, kw.party_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.party_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.party_title: exx.swim}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.kegroot.laborunit.add_party(exx.swim)

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_keg_healerunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    x_dimen = kw.plan_keg_healerunit
    root_jkeys = {kw.keg_rope: root_rope, kw.healer_name: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.healer_name: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.healer_name: exx.swim}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.kegroot.healerunit.set_healer_name(exx.swim)

    # THEN
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)


def test_plan_attr_exists_ReturnsObj_plan_keg_factunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    root_rope = sue_plan.kegroot.get_keg_rope()
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    x_dimen = kw.plan_keg_factunit
    root_jkeys = {kw.keg_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not plan_attr_exists(x_dimen, None, {})
    assert not plan_attr_exists(x_dimen, sue_plan, {})
    assert not plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)

    # WHEN
    sue_plan.add_keg(wk_rope)
    sue_plan.kegroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert plan_attr_exists(x_dimen, sue_plan, root_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, casa_jkeys)
    assert not plan_attr_exists(x_dimen, sue_plan, clean_jkeys)
