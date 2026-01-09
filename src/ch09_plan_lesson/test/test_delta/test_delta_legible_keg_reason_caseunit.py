from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_keg_reason_caseunit_INSERT_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reason_caseunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    reason_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.reason_state, reason_state_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reason_caseunit_INSERT_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reason_caseunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    reason_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    reason_divisor_value = 7
    reason_upper_value = 13
    reason_lower_value = 17
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.reason_state, reason_state_value)
    swim_planatom.set_arg(kw.reason_divisor, reason_divisor_value)
    swim_planatom.set_arg(kw.reason_upper, reason_upper_value)
    swim_planatom.set_arg(kw.reason_lower, reason_lower_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for keg '{rope_value}'. reason_lower={reason_lower_value}. reason_upper={reason_upper_value}. reason_divisor={reason_divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reason_caseunit_UPDATE_WithOutNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reason_caseunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    reason_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.reason_state, reason_state_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reason_caseunit_UPDATE_WithNumberArgs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reason_caseunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    reason_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    reason_divisor_value = 7
    reason_upper_value = 13
    reason_lower_value = 17
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.reason_state, reason_state_value)
    swim_planatom.set_arg(kw.reason_divisor, reason_divisor_value)
    swim_planatom.set_arg(kw.reason_upper, reason_upper_value)
    swim_planatom.set_arg(kw.reason_lower, reason_lower_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for keg '{rope_value}'. reason_lower={reason_lower_value}. reason_upper={reason_upper_value}. reason_divisor={reason_divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reason_caseunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reason_caseunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    casa_rope = sue_plan.make_l1_rope("casa")
    reason_context_value = sue_plan.make_rope(casa_rope, "fridge situation")
    reason_state_value = sue_plan.make_rope(reason_context_value, "dirty")
    swim_planatom = planatom_shop(dimen, kw.DELETE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.reason_state, reason_state_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"CaseUnit '{reason_state_value}' deleted from reason '{reason_context_value}' for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
