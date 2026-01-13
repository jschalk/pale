from src.ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum
from src.ch02_person._ref.ch02_semantic_types import (
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    PersonName,
    RespectGrain,
    RespectNum,
    TitleTerm,
)
from src.ch04_rope._ref.ch04_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from src.ch05_reason._ref.ch05_semantic_types import FactNum, ReasonNum
from src.ch07_plan_logic._ref.ch07_semantic_types import (
    ManaGrain,
    MomentLabel,
    PlanName,
)
from src.ch08_plan_atom._ref.ch08_semantic_types import CRUD_command
from src.ch09_plan_lesson._ref.ch09_semantic_types import FaceName
from src.ch11_bud._ref.ch11_semantic_types import SparkInt, TimeNum
from src.ch12_keep._ref.ch12_semantic_types import ManaNum


class EpochLabel(LabelTerm):
    "EpochLabel is required for every EpochUnit. It is a LabelTerm that must not contain the knot."

    pass
