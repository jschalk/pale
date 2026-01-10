from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson.delta import get_dimens_cruds_plandelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PlanDelta_get_dimens_cruds_plandelta_ReturnsObjWithCorrectDimensAndCRUDsBy_personunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.yao)
    after_sue_plan = planunit_shop(exx.sue)
    bob_person_cred_lumen = 33
    bob_person_debt_lumen = 44
    after_sue_plan.add_personunit(exx.bob, bob_person_cred_lumen, bob_person_debt_lumen)
    after_sue_plan.set_l1_keg(kegunit_shop("casa"))
    old_plandelta = plandelta_shop()
    old_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    dimen_set = [kw.plan_personunit]
    curd_set = {kw.INSERT}

    # WHEN
    new_plandelta = get_dimens_cruds_plandelta(old_plandelta, dimen_set, curd_set)

    # THEN
    new_plandelta.get_dimen_sorted_planatoms_list()
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 1
    sue_insert_dict = new_plandelta.planatoms.get(kw.INSERT)
    sue_personunit_dict = sue_insert_dict.get(kw.plan_personunit)
    bob_planatom = sue_personunit_dict.get(exx.bob)
    assert bob_planatom.get_value(kw.person_name) == exx.bob
    assert bob_planatom.get_value("person_cred_lumen") == bob_person_cred_lumen
    assert bob_planatom.get_value("person_debt_lumen") == bob_person_debt_lumen
