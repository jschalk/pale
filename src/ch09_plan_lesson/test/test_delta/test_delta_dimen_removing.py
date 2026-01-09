from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson.delta import get_dimens_cruds_plandelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PlanDelta_get_dimens_cruds_plandelta_ReturnsObjWithCorrectDimensAndCRUDsBy_voiceunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_voiceunit(exx.yao)
    after_sue_plan = planunit_shop(exx.sue)
    bob_voice_cred_lumen = 33
    bob_voice_debt_lumen = 44
    after_sue_plan.add_voiceunit(exx.bob, bob_voice_cred_lumen, bob_voice_debt_lumen)
    after_sue_plan.set_l1_keg(kegunit_shop("casa"))
    old_plandelta = plandelta_shop()
    old_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    dimen_set = [kw.plan_voiceunit]
    curd_set = {kw.INSERT}

    # WHEN
    new_plandelta = get_dimens_cruds_plandelta(old_plandelta, dimen_set, curd_set)

    # THEN
    new_plandelta.get_dimen_sorted_planatoms_list()
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 1
    sue_insert_dict = new_plandelta.planatoms.get(kw.INSERT)
    sue_voiceunit_dict = sue_insert_dict.get(kw.plan_voiceunit)
    bob_planatom = sue_voiceunit_dict.get(exx.bob)
    assert bob_planatom.get_value(kw.voice_name) == exx.bob
    assert bob_planatom.get_value("voice_cred_lumen") == bob_voice_cred_lumen
    assert bob_planatom.get_value("voice_debt_lumen") == bob_voice_debt_lumen
