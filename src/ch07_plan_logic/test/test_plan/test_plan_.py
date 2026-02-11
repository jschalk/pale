from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch04_rope.rope import create_rope, default_knot_if_None, get_default_rope
from src.ch07_plan_logic._ref.ch07_semantic_types import RespectNum
from src.ch07_plan_logic.plan_main import PlanUnit, planunit_shop
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PlanUnit_Exists():
    # ESTABLISH /  WHEN
    x_plan = PlanUnit()

    # THEN
    assert x_plan
    assert x_plan.moment_rope is None
    assert x_plan.plan_name is None
    assert x_plan.persons is None
    assert x_plan.kegroot is None
    assert x_plan.credor_respect is None
    assert x_plan.debtor_respect is None
    assert x_plan.max_tree_traverse is None
    assert x_plan.knot is None
    assert x_plan.fund_pool is None
    assert x_plan.fund_grain is None
    assert x_plan.respect_grain is None
    assert x_plan.mana_grain is None
    assert x_plan.last_lesson_id is None
    # calculated attr
    assert x_plan._keg_dict is None
    assert x_plan._keep_dict is None
    assert x_plan._healers_dict is None
    assert x_plan.tree_traverse_count is None
    assert x_plan.rational is None
    assert x_plan.keeps_justified is None
    assert x_plan.keeps_buildable is None
    assert x_plan.sum_healerunit_kegs_fund_total is None
    assert x_plan.offtrack_kids_star_set is None
    assert x_plan.offtrack_fund is None
    assert x_plan.reason_contexts is None
    assert x_plan.range_inheritors is None
    assert str(type(x_plan.kegroot)).find("None") == 8
    obj_attrs = set(x_plan.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        "_keg_dict",
        "_healers_dict",
        "_keep_dict",
        kw.keeps_buildable,
        kw.keeps_justified,
        kw.offtrack_fund,
        kw.offtrack_kids_star_set,
        kw.range_inheritors,
        kw.rational,
        kw.reason_contexts,
        kw.sum_healerunit_kegs_fund_total,
        kw.tree_traverse_count,
        kw.persons,
        kw.knot,
        kw.kegroot,
        kw.credor_respect,
        kw.debtor_respect,
        kw.groupunits,
        kw.moment_rope,
        kw.fund_grain,
        kw.fund_pool,
        kw.last_lesson_id,
        kw.max_tree_traverse,
        kw.plan_name,
        kw.mana_grain,
        kw.respect_grain,
    }


def test_planunit_shop_ReturnsObj_Scenario0_RaiseErrorWhen_moment_rope_IsLabel():
    # ESTABLISH
    iowa_str = "Iowa"

    # WHEN
    with pytest_raises(Exception) as excinfo:
        planunit_shop(plan_name=exx.sue, moment_rope=iowa_str, knot=exx.slash)

    # THEN
    exception_str = (
        f"Plan '{exx.sue}' cannot set moment_rope='{iowa_str}' where knot='{exx.slash}'"
    )
    assert str(excinfo.value) == exception_str


def test_planunit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    slash_knot = "/"
    iowa_rope = create_rope("Iowa", None, slash_knot)
    x_fund_pool = 555
    x_fund_grain = 7
    x_respect_grain = 5
    x_mana_grain = 1

    # WHEN
    x_plan = planunit_shop(
        plan_name=exx.sue,
        moment_rope=iowa_rope,
        knot=slash_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )

    # THEN
    assert x_plan
    assert x_plan.plan_name == exx.sue
    assert x_plan.moment_rope == iowa_rope
    assert x_plan.persons == {}
    assert x_plan.kegroot is not None
    assert x_plan.max_tree_traverse == 3
    assert x_plan.knot == slash_knot
    assert x_plan.fund_pool == x_fund_pool
    assert x_plan.fund_grain == x_fund_grain
    assert x_plan.respect_grain == x_respect_grain
    assert x_plan.mana_grain == x_mana_grain
    assert x_plan.credor_respect == RespectNum(validate_pool_num())
    assert x_plan.debtor_respect == RespectNum(validate_pool_num())
    assert not x_plan.last_lesson_id
    # calculated attr
    assert x_plan._keg_dict == {}
    assert x_plan._keep_dict == {}
    assert x_plan._healers_dict == {}
    assert not x_plan.tree_traverse_count
    assert x_plan.rational is False
    assert x_plan.keeps_justified is False
    assert x_plan.keeps_buildable is False
    assert x_plan.sum_healerunit_kegs_fund_total == 0
    assert x_plan.offtrack_kids_star_set == set()
    assert not x_plan.offtrack_fund
    assert x_plan.reason_contexts == set()
    assert x_plan.range_inheritors == {}
    print(f"{type(x_plan.kegroot)=}") == 0
    assert str(type(x_plan.kegroot)).find(".keg.KegUnit'>") > 0


def test_planunit_shop_ReturnsObj_Scenario2_WithoutParameters():
    # ESTABLISH / WHEN
    x_plan = planunit_shop()

    # THEN
    assert x_plan.plan_name == ""
    assert x_plan.moment_rope == get_default_rope()
    assert x_plan.knot == default_knot_if_None()
    assert x_plan.fund_pool == validate_pool_num()
    assert x_plan.fund_grain == default_grain_num_if_None()
    assert x_plan.respect_grain == default_grain_num_if_None()
    assert x_plan.mana_grain == default_grain_num_if_None()
    assert x_plan.kegroot.fund_grain == x_plan.fund_grain
    assert x_plan.kegroot.knot == x_plan.knot
    assert x_plan.kegroot.keg_uid == 1
    assert x_plan.kegroot.tree_level == 0
    assert x_plan.kegroot.knot == x_plan.knot
    assert x_plan.kegroot.parent_rope == ""


def test_PlanUnit_set_max_tree_traverse_SetsInt():
    # ESTABLISH
    zia_plan = planunit_shop(plan_name=exx.zia)
    assert zia_plan.max_tree_traverse == 3

    # WHEN
    zia_plan.set_max_tree_traverse(x_int=11)

    # THEN
    assert zia_plan.max_tree_traverse == 11


def test_PlanUnit_set_max_tree_traverse_RaisesError_Scenario0():
    # ESTABLISH
    zia_plan = planunit_shop(plan_name=exx.zia)
    assert zia_plan.max_tree_traverse == 3
    zia_tree_traverse = 1

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_max_tree_traverse(x_int=zia_tree_traverse)
    exception_str = "set_max_tree_traverse: '1' must be number that is 2 or greater"
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_max_tree_traverse_RaisesError_Scenario1():
    # ESTABLISH
    zia_plan = planunit_shop(plan_name=exx.zia)
    assert zia_plan.max_tree_traverse == 3

    # WHEN / THEN
    zia_tree_traverse = 3.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_max_tree_traverse(x_int=zia_tree_traverse)
    exception_str = f"set_max_tree_traverse: '{zia_tree_traverse}' must be number that is 2 or greater"
    assert str(excinfo.value) == exception_str


def test_PlanUnit_make_rope_ReturnsObj():
    # ESTABLISH
    slash_knot = "/"
    a45_rope = create_rope("amy45", None, slash_knot)
    sue_plan = planunit_shop(exx.sue, a45_rope, knot=slash_knot)
    v1_casa_rope = sue_plan.make_l1_rope(exx.casa)

    # WHEN
    v2_casa_rope = sue_plan.make_l1_rope(exx.casa)

    # THEN
    assert v1_casa_rope == v2_casa_rope


def test_PlanUnit_set_last_lesson_id_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)
    assert sue_plan.last_lesson_id is None

    # WHEN
    x_last_lesson_id = 89
    sue_plan.set_last_lesson_id(x_last_lesson_id)

    # THEN
    assert sue_plan.last_lesson_id == x_last_lesson_id


def test_PlanUnit_set_last_lesson_id_RaisesError():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)
    old_last_lesson_id = 89
    sue_plan.set_last_lesson_id(old_last_lesson_id)

    # WHEN / THEN
    new_last_lesson_id = 72
    assert new_last_lesson_id < old_last_lesson_id
    with pytest_raises(Exception) as excinfo:
        sue_plan.set_last_lesson_id(new_last_lesson_id)
    exception_str = f"Cannot set _last_lesson_id to {new_last_lesson_id} because it is less than {old_last_lesson_id}."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_del_last_lesson_id_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)
    old_last_lesson_id = 89
    sue_plan.set_last_lesson_id(old_last_lesson_id)
    assert sue_plan.last_lesson_id is not None

    # WHEN
    sue_plan.del_last_lesson_id()

    # THEN
    assert sue_plan.last_lesson_id is None


def test_PlanUnit_set_fund_pool_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)
    sue_fund_pool = 99000
    assert sue_plan.fund_pool == validate_pool_num()

    # WHEN
    sue_plan.set_fund_pool(sue_fund_pool)

    # THEN
    assert sue_plan.fund_pool == 99000


def test_PlanUnit_set_fund_pool_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_plan = planunit_shop(exx.zia)
    x_fund_pool = 23
    zia_plan.set_fund_pool(x_fund_pool)
    assert zia_plan.fund_grain == 1
    assert zia_plan.fund_pool == x_fund_pool

    # WHEN
    new_fund_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_fund_pool(new_fund_pool)

    # THEN
    exception_str = f"Plan '{exx.zia}' cannot set fund_pool='{new_fund_pool}'. It is not divisible by fund_grain '{zia_plan.fund_grain}'"
    assert str(excinfo.value) == exception_str
