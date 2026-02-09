from pytest import raises as pytest_raises
from src.ch02_person.group import awardunit_shop
from src.ch03_labor.labor import laborunit_shop
from src.ch04_rope.rope import create_rope, default_knot_if_None, is_sub_rope, to_rope
from src.ch05_reason.reason_main import caseunit_shop, factunit_shop, reasonunit_shop
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import get_planunit_with_4_levels
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_set_keg_ScenarioXX_RaisesErrorWhen_parent_rope_IsInvalid():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    invalid_rootlabel_swim_rope = create_rope("swimming")
    casa_keg = kegunit_shop(exx.casa)
    assert invalid_rootlabel_swim_rope != zia_plan.kegroot.get_keg_rope()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_keg_obj(casa_keg, parent_rope=invalid_rootlabel_swim_rope)
    exception_str = f"set_keg failed because parent_rope '{invalid_rootlabel_swim_rope}' has an invalid root rope. Should be {zia_plan.kegroot.get_keg_rope()}."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_keg_ScenarioXX_RaisesErrorWhen_parent_rope_KegDoesNotExist():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    swim_rope = zia_plan.make_l1_rope("swimming")

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_keg_obj(
            kegunit_shop(exx.casa),
            parent_rope=swim_rope,
            create_missing_ancestors=False,
        )
    exception_str = f"set_keg failed because '{swim_rope}' keg does not exist."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_keg_ScenarioXX_RaisesErrorWhen_keg_label_IsNotLabel():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    swim_rope = zia_plan.make_l1_rope("swimming")
    casa_rope = zia_plan.make_l1_rope(exx.casa)
    run_str = "run"
    run_rope = zia_plan.make_rope(casa_rope, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_keg_obj(kegunit_shop(run_rope), parent_rope=swim_rope)
    exception_str = f"set_keg failed because '{run_rope}' is not a LabelTerm."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_keg_ScenarioXX_SetsAttr():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    root_keg_rope = zia_plan.kegroot.get_keg_rope()
    assert not zia_plan.kegroot.kids.get(exx.casa)

    # WHEN
    zia_plan.set_keg_obj(kegunit_shop(exx.casa), parent_rope=root_keg_rope)

    # THEN
    print(f"{zia_plan.kegroot.kids.keys()=}")
    assert zia_plan.kegroot.kids.get(exx.casa)


def test_PlanUnit_keg_exists_ReturnsObj():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_rope = zia_plan.make_l1_rope(exx.casa)
    assert zia_plan.keg_exists(casa_rope) is False

    # WHEN
    zia_plan.set_keg_obj(
        kegunit_shop(exx.casa), parent_rope=zia_plan.kegroot.get_keg_rope()
    )

    # THEN
    assert zia_plan.keg_exists(casa_rope)


def test_PlanUnit_set_l1_keg_SetsAttr():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_rope = zia_plan.make_l1_rope(exx.casa)
    assert not zia_plan.kegroot.kids.get(casa_rope)

    # WHEN
    zia_plan.set_l1_keg(kegunit_shop(exx.casa))

    # THEN
    assert not zia_plan.kegroot.kids.get(casa_rope)


def test_PlanUnit_add_keg_SetsAttr_Scenario0():
    # ESTABLISH
    bob_planunit = planunit_shop(exx.bob, knot=exx.slash)
    casa_rope = bob_planunit.make_l1_rope("casa")
    assert not bob_planunit.keg_exists(casa_rope)

    # WHEN
    bob_planunit.add_keg(casa_rope)

    # THEN
    assert bob_planunit.keg_exists(casa_rope)
    casa_kegunit = bob_planunit.get_keg_obj(casa_rope)
    assert casa_kegunit.knot == bob_planunit.knot
    assert not casa_kegunit.pledge


def test_PlanUnit_add_keg_SetsAttr_Scenario1():
    # ESTABLISH
    bob_planunit = planunit_shop(exx.bob)
    casa_rope = bob_planunit.make_l1_rope("casa")
    casa_star = 13
    casa_pledge = True

    # WHEN
    bob_planunit.add_keg(casa_rope, star=casa_star, pledge=casa_pledge)

    # THEN
    casa_kegunit = bob_planunit.get_keg_obj(casa_rope)
    assert casa_kegunit.star == casa_star
    assert casa_kegunit.pledge


def test_PlanUnit_add_keg_ReturnsObj():
    # ESTABLISH
    bob_planunit = planunit_shop(exx.bob)
    casa_rope = bob_planunit.make_l1_rope("casa")
    casa_star = 13

    # WHEN
    casa_kegunit = bob_planunit.add_keg(casa_rope, star=casa_star)

    # THEN
    assert casa_kegunit.keg_label == "casa"
    assert casa_kegunit.star == casa_star


def test_PlanUnit_set_keg_ScenarioXX_AddsKegObjWithNonDefault_knot():
    # ESTABLISH
    assert exx.slash != default_knot_if_None()
    bob_plan = planunit_shop("Bob", knot=exx.slash)
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    wk_rope = bob_plan.make_l1_rope(exx.wk)
    wed_rope = bob_plan.make_rope(wk_rope, exx.wed)
    bob_plan.set_l1_keg(kegunit_shop(exx.casa))
    bob_plan.set_l1_keg(kegunit_shop(exx.wk))
    bob_plan.set_keg_obj(kegunit_shop(exx.wed), wk_rope)
    print(f"{bob_plan.kegroot.kids.keys()=}")
    assert len(bob_plan.kegroot.kids) == 2
    wed_keg = bob_plan.get_keg_obj(wed_rope)
    assert wed_keg.knot == exx.slash
    assert wed_keg.knot == bob_plan.knot

    # WHEN
    bob_plan.edit_keg_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_keg = bob_plan.get_keg_obj(casa_rope)
    assert casa_keg.reasonunits.get(wk_rope) is not None


def test_PlanUnit_set_keg_ScenarioXX_CanCreateMissingKegUnits():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    ww2_rope = sue_plan.make_l1_rope("ww2")
    battles_rope = sue_plan.make_rope(ww2_rope, "battles")
    coralsea_rope = sue_plan.make_rope(battles_rope, "coralsea")
    saratoga_keg = kegunit_shop("USS Saratoga")
    assert sue_plan.keg_exists(battles_rope) is False
    assert sue_plan.keg_exists(coralsea_rope) is False

    # WHEN
    sue_plan.set_keg_obj(saratoga_keg, parent_rope=coralsea_rope)

    # THEN
    assert sue_plan.keg_exists(battles_rope)
    assert sue_plan.keg_exists(coralsea_rope)


def test_PlanUnit_del_keg_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_rope = sue_plan.kegroot.get_keg_rope()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.del_keg_obj(rope=root_rope)
    assert str(excinfo.value) == "Kegroot cannot be deleted"


def test_PlanUnit_del_keg_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_plan.make_rope(wk_rope, sun_str)
    assert sue_plan.get_keg_obj(wk_rope)
    assert sue_plan.get_keg_obj(sun_rope)

    # WHEN
    sue_plan.del_keg_obj(rope=wk_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_obj(wk_rope)
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{wk_rope}'"
    new_sun_rope = sue_plan.make_l1_rope("Sun")
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_obj(new_sun_rope)
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{new_sun_rope}'"


def test_PlanUnit_del_keg_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    sun_str = "Sun"
    old_sun_rope = sue_plan.make_rope(wk_rope, sun_str)
    assert sue_plan.get_keg_obj(old_sun_rope)

    # WHEN
    sue_plan.del_keg_obj(rope=wk_rope, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_obj(old_sun_rope)
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{old_sun_rope}'"
    new_sun_rope = sue_plan.make_l1_rope(sun_str)
    assert sue_plan.get_keg_obj(new_sun_rope)
    new_sun_keg = sue_plan.get_keg_obj(new_sun_rope)
    assert new_sun_keg.parent_rope == sue_plan.kegroot.get_keg_rope()


def test_PlanUnit_del_keg_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_rope = sue_plan.make_rope(usa_rope, texas_str)
    usa_oregon_rope = sue_plan.make_rope(usa_rope, oregon_str)
    nation_texas_rope = sue_plan.make_rope(nation_rope, texas_str)
    nation_oregon_rope = sue_plan.make_rope(nation_rope, oregon_str)
    assert sue_plan.keg_exists(usa_rope)
    assert sue_plan.keg_exists(usa_texas_rope)
    assert sue_plan.keg_exists(usa_oregon_rope)
    assert sue_plan.keg_exists(nation_texas_rope) is False
    assert sue_plan.keg_exists(nation_oregon_rope) is False

    # WHEN
    sue_plan.del_keg_obj(rope=usa_rope, del_children=False)

    # THEN
    assert sue_plan.keg_exists(nation_texas_rope)
    assert sue_plan.keg_exists(nation_oregon_rope)
    assert sue_plan.keg_exists(usa_texas_rope) is False
    assert sue_plan.keg_exists(usa_oregon_rope) is False
    assert sue_plan.keg_exists(usa_rope) is False


def test_PlanUnit_del_keg_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    sem_jour_rope = sue_plan.make_l1_rope("sem_jours")
    mon_rope = sue_plan.make_rope(sem_jour_rope, "Mon")
    assert sue_plan.get_keg_obj(mon_rope)

    # WHEN
    sue_plan.del_keg_obj(rope=mon_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_obj(mon_rope)
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{mon_rope}'"


def test_PlanUnit_del_keg_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    usa_texas_rope = sue_plan.make_rope(usa_rope, texas_str)
    assert sue_plan.get_keg_obj(usa_texas_rope)

    # WHEN
    sue_plan.del_keg_obj(rope=usa_texas_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_obj(usa_texas_rope)
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{usa_texas_rope}'"


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario00_Star():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    print(f"{casa_rope=}")
    old_star = sue_plan.kegroot.kids[exx.casa].star
    assert old_star == 30

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, star=23)

    # THEN
    new_star = sue_plan.kegroot.kids[exx.casa].star
    assert new_star == 23


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario01_keg_uid():
    # ESTABLISH:
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # keg_uid: int = None,
    sue_plan.kegroot.kids[exx.casa].keg_uid = 34
    x_keg_uid = sue_plan.kegroot.kids[exx.casa].keg_uid
    assert x_keg_uid == 34

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, keg_uid=23)

    # THEN
    keg_uid_new = sue_plan.kegroot.kids[exx.casa].keg_uid
    assert keg_uid_new == 23


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario02_begin_close():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # begin: float = None,
    # close: float = None,
    sue_plan.kegroot.kids[exx.casa].begin = 39
    x_begin = sue_plan.kegroot.kids[exx.casa].begin
    assert x_begin == 39

    # WHEN
    sue_plan.kegroot.kids[exx.casa].close = 43

    # THEN
    x_close = sue_plan.kegroot.kids[exx.casa].close
    assert x_close == 43

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, begin=25, close=29)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].begin == 25
    assert sue_plan.kegroot.kids[exx.casa].close == 29


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario03_gogo_want_stop_want():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # gogo_want: float = None,
    # stop_want: float = None,
    sue_plan.kegroot.kids[exx.casa].gogo_want = 439
    x_gogo_want = sue_plan.kegroot.kids[exx.casa].gogo_want
    assert x_gogo_want == 439

    # WHEN
    sue_plan.kegroot.kids[exx.casa].stop_want = 443

    # THEN
    x_stop_want = sue_plan.kegroot.kids[exx.casa].stop_want
    assert x_stop_want == 443

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, gogo_want=425, stop_want=429)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].gogo_want == 425
    assert sue_plan.kegroot.kids[exx.casa].stop_want == 429


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario04_factunits():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # factunit: factunit_shop = None,
    # sue_plan.kegroot.kids[exx.casa].factunits = None
    assert sue_plan.kegroot.kids[exx.casa].factunits == {}
    sem_jours_rope = sue_plan.make_l1_rope("sem_jours")
    fact_rope = sue_plan.make_rope(sem_jours_rope, "Sun")
    x_factunit = factunit_shop(fact_context=fact_rope, fact_state=fact_rope)

    casa_factunits = sue_plan.kegroot.kids[exx.casa].factunits
    print(f"{casa_factunits=}")

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, factunit=x_factunit)
    casa_factunits = sue_plan.kegroot.kids[exx.casa].factunits
    print(f"{casa_factunits=}")

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].factunits == {
        x_factunit.fact_context: x_factunit
    }


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario05_awardunit():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # awardunit: dict = None,
    sue_plan.kegroot.kids[exx.casa].awardunits = {
        "fun": awardunit_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    awardunits = sue_plan.kegroot.kids[exx.casa].awardunits
    assert awardunits == {
        "fun": awardunit_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    x_awardunit = awardunit_shop(awardee_title="fun", give_force=4, take_force=8)

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, awardunit=x_awardunit)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].awardunits == {"fun": x_awardunit}


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario06_is_expanded():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # is_expanded: dict = None,
    sue_plan.kegroot.kids[exx.casa].is_expanded = "what"
    is_expanded = sue_plan.kegroot.kids[exx.casa].is_expanded
    assert is_expanded == "what"

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, is_expanded=True)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].is_expanded is True


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario07_pledge():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # pledge: dict = None,
    sue_plan.kegroot.kids[exx.casa].pledge = "funfun3"
    pledge = sue_plan.kegroot.kids[exx.casa].pledge
    assert pledge == "funfun3"

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, pledge=True)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].pledge is True


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario08_healerunit():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # healerunit:
    sue_plan.kegroot.kids[exx.casa].healerunit = "fun3rol"
    src_healerunit = sue_plan.kegroot.kids[exx.casa].healerunit
    assert src_healerunit == "fun3rol"

    # WHEN
    x_healerunit = healerunit_shop({exx.sue, exx.yao})
    sue_plan.add_personunit(exx.sue)
    sue_plan.add_personunit(exx.yao)
    sue_plan.edit_keg_attr(casa_rope, healerunit=x_healerunit)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].healerunit == x_healerunit


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario09_problem_bool():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    # _problem_bool: bool
    sue_plan.kegroot.kids[exx.casa].problem_bool = "fun3rol"
    src_problem_bool = sue_plan.kegroot.kids[exx.casa].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, problem_bool=x_problem_bool)

    # THEN
    assert sue_plan.kegroot.kids[exx.casa].problem_bool == x_problem_bool


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario10_laborunit():
    # ESTABLISH
    xio_plan = planunit_shop("Xio")
    run_str = "run"
    run_rope = xio_plan.make_l1_rope(run_str)
    xio_plan.set_l1_keg(kegunit_shop(run_str))
    run_keg = xio_plan.get_keg_obj(run_rope)
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(exx.sue)
    assert run_keg.laborunit == laborunit_shop()

    # WHEN
    xio_plan.edit_keg_attr(run_rope, laborunit=sue_laborunit)

    # THEN
    assert run_keg.laborunit == sue_laborunit


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario11_reasonunit():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sem_jour_str = "sem_jours"
    sem_jour_rope = sue_plan.make_l1_rope(sem_jour_str)
    wed_rope = sue_plan.make_rope(sem_jour_rope, exx.wed)

    wed_case = caseunit_shop(reason_state=wed_rope)
    casa_wk_reason = reasonunit_shop(sem_jour_rope, {wed_case.reason_state: wed_case})
    print(f"{type(casa_wk_reason.reason_context)=}")
    print(f"{casa_wk_reason.reason_context=}")

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    assert casa_keg.reasonunits is not None
    print(casa_keg.reasonunits)
    assert casa_keg.reasonunits[sem_jour_rope] is not None
    assert casa_keg.reasonunits[sem_jour_rope] == casa_wk_reason


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario12_reasonunit_knot():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    wk_rope = sue_plan.make_l1_rope("sem_jours")
    wed_rope = sue_plan.make_rope(wk_rope, "Wed")

    before_wk_reason = reasonunit_shop(wk_rope, knot=exx.slash)
    before_wk_reason.set_case(wed_rope)
    assert before_wk_reason.knot == exx.slash

    # WHEN
    sue_plan.edit_keg_attr(casa_rope, reason=before_wk_reason)

    # THEN
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    wk_reasonunit = casa_keg.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != exx.slash
    assert wk_reasonunit.knot == sue_plan.knot


def test_PlanUnit_edit_keg_attr_SetNestedKegUnitAttr_Scenario13_reason_context_knot():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", knot=exx.slash)
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    wk_rope = bob_plan.make_l1_rope(exx.wk)
    wed_rope = bob_plan.make_rope(wk_rope, exx.wed)
    bob_plan.set_l1_keg(kegunit_shop(exx.casa))
    bob_plan.set_l1_keg(kegunit_shop(exx.wk))
    bob_plan.set_keg_obj(kegunit_shop(exx.wed), wk_rope)
    print(f"{bob_plan.kegroot.kids.keys()=}")
    wed_keg = bob_plan.get_keg_obj(wed_rope)
    assert wed_keg.knot == exx.slash
    assert wed_keg.knot == bob_plan.knot

    # WHEN
    bob_plan.edit_keg_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_keg = bob_plan.get_keg_obj(casa_rope)
    assert casa_keg.knot == exx.slash
    wk_reasonunit = casa_keg.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != ","
    assert wk_reasonunit.knot == bob_plan.knot


def test_PlanUnit_edit_keg_attr_RaisesError_SetNestedKegUnitAttr_Scenario13_reason_context_knot():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    wk_rope = bob_plan.make_l1_rope(exx.wk)
    incorrect_wed_rope = bob_plan.make_l1_rope(exx.wed)
    assert not is_sub_rope(wk_rope, incorrect_wed_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_plan.edit_keg_attr(
            casa_rope, reason_context=wk_rope, reason_case=incorrect_wed_rope
        )
    exception_str = f"""Keg cannot edit reason because reason_case is not sub_rope to reason_context 
reason_context: {wk_rope}
reason_case:    {incorrect_wed_rope}"""
    assert str(excinfo.value) == exception_str


def test_PlanUnit_edit_keg_attr_RaisesError_Scenario15_When_healerunit_healer_names_DoNotExist():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    casa_rope = yao_plan.make_l1_rope(exx.casa)
    yao_plan.set_l1_keg(kegunit_shop(exx.casa))
    jour_str = "jour_range"
    jour_keg = kegunit_shop(jour_str, begin=44, close=110)
    yao_plan.set_l1_keg(jour_keg)

    casa_keg = yao_plan.get_keg_obj(casa_rope)
    assert casa_keg.begin is None
    assert casa_keg.close is None

    # WHEN / THEN
    x_healerunit = healerunit_shop({exx.sue})
    with pytest_raises(Exception) as excinfo:
        yao_plan.edit_keg_attr(casa_rope, healerunit=x_healerunit)
    exception_str = f"Keg cannot edit healerunit because group_title '{exx.sue}' does not exist as group in Plan"
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_keg_ScenarioXX_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    bob_plan.set_l1_keg(kegunit_shop(exx.casa))
    bob_plan.set_l1_keg(kegunit_shop(exx.swim))

    # WHEN
    keg_list = list(bob_plan.kegroot.kids.values())

    # THEN
    assert keg_list[0].keg_label == exx.casa


def test_PlanUnit_set_keg_ScenarioXX_adoptee_RaisesErrorIfAdopteeKegDoesNotHaveParent():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_plan.make_l1_rope(sports_str)
    bob_plan.set_l1_keg(kegunit_shop(sports_str))
    bob_plan.set_keg_obj(kegunit_shop(exx.swim), parent_rope=sports_rope)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_rope = bob_plan.make_rope(sports_rope, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_plan.set_keg_obj(
            keg_kid=kegunit_shop(summer_str),
            parent_rope=sports_rope,
            adoptees=[exx.swim, hike_str],
        )
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{hike_rope}'"


def test_PlanUnit_set_keg_ScenarioXX_adoptee_AddsAdoptee():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_plan.make_l1_rope(sports_str)
    bob_plan.set_l1_keg(kegunit_shop(sports_str))
    bob_plan.set_keg_obj(kegunit_shop(exx.swim), parent_rope=sports_rope)
    hike_str = "hike"
    bob_plan.set_keg_obj(kegunit_shop(hike_str), parent_rope=sports_rope)

    sports_swim_rope = bob_plan.make_rope(sports_rope, exx.swim)
    sports_hike_rope = bob_plan.make_rope(sports_rope, hike_str)
    assert bob_plan.keg_exists(sports_swim_rope)
    assert bob_plan.keg_exists(sports_hike_rope)
    summer_str = "summer"
    summer_rope = bob_plan.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_plan.make_rope(summer_rope, exx.swim)
    summer_hike_rope = bob_plan.make_rope(summer_rope, hike_str)
    assert bob_plan.keg_exists(summer_swim_rope) is False
    assert bob_plan.keg_exists(summer_hike_rope) is False

    # WHEN / THEN
    bob_plan.set_keg_obj(
        keg_kid=kegunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[exx.swim, hike_str],
    )

    # THEN
    summer_keg = bob_plan.get_keg_obj(summer_rope)
    print(f"{summer_keg.kids.keys()=}")
    assert bob_plan.keg_exists(summer_swim_rope)
    assert bob_plan.keg_exists(summer_hike_rope)
    assert bob_plan.keg_exists(sports_swim_rope) is False
    assert bob_plan.keg_exists(sports_hike_rope) is False


def test_PlanUnit_set_keg_ScenarioXX_bundling_SetsNewParentWithstarEqualToSumOfAdoptedKegs():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_plan.make_l1_rope(sports_str)
    bob_plan.set_l1_keg(kegunit_shop(sports_str, star=2))
    swim_star = 3
    bob_plan.set_keg_obj(kegunit_shop(exx.swim, star=swim_star), sports_rope)
    hike_str = "hike"
    hike_star = 5
    bob_plan.set_keg_obj(kegunit_shop(hike_str, star=hike_star), sports_rope)
    bball_str = "bball"
    bball_star = 7
    bob_plan.set_keg_obj(kegunit_shop(bball_str, star=bball_star), sports_rope)

    sports_swim_rope = bob_plan.make_rope(sports_rope, exx.swim)
    sports_hike_rope = bob_plan.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_plan.make_rope(sports_rope, bball_str)
    assert bob_plan.get_keg_obj(sports_swim_rope).star == swim_star
    assert bob_plan.get_keg_obj(sports_hike_rope).star == hike_star
    assert bob_plan.get_keg_obj(sports_bball_rope).star == bball_star
    summer_str = "summer"
    summer_rope = bob_plan.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_plan.make_rope(summer_rope, exx.swim)
    summer_hike_rope = bob_plan.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_plan.make_rope(summer_rope, bball_str)
    assert bob_plan.keg_exists(summer_swim_rope) is False
    assert bob_plan.keg_exists(summer_hike_rope) is False
    assert bob_plan.keg_exists(summer_bball_rope) is False

    # WHEN / THEN
    bob_plan.set_keg_obj(
        keg_kid=kegunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[exx.swim, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_plan.get_keg_obj(summer_rope).star == swim_star + hike_star
    assert bob_plan.get_keg_obj(summer_swim_rope).star == swim_star
    assert bob_plan.get_keg_obj(summer_hike_rope).star == hike_star
    assert bob_plan.keg_exists(summer_bball_rope) is False
    assert bob_plan.keg_exists(sports_swim_rope) is False
    assert bob_plan.keg_exists(sports_hike_rope) is False
    assert bob_plan.keg_exists(sports_bball_rope)


def test_PlanUnit_del_keg_obj_DeletingBundledKegReturnsKegsToOriginalState():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_plan.make_l1_rope(sports_str)
    bob_plan.set_l1_keg(kegunit_shop(sports_str, star=2))
    swim_star = 3
    bob_plan.set_keg_obj(kegunit_shop(exx.swim, star=swim_star), sports_rope)
    hike_str = "hike"
    hike_star = 5
    bob_plan.set_keg_obj(kegunit_shop(hike_str, star=hike_star), sports_rope)
    bball_str = "bball"
    bball_star = 7
    bob_plan.set_keg_obj(kegunit_shop(bball_str, star=bball_star), sports_rope)

    sports_swim_rope = bob_plan.make_rope(sports_rope, exx.swim)
    sports_hike_rope = bob_plan.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_plan.make_rope(sports_rope, bball_str)
    assert bob_plan.get_keg_obj(sports_swim_rope).star == swim_star
    assert bob_plan.get_keg_obj(sports_hike_rope).star == hike_star
    assert bob_plan.get_keg_obj(sports_bball_rope).star == bball_star
    summer_str = "summer"
    summer_rope = bob_plan.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_plan.make_rope(summer_rope, exx.swim)
    summer_hike_rope = bob_plan.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_plan.make_rope(summer_rope, bball_str)
    assert bob_plan.keg_exists(summer_swim_rope) is False
    assert bob_plan.keg_exists(summer_hike_rope) is False
    assert bob_plan.keg_exists(summer_bball_rope) is False
    bob_plan.set_keg_obj(
        keg_kid=kegunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[exx.swim, hike_str],
        bundling=True,
    )
    assert bob_plan.get_keg_obj(summer_rope).star == swim_star + hike_star
    assert bob_plan.get_keg_obj(summer_swim_rope).star == swim_star
    assert bob_plan.get_keg_obj(summer_hike_rope).star == hike_star
    assert bob_plan.keg_exists(summer_bball_rope) is False
    assert bob_plan.keg_exists(sports_swim_rope) is False
    assert bob_plan.keg_exists(sports_hike_rope) is False
    assert bob_plan.keg_exists(sports_bball_rope)
    print(f"{bob_plan._keg_dict.keys()=}")

    # WHEN
    bob_plan.del_keg_obj(rope=summer_rope, del_children=False)

    # THEN
    sports_swim_keg = bob_plan.get_keg_obj(sports_swim_rope)
    sports_hike_keg = bob_plan.get_keg_obj(sports_hike_rope)
    sports_bball_keg = bob_plan.get_keg_obj(sports_bball_rope)
    assert sports_swim_keg.star == swim_star
    assert sports_hike_keg.star == hike_star
    assert sports_bball_keg.star == bball_star


def test_PlanUnit_edit_keg_attr_DeletesKegUnit_awardunits():
    # ESTABLISH
    yao_plan = planunit_shop(exx.yao)
    yao_plan.add_personunit(exx.yao)
    yao_plan.add_personunit(exx.zia)
    yao_plan.add_personunit(exx.xio)

    swim_rope = yao_plan.make_l1_rope(exx.swim)

    yao_plan.set_l1_keg(kegunit_shop(exx.swim))
    awardunit_yao = awardunit_shop(exx.yao, give_force=10)
    awardunit_zia = awardunit_shop(exx.zia, give_force=10)
    awardunit_Xio = awardunit_shop(exx.xio, give_force=10)

    swim_keg = yao_plan.get_keg_obj(swim_rope)
    yao_plan.edit_keg_attr(swim_rope, awardunit=awardunit_yao)
    yao_plan.edit_keg_attr(swim_rope, awardunit=awardunit_zia)
    yao_plan.edit_keg_attr(swim_rope, awardunit=awardunit_Xio)

    assert len(swim_keg.awardunits) == 3
    assert len(yao_plan.kegroot.kids[exx.swim].awardunits) == 3

    # WHEN
    yao_plan.edit_keg_attr(swim_rope, awardunit_del=exx.yao)

    # THEN
    swim_keg = yao_plan.get_keg_obj(swim_rope)
    print(f"{swim_keg.keg_label=}")
    print(f"{swim_keg.awardunits=}")
    print(f"{swim_keg.awardheirs=}")

    assert len(yao_plan.kegroot.kids[exx.swim].awardunits) == 2


def test_PlanUnit__get_filtered_awardunits_keg_RemovesPerson_awardunits():
    # ESTABLISH
    example_plan = planunit_shop(exx.bob)
    xia_str = "Xia"
    hike_str = ";hikers"
    example_plan.add_personunit(xia_str)
    example_plan.get_person(xia_str).add_membership(exx.run)

    sports_str = "sports"
    sports_rope = example_plan.make_l1_rope(sports_str)
    example_plan.set_l1_keg(kegunit_shop(sports_str))
    example_plan.edit_keg_attr(sports_rope, awardunit=awardunit_shop(exx.run))
    example_plan.edit_keg_attr(sports_rope, awardunit=awardunit_shop(hike_str))
    example_plan_sports_keg = example_plan.get_keg_obj(sports_rope)
    assert len(example_plan_sports_keg.awardunits) == 2
    bob_plan = planunit_shop(exx.bob)
    bob_plan.add_personunit(xia_str)
    bob_plan.get_person(xia_str).add_membership(exx.run)
    print(f"{example_plan_sports_keg.awardunits=}")

    # WHEN
    cleaned_keg = bob_plan._get_filtered_awardunits_keg(example_plan_sports_keg)

    # THEN
    assert len(cleaned_keg.awardunits) == 1
    assert list(cleaned_keg.awardunits.keys()) == [exx.run]


def test_PlanUnit__get_filtered_awardunits_keg_RemovesGroup_awardunit():
    # ESTABLISH
    example_plan = planunit_shop(exx.bob)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_plan.add_personunit(xia_str)
    example_plan.add_personunit(zoa_str)

    swim_rope = example_plan.make_l1_rope(exx.swim)
    example_plan.set_l1_keg(kegunit_shop(exx.swim))
    example_plan.edit_keg_attr(swim_rope, awardunit=awardunit_shop(xia_str))
    example_plan.edit_keg_attr(swim_rope, awardunit=awardunit_shop(zoa_str))
    example_plan_swim_keg = example_plan.get_keg_obj(swim_rope)
    assert len(example_plan_swim_keg.awardunits) == 2
    bob_plan = planunit_shop(exx.bob)
    bob_plan.add_personunit(xia_str)

    # WHEN
    cleaned_keg = bob_plan._get_filtered_awardunits_keg(example_plan_swim_keg)

    # THEN
    assert len(cleaned_keg.awardunits) == 1
    assert list(cleaned_keg.awardunits.keys()) == [xia_str]


def test_PlanUnit_set_keg_ScenarioXX_SetsKeg_awardunits():
    # ESTABLISH
    example_plan = planunit_shop(exx.bob)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_plan.add_personunit(xia_str)
    example_plan.add_personunit(zoa_str)

    casa_rope = example_plan.make_l1_rope(exx.casa)
    swim_rope = example_plan.make_l1_rope(exx.swim)
    example_plan.set_l1_keg(kegunit_shop(exx.casa))
    example_plan.set_l1_keg(kegunit_shop(exx.swim))
    example_plan.edit_keg_attr(swim_rope, awardunit=awardunit_shop(xia_str))
    example_plan.edit_keg_attr(swim_rope, awardunit=awardunit_shop(zoa_str))
    example_plan_swim_keg = example_plan.get_keg_obj(swim_rope)
    assert len(example_plan_swim_keg.awardunits) == 2
    bob_plan = planunit_shop(exx.bob)
    bob_plan.add_personunit(xia_str)

    # WHEN
    bob_plan.set_l1_keg(example_plan_swim_keg, create_missing_kegs=False)

    # THEN
    bob_plan_swim_keg = bob_plan.get_keg_obj(swim_rope)
    assert len(bob_plan_swim_keg.awardunits) == 1
    assert list(bob_plan_swim_keg.awardunits.keys()) == [xia_str]


def test_PlanUnit_get_keg_obj_ReturnsKeg():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    brazil_str = "Brazil"
    brazil_rope = sue_plan.make_rope(nation_rope, brazil_str)

    # WHEN
    brazil_keg = sue_plan.get_keg_obj(rope=brazil_rope)

    # THEN
    assert brazil_keg is not None
    assert brazil_keg.keg_label == brazil_str

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wk_keg = sue_plan.get_keg_obj(rope=wk_rope)

    # THEN
    assert wk_keg is not None
    assert wk_keg.keg_label == wk_str

    # WHEN
    root_keg = sue_plan.get_keg_obj(sue_plan.kegroot.get_keg_rope())

    # THEN
    assert root_keg is not None
    assert root_keg.get_keg_rope() == sue_plan.kegroot.get_keg_rope()

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_rope = sue_plan.make_l1_rope(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_obj(rope=wrong_rope)
    assert str(excinfo.value) == f"get_keg_obj failed. no keg at '{wrong_rope}'"


def test_PlanUnit_keg_exists_ReturnsBool():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    cat_rope = sue_plan.make_l1_rope("cat have dinner")
    wk_rope = sue_plan.make_l1_rope("sem_jours")
    casa_rope = sue_plan.make_l1_rope("casa")
    nation_rope = sue_plan.make_l1_rope("nation")
    sun_rope = sue_plan.make_rope(wk_rope, "Sun")
    mon_rope = sue_plan.make_rope(wk_rope, "Mon")
    tue_rope = sue_plan.make_rope(wk_rope, "Tue")
    wed_rope = sue_plan.make_rope(wk_rope, "Wed")
    thu_rope = sue_plan.make_rope(wk_rope, "Thur")
    fri_rope = sue_plan.make_rope(wk_rope, "Fri")
    sat_rope = sue_plan.make_rope(wk_rope, "Sat")
    france_rope = sue_plan.make_rope(nation_rope, "France")
    brazil_rope = sue_plan.make_rope(nation_rope, "Brazil")
    usa_rope = sue_plan.make_rope(nation_rope, "USA")
    texas_rope = sue_plan.make_rope(usa_rope, "Texas")
    oregon_rope = sue_plan.make_rope(usa_rope, "Oregon")
    # do not exist in plan
    sports_rope = sue_plan.make_l1_rope("sports")
    swim_rope = sue_plan.make_rope(sports_rope, "swimming")
    idaho_rope = sue_plan.make_rope(usa_rope, "Idaho")
    japan_rope = sue_plan.make_rope(nation_rope, "Japan")

    # WHEN / THEN
    assert sue_plan.keg_exists("") is False
    assert sue_plan.keg_exists(None) is False
    assert sue_plan.keg_exists(sue_plan.kegroot.get_keg_rope())
    assert sue_plan.keg_exists(cat_rope)
    assert sue_plan.keg_exists(wk_rope)
    assert sue_plan.keg_exists(casa_rope)
    assert sue_plan.keg_exists(nation_rope)
    assert sue_plan.keg_exists(sun_rope)
    assert sue_plan.keg_exists(mon_rope)
    assert sue_plan.keg_exists(tue_rope)
    assert sue_plan.keg_exists(wed_rope)
    assert sue_plan.keg_exists(thu_rope)
    assert sue_plan.keg_exists(fri_rope)
    assert sue_plan.keg_exists(sat_rope)
    assert sue_plan.keg_exists(usa_rope)
    assert sue_plan.keg_exists(france_rope)
    assert sue_plan.keg_exists(brazil_rope)
    assert sue_plan.keg_exists(texas_rope)
    assert sue_plan.keg_exists(oregon_rope)
    assert sue_plan.keg_exists(to_rope("B")) is False
    assert sue_plan.keg_exists(sports_rope) is False
    assert sue_plan.keg_exists(swim_rope) is False
    assert sue_plan.keg_exists(idaho_rope) is False
    assert sue_plan.keg_exists(japan_rope) is False


def test_PlanUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_planunit = planunit_shop("Bob")
    assert not bob_planunit.offtrack_fund

    # WHEN
    bob_planunit.set_offtrack_fund() == 0

    # THEN
    assert bob_planunit.offtrack_fund == 0

    # ESTABLISH
    casa_rope = bob_planunit.make_l1_rope(exx.casa)
    wk_rope = bob_planunit.make_l1_rope(exx.wk)
    wed_rope = bob_planunit.make_rope(wk_rope, exx.wed)
    casa_keg = kegunit_shop(exx.casa, fund_onset=70, fund_cease=170)
    wk_keg = kegunit_shop(exx.wk, fund_onset=70, fund_cease=75)
    wed_keg = kegunit_shop(exx.wed, fund_onset=72, fund_cease=75)
    casa_keg.parent_rope = bob_planunit.kegroot.get_keg_rope()
    wk_keg.parent_rope = bob_planunit.kegroot.get_keg_rope()
    wed_keg.parent_rope = wk_rope
    bob_planunit.set_l1_keg(casa_keg)
    bob_planunit.set_l1_keg(wk_keg)
    bob_planunit.set_keg_obj(wed_keg, wk_rope)
    bob_planunit.offtrack_kids_star_set.add(casa_rope)
    bob_planunit.offtrack_kids_star_set.add(wk_rope)
    assert bob_planunit.offtrack_fund == 0

    # WHEN
    bob_planunit.set_offtrack_fund()

    # THEN
    assert bob_planunit.offtrack_fund == 105

    # WHEN
    bob_planunit.offtrack_kids_star_set.add(wed_rope)
    bob_planunit.set_offtrack_fund()

    # THEN
    assert bob_planunit.offtrack_fund == 108


def test_PlanUnit_allot_offtrack_fund_SetsCharUnit_fund_take_fund_give():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    bob_planunit = planunit_shop(exx.bob)
    bob_planunit.add_personunit(exx.bob)
    bob_planunit.add_personunit(exx.yao, person_cred_lumen=2)
    bob_planunit.add_personunit(exx.sue, person_debt_lumen=2)
    bob_planunit.set_offtrack_fund()
    assert bob_planunit.offtrack_fund == 0

    # WHEN
    bob_planunit._allot_offtrack_fund()

    # THEN
    assert bob_planunit.get_person(exx.bob).fund_give == 0
    assert bob_planunit.get_person(exx.bob).fund_take == 0
    assert bob_planunit.get_person(exx.yao).fund_give == 0
    assert bob_planunit.get_person(exx.yao).fund_take == 0
    assert bob_planunit.get_person(exx.sue).fund_give == 0
    assert bob_planunit.get_person(exx.sue).fund_take == 0

    # WHEN
    casa_rope = bob_planunit.make_l1_rope(exx.casa)
    wk_rope = bob_planunit.make_l1_rope(exx.wk)
    wed_rope = bob_planunit.make_rope(wk_rope, exx.wed)
    casa_keg = kegunit_shop(exx.casa, fund_onset=70, fund_cease=170)
    wk_keg = kegunit_shop(exx.wk, fund_onset=70, fund_cease=75)
    wed_keg = kegunit_shop(exx.wed, fund_onset=72, fund_cease=75)
    casa_keg.parent_rope = bob_planunit.kegroot.get_keg_rope()
    wk_keg.parent_rope = bob_planunit.kegroot.get_keg_rope()
    wed_keg.parent_rope = wk_rope
    bob_planunit.set_l1_keg(casa_keg)
    bob_planunit.set_l1_keg(wk_keg)
    bob_planunit.set_keg_obj(wed_keg, wk_rope)
    bob_planunit.offtrack_kids_star_set.add(casa_rope)
    bob_planunit.offtrack_kids_star_set.add(wk_rope)
    bob_planunit.set_offtrack_fund()
    assert bob_planunit.offtrack_fund == 105

    # WHEN
    bob_planunit._allot_offtrack_fund()

    # THEN
    assert bob_planunit.get_person(exx.bob).fund_give == 26
    assert bob_planunit.get_person(exx.bob).fund_take == 26
    assert bob_planunit.get_person(exx.yao).fund_give == 53
    assert bob_planunit.get_person(exx.yao).fund_take == 26
    assert bob_planunit.get_person(exx.sue).fund_give == 26
    assert bob_planunit.get_person(exx.sue).fund_take == 53

    bob_planunit.offtrack_kids_star_set.add(wed_rope)
    bob_planunit.set_offtrack_fund()

    # THEN
    assert bob_planunit.offtrack_fund == 108
