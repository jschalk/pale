from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_keg_reasonunit_INSERT_With_active_requisite():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reasonunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_plan.knot}Swimmers"
    active_requisite_value = True
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.active_requisite, active_requisite_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit created for keg '{rope_value}' with reason_context '{reason_context_value}'. active_requisite={active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reasonunit_INSERT_Without_active_requisite():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reasonunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit created for keg '{rope_value}' with reason_context '{reason_context_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reasonunit_UPDATE_active_requisite_IsTrue():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reasonunit
    reason_context_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    active_requisite_value = True
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    swim_planatom.set_arg(kw.active_requisite, active_requisite_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for keg '{rope_value}' set with active_requisite={active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reasonunit_UPDATE_active_requisite_IsNone():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reasonunit
    reason_context_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for keg '{rope_value}' and no longer checks reason_context active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_reasonunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_reasonunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    reason_context_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, kw.DELETE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.reason_context, reason_context_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"ReasonUnit reason_context='{reason_context_value}' for keg '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
