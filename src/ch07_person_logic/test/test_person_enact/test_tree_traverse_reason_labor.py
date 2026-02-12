from src.ch03_labor.labor import laborheir_shop, laborunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_enact_plan_Sets_planroot_laborheirFrom_planroot_laborunit():
    # ESTABLISH
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(exx.sue)
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.planroot.get_plan_rope()
    yao_person.edit_plan_attr(root_rope, laborunit=sue_laborunit)
    assert yao_person.planroot.laborunit == sue_laborunit
    assert not yao_person.planroot.laborheir

    # WHEN
    yao_person.enact_plan()

    # THEN
    assert yao_person.planroot.laborheir is not None
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None, laborunit=sue_laborunit, groupunits=None
    )
    assert yao_person.planroot.laborheir == expected_laborheir


def test_PersonUnit_enact_plan_Set_child_plan_laborheir_FromParent_laborunit():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    bob_person = personunit_shop(exx.bob)
    run_str = "run"
    run_rope = bob_person.make_l1_rope(run_str)
    bob_person.add_partnerunit(exx.bob)
    bob_person.set_l1_plan(planunit_shop(run_str))
    bob_person.edit_plan_attr(run_rope, laborunit=x_laborunit)
    run_plan = bob_person.get_plan_obj(run_rope)
    assert run_plan.laborunit == x_laborunit
    assert not run_plan.laborheir

    # WHEN
    bob_person.enact_plan()

    # THEN
    assert run_plan.laborheir
    assert run_plan.laborheir.person_name_is_labor

    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_person.groupunits,
    )
    expected_laborheir.set_person_name_is_labor(
        bob_person.groupunits, bob_person.person_name
    )
    print(f"{expected_laborheir.person_name_is_labor=}")
    assert (
        run_plan.laborheir.person_name_is_labor
        == expected_laborheir.person_name_is_labor
    )
    assert run_plan.laborheir == expected_laborheir


def test_PersonUnit_enact_plan_Set_grandchild_plan_laborheir_From_plankid_laborunit_Scenario0():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    swim_rope = sue_person.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_person.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_person.make_rope(morn_rope, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.add_party(party_title=swimmers_str)

    sue_person.add_partnerunit(exx.yao)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(swimmers_str)

    sue_person.set_l1_plan(planunit_shop(exx.swim))
    sue_person.set_plan_obj(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_person.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_person.edit_plan_attr(swim_rope, laborunit=x_laborunit)
    # print(sue_person.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_person.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert four_plan.laborheir is None

    # WHEN
    sue_person.enact_plan()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_person.groupunits,
    )
    assert four_plan.laborheir is not None
    assert four_plan.laborheir == x_laborheir


def test_PersonUnit_enact_plan_Set_grandchild_plan_laborheir_From_plankid_laborunit_Scenario1_solo_AttrIsPassed():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    swim_rope = sue_person.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_person.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_person.make_rope(morn_rope, four_str)
    swimmers_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    swimmers_solo_bool = True
    swimmers_laborunit.add_party(swimmers_str, solo=swimmers_solo_bool)

    sue_person.add_partnerunit(exx.yao)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(swimmers_str)

    sue_person.set_l1_plan(planunit_shop(exx.swim))
    sue_person.set_plan_obj(planunit_shop(morn_str), parent_rope=swim_rope)
    sue_person.set_plan_obj(planunit_shop(four_str), parent_rope=morn_rope)
    sue_person.edit_plan_attr(swim_rope, laborunit=swimmers_laborunit)
    # print(sue_person.make_rope(four_rope=}\n{morn_rope=))
    four_plan = sue_person.get_plan_obj(four_rope)
    assert four_plan.laborunit == laborunit_shop()
    assert not four_plan.laborheir

    # WHEN
    sue_person.enact_plan()

    # THEN
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=swimmers_laborunit,
        groupunits=sue_person.groupunits,
    )
    assert four_plan.laborheir
    assert four_plan.laborheir == expected_laborheir
    swimmers_party = four_plan.laborheir.partys.get(swimmers_str)
    assert swimmers_party.solo == swimmers_solo_bool


def test_PersonUnit__get_filtered_awardunits_plan_CleansPlan_Laborunit():
    # ESTABLISH
    sue1_person = personunit_shop(exx.sue)
    sue1_person.add_partnerunit(exx.xio)
    sue1_person.add_partnerunit(exx.zia)

    casa_rope = sue1_person.make_l1_rope(exx.casa)
    swim_rope = sue1_person.make_l1_rope(exx.swim)
    root_rope = sue1_person.planroot.get_plan_rope()
    sue1_person.set_plan_obj(planunit_shop(exx.casa), parent_rope=root_rope)
    sue1_person.set_plan_obj(planunit_shop(exx.swim), parent_rope=root_rope)
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=exx.xio)
    swim_laborunit.add_party(party_title=exx.zia)
    sue1_person.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_person_swim_plan = sue1_person.get_plan_obj(swim_rope)
    sue1_person_swim_partys = sue1_person_swim_plan.laborunit.partys
    assert len(sue1_person_swim_partys) == 2

    # WHEN
    sue2_person = personunit_shop(exx.sue)
    sue2_person.add_partnerunit(exx.xio)
    cleaned_plan = sue2_person._get_filtered_awardunits_plan(sue1_person_swim_plan)

    # THEN
    cleaned_swim_partys = cleaned_plan.laborunit.partys
    assert len(cleaned_swim_partys) == 1
    assert list(cleaned_swim_partys) == [exx.xio]


def test_PersonUnit_set_plan_CleansPlan_awardunits():
    # ESTABLISH
    sue1_person = personunit_shop("Sue")
    sue1_person.add_partnerunit(exx.xio)
    sue1_person.add_partnerunit(exx.zia)

    casa_rope = sue1_person.make_l1_rope(exx.casa)
    swim_rope = sue1_person.make_l1_rope(exx.swim)
    sue1_person.set_plan_obj(
        planunit_shop(exx.casa), parent_rope=sue1_person.planroot.get_plan_rope()
    )
    sue1_person.set_plan_obj(
        planunit_shop(exx.swim), parent_rope=sue1_person.planroot.get_plan_rope()
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=exx.xio)
    swim_laborunit.add_party(party_title=exx.zia)
    sue1_person.edit_plan_attr(swim_rope, laborunit=swim_laborunit)
    sue1_person_swim_plan = sue1_person.get_plan_obj(swim_rope)
    sue1_person_swim_partys = sue1_person_swim_plan.laborunit.partys
    assert len(sue1_person_swim_partys) == 2

    # WHEN
    sue2_person = personunit_shop("Sue")
    sue2_person.add_partnerunit(exx.xio)
    sue2_person.set_l1_plan(
        sue1_person_swim_plan, get_rid_of_missing_awardunits_awardee_titles=False
    )

    # THEN
    sue2_person_swim_plan = sue2_person.get_plan_obj(swim_rope)
    sue2_person_swim_partys = sue2_person_swim_plan.laborunit.partys
    assert len(sue2_person_swim_partys) == 1
    assert list(sue2_person_swim_partys) == [exx.xio]
