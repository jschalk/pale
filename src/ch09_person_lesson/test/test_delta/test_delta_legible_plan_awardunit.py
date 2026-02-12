from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_plan_awardunit_INSERT():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_awardunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_person.knot}Swimmers"
    give_force_value = 81
    take_force_value = 43
    swim_personatom = personatom_shop(dimen, kw.INSERT)
    swim_personatom.set_arg(kw.plan_rope, rope_value)
    swim_personatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_personatom.set_arg(kw.give_force, give_force_value)
    swim_personatom.set_arg(kw.take_force, take_force_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"AwardUnit created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_UPDATE_give_force_take_force():
    # ESTABLISH
    sue_person = personunit_shop("Sue")

    dimen = kw.person_plan_awardunit
    awardee_title_value = f"{sue_person.knot}Swimmers"
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    take_force_value = 43
    swim_personatom = personatom_shop(dimen, kw.UPDATE)
    swim_personatom.set_arg(kw.plan_rope, rope_value)
    swim_personatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_personatom.set_arg(kw.give_force, give_force_value)
    swim_personatom.set_arg(kw.take_force, take_force_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_UPDATE_give_force():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_awardunit
    awardee_title_value = f"{sue_person.knot}Swimmers"
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    give_force_value = 81
    swim_personatom = personatom_shop(dimen, kw.UPDATE)
    swim_personatom.set_arg(kw.plan_rope, rope_value)
    swim_personatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_personatom.set_arg(kw.give_force, give_force_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_UPDATE_take_force():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_awardunit
    awardee_title_value = f"{sue_person.knot}Swimmers"
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")

    take_force_value = 81
    swim_personatom = personatom_shop(dimen, kw.UPDATE)
    swim_personatom.set_arg(kw.plan_rope, rope_value)
    swim_personatom.set_arg(kw.awardee_title, awardee_title_value)
    swim_personatom.set_arg(kw.take_force, take_force_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now take_force={take_force_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_plan_awardunit_DELETE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_plan_awardunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    awardee_title_value = f"{sue_person.knot}Swimmers"
    swim_personatom = personatom_shop(dimen, kw.DELETE)
    swim_personatom.set_arg(kw.plan_rope, rope_value)
    swim_personatom.set_arg(kw.awardee_title, awardee_title_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"AwardUnit for group {awardee_title_value}, plan '{rope_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
