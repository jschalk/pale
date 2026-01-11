from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_keg_factunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_factunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    fact_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_plan.make_rope(fact_context_value, "dirty")
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.fact_context, fact_context_value)
    swim_planatom.set_arg(kw.fact_state, fact_state_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' created for reason_context '{fact_context_value}' for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_factunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_factunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    fact_upper_value = 13
    fact_lower_value = 17
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.fact_context, reason_context_value)
    swim_planatom.set_arg(kw.fact_state, fact_state_value)
    swim_planatom.set_arg(kw.fact_upper, fact_upper_value)
    swim_planatom.set_arg(kw.fact_lower, fact_lower_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' created for reason_context '{reason_context_value}' for keg '{rope_value}'. fact_lower={fact_lower_value}. fact_upper={fact_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_factunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_factunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.fact_context, reason_context_value)
    swim_planatom.set_arg(kw.fact_state, fact_state_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{reason_context_value}' for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_factunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_factunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    fact_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    fact_upper_value = 13
    fact_lower_value = 17
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.fact_context, reason_context_value)
    swim_planatom.set_arg(kw.fact_state, fact_state_value)
    swim_planatom.set_arg(kw.fact_upper, fact_upper_value)
    swim_planatom.set_arg(kw.fact_lower, fact_lower_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{reason_context_value}' for keg '{rope_value}'. fact_lower={fact_lower_value}. fact_upper={fact_upper_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_factunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_factunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    swim_planatom = planatom_shop(dimen, kw.DELETE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.fact_context, reason_context_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"FactUnit reason_context '{reason_context_value}' deleted for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
