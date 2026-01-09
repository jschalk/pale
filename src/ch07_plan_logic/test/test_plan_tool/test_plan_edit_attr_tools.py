from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_tool import (
    plan_keg_reason_caseunit_exists,
    plan_keg_reason_caseunit_get_obj,
    plan_keg_reason_caseunit_set_obj,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_plan_keg_reason_caseunit_set_obj_SetAttr_Scenario0_Pass_reason_case():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob, knot=exx.slash)
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    wk_rope = bob_plan.make_l1_rope(exx.wk)
    wed_rope = bob_plan.make_rope(wk_rope, exx.wed)
    bob_plan.set_l1_keg(kegunit_shop(exx.casa))
    bob_plan.set_l1_keg(kegunit_shop(exx.wk))
    bob_plan.set_keg_obj(kegunit_shop(exx.wed), wk_rope)
    wed_jkeys = {
        kw.keg_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: wed_rope,
    }
    assert not plan_keg_reason_caseunit_exists(bob_plan, wed_jkeys)

    # WHEN
    plan_keg_reason_caseunit_set_obj(bob_plan, wed_jkeys)

    # THEN
    assert plan_keg_reason_caseunit_exists(bob_plan, wed_jkeys)


def test_plan_keg_reason_caseunit_set_obj_SetAttr_Scenario1_Pass_reason_lower_reason_upper():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob, knot=exx.slash)
    mop_rope = bob_plan.make_l1_rope(exx.mop)
    clean_rope = bob_plan.make_l1_rope(exx.clean)
    dirtyness_rope = bob_plan.make_rope(clean_rope, exx.dirtyness)
    bob_plan.add_keg(dirtyness_rope)
    bob_plan.add_keg(mop_rope)
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_args = {
        kw.keg_rope: mop_rope,
        kw.reason_context: dirtyness_rope,
        kw.reason_state: dirtyness_rope,
        kw.reason_lower: dirtyness_reason_lower,
        kw.reason_upper: dirtyness_reason_upper,
    }
    assert not plan_keg_reason_caseunit_exists(bob_plan, dirtyness_args)

    # WHEN
    plan_keg_reason_caseunit_set_obj(plan=bob_plan, args=dirtyness_args)

    # THEN
    assert plan_keg_reason_caseunit_exists(bob_plan, dirtyness_args)
    dirtyness_case = plan_keg_reason_caseunit_get_obj(bob_plan, dirtyness_args)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper


def test_plan_keg_reason_caseunit_set_obj_SetAttr_Scenario2_Pass_reason_divisor():
    # ESTABLISH
    bob_plan = planunit_shop(exx.bob, knot=exx.slash)
    mop_rope = bob_plan.make_l1_rope(exx.mop)
    clean_rope = bob_plan.make_l1_rope(exx.clean)
    dirtyness_rope = bob_plan.make_rope(clean_rope, exx.dirtyness)
    bob_plan.add_keg(dirtyness_rope)
    bob_plan.add_keg(mop_rope)
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_reason_divisor = 11
    dirtyness_args = {
        kw.keg_rope: mop_rope,
        kw.reason_context: dirtyness_rope,
        kw.reason_state: dirtyness_rope,
        kw.reason_lower: dirtyness_reason_lower,
        kw.reason_upper: dirtyness_reason_upper,
        kw.reason_divisor: dirtyness_reason_divisor,
    }
    assert not plan_keg_reason_caseunit_exists(bob_plan, dirtyness_args)

    # WHEN
    plan_keg_reason_caseunit_set_obj(bob_plan, dirtyness_args)

    # THEN
    assert plan_keg_reason_caseunit_exists(bob_plan, dirtyness_args)
    dirtyness_case = plan_keg_reason_caseunit_get_obj(bob_plan, dirtyness_args)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper
    assert dirtyness_case.reason_divisor == dirtyness_reason_divisor
