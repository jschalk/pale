from inspect import getdoc as inspect_getdoc
from src.ch07_plan_logic._ref.ch07_semantic_types import ManaGrain, MomentRope, PlanName
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PlanName_Exists():
    # ESTABLISH
    # WHEN
    bob_PlanName_str = PlanName(exx.bob)
    # THEN
    assert bob_PlanName_str == exx.bob
    doc_str = f"""The {kw.LabelTerm} used to identify a PlanUnit.
Must be a {kw.LabelTerm}/{kw.NameTerm} because when identifying if a KegUnit is an active {kw.pledge} the {kw.PlanName} will be compared
against {kw.PersonName}s. If they match the {kw.pledge} will be active."""
    assert inspect_getdoc(bob_PlanName_str) == doc_str


def test_MomentRope_Exists():
    # ESTABLISH
    # WHEN
    bob_MomentRope_str = MomentRope(exx.bob)
    # THEN
    assert bob_MomentRope_str == exx.bob
    doc_str = f"The {kw.RopeTerm} for a Moment. Must contain knots."
    assert inspect_getdoc(bob_MomentRope_str) == doc_str


def test_ManaGrain_Exists():
    # ESTABLISH
    x_float = 0.045
    # WHEN
    y_mana_grain = ManaGrain(x_float)
    # THEN
    assert y_mana_grain == x_float
    assert inspect_getdoc(y_mana_grain) == "Smallest Unit of Mana"
