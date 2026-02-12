from src.ch01_allot._ref.ch01_semantic_types import GrainNum, PoolNum, WeightNum
from src.ch02_partner._ref.ch02_semantic_types import (
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    PartnerName,
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
from src.ch07_plan_logic._ref.ch07_semantic_types import ManaGrain, MomentRope, PlanName


class CRUD_command(str):
    pass
