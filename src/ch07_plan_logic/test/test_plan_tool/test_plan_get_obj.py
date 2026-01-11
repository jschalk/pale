from src.ch02_person.group import awardunit_shop
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_tool import (
    plan_get_obj,
    plan_keg_awardunit_get_obj,
    plan_keg_factunit_get_obj,
    plan_keg_reason_caseunit_get_obj as caseunit_get_obj,
    plan_keg_reasonunit_get_obj,
    plan_kegunit_get_obj,
    plan_person_membership_get_obj,
    plan_personunit_get_obj,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_plan_personunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao}
    sue_plan.add_personunit(exx.yao)

    # WHEN
    x_obj = plan_personunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_person(exx.yao)


def test_plan_person_membership_get_obj_ReturnsObj():
    # ESTABLISH
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao, "group_title": swim_str}
    sue_plan.add_personunit(exx.yao)
    sue_plan.get_person(exx.yao).add_membership(swim_str)

    # WHEN
    x_obj = plan_person_membership_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_person(exx.yao).get_membership(swim_str)


def test_plan_kegunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope}

    # WHEN
    x_obj = plan_kegunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope)


def test_plan_keg_awardunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    sue_plan.add_keg(casa_rope)
    sue_plan.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(exx.swim))

    # WHEN
    x_obj = plan_keg_awardunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope).get_awardunit(exx.swim)


def test_plan_keg_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    wk_rope = sue_plan.make_l1_rope("wk")
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(wk_rope)
    sue_plan.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = plan_keg_reasonunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope).get_reasonunit(wk_rope)


def test_plan_keg_reason_caseunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    thur_rope = sue_plan.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(wk_rope)
    sue_plan.add_keg(thur_rope)
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = caseunit_get_obj(sue_plan, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_keg.get_reasonunit(wk_rope).get_case(thur_rope)


def test_plan_keg_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    wk_rope = sue_plan.make_l1_rope("wk")
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(wk_rope)
    sue_plan.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = plan_keg_factunit_get_obj(sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope).factunits.get(wk_rope)


def test_plan_get_obj_ReturnsObj_PlanUnit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao}
    sue_plan.add_personunit(exx.yao)

    # WHEN
    x_obj = plan_get_obj(kw.planunit, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan


def test_plan_get_obj_ReturnsObj_plan_personunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao}
    sue_plan.add_personunit(exx.yao)

    # WHEN
    x_obj = plan_get_obj(kw.plan_personunit, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_person(exx.yao)


def test_plan_get_obj_ReturnsObj_plan_person_membership_get_obj():
    # ESTABLISH
    swim_str = ";swim"
    sue_plan = planunit_shop("Sue")
    jkeys = {kw.person_name: exx.yao, "group_title": swim_str}
    sue_plan.add_personunit(exx.yao)
    sue_plan.get_person(exx.yao).add_membership(swim_str)

    # WHEN
    x_obj = plan_get_obj(kw.plan_person_membership, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_person(exx.yao).get_membership(swim_str)


def test_plan_get_obj_ReturnsObj_plan_kegunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope}

    # WHEN
    x_obj = plan_get_obj(kw.plan_kegunit, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope)


def test_plan_get_obj_ReturnsObj_plan_keg_awardunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    sue_plan.add_keg(casa_rope)
    sue_plan.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(exx.swim))

    # WHEN
    x_obj = plan_get_obj(kw.plan_keg_awardunit, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope).get_awardunit(exx.swim)


def test_plan_get_obj_ReturnsObj_plan_keg_reasonunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    wk_rope = sue_plan.make_l1_rope("wk")
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(wk_rope)
    sue_plan.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = plan_get_obj(kw.plan_keg_reasonunit, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope).get_reasonunit(wk_rope)


def test_plan_get_obj_ReturnsObj_plan_keg_reason_caseunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    wk_rope = sue_plan.make_l1_rope(exx.wk)
    thur_rope = sue_plan.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(wk_rope)
    sue_plan.add_keg(thur_rope)
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = plan_get_obj(kw.plan_keg_reason_caseunit, sue_plan, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_keg.get_reasonunit(wk_rope).get_case(thur_rope)


def test_plan_get_obj_ReturnsObj_plan_keg_factunit_get_obj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    wk_rope = sue_plan.make_l1_rope("wk")
    sue_plan.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(wk_rope)
    sue_plan.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = plan_get_obj(kw.plan_keg_factunit, sue_plan, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_plan.get_keg_obj(casa_rope).factunits.get(wk_rope)
