from src.ch02_person.group import awardunit_shop
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop, sift_planatom
from src.ref.keywords import Ch08Keywords as kw, ExampleStrs as exx


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_personunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.zia)

    bob_atom = planatom_shop(kw.plan_personunit, kw.INSERT)
    bob_atom.set_arg(kw.person_name, exx.bob)
    zia_atom = planatom_shop(kw.plan_personunit, kw.INSERT)
    zia_atom.set_arg(kw.person_name, exx.zia)

    # WHEN
    new_bob_planatom = sift_planatom(sue_plan, bob_atom)
    new_zia_planatom = sift_planatom(sue_plan, zia_atom)

    # THEN
    assert new_bob_planatom
    assert new_bob_planatom == bob_atom
    assert not new_zia_planatom


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_person_membership():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_personunit(exx.yao)
    sue_plan.add_personunit(exx.bob)
    yao_personunit = sue_plan.get_person(exx.yao)
    yao_personunit.add_membership(exx.run)
    print(f"{yao_personunit.memberships.keys()=}")

    bob_run_atom = planatom_shop(kw.plan_person_membership, kw.INSERT)
    bob_run_atom.set_arg(kw.person_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = planatom_shop(kw.plan_person_membership, kw.INSERT)
    yao_run_atom.set_arg(kw.person_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)

    # WHEN
    new_bob_run_planatom = sift_planatom(sue_plan, bob_run_atom)
    new_yao_run_planatom = sift_planatom(sue_plan, yao_run_atom)

    # THEN
    assert new_bob_run_planatom
    assert new_bob_run_planatom == bob_run_atom
    assert not new_yao_run_planatom


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_kegunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    root_rope = sue_plan.kegroot.get_keg_rope()
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    sweep_str = "sweep"
    sweep_rope = sue_plan.make_rope(clean_rope, sweep_str)

    root_atom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    root_atom.set_arg(kw.keg_rope, root_rope)
    casa_atom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    casa_atom.set_arg(kw.keg_rope, casa_rope)
    clean_atom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    clean_atom.set_arg(kw.keg_rope, clean_rope)
    sweep_atom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    sweep_atom.set_arg(kw.keg_rope, sweep_rope)
    assert not sift_planatom(sue_plan, root_atom)
    assert sift_planatom(sue_plan, casa_atom)
    assert sift_planatom(sue_plan, clean_atom)
    assert sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_keg(casa_rope)
    # THEN
    assert not sift_planatom(sue_plan, casa_atom)
    assert sift_planatom(sue_plan, clean_atom)
    assert sift_planatom(sue_plan, sweep_atom)

    # WHEN
    sue_plan.add_keg(clean_rope)
    # THEN
    assert not sift_planatom(sue_plan, casa_atom)
    assert not sift_planatom(sue_plan, clean_atom)
    assert sift_planatom(sue_plan, sweep_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_keg_awardunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    swim_str = "Swim"

    casa_swim_atom = create_xxx_swim_atom(casa_rope, swim_str)
    clean_swim_atom = create_xxx_swim_atom(clean_rope, swim_str)
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_keg_obj(casa_rope).set_awardunit(awardunit_shop(swim_str))

    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_keg_obj(clean_rope).set_awardunit(awardunit_shop(swim_str))
    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)


def create_xxx_swim_atom(x_rope, swim_str):
    result = planatom_shop(kw.plan_keg_awardunit, kw.INSERT)
    result.set_arg(kw.keg_rope, x_rope)
    result.set_arg(kw.awardee_title, swim_str)
    return result


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_keg_reasonunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    wk_rope = sue_plan.make_l1_rope("wk")

    casa_wk_atom = create_wk_atom(casa_rope, wk_rope)
    clean_wk_atom = create_wk_atom(clean_rope, wk_rope)
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    assert sift_planatom(sue_plan, casa_wk_atom)
    assert sift_planatom(sue_plan, clean_wk_atom)

    # WHEN
    sue_plan.get_keg_obj(casa_rope).set_reasonunit(reasonunit_shop(wk_rope))

    # THEN
    assert not sift_planatom(sue_plan, casa_wk_atom)
    assert sift_planatom(sue_plan, clean_wk_atom)

    # WHEN
    sue_plan.get_keg_obj(clean_rope).set_reasonunit(reasonunit_shop(wk_rope))
    # THEN
    assert not sift_planatom(sue_plan, casa_wk_atom)
    assert not sift_planatom(sue_plan, clean_wk_atom)


def create_wk_atom(casa_rope, wk_rope):
    result = planatom_shop(kw.plan_keg_reasonunit, kw.INSERT)
    result.set_arg(kw.keg_rope, casa_rope)
    result.set_arg(kw.reason_context, wk_rope)
    return result


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_keg_reason_caseunit_Exists():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    wk_rope = sue_plan.make_l1_rope("wk")
    thur_str = "thur"
    thur_rope = sue_plan.make_rope(wk_rope, thur_str)

    casa_wk_atom = planatom_shop(kw.plan_keg_reason_caseunit, kw.INSERT)
    casa_wk_atom.set_arg(kw.keg_rope, casa_rope)
    casa_wk_atom.set_arg(kw.reason_context, wk_rope)
    casa_wk_atom.set_arg(kw.reason_state, thur_rope)
    clean_wk_atom = planatom_shop(kw.plan_keg_reason_caseunit, kw.INSERT)
    clean_wk_atom.set_arg(kw.keg_rope, clean_rope)
    clean_wk_atom.set_arg(kw.reason_context, wk_rope)
    clean_wk_atom.set_arg(kw.reason_state, thur_rope)
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    casa_keg = sue_plan.get_keg_obj(casa_rope)
    clean_keg = sue_plan.get_keg_obj(clean_rope)
    casa_keg.set_reasonunit(reasonunit_shop(wk_rope))
    clean_keg.set_reasonunit(reasonunit_shop(wk_rope))
    assert sift_planatom(sue_plan, casa_wk_atom)
    assert sift_planatom(sue_plan, clean_wk_atom)

    # WHEN
    casa_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not sift_planatom(sue_plan, casa_wk_atom)
    assert sift_planatom(sue_plan, clean_wk_atom)

    # WHEN
    clean_keg.get_reasonunit(wk_rope).set_case(thur_rope)

    # THEN
    assert not sift_planatom(sue_plan, casa_wk_atom)
    assert not sift_planatom(sue_plan, clean_wk_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_keg_partyunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(kw.plan_keg_partyunit, kw.INSERT)
    casa_swim_atom.set_arg(kw.keg_rope, casa_rope)
    casa_swim_atom.set_arg(kw.party_title, swim_str)
    clean_swim_atom = planatom_shop(kw.plan_keg_partyunit, kw.INSERT)
    clean_swim_atom.set_arg(kw.keg_rope, clean_rope)
    clean_swim_atom.set_arg(kw.party_title, swim_str)
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_keg_obj(casa_rope).laborunit.add_party(swim_str)

    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_keg_obj(clean_rope).laborunit.add_party(swim_str)
    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_keg_healerunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    swim_str = "Swim"

    casa_swim_atom = planatom_shop(kw.plan_keg_healerunit, kw.INSERT)
    casa_swim_atom.set_arg(kw.keg_rope, casa_rope)
    casa_swim_atom.set_arg(kw.healer_name, swim_str)
    clean_swim_atom = planatom_shop(kw.plan_keg_healerunit, kw.INSERT)
    clean_swim_atom.set_arg(kw.keg_rope, clean_rope)
    clean_swim_atom.set_arg(kw.healer_name, swim_str)
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    assert sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_keg_obj(casa_rope).healerunit.set_healer_name(swim_str)

    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert sift_planatom(sue_plan, clean_swim_atom)

    # WHEN
    sue_plan.get_keg_obj(clean_rope).healerunit.set_healer_name(swim_str)
    # THEN
    assert not sift_planatom(sue_plan, casa_swim_atom)
    assert not sift_planatom(sue_plan, clean_swim_atom)


def test_sift_atom_ReturnsObj_PlanAtom_INSERT_plan_keg_factunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    clean_rope = sue_plan.make_rope(casa_rope, exx.clean)
    wk_rope = sue_plan.make_l1_rope("wk")

    casa_wk_atom = planatom_shop(kw.plan_keg_factunit, kw.INSERT)
    casa_wk_atom.set_arg(kw.keg_rope, casa_rope)
    casa_wk_atom.set_arg(kw.fact_context, wk_rope)
    clean_wk_atom = planatom_shop(kw.plan_keg_factunit, kw.INSERT)
    clean_wk_atom.set_arg(kw.keg_rope, clean_rope)
    clean_wk_atom.set_arg(kw.fact_context, wk_rope)
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    assert sift_planatom(sue_plan, casa_wk_atom)
    assert sift_planatom(sue_plan, clean_wk_atom)

    # WHEN
    sue_plan.get_keg_obj(casa_rope).set_factunit(factunit_shop(wk_rope))

    # THEN
    assert not sift_planatom(sue_plan, casa_wk_atom)
    assert sift_planatom(sue_plan, clean_wk_atom)

    # WHEN
    sue_plan.get_keg_obj(clean_rope).set_factunit(factunit_shop(wk_rope))
    # THEN
    assert not sift_planatom(sue_plan, casa_wk_atom)
    assert not sift_planatom(sue_plan, clean_wk_atom)
