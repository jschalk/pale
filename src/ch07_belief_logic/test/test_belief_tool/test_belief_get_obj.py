from src.ch03_voice.group import awardunit_shop
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_get_obj,
    belief_keg_awardunit_get_obj,
    belief_keg_factunit_get_obj,
    belief_keg_reason_caseunit_get_obj as caseunit_get_obj,
    belief_keg_reasonunit_get_obj,
    belief_kegunit_get_obj,
    belief_voice_membership_get_obj,
    belief_voiceunit_get_obj,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_belief_voiceunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao}
    sue_belief.add_voiceunit(exx.yao)

    # WHEN
    x_obj = belief_voiceunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_voice(exx.yao)


def test_belief_voice_membership_get_obj_ReturnsObj():
    # ESTABLISH
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao, "group_title": swim_str}
    sue_belief.add_voiceunit(exx.yao)
    sue_belief.get_voice(exx.yao).add_membership(swim_str)

    # WHEN
    x_obj = belief_voice_membership_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_voice(exx.yao).get_membership(swim_str)


def test_belief_kegunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope}

    # WHEN
    x_obj = belief_kegunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope)


def test_belief_keg_awardunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    sue_belief.add_keg(casa_rope)
    sue_belief.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(exx.swim))

    # WHEN
    x_obj = belief_keg_awardunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope).get_awardunit(exx.swim)


def test_belief_keg_reasonunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    sue_belief.add_keg(casa_rope)
    sue_belief.add_keg(wk_rope)
    sue_belief.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = belief_keg_reasonunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope).get_reasonunit(wk_rope)


def test_belief_keg_reason_caseunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_belief.add_keg(casa_rope)
    sue_belief.add_keg(wk_rope)
    sue_belief.add_keg(thur_rope)
    casa_keg = sue_belief.get_keg_obj(casa_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = caseunit_get_obj(sue_belief, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_keg.get_reasonunit(wk_rope).get_case(thur_rope)


def test_belief_keg_factunit_get_obj_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    sue_belief.add_keg(casa_rope)
    sue_belief.add_keg(wk_rope)
    sue_belief.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = belief_keg_factunit_get_obj(sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope).factunits.get(wk_rope)


def test_belief_get_obj_ReturnsObj_BeliefUnit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao}
    sue_belief.add_voiceunit(exx.yao)

    # WHEN
    x_obj = belief_get_obj(kw.beliefunit, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief


def test_belief_get_obj_ReturnsObj_belief_voiceunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao}
    sue_belief.add_voiceunit(exx.yao)

    # WHEN
    x_obj = belief_get_obj(kw.belief_voiceunit, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_voice(exx.yao)


def test_belief_get_obj_ReturnsObj_belief_voice_membership_get_obj():
    # ESTABLISH
    swim_str = ";swim"
    sue_belief = beliefunit_shop("Sue")
    jkeys = {kw.voice_name: exx.yao, "group_title": swim_str}
    sue_belief.add_voiceunit(exx.yao)
    sue_belief.get_voice(exx.yao).add_membership(swim_str)

    # WHEN
    x_obj = belief_get_obj(kw.belief_voice_membership, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_voice(exx.yao).get_membership(swim_str)


def test_belief_get_obj_ReturnsObj_belief_kegunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope}

    # WHEN
    x_obj = belief_get_obj(kw.belief_kegunit, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope)


def test_belief_get_obj_ReturnsObj_belief_keg_awardunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.awardee_title: exx.swim}
    sue_belief.add_keg(casa_rope)
    sue_belief.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(exx.swim))

    # WHEN
    x_obj = belief_get_obj(kw.belief_keg_awardunit, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope).get_awardunit(exx.swim)


def test_belief_get_obj_ReturnsObj_belief_keg_reasonunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.reason_context: wk_rope}
    sue_belief.add_keg(casa_rope)
    sue_belief.add_keg(wk_rope)
    sue_belief.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # WHEN
    x_obj = belief_get_obj(kw.belief_keg_reasonunit, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope).get_reasonunit(wk_rope)


def test_belief_get_obj_ReturnsObj_belief_keg_reason_caseunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    wk_rope = sue_belief.make_l1_rope(exx.wk)
    thur_rope = sue_belief.make_rope(wk_rope, "thur")
    casa_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: thur_rope,
    }
    sue_belief.add_keg(casa_rope)
    sue_belief.add_keg(wk_rope)
    sue_belief.add_keg(thur_rope)
    casa_keg = sue_belief.get_keg_obj(casa_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # WHEN
    x_obj = belief_get_obj(kw.belief_keg_reason_caseunit, sue_belief, casa_jkeys)
    # THEN
    assert x_obj
    assert x_obj == casa_keg.get_reasonunit(wk_rope).get_case(thur_rope)


def test_belief_get_obj_ReturnsObj_belief_keg_factunit_get_obj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    wk_rope = sue_belief.make_l1_rope("wk")
    sue_belief.add_keg(casa_rope)
    jkeys = {kw.keg_rope: casa_rope, kw.fact_context: wk_rope}
    sue_belief.add_keg(casa_rope)
    sue_belief.add_keg(wk_rope)
    sue_belief.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # WHEN
    x_obj = belief_get_obj(kw.belief_keg_factunit, sue_belief, jkeys)
    # THEN
    assert x_obj
    assert x_obj == sue_belief.get_keg_obj(casa_rope).factunits.get(wk_rope)
