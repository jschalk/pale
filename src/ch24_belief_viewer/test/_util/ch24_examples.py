from datetime import datetime
from enum import Enum
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ref.keywords import ExampleStrs as exx

SUE_BELIEF = beliefunit_shop(exx.sue, exx.a23)
CASA_ROPE = SUE_BELIEF.make_l1_rope(exx.casa)
CLEAN_ROPE = SUE_BELIEF.make_rope(CASA_ROPE, exx.clean)
MOP_ROPE = SUE_BELIEF.make_rope(CLEAN_ROPE, exx.mop)
SWEEP_STR = "sweep"
SWEEP_ROPE = SUE_BELIEF.make_rope(CLEAN_ROPE, SWEEP_STR)
SCRUB_STR = "scrub"
SCRUB_ROPE = SUE_BELIEF.make_rope(CLEAN_ROPE, SCRUB_STR)


class ExampleValuesRef(str, Enum):
    sue = exx.sue
    a23 = exx.a23
    casa_str = exx.casa
    casa_rope = CASA_ROPE
    clean_str = exx.clean
    clean_rope = CLEAN_ROPE
    mop_str = exx.mop
    mop_rope = MOP_ROPE
    sweep_str = SWEEP_STR
    sweep_rope = SWEEP_ROPE
    scrub_str = SCRUB_STR
    scrub_rope = SCRUB_ROPE

    def __str__(self):
        return self.value
