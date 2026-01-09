from pytest import raises as pytest_raises
from src.ch03_voice.labor import laborunit_shop, partyunit_shop
from src.ch04_rope.rope import default_knot_if_None
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_belief_logic.belief_main import (
    beliefunit_shop,
    get_beliefunit_from_dict,
    get_dict_of_belief_from_dict,
)
from src.ch07_belief_logic.test._util.ch07_examples import (
    beliefunit_v001,
    get_beliefunit_laundry_example1,
    get_beliefunit_reason_context_ziet_example,
    get_beliefunit_x1_3levels_1reason_1facts,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_BeliefUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_belief = get_beliefunit_laundry_example1()
    yao_fund_pool = 23000
    yao_belief.fund_pool = yao_fund_pool
    yao_fund_grain = 23
    yao_belief.fund_grain = yao_fund_grain
    belief_tally = 23
    yao_belief.tally = belief_tally
    x_last_lesson_id = 77
    yao_belief.set_last_lesson_id(x_last_lesson_id)

    # WHEN
    belief_dict = yao_belief.to_dict()

    # THEN
    assert belief_dict is not None
    assert str(type(belief_dict)) == "<class 'dict'>"
    assert belief_dict[kw.belief_name] == yao_belief.belief_name
    assert belief_dict[kw.tally] == yao_belief.tally
    assert belief_dict[kw.tally] == belief_tally
    assert belief_dict[kw.fund_pool] == yao_fund_pool
    assert belief_dict[kw.fund_grain] == yao_fund_grain
    assert belief_dict[kw.max_tree_traverse] == yao_belief.max_tree_traverse
    assert belief_dict[kw.knot] == yao_belief.knot
    assert belief_dict[kw.credor_respect] == yao_belief.credor_respect
    assert belief_dict[kw.debtor_respect] == yao_belief.debtor_respect
    assert belief_dict[kw.last_lesson_id] == yao_belief.last_lesson_id
    assert len(belief_dict[kw.voices]) == len(yao_belief.voices)
    assert len(belief_dict[kw.voices]) != 12

    x_kegroot = yao_belief.kegroot
    kegroot_dict = belief_dict[kw.kegroot]
    assert kegroot_dict[kw.keg_label] == x_kegroot.keg_label
    assert kegroot_dict[kw.star] == x_kegroot.star
    assert len(kegroot_dict[kw.kids]) == len(x_kegroot.kids)


def test_BeliefUnit_to_dict_ReturnsObj_Scenario1_kegroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_belief = beliefunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.add_party(party_title=run_str)
    root_rope = sue_belief.kegroot.get_keg_rope()
    sue_belief.edit_keg_attr(root_rope, laborunit=x_laborunit)
    root_keg = sue_belief.get_keg_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_keg.gogo_want = x_gogo_want
    root_keg.stop_want = x_stop_want

    # WHEN
    belief_dict = sue_belief.to_dict()
    kegroot_dict = belief_dict.get(kw.kegroot)

    # THEN
    assert kegroot_dict[kw.laborunit] == x_laborunit.to_dict()
    run_partyunit = partyunit_shop(run_str)
    assert kegroot_dict[kw.laborunit] == {"partys": {run_str: run_partyunit.to_dict()}}
    assert kegroot_dict.get(kw.gogo_want) == x_gogo_want
    assert kegroot_dict.get(kw.stop_want) == x_stop_want


def test_BeliefUnit_to_dict_ReturnsObj_Scenario2_With_kegroot_healerunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(exx.yao)
    yao_voiceunit = sue_belief.get_voice(exx.yao)
    yao_voiceunit.add_membership(exx.run)
    run_healerunit = healerunit_shop()
    run_healerunit.set_healer_name(x_healer_name=exx.run)
    root_rope = sue_belief.kegroot.get_keg_rope()
    sue_belief.edit_keg_attr(root_rope, healerunit=run_healerunit)

    # WHEN
    belief_dict = sue_belief.to_dict()
    kegroot_dict = belief_dict.get(kw.kegroot)

    # THEN
    assert kegroot_dict[kw.healerunit] == run_healerunit.to_dict()


def test_BeliefUnit_to_dict_ReturnsObj_Scenario3_kegkid_LaborUnit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(exx.yao)
    yao_voiceunit = sue_belief.get_voice(exx.yao)
    yao_voiceunit.add_membership(exx.run)

    morn_str = "morning"
    morn_rope = sue_belief.make_l1_rope(morn_str)
    sue_belief.set_l1_keg(kegunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.add_party(party_title=exx.run)
    sue_belief.edit_keg_attr(morn_rope, laborunit=x_laborunit)

    # WHEN
    belief_dict = sue_belief.to_dict()
    kegroot_dict = belief_dict.get(kw.kegroot)

    # THEN
    labor_dict_x = kegroot_dict[kw.kids][morn_str][kw.laborunit]
    assert labor_dict_x == x_laborunit.to_dict()
    run_partyunit = partyunit_shop(exx.run)
    assert labor_dict_x == {"partys": {exx.run: run_partyunit.to_dict()}}


def test_BeliefUnit_to_dict_ReturnsObj_Scenario4_kegunit_WithLevels():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_belief = get_beliefunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_belief.fund_pool = x_fund_pool
    x_fund_grain = 66
    zia_belief.fund_grain = x_fund_grain
    x_respect_grain = 7
    zia_belief.respect_grain = x_respect_grain
    x_mana_grain = 0.3
    zia_belief.mana_grain = x_mana_grain
    override_str = "override"
    zia_belief.add_voiceunit(exx.yao)
    yao_voiceunit = zia_belief.get_voice(exx.yao)
    yao_voiceunit.add_membership(exx.run)
    run_healerunit = healerunit_shop({exx.run})
    root_rope = zia_belief.kegroot.get_keg_rope()
    zia_belief.edit_keg_attr(root_rope, healerunit=run_healerunit)
    zia_belief.edit_keg_attr(root_rope, problem_bool=True)

    # WHEN
    belief_dict = zia_belief.to_dict()

    # THEN
    assert belief_dict is not None
    assert belief_dict[kw.belief_name] == zia_belief.belief_name
    assert belief_dict[kw.tally] == zia_belief.tally
    assert belief_dict[kw.fund_pool] == zia_belief.fund_pool
    assert belief_dict[kw.fund_grain] == zia_belief.fund_grain
    assert belief_dict[kw.respect_grain] == zia_belief.respect_grain
    assert belief_dict[kw.mana_grain] == zia_belief.mana_grain
    assert belief_dict[kw.credor_respect] == zia_belief.credor_respect
    assert belief_dict[kw.debtor_respect] == zia_belief.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     belief_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     belief_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        belief_dict[kw.last_lesson_id]

    x_kegroot = zia_belief.kegroot
    kegroot_dict = belief_dict.get(kw.kegroot)

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


def test_BeliefUnit_to_dict_ReturnsJSON_Scenario5_BigExample():
    # ESTABLISH
    yao_belief = beliefunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_belief.make_l1_rope(hr_number_str)
    yao_belief.add_fact(
        fact_context=hr_number_rope,
        fact_state=hr_number_rope,
        fact_lower=0,
        fact_upper=23,
    )
    jour_min_str = "jour_minute"
    jour_min_rope = yao_belief.make_l1_rope(jour_min_str)
    yao_belief.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=59,
    )
    x_factunit = factunit_shop(jour_min_rope, jour_min_rope, 5, 59)
    yao_belief.edit_keg_attr(x_factunit.fact_context, factunit=x_factunit)
    yao_belief.set_max_tree_traverse(2)

    # WHEN
    belief_dict = yao_belief.to_dict()

    # THEN
    assert belief_dict[kw.belief_name] == yao_belief.belief_name
    assert belief_dict[kw.tally] == yao_belief.tally
    assert belief_dict[kw.max_tree_traverse] == 2
    assert belief_dict[kw.max_tree_traverse] == yao_belief.max_tree_traverse
    assert belief_dict[kw.knot] == yao_belief.knot

    x_kegroot = yao_belief.kegroot
    kegroot_dict = belief_dict.get(kw.kegroot)
    assert len(kegroot_dict[kw.kids]) == len(x_kegroot.kids)

    kids_dict = kegroot_dict[kw.kids]
    jour_min_dict = kids_dict[jour_min_str]
    jour_min_factunits_dict = jour_min_dict[kw.factunits]
    jour_min_keg_x = yao_belief.get_keg_obj(jour_min_rope)
    print(f"{jour_min_factunits_dict=}")
    assert len(jour_min_factunits_dict) == 1
    assert len(jour_min_factunits_dict) == len(jour_min_keg_x.factunits)

    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_belief.make_l1_rope(cont_str)
    ulti_rope = yao_belief.make_l1_rope(ulti_str)
    cont_keg = yao_belief.get_keg_obj(cont_rope)
    ulti_keg = yao_belief.get_keg_obj(ulti_rope)
    cont_reasonunits_dict = kegroot_dict[kw.kids][cont_str][kw.reasonunits]
    ulti_reasonunits_dict = kegroot_dict[kw.kids][ulti_str][kw.reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_keg.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_keg.reasonunits)

    anna_str = "Anna"
    anna_voiceunit = yao_belief.get_voice(anna_str)
    assert anna_voiceunit.get_membership(";Family").group_cred_lumen == 6.2
    assert yao_belief.voices is not None
    assert len(yao_belief.voices) == 22


def test_get_beliefunit_from_dict_ReturnsKegRoot():
    # ESTABLISH
    zia_belief = get_beliefunit_x1_3levels_1reason_1facts()
    zia_belief.set_max_tree_traverse(23)
    root_keg = zia_belief.kegroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_keg.gogo_want = zia_gogo_want
    root_keg.stop_want = zia_stop_want

    # WHEN
    json_belief = get_beliefunit_from_dict(zia_belief.to_dict())

    # THEN
    json_kegroot = json_belief.get_keg_obj(zia_belief.kegroot.get_keg_rope())
    assert json_kegroot.gogo_want == zia_gogo_want
    assert json_kegroot.stop_want == zia_stop_want


def test_get_beliefunit_from_dict_ReturnsObj_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_belief = beliefunit_shop("Bob", knot=slash_knot)
    assert before_bob_belief.knot != default_knot_if_None()

    # WHEN
    after_bob_belief = get_beliefunit_from_dict(before_bob_belief.to_dict())

    # THEN
    assert after_bob_belief.knot != default_knot_if_None()
    assert after_bob_belief.knot == slash_knot
    assert after_bob_belief.knot == before_bob_belief.knot


def test_get_beliefunit_from_dict_ReturnsObj_knot_VoiceExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_belief = beliefunit_shop("Bob", knot=slash_knot)
    bob_comma_str = ",Bob"
    before_bob_belief.add_voiceunit(bob_comma_str)
    assert before_bob_belief.voice_exists(bob_comma_str)

    # WHEN
    after_bob_belief = get_beliefunit_from_dict(before_bob_belief.to_dict())

    # THEN
    after_bob_voiceunit = after_bob_belief.get_voice(bob_comma_str)
    assert after_bob_voiceunit.groupmark == slash_knot


def test_get_beliefunit_from_dict_ReturnsObj_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_belief = beliefunit_shop("Bob", knot=slash_knot)
    swim_str = f"{slash_knot}Swimmers"
    before_bob_belief.add_voiceunit(exx.yao)
    yao_voiceunit = before_bob_belief.get_voice(exx.yao)
    yao_voiceunit.add_membership(swim_str)

    # WHEN
    after_bob_belief = get_beliefunit_from_dict(before_bob_belief.to_dict())

    # THEN
    after_yao_voiceunit = after_bob_belief.get_voice(exx.yao)
    assert after_yao_voiceunit.groupmark == slash_knot


def test_get_beliefunit_from_dict_ReturnsObj_Scenario7_kegroot_knot_IsApplied():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue", knot=exx.slash)
    root_rope = sue_belief.kegroot.get_keg_rope()
    hr_number_str = "hr_number"
    hr_number_rope = sue_belief.make_l1_rope(hr_number_str)
    sue_belief.add_keg(hr_number_rope)
    assert sue_belief.knot == exx.slash
    assert sue_belief.get_keg_obj(root_rope).knot == exx.slash
    assert sue_belief.get_keg_obj(hr_number_rope).knot == exx.slash

    # WHEN
    after_bob_belief = get_beliefunit_from_dict(sue_belief.to_dict())

    # THEN
    assert after_bob_belief.knot == exx.slash
    assert after_bob_belief.get_keg_obj(root_rope).knot == exx.slash
    assert after_bob_belief.get_keg_obj(hr_number_rope).knot == exx.slash


def test_get_beliefunit_from_dict_ExportsBeliefUnit_star():
    # ESTABLISH
    x1_belief = beliefunit_v001()
    x1_belief.tally = 15
    assert x1_belief.tally == 15
    assert x1_belief.kegroot.star != x1_belief.tally
    assert x1_belief.kegroot.star == 1

    # WHEN
    x2_belief = get_beliefunit_from_dict(x1_belief.to_dict())

    # THEN
    assert x1_belief.tally == 15
    assert x1_belief.tally == x2_belief.tally
    assert x1_belief.kegroot.star == 1
    assert x1_belief.kegroot.star == x2_belief.kegroot.star
    assert x1_belief.kegroot.kids == x2_belief.kegroot.kids


def test_get_dict_of_belief_from_dict_ReturnsDictOfBeliefUnits():
    # ESTABLISH
    x1_belief = beliefunit_v001()
    x2_belief = get_beliefunit_x1_3levels_1reason_1facts()
    x3_belief = get_beliefunit_reason_context_ziet_example()
    print(f"{x1_belief.belief_name}")
    print(f"{x2_belief.belief_name}")
    print(f"{x3_belief.belief_name}")

    cn_dict_of_dicts = {
        x1_belief.belief_name: x1_belief.to_dict(),
        x2_belief.belief_name: x2_belief.to_dict(),
        x3_belief.belief_name: x3_belief.to_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_belief_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_belief.belief_name) is not None
    assert ccn_dict_of_obj.get(x2_belief.belief_name) is not None
    assert ccn_dict_of_obj.get(x3_belief.belief_name) is not None

    ccn2_belief = ccn_dict_of_obj.get(x2_belief.belief_name)
    assert ccn2_belief.kegroot.keg_label == x2_belief.kegroot.keg_label
    assert ccn2_belief.kegroot.parent_rope == x2_belief.kegroot.parent_rope
    assert ccn2_belief.kegroot.fund_grain == x2_belief.kegroot.fund_grain
    shave_rope = ccn2_belief.make_l1_rope("shave")
    wk_rope = ccn2_belief.make_l1_rope("sem_jours")
    # assert ccn2_belief.get_keg_obj(shave_rope) == x2_belief.get_keg_obj(shave_rope)
    # assert ccn2_belief.get_keg_obj(wk_rope) == x2_belief.get_keg_obj(wk_rope)
    # assert ccn2_belief.kegroot == x2_belief.kegroot
    assert ccn2_belief.to_dict() == x2_belief.to_dict()

    ccn_belief3 = ccn_dict_of_obj.get(x3_belief.belief_name)
    assert ccn_belief3.to_dict() == x3_belief.to_dict()

    cc1_keg_root = ccn_dict_of_obj.get(x1_belief.belief_name).kegroot
    ccn_belief1 = ccn_dict_of_obj.get(x1_belief.belief_name)
    assert ccn_belief1._keg_dict == x1_belief._keg_dict
    philipa_str = "Philipa"
    ccn_philipa_voiceunit = ccn_belief1.get_voice(philipa_str)
    x1_philipa_voiceunit = x1_belief.get_voice(philipa_str)
    assert ccn_philipa_voiceunit.memberships == x1_philipa_voiceunit.memberships
    assert ccn_belief1 == x1_belief
    assert ccn_dict_of_obj.get(x1_belief.belief_name) == x1_belief
