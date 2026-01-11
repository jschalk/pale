from pytest import raises as pytest_raises
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import get_planunit_with_4_levels
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_cashout_Sets_keeps_justified_WhenPlanUnit_Empty():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified


def test_PlanUnit_cashout_Sets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified


def test_PlanUnit_cashout_Sets_keeps_justified_WhenSingleKegUnit_healerunit_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.set_l1_keg(kegunit_shop("Texas", healerunit=healerunit_shop({"Yao"})))
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified is False


def test_PlanUnit_cashout_Sets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    yao_healerunit = healerunit_shop({exx.yao})
    sue_plan.set_l1_keg(
        kegunit_shop("Texas", healerunit=yao_healerunit, problem_bool=True)
    )
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified


def test_PlanUnit_cashout_Sets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    yao_healerunit = healerunit_shop({exx.yao})

    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    sue_plan.set_l1_keg(kegunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_plan.set_keg_obj(kegunit_shop(ep_str, healerunit=yao_healerunit), texas_rope)
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified


def test_PlanUnit_cashout_Sets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    yao_healerunit = healerunit_shop({"Yao"})
    sue_plan.set_l1_keg(kegunit_shop(texas_str, healerunit=yao_healerunit))
    sue_plan.set_keg_obj(kegunit_shop("El Paso", problem_bool=True), texas_rope)
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified is False


def test_PlanUnit_cashout_RaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    yao_healerunit = healerunit_shop({"Yao"})
    texas_keg = kegunit_shop(texas_str, healerunit=yao_healerunit)
    sue_plan.set_l1_keg(texas_keg)
    elpaso_keg = kegunit_shop("El Paso", problem_bool=True)
    sue_plan.set_keg_obj(elpaso_keg, texas_rope)
    assert sue_plan.keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.cashout(keep_exceptions=True)

    # THEN
    assert (
        str(excinfo.value)
        == f"KegUnit '{elpaso_keg.get_keg_rope()}' cannot sponsor ancestor keeps."
    )


def test_PlanUnit_cashout_Sets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_healerunit = healerunit_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    texas_keg = kegunit_shop(texas_str, healerunit=yao_healerunit, problem_bool=True)
    sue_plan.set_l1_keg(texas_keg)
    elpaso_keg = kegunit_shop("El Paso", healerunit=yao_healerunit, problem_bool=True)
    sue_plan.set_keg_obj(elpaso_keg, texas_rope)
    assert sue_plan.keeps_justified is False

    # WHEN
    sue_plan.cashout()

    # THEN
    assert sue_plan.keeps_justified is False


def test_PlanUnit_get_keg_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_healerunit = healerunit_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    texas_keg = kegunit_shop(texas_str, healerunit=yao_healerunit, problem_bool=True)
    sue_plan.set_l1_keg(texas_keg)
    elpaso_keg = kegunit_shop("El Paso", healerunit=yao_healerunit, problem_bool=True)
    sue_plan.set_keg_obj(elpaso_keg, texas_rope)
    sue_plan.cashout()
    assert sue_plan.keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_keg_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because keeps_justified={sue_plan.keeps_justified}."
    )
