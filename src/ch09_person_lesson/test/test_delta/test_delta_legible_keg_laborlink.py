from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw


def test_create_legible_list_ReturnsObj_keg_partyunit_INSERT():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_keg_partyunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    party_title_value = f"{sue_person.knot}Swimmers"
    swim_personatom = personatom_shop(dimen, kw.INSERT)
    swim_personatom.set_arg(kw.keg_rope, rope_value)
    swim_personatom.set_arg(kw.party_title, party_title_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"partyunit '{party_title_value}' created for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_keg_partyunit_DELETE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_keg_partyunit
    casa_rope = sue_person.make_l1_rope("casa")
    rope_value = sue_person.make_rope(casa_rope, "clean fridge")
    party_title_value = f"{sue_person.knot}Swimmers"
    swim_personatom = personatom_shop(dimen, kw.DELETE)
    swim_personatom.set_arg(kw.keg_rope, rope_value)
    swim_personatom.set_arg(kw.party_title, party_title_value)
    # print(f"{swim_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(swim_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"partyunit '{party_title_value}' deleted for keg '{rope_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
