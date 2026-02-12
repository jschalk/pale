from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import get_minimal_persondelta, persondelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_get_minimal_persondelta_ReturnsObjWithoutUnecessaryINSERT_person_partnerunit():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_partnerunit(exx.yao)
    sue_person.add_partnerunit(exx.bob)

    partners_persondelta = persondelta_shop()
    bob_atom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    bob_atom.set_arg(kw.partner_name, exx.bob)
    yao_atom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    yao_atom.set_arg(kw.partner_name, exx.yao)
    zia_atom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    zia_atom.set_arg(kw.partner_name, exx.zia)
    partners_persondelta.set_personatom(bob_atom)
    partners_persondelta.set_personatom(yao_atom)
    partners_persondelta.set_personatom(zia_atom)
    assert len(partners_persondelta.get_sorted_personatoms()) == 3
    assert len(sue_person.partners) == 2

    # WHEN
    new_persondelta = get_minimal_persondelta(partners_persondelta, sue_person)

    # THEN
    assert len(new_persondelta.get_sorted_personatoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_person_partner_membership():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    sue_person.add_partnerunit(exx.yao)
    sue_person.add_partnerunit(exx.bob)
    yao_partnerunit = sue_person.get_partner(exx.yao)
    yao_partnerunit.add_membership(exx.run)
    print(f"{yao_partnerunit.memberships.keys()=}")

    partners_persondelta = persondelta_shop()
    bob_run_atom = personatom_shop(kw.person_partner_membership, kw.INSERT)
    bob_run_atom.set_arg(kw.partner_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = personatom_shop(kw.person_partner_membership, kw.INSERT)
    yao_run_atom.set_arg(kw.partner_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)
    zia_run_atom = personatom_shop(kw.person_partner_membership, kw.INSERT)
    zia_run_atom.set_arg(kw.partner_name, exx.zia)
    zia_run_atom.set_arg(kw.group_title, exx.run)
    partners_persondelta.set_personatom(bob_run_atom)
    partners_persondelta.set_personatom(yao_run_atom)
    partners_persondelta.set_personatom(zia_run_atom)
    print(f"{len(partners_persondelta.get_dimen_sorted_personatoms_list())=}")
    assert len(partners_persondelta.get_dimen_sorted_personatoms_list()) == 3

    # WHEN
    new_persondelta = get_minimal_persondelta(partners_persondelta, sue_person)

    # THEN
    assert len(new_persondelta.get_dimen_sorted_personatoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
