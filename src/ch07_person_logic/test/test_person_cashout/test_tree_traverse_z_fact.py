from pytest import raises as pytest_raises
from src.ch05_reason.reason_main import factheir_shop, factunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_1task_1ceo_minutes_reason_1fact,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_cashout_ChangesKegUnit_pledge_task():
    # ESTABLISH
    yao_person = get_personunit_1task_1ceo_minutes_reason_1fact()
    hr_str = "hr"
    hr_rope = yao_person.make_l1_rope(hr_str)

    # WHEN
    yao_person.add_fact(
        fact_context=hr_rope, fact_state=hr_rope, fact_lower=82, fact_upper=85
    )

    # THEN
    mail_rope = yao_person.make_l1_rope("obtain mail")
    keg_dict = yao_person.get_keg_dict()
    mail_keg = keg_dict.get(mail_rope)
    yao_person.add_fact(
        fact_context=hr_rope, fact_state=hr_rope, fact_lower=82, fact_upper=95
    )
    assert mail_keg.pledge is True
    assert mail_keg.task is False

    # WHEN
    yao_person.cashout()

    # THEN
    mail_keg = yao_person.get_keg_obj(mail_rope)
    assert mail_keg.pledge
    assert mail_keg.task


def test_PersonUnit_cashout_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    zia_person.set_l1_keg(kegunit_shop(exx.casa))
    clean_rope = zia_person.make_rope(casa_rope, exx.clean)
    clean_begin = -3
    clean_close = 7
    clean_keg = kegunit_shop(exx.clean, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_keg = kegunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_keg.stop_want = sweep_stop_want
    zia_person.set_keg_obj(clean_keg, parent_rope=casa_rope)
    zia_person.add_fact(
        fact_context=clean_rope, fact_state=clean_rope, fact_lower=1, fact_upper=5
    )
    assert zia_person.kegroot.factheirs == {}

    # WHEN
    zia_person.cashout()

    # THEN
    assert zia_person.kegroot.factheirs != {}
    clean_factheir = factheir_shop(clean_rope, clean_rope, 1.0, 5.0)
    assert zia_person.kegroot.factheirs == {clean_factheir.fact_context: clean_factheir}


def test_PersonUnit_cashout_RaisesErrorIfNon_RangeRootHasFactUnit():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    casa_rope = zia_person.make_l1_rope(exx.casa)
    zia_person.set_l1_keg(kegunit_shop(exx.casa))
    clean_rope = zia_person.make_rope(casa_rope, exx.clean)
    clean_begin = -3
    clean_close = 7
    clean_keg = kegunit_shop(exx.clean, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_rope = zia_person.make_rope(clean_rope, sweep_str)
    sweep_keg = kegunit_shop(sweep_str, addin=2)
    zia_person.set_keg_obj(clean_keg, parent_rope=casa_rope)
    zia_person.set_keg_obj(sweep_keg, parent_rope=clean_rope)
    zia_person.add_fact(sweep_rope, sweep_rope, fact_lower=1, fact_upper=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_person.cashout()

    # THEN
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_rope}'. A ranged fact keg must have _begin, _close"
    )


def test_PersonUnit_cashout_FactHeirsInherited():
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    swim_rope = zia_person.make_l1_rope(exx.swim)
    zia_person.set_l1_keg(kegunit_shop(exx.swim))
    fast_str = "fast"
    slow_str = "slow"
    fast_rope = zia_person.make_rope(swim_rope, fast_str)
    slow_rope = zia_person.make_rope(swim_rope, slow_str)
    zia_person.set_keg_obj(kegunit_shop(fast_str), parent_rope=swim_rope)
    zia_person.set_keg_obj(kegunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_person.make_l1_rope(earth_str)
    zia_person.set_l1_keg(kegunit_shop(earth_str))

    swim_keg = zia_person.get_keg_obj(swim_rope)
    fast_keg = zia_person.get_keg_obj(fast_rope)
    slow_keg = zia_person.get_keg_obj(slow_rope)
    zia_person.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    assert swim_keg.factheirs == {}
    assert fast_keg.factheirs == {}
    assert slow_keg.factheirs == {}

    # WHEN
    zia_person.cashout()

    # THEN
    assert swim_keg.factheirs != {}
    assert fast_keg.factheirs != {}
    assert slow_keg.factheirs != {}
    factheir_set_range = factheir_shop(earth_rope, earth_rope, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.fact_context: factheir_set_range}
    assert swim_keg.factheirs == factheirs_set_range
    assert fast_keg.factheirs == factheirs_set_range
    assert slow_keg.factheirs == factheirs_set_range
    print(f"{swim_keg.factheirs=}")
    assert len(swim_keg.factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_keg.factheirs.get(earth_rope)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_rope, earth_rope, None, None)
    facts_none_range = {fact_none_range.fact_context: fact_none_range}
    assert swim_keg.factheirs == facts_none_range
    assert fast_keg.factheirs == factheirs_set_range
    assert slow_keg.factheirs == factheirs_set_range

    fact_x1 = swim_keg.factheirs.get(earth_rope)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_PersonUnit_cashout_FactUnitMoldsFactHeir():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_person = personunit_shop("Zia")
    swim_rope = zia_person.make_l1_rope(exx.swim)
    zia_person.set_l1_keg(kegunit_shop(exx.swim))
    swim_keg = zia_person.get_keg_obj(swim_rope)

    fast_str = "fast"
    slow_str = "slow"
    zia_person.set_keg_obj(kegunit_shop(fast_str), parent_rope=swim_rope)
    zia_person.set_keg_obj(kegunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_person.make_l1_rope(earth_str)
    zia_person.set_l1_keg(kegunit_shop(earth_str))

    assert swim_keg.factheirs == {}

    # WHEN
    zia_person.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    zia_person.cashout()

    # THEN
    first_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    first_earthdict = {first_earthheir.fact_context: first_earthheir}
    assert swim_keg.factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(fact_context=earth_rope, fact_state=earth_rope, reason_lower=3.0, reason_upper=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_person.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=3.0, fact_upper=5.0
    )
    zia_person.cashout()

    # THEN
    after_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=3.0, fact_upper=5.0
    )
    after_earthdict = {after_earthheir.fact_context: after_earthheir}
    assert swim_keg.factheirs == after_earthdict


def test_PersonUnit_cashout_FactHeirDeletesFactUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    swim_rope = sue_person.make_l1_rope(exx.swim)
    sue_person.set_l1_keg(kegunit_shop(exx.swim))
    fast_str = "fast"
    slow_str = "slow"
    sue_person.set_keg_obj(kegunit_shop(fast_str), parent_rope=swim_rope)
    sue_person.set_keg_obj(kegunit_shop(slow_str), parent_rope=swim_rope)
    earth_str = "earth"
    earth_rope = sue_person.make_l1_rope(earth_str)
    sue_person.set_l1_keg(kegunit_shop(earth_str))
    swim_keg = sue_person.get_keg_obj(swim_rope)
    first_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=200.0, fact_upper=500.0
    )
    first_earthdict = {first_earthheir.fact_context: first_earthheir}
    sue_person.add_fact(earth_rope, earth_rope, fact_lower=200.0, fact_upper=500.0)
    assert swim_keg.factheirs == {}

    # WHEN
    sue_person.cashout()

    # THEN
    assert swim_keg.factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_rope, earth_rope, fact_lower=3.0, fact_upper=4.0)
    swim_keg.set_factunit(factunit=earth_curb)
    sue_person.cashout()

    # THEN
    assert swim_keg.factheirs == first_earthdict
    assert swim_keg.factunits == {}


def test_PersonUnit_cashout_SetstaskAsComplete():
    # ESTABLISH
    yao_person = get_personunit_1task_1ceo_minutes_reason_1fact()
    mail_str = "obtain mail"
    assert yao_person is not None
    assert len(yao_person.kegroot.kids[mail_str].reasonunits) == 1
    keg_dict = yao_person.get_keg_dict()
    mail_keg = keg_dict.get(yao_person.make_l1_rope(mail_str))
    hr_str = "hr"
    hr_rope = yao_person.make_l1_rope(hr_str)
    yao_person.add_fact(hr_rope, hr_rope, fact_lower=82, fact_upper=85)
    assert mail_keg.pledge
    assert mail_keg.task

    # WHEN
    yao_person.cashout()

    # THEN
    assert mail_keg.pledge
    assert not mail_keg.task
