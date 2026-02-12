from src.ch02_partner.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.person_tool import (
    person_attr_exists,
    person_keg_awardunit_exists,
    person_keg_factunit_exists,
    person_keg_healerunit_exists,
    person_keg_partyunit_exists,
    person_keg_reason_caseunit_exists as caseunit_exists,
    person_keg_reasonunit_exists,
    person_kegunit_exists,
    person_partner_membership_exists,
    person_partnerunit_exists,
    personunit_exists,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_personunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not personunit_exists(None)
    assert personunit_exists(personunit_shop("Sue"))


def test_person_partnerunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao}

    # WHEN / THEN
    assert not person_partnerunit_exists(None, {})
    assert not person_partnerunit_exists(sue_person, jkeys)

    # WHEN
    sue_person.add_partnerunit(exx.yao)

    # THEN
    assert person_partnerunit_exists(sue_person, jkeys)


def test_person_partner_membership_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    swim_str = ";swim"
    sue_person = personunit_shop("Sue")
    jkeys = {kw.partner_name: exx.yao, kw.group_title: swim_str}

    # WHEN / THEN
    assert not person_partner_membership_exists(None, {})
    assert not person_partner_membership_exists(sue_person, jkeys)

    # WHEN
    sue_person.add_partnerunit(exx.yao)
    # THEN
    assert not person_partner_membership_exists(sue_person, jkeys)

    # WHEN
    yao_keg = sue_person.get_partner(exx.yao)
    yao_keg.add_membership(";run")
    # THEN
    assert not person_partner_membership_exists(sue_person, jkeys)

    # WHEN
    yao_keg = sue_person.get_partner(exx.yao)
    yao_keg.add_membership(swim_str)
    # THEN
    assert person_partner_membership_exists(sue_person, jkeys)


def test_person_kegunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    root_rope = sue_person.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope}
    casa_jkeys = {kw.keg_rope: casa_rope}
    clean_jkeys = {kw.keg_rope: clean_rope}
    sweep_jkeys = {kw.keg_rope: sweep_rope}

    # WHEN / THEN
    assert not person_kegunit_exists(None, {})
    assert not person_kegunit_exists(sue_person, {})
    assert person_kegunit_exists(sue_person, root_jkeys)
    assert not person_kegunit_exists(sue_person, casa_jkeys)
    assert not person_kegunit_exists(sue_person, clean_jkeys)
    assert not person_kegunit_exists(sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_keg(casa_rope)
    # THEN
    assert not person_kegunit_exists(sue_person, {})
    assert person_kegunit_exists(sue_person, root_jkeys)
    assert person_kegunit_exists(sue_person, casa_jkeys)
    assert not person_kegunit_exists(sue_person, clean_jkeys)
    assert not person_kegunit_exists(sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_keg(clean_rope)
    # THEN
    assert not person_kegunit_exists(sue_person, {})
    assert person_kegunit_exists(sue_person, root_jkeys)
    assert person_kegunit_exists(sue_person, casa_jkeys)
    assert person_kegunit_exists(sue_person, clean_jkeys)
    assert not person_kegunit_exists(sue_person, sweep_jkeys)


def test_person_keg_awardunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    root_rope = sue_person.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.awardee_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.awardee_title: exx.swim}

    # WHEN / THEN
    assert not person_keg_awardunit_exists(None, {})
    assert not person_keg_awardunit_exists(sue_person, {})
    assert not person_keg_awardunit_exists(sue_person, root_jkeys)
    assert not person_keg_awardunit_exists(sue_person, casa_jkeys)
    assert not person_keg_awardunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.kegroot.set_awardunit(awardunit_shop(exx.swim))

    # THEN
    assert not person_keg_awardunit_exists(sue_person, {})
    assert person_keg_awardunit_exists(sue_person, root_jkeys)
    assert not person_keg_awardunit_exists(sue_person, casa_jkeys)
    assert not person_keg_awardunit_exists(sue_person, clean_jkeys)


def test_person_keg_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    root_jkeys = {kw.keg_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not person_keg_reasonunit_exists(None, {})
    assert not person_keg_reasonunit_exists(sue_person, {})
    assert not person_keg_reasonunit_exists(sue_person, root_jkeys)
    assert not person_keg_reasonunit_exists(sue_person, casa_jkeys)
    assert not person_keg_reasonunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(wk_rope)
    sue_person.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not person_keg_reasonunit_exists(sue_person, {})
    assert person_keg_reasonunit_exists(sue_person, root_jkeys)
    assert not person_keg_reasonunit_exists(sue_person, casa_jkeys)
    assert not person_keg_reasonunit_exists(sue_person, clean_jkeys)


def test_person_keg_reason_caseunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
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
    assert not caseunit_exists(sue_person, {})
    assert not caseunit_exists(sue_person, root_jkeys)
    assert not caseunit_exists(sue_person, casa_jkeys)
    assert not caseunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(wk_rope)
    sue_person.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not caseunit_exists(sue_person, {})
    assert not caseunit_exists(sue_person, root_jkeys)
    assert not caseunit_exists(sue_person, casa_jkeys)
    assert not caseunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(thur_rope)
    sue_person.kegroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not caseunit_exists(sue_person, {})
    assert caseunit_exists(sue_person, root_jkeys)
    assert not caseunit_exists(sue_person, casa_jkeys)
    assert not caseunit_exists(sue_person, clean_jkeys)


def test_person_keg_partyunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.party_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.party_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.party_title: exx.swim}

    # WHEN / THEN
    assert not person_keg_partyunit_exists(None, {})
    assert not person_keg_partyunit_exists(sue_person, {})
    assert not person_keg_partyunit_exists(sue_person, root_jkeys)
    assert not person_keg_partyunit_exists(sue_person, casa_jkeys)
    assert not person_keg_partyunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.kegroot.laborunit.add_party(exx.swim)

    # THEN
    assert not person_keg_partyunit_exists(sue_person, {})
    assert person_keg_partyunit_exists(sue_person, root_jkeys)
    assert not person_keg_partyunit_exists(sue_person, casa_jkeys)
    assert not person_keg_partyunit_exists(sue_person, clean_jkeys)


def test_person_keg_healerunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.healer_name: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.healer_name: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.healer_name: exx.swim}

    # WHEN / THEN
    assert not person_keg_healerunit_exists(None, {})
    assert not person_keg_healerunit_exists(sue_person, {})
    assert not person_keg_healerunit_exists(sue_person, root_jkeys)
    assert not person_keg_healerunit_exists(sue_person, casa_jkeys)
    assert not person_keg_healerunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.kegroot.healerunit.set_healer_name(exx.swim)

    # THEN
    assert not person_keg_healerunit_exists(sue_person, {})
    assert person_keg_healerunit_exists(sue_person, root_jkeys)
    assert not person_keg_healerunit_exists(sue_person, casa_jkeys)
    assert not person_keg_healerunit_exists(sue_person, clean_jkeys)


def test_person_keg_factunit_exists_ReturnsObj():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    root_jkeys = {kw.keg_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not person_keg_factunit_exists(None, {})
    assert not person_keg_factunit_exists(sue_person, {})
    assert not person_keg_factunit_exists(sue_person, root_jkeys)
    assert not person_keg_factunit_exists(sue_person, casa_jkeys)
    assert not person_keg_factunit_exists(sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(wk_rope)
    sue_person.kegroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not person_keg_factunit_exists(sue_person, {})
    assert person_keg_factunit_exists(sue_person, root_jkeys)
    assert not person_keg_factunit_exists(sue_person, casa_jkeys)
    assert not person_keg_factunit_exists(sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_personunit():
    # ESTABLISH / WHEN / THEN
    assert not person_attr_exists(kw.personunit, None, {})
    assert person_attr_exists(kw.personunit, personunit_shop("Sue"), {})


def test_person_attr_exists_ReturnsObj_person_partnerunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    x_jkeys = {kw.partner_name: exx.yao}

    # WHEN / THEN
    assert not person_attr_exists(kw.person_partnerunit, None, {})
    assert not person_attr_exists(kw.person_partnerunit, sue_person, x_jkeys)

    # WHEN
    sue_person.add_partnerunit(exx.yao)

    # THEN
    assert person_attr_exists(kw.person_partnerunit, sue_person, x_jkeys)


def test_person_attr_exists_ReturnsObj_person_partner_membership():
    # ESTABLISH
    swim_str = ";swim"
    sue_person = personunit_shop("Sue")
    x_jkeys = {kw.partner_name: exx.yao, kw.group_title: swim_str}
    x_dimen = kw.person_partner_membership

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, x_jkeys)

    # WHEN
    sue_person.add_partnerunit(exx.yao)
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, x_jkeys)

    # WHEN
    yao_keg = sue_person.get_partner(exx.yao)
    yao_keg.add_membership(";run")
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, x_jkeys)

    # WHEN
    yao_keg = sue_person.get_partner(exx.yao)
    yao_keg.add_membership(swim_str)
    # THEN
    assert person_attr_exists(x_dimen, sue_person, x_jkeys)


def test_person_attr_exists_ReturnsObj_person_kegunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    x_parent_rope = sue_person.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: x_parent_rope}
    casa_jkeys = {kw.keg_rope: casa_rope}
    clean_jkeys = {kw.keg_rope: clean_rope}
    sweep_jkeys = {kw.keg_rope: sweep_rope}
    x_dimen = kw.person_kegunit

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_keg(casa_rope)
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, sweep_jkeys)

    # WHEN
    sue_person.add_keg(clean_rope)
    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert person_attr_exists(x_dimen, sue_person, clean_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, sweep_jkeys)


def test_person_attr_exists_ReturnsObj_person_keg_awardunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    x_dimen = kw.person_keg_awardunit
    root_jkeys = {kw.keg_rope: root_rope, kw.awardee_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.awardee_title: exx.swim}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.kegroot.set_awardunit(awardunit_shop(exx.swim))

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_keg_reasonunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    x_dimen = kw.person_keg_reasonunit
    root_jkeys = {kw.keg_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(wk_rope)
    sue_person.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_keg_reason_caseunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    thur_rope = sue_person.make_rope(wk_rope, "thur")
    x_dimen = kw.person_keg_reason_caseunit
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
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(wk_rope)
    sue_person.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(thur_rope)
    sue_person.kegroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_keg_partyunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    x_dimen = kw.person_keg_partyunit
    root_jkeys = {kw.keg_rope: root_rope, kw.party_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.party_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.party_title: exx.swim}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.kegroot.laborunit.add_party(exx.swim)

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_keg_healerunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    x_dimen = kw.person_keg_healerunit
    root_jkeys = {kw.keg_rope: root_rope, kw.healer_name: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.healer_name: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.healer_name: exx.swim}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.kegroot.healerunit.set_healer_name(exx.swim)

    # THEN
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)


def test_person_attr_exists_ReturnsObj_person_keg_factunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    clean_rope = sue_person.make_rope(casa_rope, exx.clean)
    root_rope = sue_person.kegroot.get_keg_rope()
    wk_rope = sue_person.make_l1_rope(exx.wk)
    x_dimen = kw.person_keg_factunit
    root_jkeys = {kw.keg_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not person_attr_exists(x_dimen, None, {})
    assert not person_attr_exists(x_dimen, sue_person, {})
    assert not person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)

    # WHEN
    sue_person.add_keg(wk_rope)
    sue_person.kegroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert person_attr_exists(x_dimen, sue_person, root_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, casa_jkeys)
    assert not person_attr_exists(x_dimen, sue_person, clean_jkeys)
