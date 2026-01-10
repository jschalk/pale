from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import get_minimal_plandelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_plandelta_ReturnsObjUPDATEPlanAtom_plan_personunit():
    # ESTABLISH
    old_bob_person_cred_lumen = 34
    new_bob_person_cred_lumen = 7
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.bob, old_bob_person_cred_lumen)
    sue_plan.add_personunit(exx.yao)

    persons_plandelta = plandelta_shop()
    bob_atom = planatom_shop(kw.plan_personunit, kw.INSERT)
    bob_atom.set_arg(kw.person_name, exx.bob)
    bob_atom.set_arg(kw.person_cred_lumen, new_bob_person_cred_lumen)
    yao_atom = planatom_shop(kw.plan_personunit, kw.INSERT)
    yao_atom.set_arg(kw.person_name, exx.yao)
    persons_plandelta.set_planatom(bob_atom)
    persons_plandelta.set_planatom(yao_atom)
    assert len(persons_plandelta.get_sorted_planatoms()) == 2

    # WHEN
    new_plandelta = get_minimal_plandelta(persons_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_sorted_planatoms()) == 1
    new_planatom = new_plandelta.get_sorted_planatoms()[0]
    assert new_planatom.crud_str == kw.UPDATE
    new_jvalues = new_planatom.get_jvalues_dict()
    assert new_jvalues == {kw.person_cred_lumen: new_bob_person_cred_lumen}
