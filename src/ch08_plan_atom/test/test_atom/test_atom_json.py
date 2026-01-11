from src.ch04_rope.rope import create_rope
from src.ch08_plan_atom.atom_main import get_planatom_from_dict, planatom_shop
from src.ref.keywords import Ch08Keywords as kw


def test_PlanAtom_to_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.plan_keg_factunit
    knee_reason_lower = 7
    knee_reason_upper = 13
    insert_factunit_planatom = planatom_shop(x_dimen, kw.INSERT)
    insert_factunit_planatom.set_jkey(kw.keg_rope, ball_rope)
    insert_factunit_planatom.set_jkey(kw.fact_context, knee_rope)
    insert_factunit_planatom.set_jvalue(kw.fact_lower, knee_reason_lower)
    insert_factunit_planatom.set_jvalue(kw.fact_upper, knee_reason_upper)

    # WHEN
    atom_dict = insert_factunit_planatom.to_dict()

    # THEN
    assert atom_dict == {
        kw.dimen: x_dimen,
        kw.crud: kw.INSERT,
        kw.jkeys: {kw.keg_rope: ball_rope, kw.fact_context: knee_rope},
        kw.jvalues: {
            kw.fact_lower: knee_reason_lower,
            kw.fact_upper: knee_reason_upper,
        },
    }


def test_get_planatom_from_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.plan_keg_factunit
    knee_reason_lower = 7
    knee_reason_upper = 13
    gen_planatom = planatom_shop(x_dimen, kw.INSERT)
    gen_planatom.set_jkey(kw.keg_rope, ball_rope)
    gen_planatom.set_jkey(kw.fact_context, knee_rope)
    gen_planatom.set_jvalue(kw.fact_lower, knee_reason_lower)
    gen_planatom.set_jvalue(kw.fact_upper, knee_reason_upper)
    atom_serializable_dict = gen_planatom.to_dict()

    # WHEN
    gen_planatom = get_planatom_from_dict(atom_serializable_dict)

    # THEN
    assert gen_planatom.dimen == gen_planatom.dimen
    assert gen_planatom.crud_str == gen_planatom.crud_str
    assert gen_planatom.jkeys == gen_planatom.jkeys
    assert gen_planatom.jvalues == gen_planatom.jvalues
    assert gen_planatom == gen_planatom
