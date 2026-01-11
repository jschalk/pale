from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch10_plan_listen.listen_main import (
    _allocate_irrational_person_debt_lumen,
    generate_ingest_list,
    generate_perspective_agenda,
)
from src.ref.keywords import ExampleStrs as exx


def test_allocate_irrational_person_debt_lumen_SetsPlanAttr():
    # ESTABLISH
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    yao_plan = planunit_shop(exx.yao)
    yao_plan.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    zia_personunit = yao_plan.get_person(exx.zia)
    assert zia_personunit.irrational_person_debt_lumen == 0

    # WHEN
    _allocate_irrational_person_debt_lumen(yao_plan, exx.zia)

    # THEN
    assert zia_personunit.irrational_person_debt_lumen == zia_person_debt_lumen


def test_generate_perspective_agenda_GrabsAgendatasks():
    # ESTABLISH
    yao_speaker = planunit_shop(exx.yao)
    yao_speaker.add_personunit(exx.yao)
    yao_speaker.set_person_respect(20)
    casa_rope = yao_speaker.make_l1_rope(exx.casa)
    situation_str = "situation"
    situation_rope = yao_speaker.make_rope(casa_rope, situation_str)
    clean_rope = yao_speaker.make_rope(situation_rope, exx.clean)
    dirty_str = "dirty"
    dirty_rope = yao_speaker.make_rope(situation_rope, dirty_str)
    sweep_str = "sweep"
    sweep_rope = yao_speaker.make_rope(casa_rope, sweep_str)
    yao_speaker.set_keg_obj(kegunit_shop(exx.clean), situation_rope)
    yao_speaker.set_keg_obj(kegunit_shop(dirty_str), situation_rope)
    yao_speaker.set_keg_obj(kegunit_shop(sweep_str, pledge=True), casa_rope)
    yao_speaker.edit_keg_attr(
        sweep_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    yao_speaker.add_fact(situation_rope, clean_rope)
    assert len(yao_speaker.get_agenda_dict()) == 0

    # WHEN
    agenda_list = generate_perspective_agenda(yao_speaker)

    # THEN
    assert len(agenda_list) == 1


def test_generate_ingest_list_ReturnsList_v1():
    # ESTABLISH
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.set_l1_keg(kegunit_shop(exx.clean, pledge=True))
    zia_debtor_pool = 78
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        keg_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_planunit.make_l1_rope(exx.clean)
    clean_rope = zia_planunit.make_l1_rope(exx.clean)
    clean_kegunit = zia_planunit.get_keg_obj(clean_rope)
    assert ingested_list[0] == clean_kegunit
    assert ingested_list[0].star == zia_debtor_pool


def test_generate_ingest_list_ReturnsList_v2():
    # ESTABLISH
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.set_l1_keg(kegunit_shop(exx.clean, pledge=True))
    zia_planunit.set_l1_keg(kegunit_shop(exx.cuisine, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        keg_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_planunit.make_l1_rope(exx.clean)
    assert len(ingested_list) == 2
    clean_rope = zia_planunit.make_l1_rope(exx.clean)
    cuisine_rope = zia_planunit.make_l1_rope(exx.cuisine)
    clean_kegunit = zia_planunit.get_keg_obj(clean_rope)
    cuisine_kegunit = zia_planunit.get_keg_obj(cuisine_rope)
    assert ingested_list[0] == cuisine_kegunit
    assert ingested_list[0].star == 16.0
    assert ingested_list == [cuisine_kegunit, clean_kegunit]


def test_generate_ingest_list_ReturnsList_v3():
    # ESTABLISH
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.set_l1_keg(kegunit_shop(exx.clean, pledge=True))
    zia_planunit.set_l1_keg(kegunit_shop(exx.cuisine, star=3, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        keg_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_planunit.make_l1_rope(exx.clean)
    cuisine_rope = zia_planunit.make_l1_rope(exx.cuisine)
    clean_kegunit = zia_planunit.get_keg_obj(clean_rope)
    cuisine_kegunit = zia_planunit.get_keg_obj(cuisine_rope)
    assert ingested_list == [cuisine_kegunit, clean_kegunit]
    assert ingested_list[0].star == 24.0
    assert ingested_list[1].star == 8.0


def test_generate_ingest_list_ReturnsList_v4():
    # ESTABLISH
    zia_planunit = planunit_shop(exx.zia)
    zia_planunit.set_l1_keg(kegunit_shop(exx.clean, pledge=True))
    zia_planunit.set_l1_keg(kegunit_shop(exx.cuisine, star=2, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        keg_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_respect=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_planunit.make_l1_rope(exx.clean)
    cuisine_rope = zia_planunit.make_l1_rope(exx.cuisine)
    clean_kegunit = zia_planunit.get_keg_obj(clean_rope)
    cuisine_kegunit = zia_planunit.get_keg_obj(cuisine_rope)
    assert ingested_list[0].star == 22
    assert ingested_list[1].star == 10
    assert ingested_list == [cuisine_kegunit, clean_kegunit]
