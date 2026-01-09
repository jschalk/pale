from inspect import getdoc as inspect_getdoc
from src.ch07_plan_logic._ref.ch07_semantic_types import (
    ManaGrain,
    MomentLabel,
    PlanName,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PlanName_Exists():
    # ESTABLISH
    # WHEN
    bob_PlanName_str = PlanName(exx.bob)
    # THEN
    assert bob_PlanName_str == exx.bob
    doc_str = f"A {kw.NameTerm} used to identify a PlanUnit's plan"
    assert inspect_getdoc(bob_PlanName_str) == doc_str


def test_MomentLabel_Exists():
    # ESTABLISH
    # WHEN
    bob_MomentLabel_str = MomentLabel(exx.bob)
    # THEN
    assert bob_MomentLabel_str == exx.bob
    doc_str = f"A {kw.LabelTerm} for a Moment. Cannot contain knot."
    assert inspect_getdoc(bob_MomentLabel_str) == doc_str


def test_ManaGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_mana_grain = ManaGrain(x_float)
    # THEN
    assert y_mana_grain == x_float
    assert inspect_getdoc(y_mana_grain) == "Smallest Unit of Mana"
