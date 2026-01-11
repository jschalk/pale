from src.ch07_plan_logic.plan_main import PlanUnit
from src.ch14_moment.test._util.ch14_examples import _example_empty_bob_planunit
from src.ref.keywords import ExampleStrs as exx


def get_mop_with_no_reason_planunit_example() -> PlanUnit:
    bob_plan = _example_empty_bob_planunit()
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    mop_rope = bob_plan.make_rope(casa_rope, exx.mop)
    bob_plan.add_keg(mop_rope, pledge=True)
    return bob_plan


def get_bob_mop_reason_planunit_example() -> PlanUnit:
    bob_plan = _example_empty_bob_planunit()
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, exx.mop)
    bob_plan.add_keg(floor_rope)
    bob_plan.add_keg(clean_rope)
    bob_plan.add_keg(dirty_rope)
    bob_plan.add_keg(mop_rope, pledge=True)
    bob_plan.edit_keg_attr(mop_rope, reason_context=floor_rope, reason_case=clean_rope)
    return bob_plan
