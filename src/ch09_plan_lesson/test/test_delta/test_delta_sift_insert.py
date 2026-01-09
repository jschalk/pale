from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import get_minimal_plandelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_get_minimal_plandelta_ReturnsObjWithoutUnecessaryINSERT_plan_voiceunit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)

    voices_plandelta = plandelta_shop()
    bob_atom = planatom_shop(kw.plan_voiceunit, kw.INSERT)
    bob_atom.set_arg(kw.voice_name, exx.bob)
    yao_atom = planatom_shop(kw.plan_voiceunit, kw.INSERT)
    yao_atom.set_arg(kw.voice_name, exx.yao)
    zia_atom = planatom_shop(kw.plan_voiceunit, kw.INSERT)
    zia_atom.set_arg(kw.voice_name, exx.zia)
    voices_plandelta.set_planatom(bob_atom)
    voices_plandelta.set_planatom(yao_atom)
    voices_plandelta.set_planatom(zia_atom)
    assert len(voices_plandelta.get_sorted_planatoms()) == 3
    assert len(sue_plan.voices) == 2

    # WHEN
    new_plandelta = get_minimal_plandelta(voices_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_sorted_planatoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_plan_voice_membership():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)
    yao_voiceunit = sue_plan.get_voice(exx.yao)
    yao_voiceunit.add_membership(exx.run)
    print(f"{yao_voiceunit.memberships.keys()=}")

    voices_plandelta = plandelta_shop()
    bob_run_atom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
    bob_run_atom.set_arg(kw.voice_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, exx.run)
    yao_run_atom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
    yao_run_atom.set_arg(kw.voice_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, exx.run)
    zia_run_atom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
    zia_run_atom.set_arg(kw.voice_name, exx.zia)
    zia_run_atom.set_arg(kw.group_title, exx.run)
    voices_plandelta.set_planatom(bob_run_atom)
    voices_plandelta.set_planatom(yao_run_atom)
    voices_plandelta.set_planatom(zia_run_atom)
    print(f"{len(voices_plandelta.get_dimen_sorted_planatoms_list())=}")
    assert len(voices_plandelta.get_dimen_sorted_planatoms_list()) == 3

    # WHEN
    new_plandelta = get_minimal_plandelta(voices_plandelta, sue_plan)

    # THEN
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
