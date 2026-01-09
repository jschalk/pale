from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch06_keg.keg import kegunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch10_belief_listen.listen_main import (
    create_empty_belief_from_belief,
    listen_to_speaker_agenda,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_speaker_agenda_RaisesErrorIfPoolIsNotSet():
    # ESTABLISH
    yao_beliefunit = beliefunit_shop(exx.yao)
    zia_beliefunit = beliefunit_shop(exx.zia)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_speaker_agenda(yao_beliefunit, zia_beliefunit)

    # THEN
    assertion_fail_str = f"listener '{exx.yao}' belief is assumed to have {zia_beliefunit.belief_name} voiceunit."
    assert str(excinfo.value) == assertion_fail_str


def test_listen_to_speaker_agenda_ReturnsEqualBelief():
    # ESTABLISH
    yao_beliefunit = beliefunit_shop(exx.yao)
    yao_beliefunit.add_voiceunit(exx.zia)
    yao_beliefunit.set_voice_respect(100)
    zia_beliefunit = beliefunit_shop(exx.zia)

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(yao_beliefunit, zia_beliefunit)

    # THEN
    assert after_yao_beliefunit == yao_beliefunit


def test_listen_to_speaker_agenda_ReturnsSingletaskBelief():
    # ESTABLISH
    before_yao_beliefunit = beliefunit_shop(exx.yao)
    before_yao_beliefunit.add_voiceunit(exx.zia)
    yao_voice_voice_debt_lumen = 77
    before_yao_beliefunit.set_voice_respect(yao_voice_voice_debt_lumen)
    zia_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    zia_clean_kegunit.laborunit.add_party(exx.yao)
    zia_beliefunit = beliefunit_shop(exx.zia)
    zia_beliefunit.add_voiceunit(exx.yao)
    zia_beliefunit.set_l1_keg(zia_clean_kegunit)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(exx.yao)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 1
    print(f"{zia_yao_beliefunit.get_agenda_dict()=}")

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    clean_rope = zia_beliefunit.make_l1_rope(exx.clean)
    yao_clean_kegunit = after_yao_beliefunit.get_keg_obj(clean_rope)
    print(f"{yao_clean_kegunit.star=}")
    assert yao_clean_kegunit.star != zia_clean_kegunit.star
    assert yao_clean_kegunit.star == yao_voice_voice_debt_lumen
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_ReturnsLevel2taskBelief():
    # ESTABLISH
    before_yao_beliefunit = beliefunit_shop(exx.yao)
    before_yao_beliefunit.add_voiceunit(exx.zia)
    yao_voice_debt_lumen = 77
    before_yao_beliefunit.set_voice_respect(yao_voice_debt_lumen)
    zia_beliefunit = beliefunit_shop(exx.zia)
    zia_beliefunit.add_voiceunit(exx.yao)
    zia_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    zia_clean_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_beliefunit.make_l1_rope("casa")
    zia_beliefunit.set_keg_obj(zia_clean_kegunit, casa_rope)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(exx.yao)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 1
    print(f"{zia_yao_beliefunit.get_agenda_dict()=}")

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    clean_rope = zia_beliefunit.make_rope(casa_rope, exx.clean)
    yao_clean_kegunit = after_yao_beliefunit.get_keg_obj(clean_rope)
    print(f"{yao_clean_kegunit.star=}")
    assert yao_clean_kegunit.star != zia_clean_kegunit.star
    assert yao_clean_kegunit.star == yao_voice_debt_lumen
    after_casa_kegunit = after_yao_beliefunit.get_keg_obj(casa_rope)
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == yao_voice_debt_lumen
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 1


def test_listen_to_speaker_agenda_Returns2AgendaKegsLevel2taskBelief():
    # ESTABLISH
    before_yao_beliefunit = beliefunit_shop(exx.yao)
    before_yao_beliefunit.add_voiceunit(exx.zia)
    yao_voice_debt_lumen = 55
    before_yao_beliefunit.set_voice_respect(yao_voice_debt_lumen)

    zia_beliefunit = beliefunit_shop(exx.zia)
    zia_beliefunit.add_voiceunit(exx.yao)
    fly_str = "fly"
    yao_clean_kegunit = kegunit_shop(exx.clean, pledge=True)
    yao_clean_kegunit.laborunit.add_party(exx.yao)
    yao_cuisine_kegunit = kegunit_shop(exx.cuisine, pledge=True)
    yao_cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_fly_kegunit = kegunit_shop(fly_str, pledge=True)
    yao_fly_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_beliefunit.make_l1_rope("casa")
    fly_rope = zia_beliefunit.make_l1_rope(fly_str)
    zia_beliefunit.set_keg_obj(yao_clean_kegunit, casa_rope)
    zia_beliefunit.set_keg_obj(yao_cuisine_kegunit, casa_rope)
    zia_beliefunit.set_l1_keg(yao_fly_kegunit)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(exx.yao)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    clean_rope = zia_beliefunit.make_rope(casa_rope, exx.clean)
    cuisine_rope = zia_beliefunit.make_rope(casa_rope, exx.cuisine)
    after_cuisine_kegunit = after_yao_beliefunit.get_keg_obj(cuisine_rope)
    after_clean_kegunit = after_yao_beliefunit.get_keg_obj(clean_rope)
    after_casa_kegunit = after_yao_beliefunit.get_keg_obj(casa_rope)
    after_fly_kegunit = after_yao_beliefunit.get_keg_obj(fly_rope)
    print(f"{after_clean_kegunit.star=}")
    assert after_clean_kegunit.star != yao_clean_kegunit.star
    assert after_clean_kegunit.star == 19
    print(f"{after_cuisine_kegunit.star=}")
    assert after_cuisine_kegunit.star != yao_cuisine_kegunit.star
    assert after_cuisine_kegunit.star == 18
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == 37
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 3
    assert after_fly_kegunit.star != 1
    assert after_fly_kegunit.star == 18


def test_listen_to_speaker_agenda_Returns2AgendaKegsLevel2taskBeliefWhereAnKegUnitExistsInAdvance():
    # ESTABLISH
    before_yao_beliefunit = beliefunit_shop(exx.yao)
    before_yao_beliefunit.add_voiceunit(exx.zia)
    yao_voice_debt_lumen = 55
    before_yao_beliefunit.set_voice_respect(yao_voice_debt_lumen)
    zia_beliefunit = beliefunit_shop(exx.zia)
    zia_beliefunit.add_voiceunit(exx.yao)
    dish_str = "dish"
    fly_str = "fly"
    yao_dish_kegunit = kegunit_shop(dish_str, pledge=True)
    yao_dish_kegunit.laborunit.add_party(exx.yao)
    yao_cuisine_kegunit = kegunit_shop(exx.cuisine, pledge=True)
    yao_cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_fly_kegunit = kegunit_shop(fly_str, pledge=True)
    yao_fly_kegunit.laborunit.add_party(exx.yao)
    casa_rope = zia_beliefunit.make_l1_rope("casa")
    dish_rope = zia_beliefunit.make_rope(casa_rope, dish_str)
    fly_rope = zia_beliefunit.make_l1_rope(fly_str)
    before_yao_dish_kegunit = kegunit_shop(dish_str, pledge=True)
    before_yao_dish_kegunit.laborunit.add_party(exx.yao)
    before_yao_beliefunit.set_keg_obj(before_yao_dish_kegunit, casa_rope)
    before_yao_beliefunit.edit_keg_attr(dish_rope, star=1000)
    zia_beliefunit.set_keg_obj(yao_dish_kegunit, casa_rope)
    zia_beliefunit.set_keg_obj(yao_cuisine_kegunit, casa_rope)
    zia_beliefunit.set_l1_keg(yao_fly_kegunit)
    assert len(zia_beliefunit.get_agenda_dict()) == 0
    zia_yao_beliefunit = copy_deepcopy(zia_beliefunit)
    zia_yao_beliefunit.set_belief_name(exx.yao)
    assert len(zia_yao_beliefunit.get_agenda_dict()) == 3

    # WHEN
    after_yao_beliefunit = listen_to_speaker_agenda(
        before_yao_beliefunit, zia_beliefunit
    )

    # THEN
    cuisine_rope = zia_beliefunit.make_rope(casa_rope, exx.cuisine)
    after_cuisine_kegunit = after_yao_beliefunit.get_keg_obj(cuisine_rope)
    after_dish_kegunit = after_yao_beliefunit.get_keg_obj(dish_rope)
    after_casa_kegunit = after_yao_beliefunit.get_keg_obj(casa_rope)
    after_fly_kegunit = after_yao_beliefunit.get_keg_obj(fly_rope)
    print(f"{after_dish_kegunit.star=}")
    assert after_dish_kegunit.star != yao_dish_kegunit.star
    assert after_dish_kegunit.star == 1018
    print(f"{after_cuisine_kegunit.star=}")
    assert after_cuisine_kegunit.star != yao_cuisine_kegunit.star
    assert after_cuisine_kegunit.star == 19
    print(f"{after_casa_kegunit.star=}")
    assert after_casa_kegunit.star != 1
    assert after_casa_kegunit.star == 38
    assert after_yao_beliefunit == before_yao_beliefunit
    assert len(after_yao_beliefunit.get_agenda_dict()) == 3
    assert after_fly_kegunit.star != 1
    assert after_fly_kegunit.star == 18


def test_listen_to_speaker_agenda_ProcessesIrrationalBelief():
    # ESTABLISH
    yao_duty = beliefunit_shop(exx.yao)
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    sue_voice_cred_lumen = 57
    sue_voice_debt_lumen = 51
    yao_duty.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_duty.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_duty.set_voice_respect(yao_pool)

    sue_beliefunit = beliefunit_shop(exx.sue)
    sue_beliefunit.set_max_tree_traverse(6)
    vacuum_str = "vacuum"
    vacuum_rope = sue_beliefunit.make_l1_rope(vacuum_str)
    sue_beliefunit.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = sue_beliefunit.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_beliefunit.make_l1_rope(egg_str)
    sue_beliefunit.set_l1_keg(kegunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_beliefunit.make_l1_rope(chicken_str)
    sue_beliefunit.set_l1_keg(kegunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_beliefunit.edit_keg_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_beliefunit.edit_keg_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    sue_beliefunit.cashout()
    assert sue_beliefunit.rational is False
    assert len(sue_beliefunit.get_agenda_dict()) == 3

    # WHEN
    yao_vision = create_empty_belief_from_belief(yao_duty, exx.yao)
    yao_vision.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_vision.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_vision.set_voice_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, sue_beliefunit)
    yao_vision.cashout()

    # THEN irrational belief is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_voiceunit = yao_vision.get_voice(exx.zia)
    sue_voiceunit = yao_vision.get_voice(exx.sue)
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.irrational_voice_debt_lumen=}")
    assert zia_voiceunit.irrational_voice_debt_lumen == 0
    assert sue_voiceunit.irrational_voice_debt_lumen == 51


def test_listen_to_speaker_agenda_ProcessesBarrenBelief():
    # ESTABLISH
    yao_duty = beliefunit_shop(exx.yao)
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    sue_voice_cred_lumen = 57
    sue_voice_debt_lumen = 51
    yao_duty.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_duty.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_duty.set_voice_respect(yao_pool)

    # WHEN
    sue_vision = create_empty_belief_from_belief(yao_duty, exx.sue)
    yao_vision = create_empty_belief_from_belief(yao_duty, exx.yao)
    yao_vision.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_vision.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_vision.set_voice_respect(yao_pool)
    yao_vision = listen_to_speaker_agenda(yao_vision, speaker=sue_vision)

    # THEN irrational belief is ignored
    assert len(yao_vision.get_agenda_dict()) != 3
    assert len(yao_vision.get_agenda_dict()) == 0
    zia_voiceunit = yao_vision.get_voice(exx.zia)
    sue_voiceunit = yao_vision.get_voice(exx.sue)
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.irrational_voice_debt_lumen=}")
    assert zia_voiceunit.irrational_voice_debt_lumen == 0
    assert zia_voiceunit.inallocable_voice_debt_lumen == 0
    assert sue_voiceunit.irrational_voice_debt_lumen == 0
    assert sue_voiceunit.inallocable_voice_debt_lumen == 51
