from src.ch02_partner.group import awardheir_shop, awardunit_shop
from src.ch03_labor.labor import laborheir_shop, laborunit_shop
from src.ch04_rope.rope import create_rope
from src.ch05_reason.reason_main import (
    caseunit_shop,
    factheir_shop,
    factunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.ch06_keg.keg import kegunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_KegUnit_clear_all_partner_cred_debt_ClearsAttrs():
    # ESTABLISH
    ball_str = "ball"
    ball_keg = kegunit_shop(ball_str, all_partner_cred=55, all_partner_debt=33)
    assert ball_keg.all_partner_cred == 55
    assert ball_keg.all_partner_debt == 33

    # WHEN
    ball_keg.clear_all_partner_cred_debt()

    # THEN
    assert ball_keg.all_partner_cred is None
    assert ball_keg.all_partner_debt is None


def test_KegUnit_set_fund_attr_ReturnsObj():
    # ESTABLISH
    texas_str = "texas"
    texas_keg = kegunit_shop(texas_str)
    swim_str = ";swimmers"
    texas_keg.awardheirs[swim_str] = awardheir_shop(swim_str, 2, 3)
    texas_keg.awardheirs[exx.run] = awardheir_shop(exx.run, 1, 5)
    assert not texas_keg.fund_onset
    assert not texas_keg.fund_cease
    assert not texas_keg.fund_ratio
    swim_awardheir = texas_keg.awardheirs.get(swim_str)
    run_awardheir = texas_keg.awardheirs.get(exx.run)
    assert not swim_awardheir.fund_give
    assert not swim_awardheir.fund_take
    assert not run_awardheir.fund_give
    assert not run_awardheir.fund_take
    x_onset = 70
    x_cease = 100
    x_fund_pool = 120

    # WHEN
    texas_keg.set_fund_attr(x_onset, x_cease, x_fund_pool)

    # THEN
    assert texas_keg.fund_onset == x_onset
    assert texas_keg.fund_cease == x_cease
    assert texas_keg.fund_ratio >= 0.25
    swim_awardheir = texas_keg.awardheirs.get(swim_str)
    run_awardheir = texas_keg.awardheirs.get(exx.run)
    assert swim_awardheir.fund_give == 20
    assert swim_awardheir.fund_take == 11
    assert run_awardheir.fund_give == 10
    assert run_awardheir.fund_take == 19


def test_KegUnit_get_keg_fund_total_ReturnsObj():
    # ESTABLISH
    texas_str = "texas"
    texas_keg = kegunit_shop(texas_str)

    # WHEN / THEN
    assert texas_keg.get_keg_fund_total() == 0

    # WHEN / THEN
    texas_keg.fund_onset = 3
    texas_keg.fund_cease = 14
    assert texas_keg.get_keg_fund_total() == 11


def test_KegUnit_set_awardunit_SetsAttr():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_kegunit = kegunit_shop(sport_str)
    assert not sport_kegunit.awardunits.get(biker_str)

    # WHEN
    sport_kegunit.set_awardunit(awardunit_shop(biker_str))

    # THEN
    assert sport_kegunit.awardunits.get(biker_str)


def test_KegUnit_awardunit_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_kegunit = kegunit_shop(sport_str)
    assert not sport_kegunit.awardunit_exists(biker_str)

    # WHEN
    sport_kegunit.set_awardunit(awardunit_shop(biker_str))

    # THEN
    assert sport_kegunit.awardunit_exists(biker_str)


def test_KegUnit_get_awardunit_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    sport_str = "sport"
    sport_kegunit = kegunit_shop(sport_str)
    sport_kegunit.set_awardunit(awardunit_shop(biker_str))

    # WHEN
    biker_awardunit = sport_kegunit.get_awardunit(biker_str)

    # THEN
    assert biker_awardunit
    assert biker_awardunit.awardee_title == biker_str


def test_KegUnit_set_awardheirs_fund_give_fund_take_SetsAttr_WithValues():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str, biker_give_force, biker_take_force)
    swim_str = "swimmers"
    swim_group_title = swim_str
    swim_give_force = 29
    swim_take_force = 32
    swim_awardheir = awardheir_shop(swim_group_title, swim_give_force, swim_take_force)
    x_awardheirs = {
        swim_awardheir.awardee_title: swim_awardheir,
        biker_awardheir.awardee_title: biker_awardheir,
    }
    sport_str = "sport"
    sport_keg = kegunit_shop(sport_str, awardheirs=x_awardheirs)
    assert sport_keg.fund_grain == 1
    assert len(sport_keg.awardheirs) == 2
    swim_awardheir = sport_keg.awardheirs.get(swim_str)
    assert not swim_awardheir.fund_give
    assert not swim_awardheir.fund_take
    biker_awardheir = sport_keg.awardheirs.get(biker_str)
    assert not biker_awardheir.fund_give
    assert not biker_awardheir.fund_take

    # WHEN
    sport_keg.fund_onset = 91
    sport_keg.fund_cease = 820
    sport_keg.set_awardheirs_fund_give_fund_take()

    # THEN
    print(f"{len(sport_keg.awardheirs)=}")
    swim_awardheir = sport_keg.awardheirs.get(swim_str)
    assert swim_awardheir.fund_give == 516
    assert swim_awardheir.fund_take == 496
    biker_awardheir = sport_keg.awardheirs.get(biker_str)
    assert biker_awardheir.fund_give == 213
    assert biker_awardheir.fund_take == 233


def test_KegUnit_awardheir_exists_ReturnsObj():
    # ESTABLISH
    biker_str = "bikers2"
    biker_awardheir = awardheir_shop(biker_str)
    sport_str = "sport"
    sport_kegunit = kegunit_shop(sport_str)
    assert not sport_kegunit.awardheir_exists()

    # WHEN
    sport_kegunit.awardheirs[biker_str] = biker_awardheir

    # THEN
    assert sport_kegunit.awardheir_exists()


def test_KegUnit_set_awardheirs_fund_give_fund_take_ReturnsObj_NoValues():
    # ESTABLISH /WHEN
    sport_str = "sport"
    sport_keg = kegunit_shop(sport_str)

    # WHEN / THEN
    # does not crash with empty set
    sport_keg.set_awardheirs_fund_give_fund_take()


def test_KegUnit_set_reasonheirsAcceptsNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_rope = create_rope(ball_str)
    run_str = "run"
    run_rope = create_rope(ball_rope, run_str)
    ball_keg = kegunit_shop(ball_str)
    run_case = caseunit_shop(reason_state=run_rope, reason_lower=0, reason_upper=7)
    run_cases = {run_case.reason_state: run_case}
    reasonheir = reasonheir_shop(run_rope, cases=run_cases)
    reasonheirs = {reasonheir.reason_context: reasonheir}
    assert ball_keg.reasonheirs == {}

    # WHEN
    ball_keg.set_reasonheirs(reasonheirs=reasonheirs, person_keg_dict={})

    # THEN
    assert ball_keg.reasonheirs == reasonheirs
    assert id(ball_keg.reasonheirs) != id(reasonheirs)


def test_KegUnit_set_reasonheirsRefusesNewValues():
    # ESTABLISH
    ball_str = "ball"
    ball_rope = create_rope(ball_str)
    run_str = "run"
    run_rope = create_rope(ball_rope, run_str)
    run_case = caseunit_shop(reason_state=run_rope, reason_lower=0, reason_upper=7)
    run_cases = {run_case.reason_state: run_case}
    run_reasonunit = reasonunit_shop(reason_context=run_rope, cases=run_cases)
    run_reasonunits = {run_reasonunit.reason_context: run_reasonunit}
    ball_keg = kegunit_shop(ball_str, reasonunits=run_reasonunits)
    assert ball_keg.reasonunits != {}

    # WHEN
    ball_keg.set_reasonheirs(reasonheirs={}, person_keg_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_rope, cases=run_cases)
    reasonheirs = {reasonheir.reason_context: reasonheir}
    assert ball_keg.reasonheirs == reasonheirs


def test_KegUnit_set_range_inheritors_factheirs_SetsAttrNoParameters():
    # ESTABLISH
    ball_keg = kegunit_shop("ball")
    assert ball_keg.factheirs == {}

    # WHEN
    ball_keg.set_range_inheritors_factheirs(person_keg_dict={}, range_inheritors={})

    # THEN
    assert ball_keg.factheirs == {}


def test_KegUnit_set_range_inheritors_factheirs_SetsAttrNewFactHeir():
    # ESTABLISH
    wk_rope = create_rope(exx.a23, exx.wk)
    wk_reason_lower = 3
    wk_reason_upper = 7
    wk_addin = 10
    wk_keg = kegunit_shop(exx.wk, parent_rope=exx.a23, addin=wk_addin)
    wk_factheir = factheir_shop(wk_rope, wk_rope, wk_reason_lower, wk_reason_upper)
    tue_str = "Tue"
    tue_rope = create_rope(wk_rope, tue_str)
    tue_addin = 100
    tue_keg = kegunit_shop(tue_str, parent_rope=wk_rope, addin=tue_addin)
    ball_str = "ball"
    ball_rope = create_rope(exx.a23, ball_str)
    ball_keg = kegunit_shop(ball_str)
    ball_keg._set_factheir(wk_factheir)
    tue_reasonheirs = {tue_rope: reasonheir_shop(tue_rope, None, False)}
    x_person_keg_dict = {
        wk_keg.get_keg_rope(): wk_keg,
        tue_keg.get_keg_rope(): tue_keg,
    }
    ball_keg.set_reasonheirs(x_person_keg_dict, tue_reasonheirs)

    x_range_inheritors = {tue_rope: wk_rope}
    assert len(ball_keg.reasonheirs) == 1
    assert ball_keg.factheirs == {wk_rope: wk_factheir}
    assert ball_keg.factheirs.get(wk_rope)
    assert len(ball_keg.factheirs) == 1
    assert ball_keg.factheirs.get(tue_rope) is None

    # WHEN
    ball_keg.set_range_inheritors_factheirs(x_person_keg_dict, x_range_inheritors)

    # THEN
    tue_reason_lower = 113
    tue_reason_upper = 117
    tue_factheir = factheir_shop(tue_rope, tue_rope, tue_reason_lower, tue_reason_upper)
    assert len(ball_keg.factheirs) == 2
    assert ball_keg.factheirs == {tue_rope: tue_factheir, wk_rope: wk_factheir}


def test_KegUnit_set_reasonunit_SetsAttr():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    assert not clean_keg.reasonunits.get(dirty_str)

    # WHEN
    clean_keg.set_reasonunit(reasonunit_shop(reason_context=dirty_str))

    # THEN
    assert clean_keg.reasonunits.get(dirty_str)
    x_reasonunit = clean_keg.get_reasonunit(reason_context=dirty_str)
    assert x_reasonunit is not None
    assert x_reasonunit.reason_context == dirty_str


def test_KegUnit_reasonunit_exists_ReturnsObj():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    assert not clean_keg.reasonunit_exists(dirty_str)

    # WHEN
    clean_keg.set_reasonunit(reasonunit_shop(reason_context=dirty_str))

    # THEN
    assert clean_keg.reasonunit_exists(dirty_str)


def test_KegUnit_get_reasonunit_ReturnsObj():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    clean_keg.set_reasonunit(reasonunit_shop(reason_context=dirty_str))

    # WHEN
    x_reasonunit = clean_keg.get_reasonunit(reason_context=dirty_str)

    # THEN
    assert x_reasonunit is not None
    assert x_reasonunit.reason_context == dirty_str


def test_KegUnit_get_reasonheir_ReturnsObj_Scenario0():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    x_reasonheir = reasonheir_shop(reason_context=dirty_str)
    x_reasonheirs = {x_reasonheir.reason_context: x_reasonheir}
    clean_keg.set_reasonheirs(reasonheirs=x_reasonheirs, person_keg_dict={})

    # WHEN
    z_reasonheir = clean_keg.get_reasonheir(reason_context=dirty_str)

    # THEN
    assert z_reasonheir is not None
    assert z_reasonheir.reason_context == dirty_str


def test_KegUnit_get_reasonheir_ReturnsObj_Scenario1_person_keg_IsEmpty():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    x_reasonheir = reasonheir_shop(dirty_str)
    x_reasonheirs = {x_reasonheir.reason_context: x_reasonheir}
    clean_keg.set_reasonheirs(reasonheirs=x_reasonheirs, person_keg_dict={})

    # WHEN
    test6_str = "test6"
    reason_heir_test6 = clean_keg.get_reasonheir(reason_context=test6_str)

    # THEN
    assert reason_heir_test6 is None


def test_KegUnit_set_keg_active_SetsAttr_Scenario0_keg_active_hx_ToNonEmpty():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    assert clean_keg.keg_active_hx == {}

    # WHEN
    clean_keg.set_keg_active(tree_traverse_count=3)
    # THEN
    assert clean_keg.keg_active_hx == {3: True}


def test_KegUnit_set_keg_active_SetAttr_Scenario1_keg_active_hx_ResetToTrue():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    clean_keg.keg_active_hx = {0: True, 4: False}
    assert clean_keg.keg_active_hx != {0: True}
    # WHEN
    clean_keg.set_keg_active(tree_traverse_count=0)
    # THEN
    assert clean_keg.keg_active_hx == {0: True}


def test_KegUnit_set_factunit_SetsAttr():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    assert not clean_keg.factunits.get(dirty_str)

    # WHEN
    clean_keg.set_factunit(factunit_shop(fact_context=dirty_str))

    # THEN
    assert clean_keg.factunits.get(dirty_str)


def test_KegUnit_factunit_exists_ReturnsObj():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    dirty_str = "dirty"
    assert not clean_keg.factunit_exists(dirty_str)

    # WHEN
    clean_keg.set_factunit(factunit_shop(fact_context=dirty_str))

    # THEN
    assert clean_keg.factunit_exists(dirty_str)


# def test_KegUnit_set_keg_active_IfFullactive_hxResetToFalse():
#     # ESTABLISH
# clean_keg = kegunit_shop(exx.clean)
#     clean_keg.set_reason_case(
#         reason_context="testing1,sec",
#         case="testing1,sec,next",
#         reason_lower=None,
#         reason_upper=None,
#         reason_divisor=None,
#     )
#     clean_keg.keg_active_hx = {0: True, 4: False}
#     assert clean_keg.keg_active_hx != {0: False}
#     # WHEN
#     clean_keg.set_keg_active(tree_traverse_count=0)
#     # THEN
#     assert clean_keg.keg_active_hx == {0: False}


def test_KegUnit_record_keg_active_hx_SetsAttr_keg_active_hx():
    # ESTABLISH
    clean_keg = kegunit_shop(exx.clean)
    assert clean_keg.keg_active_hx == {}

    # WHEN
    clean_keg.record_keg_active_hx(0, prev_keg_active=None, now_keg_active=True)
    # THEN
    assert clean_keg.keg_active_hx == {0: True}

    # WHEN
    clean_keg.record_keg_active_hx(1, prev_keg_active=True, now_keg_active=True)
    # THEN
    assert clean_keg.keg_active_hx == {0: True}

    # WHEN
    clean_keg.record_keg_active_hx(2, prev_keg_active=True, now_keg_active=False)
    # THEN
    assert clean_keg.keg_active_hx == {0: True, 2: False}

    # WHEN
    clean_keg.record_keg_active_hx(3, prev_keg_active=False, now_keg_active=False)
    # THEN
    assert clean_keg.keg_active_hx == {0: True, 2: False}

    # WHEN
    clean_keg.record_keg_active_hx(4, prev_keg_active=False, now_keg_active=True)
    # THEN
    assert clean_keg.keg_active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_keg.record_keg_active_hx(0, prev_keg_active=False, now_keg_active=False)
    # THEN
    assert clean_keg.keg_active_hx == {0: False}


def test_KegUnit_set_laborunit_empty_if_None_SetsAttr():
    # ESTABLISH
    run_str = "run"
    run_keg = kegunit_shop(run_str)
    run_keg.laborunit = None
    assert run_keg.laborunit is None

    # WHEN
    run_keg.set_laborunit_empty_if_None()

    # THEN
    assert run_keg.laborunit is not None
    assert run_keg.laborunit == laborunit_shop()


def test_KegUnit_set_laborheir_SetsAttr():
    # ESTABLISH
    swim_str = "swimmers"
    sport_str = "sports"
    sport_keg = kegunit_shop(sport_str)
    sport_keg.laborunit.add_party(party_title=swim_str)
    # assert sport_keg.laborheir is None

    # WHEN
    sport_keg.set_laborheir(parent_laborheir=None, groupunits=None)

    # THEN
    assert sport_keg.laborheir is not None
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_party(party_title=swim_str)
    swim_laborheir = laborheir_shop()
    swim_laborheir.set_partys(
        laborunit=swim_laborunit, parent_laborheir=None, groupunits=None
    )
    assert sport_keg.laborheir == swim_laborheir
