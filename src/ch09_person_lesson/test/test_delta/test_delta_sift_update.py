from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import get_minimal_persondelta, persondelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_persondelta_ReturnsObjUPDATEPersonAtom_person_partnerunit():
    # ESTABLISH
    old_bob_partner_cred_lumen = 34
    new_bob_partner_cred_lumen = 7
    sue_person = personunit_shop("Sue")
    sue_person.add_partnerunit(exx.bob, old_bob_partner_cred_lumen)
    sue_person.add_partnerunit(exx.yao)

    partners_persondelta = persondelta_shop()
    bob_atom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    bob_atom.set_arg(kw.partner_name, exx.bob)
    bob_atom.set_arg(kw.partner_cred_lumen, new_bob_partner_cred_lumen)
    yao_atom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    yao_atom.set_arg(kw.partner_name, exx.yao)
    partners_persondelta.set_personatom(bob_atom)
    partners_persondelta.set_personatom(yao_atom)
    assert len(partners_persondelta.get_sorted_personatoms()) == 2

    # WHEN
    new_persondelta = get_minimal_persondelta(partners_persondelta, sue_person)

    # THEN
    assert len(new_persondelta.get_sorted_personatoms()) == 1
    new_personatom = new_persondelta.get_sorted_personatoms()[0]
    assert new_personatom.crud_str == kw.UPDATE
    new_jvalues = new_personatom.get_jvalues_dict()
    assert new_jvalues == {kw.partner_cred_lumen: new_bob_partner_cred_lumen}
