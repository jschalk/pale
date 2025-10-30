from src.ch03_voice.labor import laborheir_shop, laborunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_BeliefUnit_cashout_Sets_planroot_laborheirFrom_planroot_laborunit():
    # ESTABLISH
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(exx.sue)
    yao_belief = beliefunit_shop("Yao")
    root_rope = yao_belief.planroot.get_plan_rope()
    yao_belief.edit_plan_attr(root_rope, laborunit=sue_laborunit)
    assert yao_belief.planroot.laborunit == sue_laborunit
    assert not yao_belief.planroot.laborheir

    # WHEN
    yao_belief.cashout()

    # THEN
    assert yao_belief.planroot.laborheir is not None
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None, laborunit=sue_laborunit, groupunits=None
    )
    assert yao_belief.planroot.laborheir == expected_laborheir


def test_BeliefUnit_cashout_Set_child_plan_laborheir_FromParent_laborunit():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    bob_belief = beliefunit_shop(exx.bob)
    run_str = "run"
    run_rope = bob_belief.make_l1_rope(run_str)
    bob_belief.add_voiceunit(exx.bob)
    bob_belief.set_l1_plan(planunit_shop(run_str))
    bob_belief.edit_plan_attr(run_rope, laborunit=x_laborunit)
    run_plan = bob_belief.get_plan_obj(run_rope)
    assert run_plan.laborunit == x_laborunit
    assert not run_plan.laborheir

    # WHEN
    bob_belief.cashout()

    # THEN
    assert run_plan.laborheir
    assert run_plan.laborheir.belief_name_is_labor

    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_belief.groupunits,
    )
    x_laborheir.set_belief_name_is_labor(bob_belief.groupunits, bob_belief.belief_name)
    print(f"{x_laborheir.belief_name_is_labor=}")
    assert run_plan.laborheir.belief_name_is_labor == x_laborheir.belief_name_is_labor
    assert run_plan.laborheir == x_laborheir


def test_BeliefUnit_cashout_Set_grandchild_plan_laborheir_From_plankid_laborunit_Scenario0():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    swim_rope = sue_belief.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_belief.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_belief.make_rope(morn_rope, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.add_party(party_title=swimmers_str)

    sue_belief.add_voiceunit(exx.yao)
    yao_voiceunit = sue_belief.get_voice(exx.yao)
    yao_voiceunit.add_membership(swimmers_str)

    sue_belief.set_l1_plan(planunit_shop(exx.swim))
    sue_belief.set_plan_obj(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_belief.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_belief.edit_plan_attr(swim_rope, laborunit=x_laborunit)
    # print(sue_belief.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_belief.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert four_plan.laborheir is None

    # WHEN
    sue_belief.cashout()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_belief.groupunits,
    )
    assert four_plan.laborheir is not None
    assert four_plan.laborheir == x_laborheir


def test_BeliefUnit_cashout_Set_grandchild_plan_laborheir_From_plankid_laborunit_Scenario1_solo_AttrIsPassed():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    swim_rope = sue_belief.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_belief.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_belief.make_rope(morn_rope, four_str)
    swimmers_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    swimmers_solo_bool = True
    swimmers_laborunit.add_party(swimmers_str, solo=swimmers_solo_bool)

    sue_belief.add_voiceunit(exx.yao)
    yao_voiceunit = sue_belief.get_voice(exx.yao)
    yao_voiceunit.add_membership(swimmers_str)

    sue_belief.set_l1_plan(planunit_shop(exx.swim))
    sue_belief.set_plan_obj(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_belief.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_belief.edit_plan_attr(swim_rope, laborunit=swimmers_laborunit)
    # print(sue_belief.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_belief.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert not four_plan.laborheir

    # WHEN
    sue_belief.cashout()

    # THEN
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=swimmers_laborunit,
        groupunits=sue_belief.groupunits,
    )
    assert four_plan.laborheir
    assert four_plan.laborheir == expected_laborheir
    swimmers_party = four_plan.laborheir.partys.get(swimmers_str)
    assert swimmers_party.solo == swimmers_solo_bool


def test_BeliefUnit__get_filtered_awardunits_plan_CleansPlan_Laborunit():
    # ESTABLISH
    sue1_belief = beliefunit_shop(exx.sue)
    sue1_belief.add_voiceunit(exx.xio)
    sue1_belief.add_voiceunit(exx.zia)

    casa_rope = sue1_belief.make_l1_rope(exx.casa)
    swim_rope = sue1_belief.make_l1_rope(exx.swim)
    root_rope = sue1_belief.planroot.get_plan_rope()
    sue1_belief.set_plan_obj(planunit_shop(exx.casa), parent_rope=root_rope)
    sue1_belief.set_plan_obj(planunit_shop(exx.swim), parent_rope=root_rope)
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=exx.xio)
    swim_laborunit.add_party(party_title=exx.zia)
    sue1_belief.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_belief_swim_plan = sue1_belief.get_plan_obj(swim_rope)
    sue1_belief_swim_partys = sue1_belief_swim_plan.laborunit.partys
    assert len(sue1_belief_swim_partys) == 2

    # WHEN
    sue2_belief = beliefunit_shop(exx.sue)
    sue2_belief.add_voiceunit(exx.xio)
    cleaned_plan = sue2_belief._get_filtered_awardunits_plan(sue1_belief_swim_plan)

    # THEN
    cleaned_swim_partys = cleaned_plan.laborunit.partys
    assert len(cleaned_swim_partys) == 1
    assert list(cleaned_swim_partys) == [exx.xio]


def test_BeliefUnit_set_plan_CleansPlan_awardunits():
    # ESTABLISH
    sue1_belief = beliefunit_shop("Sue")
    sue1_belief.add_voiceunit(exx.xio)
    sue1_belief.add_voiceunit(exx.zia)

    casa_rope = sue1_belief.make_l1_rope(exx.casa)
    swim_rope = sue1_belief.make_l1_rope(exx.swim)
    sue1_belief.set_plan_obj(
        planunit_shop(exx.casa), parent_rope=sue1_belief.planroot.get_plan_rope()
    )
    sue1_belief.set_plan_obj(
        planunit_shop(exx.swim), parent_rope=sue1_belief.planroot.get_plan_rope()
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=exx.xio)
    swim_laborunit.add_party(party_title=exx.zia)
    sue1_belief.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_belief_swim_plan = sue1_belief.get_plan_obj(swim_rope)
    sue1_belief_swim_partys = sue1_belief_swim_plan.laborunit.partys
    assert len(sue1_belief_swim_partys) == 2

    # WHEN
    sue2_belief = beliefunit_shop("Sue")
    sue2_belief.add_voiceunit(exx.xio)
    sue2_belief.set_l1_plan(
        sue1_belief_swim_plan, get_rid_of_missing_awardunits_awardee_titles=False
    )

    # THEN
    sue2_belief_swim_plan = sue2_belief.get_plan_obj(swim_rope)
    sue2_belief_swim_partys = sue2_belief_swim_plan.laborunit.partys
    assert len(sue2_belief_swim_partys) == 1
    assert list(sue2_belief_swim_partys) == [exx.xio]
