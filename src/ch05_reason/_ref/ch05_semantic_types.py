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


class ReasonNum(float):
    """A numeric value that may converted to other Semantic Types by an external process driven by context."""

    pass


class FactNum(float):
    """A numeric value that may converted to other Semantic Types by an external process driven by context."""

    pass
