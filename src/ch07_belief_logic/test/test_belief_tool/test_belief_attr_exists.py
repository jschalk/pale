from src.ch03_voice.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_attr_exists,
    belief_keg_awardunit_exists,
    belief_keg_factunit_exists,
    belief_keg_healerunit_exists,
    belief_keg_partyunit_exists,
    belief_keg_reason_caseunit_exists as caseunit_exists,
    belief_keg_reasonunit_exists,
    belief_kegunit_exists,
    belief_voice_membership_exists,
    belief_voiceunit_exists,
    beliefunit_exists,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_beliefunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not beliefunit_exists(None)
    assert beliefunit_exists(beliefunit_shop("Sue"))


def test_belief_voiceunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao}

    # WHEN / THEN
    assert not belief_voiceunit_exists(None, {})
    assert not belief_voiceunit_exists(sue_belief, jkeys)

    # WHEN
    sue_belief.add_voiceunit(exx.yao)

    # THEN
    assert belief_voiceunit_exists(sue_belief, jkeys)


def test_belief_voice_membership_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao, kw.group_title: swim_str}

    # WHEN / THEN
    assert not belief_voice_membership_exists(None, {})
    assert not belief_voice_membership_exists(sue_belief, jkeys)

    # WHEN
    sue_belief.add_voiceunit(exx.yao)
    # THEN
    assert not belief_voice_membership_exists(sue_belief, jkeys)

    # WHEN
    yao_keg = sue_belief.get_voice(exx.yao)
    yao_keg.add_membership(";run")
    # THEN
    assert not belief_voice_membership_exists(sue_belief, jkeys)

    # WHEN
    yao_keg = sue_belief.get_voice(exx.yao)
    yao_keg.add_membership(swim_str)
    # THEN
    assert belief_voice_membership_exists(sue_belief, jkeys)


def test_belief_kegunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    root_rope = sue_belief.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope}
    casa_jkeys = {kw.keg_rope: casa_rope}
    clean_jkeys = {kw.keg_rope: clean_rope}
    sweep_jkeys = {kw.keg_rope: sweep_rope}

    # WHEN / THEN
    assert not belief_kegunit_exists(None, {})
    assert not belief_kegunit_exists(sue_belief, {})
    assert belief_kegunit_exists(sue_belief, root_jkeys)
    assert not belief_kegunit_exists(sue_belief, casa_jkeys)
    assert not belief_kegunit_exists(sue_belief, clean_jkeys)
    assert not belief_kegunit_exists(sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_keg(casa_rope)
    # THEN
    assert not belief_kegunit_exists(sue_belief, {})
    assert belief_kegunit_exists(sue_belief, root_jkeys)
    assert belief_kegunit_exists(sue_belief, casa_jkeys)
    assert not belief_kegunit_exists(sue_belief, clean_jkeys)
    assert not belief_kegunit_exists(sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_keg(clean_rope)
    # THEN
    assert not belief_kegunit_exists(sue_belief, {})
    assert belief_kegunit_exists(sue_belief, root_jkeys)
    assert belief_kegunit_exists(sue_belief, casa_jkeys)
    assert belief_kegunit_exists(sue_belief, clean_jkeys)
    assert not belief_kegunit_exists(sue_belief, sweep_jkeys)


def test_belief_keg_awardunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    root_rope = sue_belief.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.awardee_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.awardee_title: exx.swim}

    # WHEN / THEN
    assert not belief_keg_awardunit_exists(None, {})
    assert not belief_keg_awardunit_exists(sue_belief, {})
    assert not belief_keg_awardunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_awardunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_awardunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.kegroot.set_awardunit(awardunit_shop(exx.swim))

    # THEN
    assert not belief_keg_awardunit_exists(sue_belief, {})
    assert belief_keg_awardunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_awardunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_awardunit_exists(sue_belief, clean_jkeys)


def test_belief_keg_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    root_jkeys = {kw.keg_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not belief_keg_reasonunit_exists(None, {})
    assert not belief_keg_reasonunit_exists(sue_belief, {})
    assert not belief_keg_reasonunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_reasonunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_reasonunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(wk_rope)
    sue_belief.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not belief_keg_reasonunit_exists(sue_belief, {})
    assert belief_keg_reasonunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_reasonunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_reasonunit_exists(sue_belief, clean_jkeys)


def test_belief_keg_reason_caseunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
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
    assert not caseunit_exists(sue_belief, {})
    assert not caseunit_exists(sue_belief, root_jkeys)
    assert not caseunit_exists(sue_belief, casa_jkeys)
    assert not caseunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(wk_rope)
    sue_belief.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not caseunit_exists(sue_belief, {})
    assert not caseunit_exists(sue_belief, root_jkeys)
    assert not caseunit_exists(sue_belief, casa_jkeys)
    assert not caseunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(thur_rope)
    sue_belief.kegroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not caseunit_exists(sue_belief, {})
    assert caseunit_exists(sue_belief, root_jkeys)
    assert not caseunit_exists(sue_belief, casa_jkeys)
    assert not caseunit_exists(sue_belief, clean_jkeys)


def test_belief_keg_partyunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.party_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.party_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.party_title: exx.swim}

    # WHEN / THEN
    assert not belief_keg_partyunit_exists(None, {})
    assert not belief_keg_partyunit_exists(sue_belief, {})
    assert not belief_keg_partyunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_partyunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_partyunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.kegroot.laborunit.add_party(exx.swim)

    # THEN
    assert not belief_keg_partyunit_exists(sue_belief, {})
    assert belief_keg_partyunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_partyunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_partyunit_exists(sue_belief, clean_jkeys)


def test_belief_keg_healerunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: root_rope, kw.healer_name: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.healer_name: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.healer_name: exx.swim}

    # WHEN / THEN
    assert not belief_keg_healerunit_exists(None, {})
    assert not belief_keg_healerunit_exists(sue_belief, {})
    assert not belief_keg_healerunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_healerunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_healerunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.kegroot.healerunit.set_healer_name(exx.swim)

    # THEN
    assert not belief_keg_healerunit_exists(sue_belief, {})
    assert belief_keg_healerunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_healerunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_healerunit_exists(sue_belief, clean_jkeys)


def test_belief_keg_factunit_exists_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    root_jkeys = {kw.keg_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not belief_keg_factunit_exists(None, {})
    assert not belief_keg_factunit_exists(sue_belief, {})
    assert not belief_keg_factunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_factunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_factunit_exists(sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(wk_rope)
    sue_belief.kegroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not belief_keg_factunit_exists(sue_belief, {})
    assert belief_keg_factunit_exists(sue_belief, root_jkeys)
    assert not belief_keg_factunit_exists(sue_belief, casa_jkeys)
    assert not belief_keg_factunit_exists(sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_beliefunit():
    # ESTABLISH / WHEN / THEN
    assert not belief_attr_exists(kw.beliefunit, None, {})
    assert belief_attr_exists(kw.beliefunit, beliefunit_shop("Sue"), {})


def test_belief_attr_exists_ReturnsObj_belief_voiceunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    x_jkeys = {kw.voice_name: exx.yao}

    # WHEN / THEN
    assert not belief_attr_exists(kw.belief_voiceunit, None, {})
    assert not belief_attr_exists(kw.belief_voiceunit, sue_belief, x_jkeys)

    # WHEN
    sue_belief.add_voiceunit(exx.yao)

    # THEN
    assert belief_attr_exists(kw.belief_voiceunit, sue_belief, x_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_voice_membership():
    # ESTABLISH
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    x_jkeys = {kw.voice_name: exx.yao, kw.group_title: swim_str}
    x_dimen = kw.belief_voice_membership

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, x_jkeys)

    # WHEN
    sue_belief.add_voiceunit(exx.yao)
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, x_jkeys)

    # WHEN
    yao_keg = sue_belief.get_voice(exx.yao)
    yao_keg.add_membership(";run")
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, x_jkeys)

    # WHEN
    yao_keg = sue_belief.get_voice(exx.yao)
    yao_keg.add_membership(swim_str)
    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, x_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_kegunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    x_parent_rope = sue_belief.kegroot.get_keg_rope()
    root_jkeys = {kw.keg_rope: x_parent_rope}
    casa_jkeys = {kw.keg_rope: casa_rope}
    clean_jkeys = {kw.keg_rope: clean_rope}
    sweep_jkeys = {kw.keg_rope: sweep_rope}
    x_dimen = kw.belief_kegunit

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_keg(casa_rope)
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, sweep_jkeys)

    # WHEN
    sue_belief.add_keg(clean_rope)
    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, sweep_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_keg_awardunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    x_dimen = kw.belief_keg_awardunit
    root_jkeys = {kw.keg_rope: root_rope, kw.awardee_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.awardee_title: exx.swim}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.kegroot.set_awardunit(awardunit_shop(exx.swim))

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_keg_reasonunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    x_dimen = kw.belief_keg_reasonunit
    root_jkeys = {kw.keg_rope: root_rope, kw.reason_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.reason_context: wk_rope}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(wk_rope)
    sue_belief.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_keg_reason_caseunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    x_dimen = kw.belief_keg_reason_caseunit
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
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(wk_rope)
    sue_belief.kegroot.set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(thur_rope)
    sue_belief.kegroot.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_keg_partyunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    x_dimen = kw.belief_keg_partyunit
    root_jkeys = {kw.keg_rope: root_rope, kw.party_title: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.party_title: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.party_title: exx.swim}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.kegroot.laborunit.add_party(exx.swim)

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_keg_healerunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    x_dimen = kw.belief_keg_healerunit
    root_jkeys = {kw.keg_rope: root_rope, kw.healer_name: exx.swim}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.healer_name: exx.swim}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.healer_name: exx.swim}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.kegroot.healerunit.set_healer_name(exx.swim)

    # THEN
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)


def test_belief_attr_exists_ReturnsObj_belief_keg_factunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    clean_rope = sue_belief.make_rope(casa_rope, exx.clean)
    root_rope = sue_belief.kegroot.get_keg_rope()
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    x_dimen = kw.belief_keg_factunit
    root_jkeys = {kw.keg_rope: root_rope, kw.fact_context: wk_rope}
    casa_jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    clean_jkeys = {kw.keg_rope: clean_rope, kw.fact_context: wk_rope}

    # WHEN / THEN
    assert not belief_attr_exists(x_dimen, None, {})
    assert not belief_attr_exists(x_dimen, sue_belief, {})
    assert not belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)

    # WHEN
    sue_belief.add_keg(wk_rope)
    sue_belief.kegroot.set_factunit(factunit_shop(wk_rope))

    # THEN
    assert belief_attr_exists(x_dimen, sue_belief, root_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, casa_jkeys)
    assert not belief_attr_exists(x_dimen, sue_belief, clean_jkeys)
