from src.ch06_keg.keg import kegunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_lesson.delta import beliefdelta_shop, get_dimens_cruds_beliefdelta
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_BeliefDelta_get_dimens_cruds_beliefdelta_ReturnsObjWithCorrectDimensAndCRUDsBy_voiceunit_insert():
    # ESTABLISH
    before_sue_belief = beliefunit_shop(exx.sue)
    before_sue_belief.add_voiceunit(exx.yao)
    after_sue_belief = beliefunit_shop(exx.sue)
    bob_voice_cred_lumen = 33
    bob_voice_debt_lumen = 44
    after_sue_belief.add_voiceunit(exx.bob, bob_voice_cred_lumen, bob_voice_debt_lumen)
    after_sue_belief.set_l1_keg(kegunit_shop("casa"))
    old_beliefdelta = beliefdelta_shop()
    old_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    dimen_set = [kw.belief_voiceunit]
    curd_set = {kw.INSERT}

    # WHEN
    new_beliefdelta = get_dimens_cruds_beliefdelta(old_beliefdelta, dimen_set, curd_set)

    # THEN
    new_beliefdelta.get_dimen_sorted_beliefatoms_list()
    assert len(new_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 1
    sue_insert_dict = new_beliefdelta.beliefatoms.get(kw.INSERT)
    sue_voiceunit_dict = sue_insert_dict.get(kw.belief_voiceunit)
    bob_beliefatom = sue_voiceunit_dict.get(exx.bob)
    assert bob_beliefatom.get_value(kw.voice_name) == exx.bob
    assert bob_beliefatom.get_value("voice_cred_lumen") == bob_voice_cred_lumen
    assert bob_beliefatom.get_value("voice_debt_lumen") == bob_voice_debt_lumen
