from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom.atom_main import beliefatom_shop
from src.ch09_belief_lesson.delta import beliefdelta_shop, get_minimal_beliefdelta
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_get_minimal_beliefdelta_ReturnsObjWithoutUnecessaryINSERT_belief_voiceunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(exx.yao)
    sue_belief.add_voiceunit(exx.bob)

    voices_beliefdelta = beliefdelta_shop()
    bob_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    bob_atom.set_arg(kw.voice_name, exx.bob)
    yao_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    yao_atom.set_arg(kw.voice_name, exx.yao)
    zia_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    zia_atom.set_arg(kw.voice_name, exx.zia)
    voices_beliefdelta.set_beliefatom(bob_atom)
    voices_beliefdelta.set_beliefatom(yao_atom)
    voices_beliefdelta.set_beliefatom(zia_atom)
    assert len(voices_beliefdelta.get_sorted_beliefatoms()) == 3
    assert len(sue_belief.voices) == 2

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(voices_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_sorted_beliefatoms()) == 1


def test_sift_ReturnsObjWithoutUnecessaryINSERT_belief_voice_membership():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(exx.yao)
    sue_belief.add_voiceunit(exx.bob)
    yao_voiceunit = sue_belief.get_voice(exx.yao)
    run_str = ";run"
    run_str = ";run"
    yao_voiceunit.add_membership(run_str)
    print(f"{yao_voiceunit.memberships.keys()=}")

    voices_beliefdelta = beliefdelta_shop()
    bob_run_atom = beliefatom_shop(kw.belief_voice_membership, kw.INSERT)
    bob_run_atom.set_arg(kw.voice_name, exx.bob)
    bob_run_atom.set_arg(kw.group_title, run_str)
    yao_run_atom = beliefatom_shop(kw.belief_voice_membership, kw.INSERT)
    yao_run_atom.set_arg(kw.voice_name, exx.yao)
    yao_run_atom.set_arg(kw.group_title, run_str)
    zia_run_atom = beliefatom_shop(kw.belief_voice_membership, kw.INSERT)
    zia_run_atom.set_arg(kw.voice_name, exx.zia)
    zia_run_atom.set_arg(kw.group_title, run_str)
    voices_beliefdelta.set_beliefatom(bob_run_atom)
    voices_beliefdelta.set_beliefatom(yao_run_atom)
    voices_beliefdelta.set_beliefatom(zia_run_atom)
    print(f"{len(voices_beliefdelta.get_dimen_sorted_beliefatoms_list())=}")
    assert len(voices_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 3

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(voices_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 2


# all atom dimens are covered by "sift_atom" tests
