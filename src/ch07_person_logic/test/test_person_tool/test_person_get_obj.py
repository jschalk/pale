from src.ch02_partner.group import awardunit_shop
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.person_tool import (
    person_get_obj,
    person_keg_awardunit_get_obj,
    person_keg_factunit_get_obj,
    person_keg_reason_caseunit_get_obj as caseunit_get_obj,
    person_keg_reasonunit_get_obj,
    person_kegunit_get_obj,
    person_partner_membership_get_obj,
    person_partnerunit_get_obj,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_person_partnerunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao}
    sue_person.add_partnerunit(exx.yao)

    # WHEN
    x_obj = person_partnerunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_partner(exx.yao)


def test_person_partner_membership_get_obj_ReturnsObj():
    # ESTABLISH
    swim_str = ";swim"
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao, "group_title": swim_str}
    sue_person.add_partnerunit(exx.yao)
    sue_person.get_partner(exx.yao).add_membership(swim_str)

    # WHEN
    x_obj = person_partner_membership_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_partner(exx.yao).get_membership(swim_str)


def test_person_kegunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope}

    # WHEN
    x_obj = person_kegunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope)


def test_person_keg_awardunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    sue_person.add_keg(casa_rope)
    sue_person.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(exx.swim))

    # WHEN
    x_obj = person_keg_awardunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope).get_awardunit(exx.swim)


def test_person_keg_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    sue_person.add_keg(casa_rope)
    sue_person.add_keg(wk_rope)
    sue_person.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = person_keg_reasonunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope).get_reasonunit(wk_rope)


def test_person_keg_reason_caseunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_person.add_keg(casa_rope)
    sue_person.add_keg(wk_rope)
    sue_person.add_keg(thur_rope)
    casa_keg = sue_person.get_keg_obj(casa_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = caseunit_get_obj(sue_person, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_keg.get_reasonunit(wk_rope).get_case(thur_rope)


def test_person_keg_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    sue_person.add_keg(casa_rope)
    sue_person.add_keg(wk_rope)
    sue_person.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = person_keg_factunit_get_obj(sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope).factunits.get(wk_rope)


def test_person_get_obj_ReturnsObj_PersonUnit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao}
    sue_person.add_partnerunit(exx.yao)

    # WHEN
    x_obj = person_get_obj(kw.personunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person


def test_person_get_obj_ReturnsObj_person_partnerunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao}
    sue_person.add_partnerunit(exx.yao)

    # WHEN
    x_obj = person_get_obj(kw.person_partnerunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_partner(exx.yao)


def test_person_get_obj_ReturnsObj_person_partner_membership_get_obj():
    # ESTABLISH
    swim_str = ";swim"
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao, "group_title": swim_str}
    sue_person.add_partnerunit(exx.yao)
    sue_person.get_partner(exx.yao).add_membership(swim_str)

    # WHEN
    x_obj = person_get_obj(kw.person_partner_membership, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_partner(exx.yao).get_membership(swim_str)


def test_person_get_obj_ReturnsObj_person_kegunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope}

    # WHEN
    x_obj = person_get_obj(kw.person_kegunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope)


def test_person_get_obj_ReturnsObj_person_keg_awardunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    sue_person.add_keg(casa_rope)
    sue_person.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(exx.swim))

    # WHEN
    x_obj = person_get_obj(kw.person_keg_awardunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope).get_awardunit(exx.swim)


def test_person_get_obj_ReturnsObj_person_keg_reasonunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    sue_person.add_keg(casa_rope)
    sue_person.add_keg(wk_rope)
    sue_person.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = person_get_obj(kw.person_keg_reasonunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope).get_reasonunit(wk_rope)


def test_person_get_obj_ReturnsObj_person_keg_reason_caseunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_person.add_keg(casa_rope)
    sue_person.add_keg(wk_rope)
    sue_person.add_keg(thur_rope)
    casa_keg = sue_person.get_keg_obj(casa_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = person_get_obj(kw.person_keg_reason_caseunit, sue_person, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_keg.get_reasonunit(wk_rope).get_case(thur_rope)


def test_person_get_obj_ReturnsObj_person_keg_factunit_get_obj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    wk_rope = sue_person.make_l1_rope("wk")
    sue_person.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    sue_person.add_keg(casa_rope)
    sue_person.add_keg(wk_rope)
    sue_person.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = person_get_obj(kw.person_keg_factunit, sue_person, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_person.get_keg_obj(casa_rope).factunits.get(wk_rope)
