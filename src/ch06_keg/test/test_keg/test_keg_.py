from src.ch01_allot.allot import default_grain_num_if_None
from src.ch02_person.group import awardunit_shop
from src.ch03_labor.labor import laborunit_shop
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import KegUnit, kegunit_shop
from src.ref.keywords import Ch06Keywords as kw, ExampleStrs as exx


def test_KegUnit_Exists():
    # ESTABLISH
    x_kegunit = KegUnit()

    # WHEN / THEN
    assert x_kegunit
    assert x_kegunit.kids is None
    assert x_kegunit.star is None
    assert x_kegunit.keg_label is None
    assert x_kegunit.uid is None
    assert x_kegunit.reasonunits is None
    assert x_kegunit.reasonheirs is None  # calculated field
    assert x_kegunit.laborunit is None
    assert x_kegunit.laborheir is None  # calculated field
    assert x_kegunit.factunits is None
    assert x_kegunit.factheirs is None  # calculated field
    assert x_kegunit.awardunits is None
    assert x_kegunit.awardlines is None  # calculated field'
    assert x_kegunit.awardheirs is None  # calculated field'
    assert x_kegunit.knot is None
    assert x_kegunit.begin is None
    assert x_kegunit.close is None
    assert x_kegunit.addin is None
    assert x_kegunit.numor is None
    assert x_kegunit.denom is None
    assert x_kegunit.morph is None
    assert x_kegunit.gogo_want is None
    assert x_kegunit.stop_want is None
    assert x_kegunit.pledge is None
    assert x_kegunit.problem_bool is None
    assert x_kegunit.healerunit is None
    # calculated_fields
    assert x_kegunit.range_evaluated is None
    assert x_kegunit.gogo_calc is None
    assert x_kegunit.stop_calc is None
    assert x_kegunit.descendant_pledge_count is None
    assert x_kegunit.is_expanded is None
    assert x_kegunit.all_person_cred is None
    assert x_kegunit.all_person_debt is None
    assert x_kegunit.tree_level is None
    assert x_kegunit.keg_active_hx is None
    assert x_kegunit.fund_ratio is None
    assert x_kegunit.fund_grain is None
    assert x_kegunit.fund_onset is None
    assert x_kegunit.fund_cease is None
    assert x_kegunit.healerunit_ratio is None
    obj_attrs = set(x_kegunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.keg_active,
        kw.keg_active_hx,
        kw.all_person_cred,
        kw.all_person_debt,
        kw.awardheirs,
        kw.awardlines,
        kw.descendant_pledge_count,
        kw.factheirs,
        kw.fund_cease,
        kw.fund_onset,
        kw.fund_ratio,
        kw.gogo_calc,
        kw.healerunit_ratio,
        kw.is_expanded,
        kw.kids,
        kw.laborheir,
        kw.tree_level,
        kw.range_evaluated,
        kw.reasonheirs,
        kw.stop_calc,
        kw.task,
        kw.uid,
        kw.addin,
        kw.awardunits,
        kw.begin,
        kw.knot,
        kw.close,
        kw.keg_label,
        kw.denom,
        kw.factunits,
        kw.fund_grain,
        kw.gogo_want,
        kw.healerunit,
        kw.laborunit,
        kw.star,
        kw.morph,
        kw.numor,
        kw.parent_rope,
        kw.pledge,
        kw.problem_bool,
        kw.reasonunits,
        kw.stop_want,
    }


from pytest import raises as pytest_raises
from src.ch06_keg.keg import kegunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_KegUnit_set_keg_label_Scenario0_SetsAttr():
    # ESTABLISH
    el_paso_str = "El Paso"
    el_paso_keg = kegunit_shop(el_paso_str)
    assert el_paso_keg.keg_label != exx.casa

    # WHEN
    el_paso_keg.set_keg_label(exx.casa)

    # THEN
    assert el_paso_keg.keg_label == exx.casa


def test_KegUnit_set_keg_label_Scenario1_RaisesErrorWhen_keg_label_IsNone():
    # ESTABLISH
    casa_keg = kegunit_shop(exx.casa)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_keg.set_keg_label(keg_label=None)
    assert str(excinfo.value) == "Cannot set Keg's Label empty or None"


def test_kegunit_shop_ReturnsObj_WithOneParameter():
    # ESTABLISH

    # WHEN
    x_kegunit = kegunit_shop(exx.casa)

    # THEN
    assert x_kegunit
    assert x_kegunit.kids == {}
    assert x_kegunit.star == 1
    assert x_kegunit.keg_label == exx.casa
    assert not x_kegunit.uid
    assert not x_kegunit.begin
    assert not x_kegunit.close
    assert not x_kegunit.addin
    assert not x_kegunit.numor
    assert not x_kegunit.denom
    assert not x_kegunit.morph
    assert x_kegunit.pledge is False
    assert x_kegunit.problem_bool is False
    assert x_kegunit.descendant_pledge_count is None
    assert x_kegunit.awardlines == {}
    assert x_kegunit.awardunits == {}
    assert x_kegunit.awardheirs == {}
    assert x_kegunit.is_expanded is True
    assert x_kegunit.factheirs == {}
    assert x_kegunit.factunits == {}
    assert x_kegunit.healerunit == healerunit_shop()
    assert x_kegunit.gogo_calc is None
    assert x_kegunit.stop_calc is None
    assert x_kegunit.tree_level is None
    assert x_kegunit.keg_active_hx == {}
    assert x_kegunit.fund_ratio is None
    assert x_kegunit.fund_grain == default_grain_num_if_None()
    assert x_kegunit.fund_onset is None
    assert x_kegunit.fund_cease is None
    assert x_kegunit.reasonunits == {}
    assert x_kegunit.reasonheirs == {}
    assert x_kegunit.laborunit == laborunit_shop()
    assert x_kegunit.laborheir is None
    assert x_kegunit.knot == default_knot_if_None()
    assert x_kegunit.all_person_cred is None
    assert x_kegunit.all_person_debt is None
    assert x_kegunit.healerunit_ratio == 0


def test_kegunit_shop_Allows_starToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_kegunit = kegunit_shop("run", star=zero_int)
    # THEN
    assert x_kegunit.star == zero_int


def test_kegunit_shop_Allows_doesNotAllow_starToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_kegunit = kegunit_shop("run", star=negative_int)
    # THEN
    zero_int = 0
    assert x_kegunit.star == zero_int


def test_kegunit_shop_ReturnsObj_Given_healerunit_Parameter():
    # ESTABLISH
    x_healerunit = healerunit_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_grain = 88

    # WHEN
    x_kegunit = kegunit_shop(
        exx.clean,
        healerunit=x_healerunit,
        problem_bool=x_problem_bool,
        fund_grain=x_fund_grain,
    )

    # THEN
    assert x_kegunit.healerunit == x_healerunit
    assert x_kegunit.problem_bool == x_problem_bool
    assert x_kegunit.fund_grain == x_fund_grain


def test_kegunit_shop_ReturnsObjWith_awardunits():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardunit = awardunit_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_title = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardunit = awardunit_shop(swim_group_title, swim_give_force, swim_take_force)
    x_awardunits = {
        swim_awardunit.awardee_title: swim_awardunit,
        biker_awardunit.awardee_title: biker_awardunit,
    }

    # WHEN
    sport_str = "sport"
    sport_keg = kegunit_shop(keg_label=sport_str, awardunits=x_awardunits)

    # THEN
    assert sport_keg.awardunits == x_awardunits


def test_kegunit_shop_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_str = "sport"
    sport_keg = kegunit_shop(
        sport_str, gogo_want=sport_gogo_want, stop_want=sport_stop_want
    )

    # THEN
    assert sport_keg.gogo_want == sport_gogo_want
    assert sport_keg.stop_want == sport_stop_want


def test_KegUnit_get_obj_key_ReturnsInfo():
    # ESTABLISH / WHEN
    red_keg = kegunit_shop(exx.red)

    # THEN
    assert red_keg.get_obj_key() == exx.red


def test_KegUnit_set_knot_SetsAttr():
    # ESTABLISH
    casa_keg = kegunit_shop(exx.casa)
    casa_keg.set_parent_rope("")

    # WHEN
    casa_keg.set_knot(exx.slash)

    # THEN
    assert casa_keg.knot == exx.slash


def test_KegUnit_get_obj_key_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(exx.a23, round_str)
    ball_str = "ball"

    # WHEN
    ball_keg = kegunit_shop(keg_label=ball_str, parent_rope=round_rope)

    # THEN
    assert ball_keg.get_obj_key() == ball_str


def test_KegUnit_get_rope_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(exx.a23, round_str, knot=exx.slash)
    ball_str = "ball"

    # WHEN
    ball_keg = kegunit_shop(ball_str, parent_rope=round_rope, knot=exx.slash)

    # THEN
    ball_rope = create_rope(round_rope, ball_str, knot=exx.slash)
    assert ball_keg.get_keg_rope() == ball_rope


def test_KegUnit_set_parent_rope_SetsAttr():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(exx.a23, round_str, knot=exx.slash)
    ball_str = "ball"
    ball_keg = kegunit_shop(ball_str, parent_rope=round_rope, knot=exx.slash)
    assert ball_keg.parent_rope == round_rope

    # WHEN
    sports_rope = create_rope(exx.a23, "sports", knot=exx.slash)
    ball_keg.set_parent_rope(parent_rope=sports_rope)

    # THEN
    assert ball_keg.parent_rope == sports_rope


def test_KegUnit_clear_descendant_pledge_count_ClearsAttrs():
    # ESTABLISH
    ball_str = "ball"
    ball_keg = kegunit_shop(ball_str, descendant_pledge_count=55)
    assert ball_keg.descendant_pledge_count == 55

    # WHEN
    ball_keg.clear_descendant_pledge_count()

    # THEN
    assert ball_keg.descendant_pledge_count is None


def test_KegUnit_add_to_descendant_pledge_count_AddsToCount():
    # ESTABLISH
    ball_str = "ball"
    ball_keg = kegunit_shop(ball_str, descendant_pledge_count=55)
    ball_keg.clear_descendant_pledge_count()
    assert not ball_keg.descendant_pledge_count

    # WHEN
    ball_keg.add_to_descendant_pledge_count(44)

    # THEN
    assert ball_keg.descendant_pledge_count == 44

    # WHEN
    ball_keg.add_to_descendant_pledge_count(33)

    # THEN
    assert ball_keg.descendant_pledge_count == 77


def test_KegUnit_has_begin_close_ReturnsObj():
    # ESTABLISH
    swim_keg = kegunit_shop(exx.swim)
    assert not swim_keg.has_begin_close()
    # WHEN
    swim_keg.begin = 9
    # THEN
    assert not swim_keg.has_begin_close()
    # WHEN
    swim_keg.close = 10
    # THEN
    assert swim_keg.has_begin_close()
    # WHEN
    swim_keg.begin = None
    # THEN
    assert not swim_keg.has_begin_close()


def test_KegUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_keg = kegunit_shop(num_range_str)
    num_range_keg.range_evaluated = True
    num_range_keg.gogo_calc = 3
    num_range_keg.stop_calc = 4
    assert num_range_keg.range_evaluated
    assert num_range_keg.gogo_calc
    assert num_range_keg.stop_calc

    # WHEN
    num_range_keg.clear_gogo_calc_stop_calc()

    # THEN
    assert not num_range_keg.range_evaluated
    assert not num_range_keg.gogo_calc
    assert not num_range_keg.stop_calc


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert not num_range_keg.range_evaluated
    assert num_range_keg.gogo_calc
    assert num_range_keg.stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.range_evaluated
    assert num_range_keg.gogo_calc == init_gogo_calc / num_range_denom
    assert num_range_keg.stop_calc == init_stop_calc / num_range_denom
    assert num_range_keg.gogo_calc == 3
    assert num_range_keg.stop_calc == 6


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc
    assert num_range_keg.stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == 0
    assert num_range_keg.stop_calc == num_range_denom
    assert num_range_keg.gogo_calc == 0
    assert num_range_keg.stop_calc == 7


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc
    assert num_range_keg.stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == 0
    assert (
        num_range_keg.stop_calc == (init_stop_calc - init_gogo_calc) % num_range_denom
    )
    assert num_range_keg.gogo_calc == 0
    assert num_range_keg.stop_calc == 3


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc
    assert num_range_keg.stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == init_gogo_calc % num_range_denom
    assert num_range_keg.stop_calc == init_stop_calc % num_range_denom
    assert num_range_keg.gogo_calc == 1
    assert num_range_keg.stop_calc == 4


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == gogo_want
    assert num_range_keg.stop_calc == stop_want
    assert num_range_keg.gogo_calc == 30
    assert num_range_keg.stop_calc == 40


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc
    assert num_range_keg.gogo_calc == 21
    assert num_range_keg.stop_calc == 45


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == stop_want
    assert num_range_keg.gogo_calc == 21
    assert num_range_keg.stop_calc == 40


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_keg.gogo_calc == gogo_want
    assert num_range_keg.stop_calc == init_stop_calc
    assert num_range_keg.gogo_calc == 30
    assert num_range_keg.stop_calc == 45


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_keg.gogo_calc
    assert not num_range_keg.stop_calc


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_keg.gogo_calc
    assert not num_range_keg.stop_calc


def test_KegUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_keg = kegunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    num_range_keg.gogo_want = gogo_want
    num_range_keg.stop_want = stop_want
    num_range_keg.gogo_calc = init_gogo_calc
    num_range_keg.stop_calc = init_stop_calc
    num_range_keg.denom = num_range_denom
    assert num_range_keg.gogo_calc == init_gogo_calc
    assert num_range_keg.stop_calc == init_stop_calc

    # WHEN
    num_range_keg._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_keg.gogo_calc
    assert not num_range_keg.stop_calc
