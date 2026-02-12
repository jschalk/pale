# from src.ch07_plan_logic.plan_tool import pass
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import get_minimal_plandelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_get_minimal_plandelta_ReturnsObjWithoutUnecessaryDELETE_plan_partnerunit():
    # ESTABLISH plandelta with 2 partnerunits, plandelta DELETE 3 plandeltas,
    # assert plandelta has 3 atoms
    sue_plan = planunit_shop("Sue")
    sue_plan.add_partnerunit(exx.yao)
    sue_plan.add_partnerunit(exx.bob)

    partners_plandelta = plandelta_shop()
    bob_atom = planatom_shop(kw.plan_partnerunit, kw.DELETE)
    bob_atom.set_arg(kw.partner_name, exx.bob)
    yao_atom = planatom_shop(kw.plan_partnerunit, kw.DELETE)
    yao_atom.set_arg(kw.partner_name, exx.yao)
    zia_atom = planatom_shop(kw.plan_partnerunit, kw.DELETE)
    zia_atom.set_arg(kw.partner_name, exx.zia)
    partners_plandelta.set_planatom(bob_atom)
    partners_plandelta.set_planatom(yao_atom)
    partners_plandelta.set_planatom(zia_atom)
    assert len(partners_plandelta.get_sorted_planatoms()) == 3
    assert len(sue_plan.partners) == 2

    # WHEN
    new_plandelta = get_minimal_plandelta(partners_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_sorted_planatoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_plan_partner_membership():
    # ESTABLISH plandelta with 2 partnerunits, plandelta DELETE 3 plandeltas,
    # assert plandelta has 3 atoms
    sue_plan = planunit_shop("Sue")
    sue_plan.add_partnerunit(exx.yao)
    sue_plan.add_partnerunit(exx.bob)
    yao_partnerunit = sue_plan.get_partner(exx.yao)
    swim_str = ";swim"
    yao_partnerunit.add_membership(exx.run)
    yao_partnerunit.add_membership(swim_str)
    print(f"{yao_partnerunit.memberships.keys()=}")

    partners_plandelta = plandelta_shop()
    bob_run_atom = planatom_shop(kw.plan_partner_membership, kw.DELETE)
    bob_run_atom.set_arg(kw.partner_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = planatom_shop(kw.plan_partner_membership, kw.DELETE)
    yao_run_atom.set_arg(kw.partner_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)
    zia_run_atom = planatom_shop(kw.plan_partner_membership, kw.DELETE)
    zia_run_atom.set_arg(kw.partner_name, exx.zia)
    zia_run_atom.set_arg(kw.group_title, exx.run)
    partners_plandelta.set_planatom(bob_run_atom)
    partners_plandelta.set_planatom(yao_run_atom)
    partners_plandelta.set_planatom(zia_run_atom)
    print(f"{len(partners_plandelta.get_dimen_sorted_planatoms_list())=}")
    assert len(partners_plandelta.get_dimen_sorted_planatoms_list()) == 3

    # WHEN
    new_plandelta = get_minimal_plandelta(partners_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 1
