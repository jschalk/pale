from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_keg_awardunit_INSERT():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_awardunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_planatom = planatom_shop(dimen, kw.INSERT)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_planatom.set_arg(kw.give_force, give_force_value)
    swim_planatom.set_arg(kw.take_force, take_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"AwardUnit created for group {awardee_title_value} for keg '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_awardunit_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")

    dimen = kw.plan_keg_awardunit
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_planatom.set_arg(kw.give_force, give_force_value)
    swim_planatom.set_arg(kw.take_force, take_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for keg '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_awardunit_UPDATE_give_force():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_awardunit
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_planatom.set_arg(kw.give_force, give_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for keg '{rope_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_awardunit_UPDATE_take_force():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_awardunit
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")

    take_force_value = 81
    swim_planatom = planatom_shop(dimen, kw.UPDATE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_planatom.set_arg(kw.take_force, take_force_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for keg '{rope_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_awardunit_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = kw.plan_keg_awardunit
    casa_rope = sue_plan.make_l1_rope("casa")
    rope_value = sue_plan.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_plan.knot}Swimmers"
    swim_planatom = planatom_shop(dimen, kw.DELETE)
    swim_planatom.set_arg(kw.keg_rope, rope_value)
    swim_planatom.set_arg(kw.awardee_title, awardee_title_value)
    # print(f"{swim_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(swim_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"AwardUnit for group {awardee_title_value}, keg '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
