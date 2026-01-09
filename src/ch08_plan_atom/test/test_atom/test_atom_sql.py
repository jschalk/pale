from pytest import raises as pytest_raises
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_rowdata
from src.ch04_rope.rope import create_rope
from src.ch08_plan_atom.atom_main import get_planatom_from_rowdata, planatom_shop
from src.ref.keywords import Ch08Keywords as kw


def test_PlanAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.plan_keg_factunit
    update_disc_planatom = planatom_shop(x_dimen, kw.UPDATE)
    update_disc_planatom.set_jkey("reason_context", knee_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_planatom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_dimen}' with is_valid=False."
    )


def test_PlanAtom_get_insert_sqlstr_ReturnsObj_PlanUnitSimpleAttrs():
    # ESTABLISH
    new2_value = 66
    dimen = kw.planunit
    opt_arg2 = kw.max_tree_traverse
    x_planatom = planatom_shop(dimen, kw.UPDATE)
    x_planatom.set_jvalue(opt_arg2, new2_value)
    x_table = "atom_hx"
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {dimen}_{kw.UPDATE}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""

    # WHEN / THEN
    assert x_planatom.get_insert_sqlstr() == example_sqlstr


def test_PlanAtom_get_insert_sqlstr_ReturnsObj_keg_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_reason_lower = 7
    x_dimen = kw.plan_keg_factunit
    update_disc_planatom = planatom_shop(x_dimen, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_planatom.set_jvalue(kw.fact_lower, knee_reason_lower)

    # WHEN
    generated_sqlstr = update_disc_planatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {kw.atom_hx} (
  {x_dimen}_{kw.INSERT}_{kw.keg_rope}
, {x_dimen}_{kw.INSERT}_{kw.fact_context}
, {x_dimen}_{kw.INSERT}_{kw.fact_lower}
)
VALUES (
  '{ball_rope}'
, '{knee_rope}'
, {knee_reason_lower}
)
;"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_planatom_from_rowdata_ReturnsObj_keg_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_fact_lower = 7
    x_dimen = kw.plan_keg_factunit
    x_sqlstr = f"""SELECT
  '{ball_rope}' as {x_dimen}_{kw.INSERT}_{kw.keg_rope}
, '{knee_rope}' as {x_dimen}_{kw.INSERT}_{kw.fact_context}
, {knee_fact_lower} as {x_dimen}_{kw.INSERT}_{kw.fact_lower}
"""
    with sqlite3_connect(":memory:") as x_conn:
        x_rowdata = get_rowdata(kw.atom_hx, x_conn, x_sqlstr)

    # WHEN
    x_planatom = get_planatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_planatom = planatom_shop(x_dimen, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_planatom.set_jvalue(kw.fact_lower, knee_fact_lower)
    assert update_disc_planatom.dimen == x_planatom.dimen
    assert update_disc_planatom.crud_str == x_planatom.crud_str
    assert update_disc_planatom.jkeys == x_planatom.jkeys
    assert update_disc_planatom.jvalues == x_planatom.jvalues
