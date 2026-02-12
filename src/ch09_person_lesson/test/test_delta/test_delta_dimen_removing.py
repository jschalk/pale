from src.ch06_keg.keg import kegunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson.delta import get_dimens_cruds_persondelta, persondelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PersonDelta_get_dimens_cruds_persondelta_ReturnsObjWithCorrectDimensAndCRUDsBy_partnerunit_insert():
    # ESTABLISH
    before_sue_person = personunit_shop(exx.sue)
    before_sue_person.add_partnerunit(exx.yao)
    after_sue_person = personunit_shop(exx.sue)
    bob_partner_cred_lumen = 33
    bob_partner_debt_lumen = 44
    after_sue_person.add_partnerunit(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    after_sue_person.set_l1_keg(kegunit_shop("casa"))
    old_persondelta = persondelta_shop()
    old_persondelta.add_all_different_personatoms(before_sue_person, after_sue_person)

    dimen_set = [kw.person_partnerunit]
    curd_set = {kw.INSERT}

    # WHEN
    new_persondelta = get_dimens_cruds_persondelta(old_persondelta, dimen_set, curd_set)

    # THEN
    new_persondelta.get_dimen_sorted_personatoms_list()
    assert len(new_persondelta.get_dimen_sorted_personatoms_list()) == 1
    sue_insert_dict = new_persondelta.personatoms.get(kw.INSERT)
    sue_partnerunit_dict = sue_insert_dict.get(kw.person_partnerunit)
    bob_personatom = sue_partnerunit_dict.get(exx.bob)
    assert bob_personatom.get_value(kw.partner_name) == exx.bob
    assert bob_personatom.get_value("partner_cred_lumen") == bob_partner_cred_lumen
    assert bob_personatom.get_value("partner_debt_lumen") == bob_partner_debt_lumen
