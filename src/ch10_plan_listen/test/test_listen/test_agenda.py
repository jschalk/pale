from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch10_plan_listen.listen_main import (
    create_empty_plan_from_plan,
    listen_to_speaker_agenda,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_planunit = planunit_shop(exx.yao)
    zia_planunit = planunit_shop(exx.zia)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_planunit, zia_planunit)

    # THEN
    assertion_fail_str = f"listener '{exx.yao}' plan is assumed to have {zia_planunit.plan_name} personunit."
    assert str(excinfo.value) == assertion_fail_str


def test_listen_to_speaker_agenda_ReturnsEqualPlan():
    # ESTABLISH
    yao_planunit = planunit_shop(exx.yao)
    yao_planunit.add_personunit(exx.zia)
    yao_planunit.set_person_respect(100)
    zia_planunit = planunit_shop(exx.zia)

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(yao_planunit, zia_planunit)

    # THEN
    assert after_yao_planunit == yao_planunit


def test_listen_to_speaker_agenda_ReturnsSingletaskPlan():
    # ESTABLISH
    before_yao_planunit = planunit_shop(exx.yao)
    before_yao_planunit.add_personunit(exx.zia)
    yao_person_person_debt_lumen = 77
    before_yao_planunit.set_person_respect(yao_person_person_debt_lumen)
    zia_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    zia_clean_kegunit.laborunit.add_party(exx.yao)
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.add_personunit(exx.yao)
    zia_planunit.set_l1_keg(zia_clean_kegunit)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_plan_name(exx.yao)
    assert len(zia_yao_planunit.get_agenda_dict()) == 1
    print(f"{zia_yao_planunit.get_agenda_dict()=}")

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    clean_rope = zia_planunit.make_l1_rope(exx.clean)
    yao_clean_kegunit = after_yao_planunit.get_keg_obj(clean_rope)
    print(f"{yao_clean_kegunit.star=}")
    assert yao_clean_kegunit.star != zia_clean_kegunit.star
    assert yao_clean_kegunit.star == yao_person_person_debt_lumen
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2taskPlan():
    # ESTABLISH
    before_yao_planunit = planunit_shop(exx.yao)
    before_yao_planunit.add_personunit(exx.zia)
    yao_person_debt_lumen = 77
    before_yao_planunit.set_person_respect(yao_person_debt_lumen)
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.add_personunit(exx.yao)
    zia_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    zia_clean_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_planunit.make_l1_rope("casa")
    zia_planunit.set_keg_obj(zia_clean_kegunit, casa_rope)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_plan_name(exx.yao)
    assert len(zia_yao_planunit.get_agenda_dict()) == 1
    print(f"{zia_yao_planunit.get_agenda_dict()=}")

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    clean_rope = zia_planunit.make_rope(casa_rope, exx.clean)
    yao_clean_kegunit = after_yao_planunit.get_keg_obj(clean_rope)
    print(f"{yao_clean_kegunit.star=}")
    assert yao_clean_kegunit.star != zia_clean_kegunit.star
    assert yao_clean_kegunit.star == yao_person_debt_lumen
    after_casa_kegunit = after_yao_planunit.get_keg_obj(casa_rope)
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == yao_person_debt_lumen
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaKegsLevel2taskPlan():
    # ESTABLISH
    before_yao_planunit = planunit_shop(exx.yao)
    before_yao_planunit.add_personunit(exx.zia)
    yao_person_debt_lumen = 55
    before_yao_planunit.set_person_respect(yao_person_debt_lumen)

    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.add_personunit(exx.yao)
    fly_str = "fly"
    yao_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    yao_clean_kegunit.laborunit.add_party(exx.yao)
    yao_cuisine_kegunit = kegunit_shop(exx.cuisine, pledge=True)
    yao_cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_fly_kegunit = kegunit_shop(fly_str, pledge=True)
    yao_fly_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_planunit.make_l1_rope("casa")
    fly_rope = zia_planunit.make_l1_rope(fly_str)
    zia_planunit.set_keg_obj(yao_clean_kegunit, casa_rope)
    zia_planunit.set_keg_obj(yao_cuisine_kegunit, casa_rope)
    zia_planunit.set_l1_keg(yao_fly_kegunit)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_plan_name(exx.yao)
    assert len(zia_yao_planunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    clean_rope = zia_planunit.make_rope(casa_rope, exx.clean)
    cuisine_rope = zia_planunit.make_rope(casa_rope, exx.cuisine)
    after_cuisine_kegunit = after_yao_planunit.get_keg_obj(cuisine_rope)
    after_clean_kegunit = after_yao_planunit.get_keg_obj(clean_rope)
    after_casa_kegunit = after_yao_planunit.get_keg_obj(casa_rope)
    after_fly_kegunit = after_yao_planunit.get_keg_obj(fly_rope)
    print(f"{after_clean_kegunit.star=}")
    assert after_clean_kegunit.star != yao_clean_kegunit.star
    assert after_clean_kegunit.star == 19
    print(f"{after_cuisine_kegunit.star=}")
    assert after_cuisine_kegunit.star != yao_cuisine_kegunit.star
    assert after_cuisine_kegunit.star == 18
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == 37
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 3
    assert after_fly_kegunit.star != 1
    assert after_fly_kegunit.star == 18


def test_listen_to_speaker_agenda_Returns2AgendaKegsLevel2taskPlanWhereAnKegUnitExistsInAdvance():
    # ESTABLISH
    before_yao_planunit = planunit_shop(exx.yao)
    before_yao_planunit.add_personunit(exx.zia)
    yao_person_debt_lumen = 55
    before_yao_planunit.set_person_respect(yao_person_debt_lumen)
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.add_personunit(exx.yao)
    dish_str = "dish"
    fly_str = "fly"
    yao_dish_kegunit = kegunit_shop(dish_str, pledge=True)
    yao_dish_kegunit.laborunit.add_party(exx.yao)
    yao_cuisine_kegunit = kegunit_shop(exx.cuisine, pledge=True)
    yao_cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_fly_kegunit = kegunit_shop(fly_str, pledge=True)
    yao_fly_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_planunit.make_l1_rope("casa")
    dish_rope = zia_planunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_planunit.make_l1_rope(fly_str)
    before_yao_dish_kegunit = kegunit_shop(dish_str, pledge=True)
    before_yao_dish_kegunit.laborunit.add_party(exx.yao)
    before_yao_planunit.set_keg_obj(before_yao_dish_kegunit, casa_rope)
    before_yao_planunit.edit_keg_attr(dish_rope, star=1000)
    zia_planunit.set_keg_obj(yao_dish_kegunit, casa_rope)
    zia_planunit.set_keg_obj(yao_cuisine_kegunit, casa_rope)
    zia_planunit.set_l1_keg(yao_fly_kegunit)
    assert len(zia_planunit.get_agenda_dict()) == 0
    zia_yao_planunit = copy_deepcopy(zia_planunit)
    zia_yao_planunit.set_plan_name(exx.yao)
    assert len(zia_yao_planunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_planunit = listen_to_speaker_agenda(before_yao_planunit, zia_planunit)

    # THEN
    cuisine_rope = zia_planunit.make_rope(casa_rope, exx.cuisine)
    after_cuisine_kegunit = after_yao_planunit.get_keg_obj(cuisine_rope)
    after_dish_kegunit = after_yao_planunit.get_keg_obj(dish_rope)
    after_casa_kegunit = after_yao_planunit.get_keg_obj(casa_rope)
    after_fly_kegunit = after_yao_planunit.get_keg_obj(fly_rope)
    print(f"{after_dish_kegunit.star=}")
    assert after_dish_kegunit.star != yao_dish_kegunit.star
    assert after_dish_kegunit.star == 1018
    print(f"{after_cuisine_kegunit.star=}")
    assert after_cuisine_kegunit.star != yao_cuisine_kegunit.star
    assert after_cuisine_kegunit.star == 19
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == 38
    assert after_yao_planunit == before_yao_planunit
    assert len(after_yao_planunit.get_agenda_dict()) == 3
    assert after_fly_kegunit.star != 1
    assert after_fly_kegunit.star == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalPlan():
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao)
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    sue_person_cred_lumen = 57
    sue_person_debt_lumen = 51
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_duty.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    yao_pool = 92
    yao_duty.set_person_respect(yao_pool)

    sue_planunit = planunit_shop(exx.sue)
    sue_planunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_planunit.make_l1_rope(vacuum_str)
    sue_planunit.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = sue_planunit.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_planunit.make_l1_rope(egg_str)
    sue_planunit.set_l1_keg(kegunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_planunit.make_l1_rope(chicken_str)
    sue_planunit.set_l1_keg(kegunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_planunit.edit_keg_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_planunit.edit_keg_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    sue_planunit.cashout()
    assert sue_planunit.rational is False
    assert len(sue_planunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_plan_from_plan(yao_duty, exx.yao)
    yao_vision.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_vision.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    yao_vision.set_person_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_planunit)
    yao_vision.cashout()

    # THEN irrational plan is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_personunit = yao_vision.get_person(exx.zia)
    sue_personunit = yao_vision.get_person(exx.sue)
    print(f"{sue_personunit.person_debt_lumen=}")
    print(f"{sue_personunit.irrational_person_debt_lumen=}")
    assert zia_personunit.irrational_person_debt_lumen == 0
    assert sue_personunit.irrational_person_debt_lumen == 51


def test_listen_to_speaker_agenda_ProcessesBarrenPlan():
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao)
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    sue_person_cred_lumen = 57
    sue_person_debt_lumen = 51
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_duty.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    yao_pool = 92
    yao_duty.set_person_respect(yao_pool)

    # WHEN
    sue_vision = create_empty_plan_from_plan(yao_duty, exx.sue)
    yao_vision = create_empty_plan_from_plan(yao_duty, exx.yao)
    yao_vision.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_vision.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    yao_vision.set_person_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational plan is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_personunit = yao_vision.get_person(exx.zia)
    sue_personunit = yao_vision.get_person(exx.sue)
    print(f"{sue_personunit.person_debt_lumen=}")
    print(f"{sue_personunit.irrational_person_debt_lumen=}")
    assert zia_personunit.irrational_person_debt_lumen == 0
    assert zia_personunit.inallocable_person_debt_lumen == 0
    assert sue_personunit.irrational_person_debt_lumen == 0
    assert sue_personunit.inallocable_person_debt_lumen == 51
