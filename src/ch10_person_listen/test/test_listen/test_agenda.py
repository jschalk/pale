from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch06_keg.keg import kegunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch10_person_listen.listen_main import (
    create_empty_person_from_person,
    listen_to_speaker_agenda,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    zia_personunit = personunit_shop(exx.zia)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_personunit, zia_personunit)

    # THEN
    assertion_fail_str = f"listener '{exx.yao}' person is assumed to have {zia_personunit.person_name} partnerunit."
    assert str(excinfo.value) == assertion_fail_str


def test_listen_to_speaker_agenda_ReturnsEqualPerson():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    yao_personunit.add_partnerunit(exx.zia)
    yao_personunit.set_partner_respect(100)
    zia_personunit = personunit_shop(exx.zia)

    # WHEN
    after_yao_personunit = listen_to_speaker_agenda(yao_personunit, zia_personunit)

    # THEN
    assert after_yao_personunit == yao_personunit


def test_listen_to_speaker_agenda_ReturnsSingletaskPerson():
    # ESTABLISH
    before_yao_personunit = personunit_shop(exx.yao)
    before_yao_personunit.add_partnerunit(exx.zia)
    yao_partner_partner_debt_lumen = 77
    before_yao_personunit.set_partner_respect(yao_partner_partner_debt_lumen)
    zia_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    zia_clean_kegunit.laborunit.add_party(exx.yao)
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.add_partnerunit(exx.yao)
    zia_personunit.set_l1_keg(zia_clean_kegunit)
    assert len(zia_personunit.get_agenda_dict()) == 0
    zia_yao_personunit = copy_deepcopy(zia_personunit)
    zia_yao_personunit.set_person_name(exx.yao)
    assert len(zia_yao_personunit.get_agenda_dict()) == 1
    print(f"{zia_yao_personunit.get_agenda_dict()=}")

    # WHEN
    after_yao_personunit = listen_to_speaker_agenda(
        before_yao_personunit, zia_personunit
    )

    # THEN
    clean_rope = zia_personunit.make_l1_rope(exx.clean)
    yao_clean_kegunit = after_yao_personunit.get_keg_obj(clean_rope)
    print(f"{yao_clean_kegunit.star=}")
    assert yao_clean_kegunit.star != zia_clean_kegunit.star
    assert yao_clean_kegunit.star == yao_partner_partner_debt_lumen
    assert after_yao_personunit == before_yao_personunit
    assert len(after_yao_personunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2taskPerson():
    # ESTABLISH
    before_yao_personunit = personunit_shop(exx.yao)
    before_yao_personunit.add_partnerunit(exx.zia)
    yao_partner_debt_lumen = 77
    before_yao_personunit.set_partner_respect(yao_partner_debt_lumen)
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.add_partnerunit(exx.yao)
    zia_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    zia_clean_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_personunit.make_l1_rope("casa")
    zia_personunit.set_keg_obj(zia_clean_kegunit, casa_rope)
    assert len(zia_personunit.get_agenda_dict()) == 0
    zia_yao_personunit = copy_deepcopy(zia_personunit)
    zia_yao_personunit.set_person_name(exx.yao)
    assert len(zia_yao_personunit.get_agenda_dict()) == 1
    print(f"{zia_yao_personunit.get_agenda_dict()=}")

    # WHEN
    after_yao_personunit = listen_to_speaker_agenda(
        before_yao_personunit, zia_personunit
    )

    # THEN
    clean_rope = zia_personunit.make_rope(casa_rope, exx.clean)
    yao_clean_kegunit = after_yao_personunit.get_keg_obj(clean_rope)
    print(f"{yao_clean_kegunit.star=}")
    assert yao_clean_kegunit.star != zia_clean_kegunit.star
    assert yao_clean_kegunit.star == yao_partner_debt_lumen
    after_casa_kegunit = after_yao_personunit.get_keg_obj(casa_rope)
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == yao_partner_debt_lumen
    assert after_yao_personunit == before_yao_personunit
    assert len(after_yao_personunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaKegsLevel2taskPerson():
    # ESTABLISH
    before_yao_personunit = personunit_shop(exx.yao)
    before_yao_personunit.add_partnerunit(exx.zia)
    yao_partner_debt_lumen = 55
    before_yao_personunit.set_partner_respect(yao_partner_debt_lumen)

    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.add_partnerunit(exx.yao)
    fly_str = "fly"
    yao_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    yao_clean_kegunit.laborunit.add_party(exx.yao)
    yao_cuisine_kegunit = kegunit_shop(exx.cuisine, pledge=True)
    yao_cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_fly_kegunit = kegunit_shop(fly_str, pledge=True)
    yao_fly_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_personunit.make_l1_rope("casa")
    fly_rope = zia_personunit.make_l1_rope(fly_str)
    zia_personunit.set_keg_obj(yao_clean_kegunit, casa_rope)
    zia_personunit.set_keg_obj(yao_cuisine_kegunit, casa_rope)
    zia_personunit.set_l1_keg(yao_fly_kegunit)
    assert len(zia_personunit.get_agenda_dict()) == 0
    zia_yao_personunit = copy_deepcopy(zia_personunit)
    zia_yao_personunit.set_person_name(exx.yao)
    assert len(zia_yao_personunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_personunit = listen_to_speaker_agenda(
        before_yao_personunit, zia_personunit
    )

    # THEN
    clean_rope = zia_personunit.make_rope(casa_rope, exx.clean)
    cuisine_rope = zia_personunit.make_rope(casa_rope, exx.cuisine)
    after_cuisine_kegunit = after_yao_personunit.get_keg_obj(cuisine_rope)
    after_clean_kegunit = after_yao_personunit.get_keg_obj(clean_rope)
    after_casa_kegunit = after_yao_personunit.get_keg_obj(casa_rope)
    after_fly_kegunit = after_yao_personunit.get_keg_obj(fly_rope)
    print(f"{after_clean_kegunit.star=}")
    assert after_clean_kegunit.star != yao_clean_kegunit.star
    assert after_clean_kegunit.star == 19
    print(f"{after_cuisine_kegunit.star=}")
    assert after_cuisine_kegunit.star != yao_cuisine_kegunit.star
    assert after_cuisine_kegunit.star == 18
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == 37
    assert after_yao_personunit == before_yao_personunit
    assert len(after_yao_personunit.get_agenda_dict()) == 3
    assert after_fly_kegunit.star != 1
    assert after_fly_kegunit.star == 18


def test_listen_to_speaker_agenda_Returns2AgendaKegsLevel2taskPersonWhereAnKegUnitExistsInAdvance():
    # ESTABLISH
    before_yao_personunit = personunit_shop(exx.yao)
    before_yao_personunit.add_partnerunit(exx.zia)
    yao_partner_debt_lumen = 55
    before_yao_personunit.set_partner_respect(yao_partner_debt_lumen)
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.add_partnerunit(exx.yao)
    dish_str = "dish"
    fly_str = "fly"
    yao_dish_kegunit = kegunit_shop(dish_str, pledge=True)
    yao_dish_kegunit.laborunit.add_party(exx.yao)
    yao_cuisine_kegunit = kegunit_shop(exx.cuisine, pledge=True)
    yao_cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_fly_kegunit = kegunit_shop(fly_str, pledge=True)
    yao_fly_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_personunit.make_l1_rope("casa")
    dish_rope = zia_personunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_personunit.make_l1_rope(fly_str)
    before_yao_dish_kegunit = kegunit_shop(dish_str, pledge=True)
    before_yao_dish_kegunit.laborunit.add_party(exx.yao)
    before_yao_personunit.set_keg_obj(before_yao_dish_kegunit, casa_rope)
    before_yao_personunit.edit_keg_attr(dish_rope, star=1000)
    zia_personunit.set_keg_obj(yao_dish_kegunit, casa_rope)
    zia_personunit.set_keg_obj(yao_cuisine_kegunit, casa_rope)
    zia_personunit.set_l1_keg(yao_fly_kegunit)
    assert len(zia_personunit.get_agenda_dict()) == 0
    zia_yao_personunit = copy_deepcopy(zia_personunit)
    zia_yao_personunit.set_person_name(exx.yao)
    assert len(zia_yao_personunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_personunit = listen_to_speaker_agenda(
        before_yao_personunit, zia_personunit
    )

    # THEN
    cuisine_rope = zia_personunit.make_rope(casa_rope, exx.cuisine)
    after_cuisine_kegunit = after_yao_personunit.get_keg_obj(cuisine_rope)
    after_dish_kegunit = after_yao_personunit.get_keg_obj(dish_rope)
    after_casa_kegunit = after_yao_personunit.get_keg_obj(casa_rope)
    after_fly_kegunit = after_yao_personunit.get_keg_obj(fly_rope)
    print(f"{after_dish_kegunit.star=}")
    assert after_dish_kegunit.star != yao_dish_kegunit.star
    assert after_dish_kegunit.star == 1018
    print(f"{after_cuisine_kegunit.star=}")
    assert after_cuisine_kegunit.star != yao_cuisine_kegunit.star
    assert after_cuisine_kegunit.star == 19
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == 38
    assert after_yao_personunit == before_yao_personunit
    assert len(after_yao_personunit.get_agenda_dict()) == 3
    assert after_fly_kegunit.star != 1
    assert after_fly_kegunit.star == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalPerson():
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    sue_partner_cred_lumen = 57
    sue_partner_debt_lumen = 51
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_duty.set_partner_respect(yao_pool)

    sue_personunit = personunit_shop(exx.sue)
    sue_personunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_personunit.make_l1_rope(vacuum_str)
    sue_personunit.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = sue_personunit.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_personunit.make_l1_rope(egg_str)
    sue_personunit.set_l1_keg(kegunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_personunit.make_l1_rope(chicken_str)
    sue_personunit.set_l1_keg(kegunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_personunit.edit_keg_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_personunit.edit_keg_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    sue_personunit.cashout()
    assert sue_personunit.rational is False
    assert len(sue_personunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_person_from_person(yao_duty, exx.yao)
    yao_vision.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_vision.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_vision.set_partner_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_personunit)
    yao_vision.cashout()

    # THEN irrational person is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_partnerunit = yao_vision.get_partner(exx.zia)
    sue_partnerunit = yao_vision.get_partner(exx.sue)
    print(f"{sue_partnerunit.partner_debt_lumen=}")
    print(f"{sue_partnerunit.irrational_partner_debt_lumen=}")
    assert zia_partnerunit.irrational_partner_debt_lumen == 0
    assert sue_partnerunit.irrational_partner_debt_lumen == 51


def test_listen_to_speaker_agenda_ProcessesBarrenPerson():
    # ESTABLISH
    yao_duty = personunit_shop(exx.yao)
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    sue_partner_cred_lumen = 57
    sue_partner_debt_lumen = 51
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_duty.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_pool = 92
    yao_duty.set_partner_respect(yao_pool)

    # WHEN
    sue_vision = create_empty_person_from_person(yao_duty, exx.sue)
    yao_vision = create_empty_person_from_person(yao_duty, exx.yao)
    yao_vision.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    yao_vision.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)
    yao_vision.set_partner_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational person is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_partnerunit = yao_vision.get_partner(exx.zia)
    sue_partnerunit = yao_vision.get_partner(exx.sue)
    print(f"{sue_partnerunit.partner_debt_lumen=}")
    print(f"{sue_partnerunit.irrational_partner_debt_lumen=}")
    assert zia_partnerunit.irrational_partner_debt_lumen == 0
    assert zia_partnerunit.inallocable_partner_debt_lumen == 0
    assert sue_partnerunit.irrational_partner_debt_lumen == 0
    assert sue_partnerunit.inallocable_partner_debt_lumen == 51
