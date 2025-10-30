from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch15_moment.test._util.ch15_examples import _example_empty_bob_beliefunit
from src.ref.keywords import ExampleStrs as exx


def get_mop_with_no_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
    casa_rope = bob_belief.make_l1_rope(exx.casa)
    mop_rope = bob_belief.make_rope(casa_rope, exx.mop)
    bob_belief.add_plan(mop_rope, pledge=True)
    return bob_belief


def get_bob_mop_reason_beliefunit_example() -> BeliefUnit:
    bob_belief = _example_empty_bob_beliefunit()
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_belief.make_l1_rope(exx.casa)
    floor_rope = bob_belief.make_rope(casa_rope, floor_str)
    clean_rope = bob_belief.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_belief.make_rope(floor_rope, dirty_str)
    mop_rope = bob_belief.make_rope(casa_rope, exx.mop)
    bob_belief.add_plan(floor_rope)
    bob_belief.add_plan(clean_rope)
    bob_belief.add_plan(dirty_rope)
    bob_belief.add_plan(mop_rope, pledge=True)
    bob_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    return bob_belief
