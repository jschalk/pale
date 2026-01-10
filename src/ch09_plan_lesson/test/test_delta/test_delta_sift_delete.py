# from src.ch07_plan_logic.plan_tool import pass
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import get_minimal_plandelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_get_minimal_plandelta_ReturnsObjWithoutUnecessaryDELETE_plan_personunit():
    # ESTABLISH plandelta with 2 personunits, plandelta DELETE 3 plandeltas,
    # assert plandelta has 3 atoms
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    sue_plan.add_personunit(exx.bob)

    persons_plandelta = plandelta_shop()
    bob_atom = planatom_shop(kw.plan_personunit, kw.DELETE)
    bob_atom.set_arg(kw.person_name, exx.bob)
    yao_atom = planatom_shop(kw.plan_personunit, kw.DELETE)
    yao_atom.set_arg(kw.person_name, exx.yao)
    zia_atom = planatom_shop(kw.plan_personunit, kw.DELETE)
    zia_atom.set_arg(kw.person_name, exx.zia)
    persons_plandelta.set_planatom(bob_atom)
    persons_plandelta.set_planatom(yao_atom)
    persons_plandelta.set_planatom(zia_atom)
    assert len(persons_plandelta.get_sorted_planatoms()) == 3
    assert len(sue_plan.persons) == 2

    # WHEN
    new_plandelta = get_minimal_plandelta(persons_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_sorted_planatoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_plan_person_membership():
    # ESTABLISH plandelta with 2 personunits, plandelta DELETE 3 plandeltas,
    # assert plandelta has 3 atoms
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    sue_plan.add_personunit(exx.bob)
    yao_personunit = sue_plan.get_person(exx.yao)
    swim_str = ";swim"
    yao_personunit.add_membership(exx.run)
    yao_personunit.add_membership(swim_str)
    print(f"{yao_personunit.memberships.keys()=}")

    persons_plandelta = plandelta_shop()
    bob_run_atom = planatom_shop(kw.plan_person_membership, kw.DELETE)
    bob_run_atom.set_arg(kw.person_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = planatom_shop(kw.plan_person_membership, kw.DELETE)
    yao_run_atom.set_arg(kw.person_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)
    zia_run_atom = planatom_shop(kw.plan_person_membership, kw.DELETE)
    zia_run_atom.set_arg(kw.person_name, exx.zia)
    zia_run_atom.set_arg(kw.group_title, exx.run)
    persons_plandelta.set_planatom(bob_run_atom)
    persons_plandelta.set_planatom(yao_run_atom)
    persons_plandelta.set_planatom(zia_run_atom)
    print(f"{len(persons_plandelta.get_dimen_sorted_planatoms_list())=}")
    assert len(persons_plandelta.get_dimen_sorted_planatoms_list()) == 3

    # WHEN
    new_plandelta = get_minimal_plandelta(persons_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 1
