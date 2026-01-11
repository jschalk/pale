from src.ch03_labor.labor import laborheir_shop, laborunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_cashout_Sets_kegroot_laborheirFrom_kegroot_laborunit():
    # ESTABLISH
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(exx.sue)
    yao_plan = planunit_shop("Yao")
    root_rope = yao_plan.kegroot.get_keg_rope()
    yao_plan.edit_keg_attr(root_rope, laborunit=sue_laborunit)
    assert yao_plan.kegroot.laborunit == sue_laborunit
    assert not yao_plan.kegroot.laborheir

    # WHEN
    yao_plan.cashout()

    # THEN
    assert yao_plan.kegroot.laborheir is not None
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None, laborunit=sue_laborunit, groupunits=None
    )
    assert yao_plan.kegroot.laborheir == expected_laborheir


def test_PlanUnit_cashout_Set_child_keg_laborheir_FromParent_laborunit():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    bob_plan = planunit_shop(exx.bob)
    run_str = "run"
    run_rope = bob_plan.make_l1_rope(run_str)
    bob_plan.add_personunit(exx.bob)
    bob_plan.set_l1_keg(kegunit_shop(run_str))
    bob_plan.edit_keg_attr(run_rope, laborunit=x_laborunit)
    run_keg = bob_plan.get_keg_obj(run_rope)
    assert run_keg.laborunit == x_laborunit
    assert not run_keg.laborheir

    # WHEN
    bob_plan.cashout()

    # THEN
    assert run_keg.laborheir
    assert run_keg.laborheir.plan_name_is_labor

    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=bob_plan.groupunits,
    )
    expected_laborheir.set_plan_name_is_labor(bob_plan.groupunits, bob_plan.plan_name)
    print(f"{expected_laborheir.plan_name_is_labor=}")
    assert run_keg.laborheir.plan_name_is_labor == expected_laborheir.plan_name_is_labor
    assert run_keg.laborheir == expected_laborheir


def test_PlanUnit_cashout_Set_grandchild_keg_laborheir_From_kegkid_laborunit_Scenario0():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    swim_rope = sue_plan.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_plan.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_plan.make_rope(morn_rope, four_str)
    x_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    x_laborunit.add_party(party_title=swimmers_str)

    sue_plan.add_personunit(exx.yao)
    yao_personunit = sue_plan.get_person(exx.yao)
    yao_personunit.add_membership(swimmers_str)

    sue_plan.set_l1_keg(kegunit_shop(exx.swim))
    sue_plan.set_keg_obj(kegunit_shop(morn_str), parent_rope=swim_rope)
    sue_plan.set_keg_obj(kegunit_shop(four_str), parent_rope=morn_rope)
    sue_plan.edit_keg_attr(swim_rope, laborunit=x_laborunit)
    # print(sue_plan.make_rope(four_rope=}\n{morn_rope=))
    four_keg = sue_plan.get_keg_obj(four_rope)
    assert four_keg.laborunit == laborunit_shop()
    assert four_keg.laborheir is None

    # WHEN
    sue_plan.cashout()

    # THEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=x_laborunit,
        groupunits=sue_plan.groupunits,
    )
    assert four_keg.laborheir is not None
    assert four_keg.laborheir == x_laborheir


def test_PlanUnit_cashout_Set_grandchild_keg_laborheir_From_kegkid_laborunit_Scenario1_solo_AttrIsPassed():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    swim_rope = sue_plan.make_l1_rope(exx.swim)
    morn_str = "morning"
    morn_rope = sue_plan.make_rope(swim_rope, morn_str)
    four_str = "fourth"
    four_rope = sue_plan.make_rope(morn_rope, four_str)
    swimmers_laborunit = laborunit_shop()
    swimmers_str = ";swimmers"
    swimmers_solo_bool = True
    swimmers_laborunit.add_party(swimmers_str, solo=swimmers_solo_bool)

    sue_plan.add_personunit(exx.yao)
    yao_personunit = sue_plan.get_person(exx.yao)
    yao_personunit.add_membership(swimmers_str)

    sue_plan.set_l1_keg(kegunit_shop(exx.swim))
    sue_plan.set_keg_obj(kegunit_shop(morn_str), parent_rope=swim_rope)
    sue_plan.set_keg_obj(kegunit_shop(four_str), parent_rope=morn_rope)
    sue_plan.edit_keg_attr(swim_rope, laborunit=swimmers_laborunit)
    # print(sue_plan.make_rope(four_rope=}\n{morn_rope=))
    four_keg = sue_plan.get_keg_obj(four_rope)
    assert four_keg.laborunit == laborunit_shop()
    assert not four_keg.laborheir

    # WHEN
    sue_plan.cashout()

    # THEN
    expected_laborheir = laborheir_shop()
    expected_laborheir.set_partys(
        parent_laborheir=None,
        laborunit=swimmers_laborunit,
        groupunits=sue_plan.groupunits,
    )
    assert four_keg.laborheir
    assert four_keg.laborheir == expected_laborheir
    swimmers_party = four_keg.laborheir.partys.get(swimmers_str)
    assert swimmers_party.solo == swimmers_solo_bool


def test_PlanUnit__get_filtered_awardunits_keg_CleansKeg_Laborunit():
    # ESTABLISH
    sue1_plan = planunit_shop(exx.sue)
    sue1_plan.add_personunit(exx.xio)
    sue1_plan.add_personunit(exx.zia)

    casa_rope = sue1_plan.make_l1_rope(exx.casa)
    swim_rope = sue1_plan.make_l1_rope(exx.swim)
    root_rope = sue1_plan.kegroot.get_keg_rope()
    sue1_plan.set_keg_obj(kegunit_shop(exx.casa), parent_rope=root_rope)
    sue1_plan.set_keg_obj(kegunit_shop(exx.swim), parent_rope=root_rope)
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=exx.xio)
    swim_laborunit.add_party(party_title=exx.zia)
    sue1_plan.edit_keg_attr(swim_rope, laborunit=swim_laborunit)
    sue1_plan_swim_keg = sue1_plan.get_keg_obj(swim_rope)
    sue1_plan_swim_partys = sue1_plan_swim_keg.laborunit.partys
    assert len(sue1_plan_swim_partys) == 2

    # WHEN
    sue2_plan = planunit_shop(exx.sue)
    sue2_plan.add_personunit(exx.xio)
    cleaned_keg = sue2_plan._get_filtered_awardunits_keg(sue1_plan_swim_keg)

    # THEN
    cleaned_swim_partys = cleaned_keg.laborunit.partys
    assert len(cleaned_swim_partys) == 1
    assert list(cleaned_swim_partys) == [exx.xio]


def test_PlanUnit_set_keg_CleansKeg_awardunits():
    # ESTABLISH
    sue1_plan = planunit_shop("Sue")
    sue1_plan.add_personunit(exx.xio)
    sue1_plan.add_personunit(exx.zia)

    casa_rope = sue1_plan.make_l1_rope(exx.casa)
    swim_rope = sue1_plan.make_l1_rope(exx.swim)
    sue1_plan.set_keg_obj(
        kegunit_shop(exx.casa), parent_rope=sue1_plan.kegroot.get_keg_rope()
    )
    sue1_plan.set_keg_obj(
        kegunit_shop(exx.swim), parent_rope=sue1_plan.kegroot.get_keg_rope()
    )
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=exx.xio)
    swim_laborunit.add_party(party_title=exx.zia)
    sue1_plan.edit_keg_attr(swim_rope, laborunit=swim_laborunit)
    sue1_plan_swim_keg = sue1_plan.get_keg_obj(swim_rope)
    sue1_plan_swim_partys = sue1_plan_swim_keg.laborunit.partys
    assert len(sue1_plan_swim_partys) == 2

    # WHEN
    sue2_plan = planunit_shop("Sue")
    sue2_plan.add_personunit(exx.xio)
    sue2_plan.set_l1_keg(
        sue1_plan_swim_keg, get_rid_of_missing_awardunits_awardee_titles=False
    )

    # THEN
    sue2_plan_swim_keg = sue2_plan.get_keg_obj(swim_rope)
    sue2_plan_swim_partys = sue2_plan_swim_keg.laborunit.partys
    assert len(sue2_plan_swim_partys) == 1
    assert list(sue2_plan_swim_partys) == [exx.xio]
