from inspect import getdoc as inspect_getdoc
from src.ch05_reason._ref.ch05_semantic_types import CotoNum
from src.ref.keywords import Ch05Keywords as kw


def test_CotoNum_Exists():
    # ESTABLISH
    four_int = 4
    # WHEN
    four_cotonum = CotoNum(four_int)
    # THEN
    assert four_int == four_cotonum
    doc_str = """A numeric value that may converted to other Semantic Types by an external process driven by context."""
    assert inspect_getdoc(four_cotonum) == doc_str
