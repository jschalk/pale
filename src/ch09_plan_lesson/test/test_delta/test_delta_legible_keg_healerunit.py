from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_keg_healerunit_INSERT():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_healerunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.healer_name, healer_name_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' created for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_healerunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_healerunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    healer_name_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, kw.DELETE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.healer_name, healer_name_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"HealerUnit '{healer_name_value}' deleted for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
