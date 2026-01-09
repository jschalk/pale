from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_kegunit_INSERT():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_kegunit
    _problem_bool_str = kw.problem_bool
    clean_label = "clean fridge"
    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    star_value = 43
    pledge_value = False
    clean_planatom = planatom_shop(dimen, kw.INSERT)
    clean_planatom.set_arg(kw.keg_rope, clean_rope)
    clean_planatom.set_arg(kw.addin, addin_value)
    clean_planatom.set_arg(kw.begin, begin_value)
    clean_planatom.set_arg(kw.close, close_value)
    clean_planatom.set_arg(kw.denom, denom_value)
    clean_planatom.set_arg(kw.numor, numor_value)
    clean_planatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_planatom.set_arg(kw.morph, morph_value)
    clean_planatom.set_arg(kw.star, star_value)
    clean_planatom.set_arg(kw.pledge, pledge_value)

    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(clean_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Created Keg '{clean_rope}'. addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.star={star_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_kegunit_UPDATE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_kegunit
    _problem_bool_str = kw.problem_bool
    clean_label = "clean fridge"
    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_rope(casa_rope, clean_label)
    addin_value = 7
    begin_value = 13
    close_value = 17
    denom_value = 23
    numor_value = 29
    problem_bool_value = False
    morph_value = 37
    star_value = 43
    pledge_value = False
    clean_planatom = planatom_shop(dimen, kw.UPDATE)
    clean_planatom.set_arg(kw.keg_rope, clean_rope)
    clean_planatom.set_arg(kw.addin, addin_value)
    clean_planatom.set_arg(kw.begin, begin_value)
    clean_planatom.set_arg(kw.close, close_value)
    clean_planatom.set_arg(kw.denom, denom_value)
    clean_planatom.set_arg(kw.numor, numor_value)
    clean_planatom.set_arg(_problem_bool_str, problem_bool_value)
    clean_planatom.set_arg(kw.morph, morph_value)
    clean_planatom.set_arg(kw.star, star_value)
    clean_planatom.set_arg(kw.pledge, pledge_value)

    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(clean_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Keg '{clean_rope}' set these attrs: addin={addin_value}.begin={begin_value}.close={close_value}.denom={denom_value}.numor={numor_value}.problem_bool={problem_bool_value}.morph={morph_value}.star={star_value}.pledge={pledge_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_kegunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_kegunit
    clean_label = "clean fridge"
    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_rope(casa_rope, clean_label)
    clean_planatom = planatom_shop(dimen, kw.DELETE)
    clean_planatom.set_arg(kw.keg_rope, clean_rope)

    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(clean_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Keg '{clean_rope}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
