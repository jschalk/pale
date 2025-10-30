from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_belief_plan_reason_caseunit_set_obj_SetAttr_Scenario0_Pass_reason_case():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob, knot=exx.slash)
    casa_rope = bob_belief.make_l1_rope(exx.casa)
    wk_rope = bob_belief.make_l1_rope(exx.wk)
    wed_rope = bob_belief.make_rope(wk_rope, exx.wed)
    bob_belief.set_l1_plan(planunit_shop(exx.casa))
    bob_belief.set_l1_plan(planunit_shop(exx.wk))
    bob_belief.set_plan_obj(planunit_shop(exx.wed), wk_rope)
    wed_jkeys = {
        kw.plan_rope: casa_rope,
        kw.reason_context: wk_rope,
        kw.reason_state: wed_rope,
    }
    assert not belief_plan_reason_caseunit_exists(bob_belief, wed_jkeys)

    # WHEN
    belief_plan_reason_caseunit_set_obj(bob_belief, wed_jkeys)

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, wed_jkeys)


def test_belief_plan_reason_caseunit_set_obj_SetAttr_Scenario1_Pass_reason_lower_reason_upper():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob, knot=exx.slash)
    mop_rope = bob_belief.make_l1_rope(exx.mop)
    clean_rope = bob_belief.make_l1_rope(exx.clean)
    dirtyness_rope = bob_belief.make_rope(clean_rope, exx.dirtyness)
    bob_belief.add_plan(dirtyness_rope)
    bob_belief.add_plan(mop_rope)
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_args = {
        kw.plan_rope: mop_rope,
        kw.reason_context: dirtyness_rope,
        kw.reason_state: dirtyness_rope,
        kw.reason_lower: dirtyness_reason_lower,
        kw.reason_upper: dirtyness_reason_upper,
    }
    assert not belief_plan_reason_caseunit_exists(bob_belief, dirtyness_args)

    # WHEN
    belief_plan_reason_caseunit_set_obj(belief=bob_belief, args=dirtyness_args)

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, dirtyness_args)
    dirtyness_case = belief_plan_reason_caseunit_get_obj(bob_belief, dirtyness_args)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper


def test_belief_plan_reason_caseunit_set_obj_SetAttr_Scenario2_Pass_reason_divisor():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob, knot=exx.slash)
    mop_rope = bob_belief.make_l1_rope(exx.mop)
    clean_rope = bob_belief.make_l1_rope(exx.clean)
    dirtyness_rope = bob_belief.make_rope(clean_rope, exx.dirtyness)
    bob_belief.add_plan(dirtyness_rope)
    bob_belief.add_plan(mop_rope)
    dirtyness_reason_lower = 5
    dirtyness_reason_upper = 7
    dirtyness_reason_divisor = 11
    dirtyness_args = {
        kw.plan_rope: mop_rope,
        kw.reason_context: dirtyness_rope,
        kw.reason_state: dirtyness_rope,
        kw.reason_lower: dirtyness_reason_lower,
        kw.reason_upper: dirtyness_reason_upper,
        kw.reason_divisor: dirtyness_reason_divisor,
    }
    assert not belief_plan_reason_caseunit_exists(bob_belief, dirtyness_args)

    # WHEN
    belief_plan_reason_caseunit_set_obj(bob_belief, dirtyness_args)

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, dirtyness_args)
    dirtyness_case = belief_plan_reason_caseunit_get_obj(bob_belief, dirtyness_args)
    assert dirtyness_case
    assert dirtyness_case.reason_lower == dirtyness_reason_lower
    assert dirtyness_case.reason_upper == dirtyness_reason_upper
    assert dirtyness_case.reason_divisor == dirtyness_reason_divisor
