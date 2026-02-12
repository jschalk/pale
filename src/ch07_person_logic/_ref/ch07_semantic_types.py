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


class MomentRope(RopeTerm):  # Created to help track the object class relations
    """The RopeTerm for a Moment. Must contain knots."""

    pass


class PersonName(LabelTerm):
    """The LabelTerm used to identify a PersonUnit.
    Must be a LabelTerm/NameTerm because when identifying if a KegUnit is an active pledge the PersonName will be compared
    against PartnerNames. If they match the pledge will be active."""

    pass


class ManaGrain(float):
    """Smallest Unit of Mana"""

    pass
