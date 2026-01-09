from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_tool import (
    get_credit_ledger,
    get_plan_voice_agenda_award_array,
    get_plan_voice_agenda_award_csv,
    get_voice_agenda_net_ledger,
    get_voice_mandate_ledger,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_plan_voice_agenda_award_array_ReturnsObj_ScenarioZeroVoiceUnits():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")

    # WHEN / THEN
    assert get_plan_voice_agenda_award_array(sue_plan) == []


def test_get_plan_voice_agenda_award_array_ReturnsObj_ScenarioSingleVoiceUnit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)

    # WHEN / THEN
    assert len(get_plan_voice_agenda_award_array(sue_plan)) == 1


def test_get_plan_voice_agenda_award_array_ReturnsObj_ScenarioMultipleVoiceUnit():
    # ESTABLISH
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.add_voiceunit(exx.zia)
    sue_plan.get_voice(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_voice(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_voice(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_voice(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_voice_agenda_award_array = get_plan_voice_agenda_award_array(sue_plan)

    # THEN
    assert len(plan_voice_agenda_award_array) == 3
    assert plan_voice_agenda_award_array[0][0] == exx.bob
    assert plan_voice_agenda_award_array[1][0] == exx.yao
    assert plan_voice_agenda_award_array[2][0] == exx.zia
    assert len(plan_voice_agenda_award_array[0]) == 3
    assert len(plan_voice_agenda_award_array[1]) == 3
    assert len(plan_voice_agenda_award_array[2]) == 3
    assert plan_voice_agenda_award_array[0][1] == bob_fund_agenda_take
    assert plan_voice_agenda_award_array[0][2] == bob_fund_agenda_give
    assert plan_voice_agenda_award_array[1][1] == yao_fund_agenda_take
    assert plan_voice_agenda_award_array[1][2] == yao_fund_agenda_give


def test_get_plan_voice_agenda_award_csv_ReturnsObj_ScenarioMultipleVoiceUnit():
    # ESTABLISH
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.add_voiceunit(exx.zia)
    sue_plan.get_voice(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_voice(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_voice(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_voice(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_voice_agenda_award_csv_str = get_plan_voice_agenda_award_csv(sue_plan)

    # THEN
    print(f"{plan_voice_agenda_award_csv_str=}")
    print("")
    example_csv_str = f"""voice_name,fund_agenda_take,fund_agenda_give
{exx.bob},{bob_fund_agenda_take},{bob_fund_agenda_give}
{exx.yao},{yao_fund_agenda_take},{yao_fund_agenda_give}
{exx.zia},0,0
"""
    print(f"{example_csv_str=}")
    assert plan_voice_agenda_award_csv_str == example_csv_str


def test_get_plan_voice_agenda_award_csv_ReturnsObj_cashout_True():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.add_voiceunit(exx.xio)
    sue_plan.add_voiceunit(exx.zia)
    empty_voice_agenda_award = f"""voice_name,fund_agenda_take,fund_agenda_give
{exx.bob},0,0
{exx.xio},0,0
{exx.yao},0,0
{exx.zia},0,0
"""
    assert empty_voice_agenda_award == get_plan_voice_agenda_award_csv(sue_plan)

    # WHEN
    plan_voice_agenda_award_csv_str = get_plan_voice_agenda_award_csv(
        sue_plan, cashout=True
    )

    # THEN
    print(f"{plan_voice_agenda_award_csv_str=}")
    print("")
    q_fund_agenda_give = int(sue_plan.fund_pool * 0.25)
    q_fund_agenda_take = int(sue_plan.fund_pool * 0.25)
    example_csv_str = f"""voice_name,fund_agenda_take,fund_agenda_give
{exx.bob},{q_fund_agenda_take},{q_fund_agenda_give}
{exx.xio},{q_fund_agenda_take},{q_fund_agenda_give}
{exx.yao},{q_fund_agenda_take},{q_fund_agenda_give}
{exx.zia},{q_fund_agenda_take},{q_fund_agenda_give}
"""
    print(f"{example_csv_str=}")
    assert plan_voice_agenda_award_csv_str == example_csv_str


def test_get_voice_mandate_ledger_ReturnsObj_Scenario0_MultipleVoiceUnit():
    # ESTABLISH
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_plan = planunit_shop("Sue", fund_pool=200)
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.add_voiceunit(exx.zia)
    sue_plan.get_voice(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_voice(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_voice(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_voice(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_bud_net_dict = get_voice_mandate_ledger(sue_plan)

    # THEN
    print(f"{plan_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.bob: 58,
        exx.yao: 142,
        exx.zia: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == plan_bud_net_dict


def test_get_voice_mandate_ledger_ReturnsObj_Scenario1_cashout_True():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao, 13, 5)
    sue_plan.add_voiceunit(exx.bob, 5, 7)
    sue_plan.add_voiceunit(exx.xio, 2, 3)
    sue_plan.add_voiceunit(exx.zia, 0, 0)
    pool4th = sue_plan.fund_pool / 4
    pre_settle_voice_mandate_ledger = {
        exx.bob: pool4th,
        exx.xio: pool4th,
        exx.yao: pool4th,
        exx.zia: pool4th,
    }
    assert get_voice_mandate_ledger(sue_plan) == pre_settle_voice_mandate_ledger

    # WHEN
    sue_plan_settle_net_dict = get_voice_mandate_ledger(sue_plan, cashout=True)

    # THEN
    assert sue_plan_settle_net_dict != pre_settle_voice_mandate_ledger
    print(f"{sue_plan_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.yao: 650000000,
        exx.bob: 250000000,
        exx.xio: 100000000,
        exx.zia: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_plan_settle_net_dict.get(exx.yao) != None
    assert sue_plan_settle_net_dict.get(exx.bob) != None
    assert sue_plan_settle_net_dict.get(exx.xio) != None
    assert sue_plan_settle_net_dict.get(exx.zia) != None
    assert sue_plan_settle_net_dict == example_bud_net_dict


def test_get_voice_mandate_ledger_ReturnsObj_Scenario2_No_voiceunits():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    empty_voice_mandate_ledger = {exx.sue: sue_plan.fund_pool}

    # WHEN / THEN
    assert get_voice_mandate_ledger(sue_plan) == empty_voice_mandate_ledger


def test_get_voice_mandate_ledger_ReturnsObj_Scenario3_No_planunit():
    # ESTABLISH / WHEN / THEN
    assert get_voice_mandate_ledger(None) == {}


def test_get_voice_mandate_ledger_ReturnsObj_Scenario4_MandateSumEqual_fund_pool():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao, 13, 5)
    sue_plan.add_voiceunit(exx.bob, 5, 7)
    sue_plan.add_voiceunit(exx.xio, 2, 3)
    sue_plan.add_voiceunit(exx.zia, 0, 0)
    pool4th = sue_plan.fund_pool / 4
    pre_settle_voice_mandate_ledger = {
        exx.bob: pool4th,
        exx.xio: pool4th,
        exx.yao: pool4th,
        exx.zia: pool4th,
    }
    assert get_voice_mandate_ledger(sue_plan) == pre_settle_voice_mandate_ledger

    # WHEN
    sue_plan_settle_net_dict = get_voice_mandate_ledger(sue_plan, cashout=True)

    # THEN
    assert sue_plan_settle_net_dict != pre_settle_voice_mandate_ledger
    print(f"{sue_plan_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.yao: 650000000,
        exx.bob: 250000000,
        exx.xio: 100000000,
        exx.zia: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_plan_settle_net_dict.get(exx.yao) != None
    assert sue_plan_settle_net_dict.get(exx.bob) != None
    assert sue_plan_settle_net_dict.get(exx.xio) != None
    assert sue_plan_settle_net_dict.get(exx.zia) != None
    assert sue_plan_settle_net_dict == example_bud_net_dict


def test_get_voice_mandate_ledger_ReturnsObj_Scenario5_Zero_fund_agenda_give():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_fund_pool = 800
    sue_plan.set_fund_pool(sue_fund_pool)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    floor_rope = sue_plan.make_rope(casa_rope, floor_str)
    clean_rope = sue_plan.make_rope(floor_rope, exx.clean)
    dirty_rope = sue_plan.make_rope(floor_rope, dirty_str)
    mop_rope = sue_plan.make_rope(casa_rope, exx.mop)
    sue_plan.add_keg(floor_rope)
    sue_plan.add_keg(clean_rope)
    sue_plan.add_keg(dirty_rope)
    sue_plan.add_keg(mop_rope, pledge=True)
    sue_plan.edit_keg_attr(mop_rope, reason_context=floor_rope, reason_case=clean_rope)
    sue_plan.add_voiceunit(exx.yao, 13, 5)

    # WHEN
    sue_plan_settle_net_dict = get_voice_mandate_ledger(sue_plan, cashout=True)

    # THEN
    assert sue_plan_settle_net_dict == {exx.yao: sue_fund_pool}


def test_get_voice_agenda_net_ledger_ReturnsObj_ScenarioMultipleVoiceUnit():
    # ESTABLISH
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.add_voiceunit(exx.zia)
    sue_plan.get_voice(exx.yao).fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_voice(exx.yao).fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_voice(exx.bob).fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_voice(exx.bob).fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_bud_net_dict = get_voice_agenda_net_ledger(sue_plan)

    # THEN
    print(f"{plan_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.bob: bob_fund_agenda_give - bob_fund_agenda_take,
        exx.yao: yao_fund_agenda_give - yao_fund_agenda_take,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == plan_bud_net_dict


def test_get_voice_agenda_net_ledger_ReturnsObj_cashout_True():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.add_voiceunit(exx.yao, 13, 5)
    sue_plan.add_voiceunit(exx.bob, 5, 7)
    sue_plan.add_voiceunit(exx.xio, 2, 3)
    sue_plan.add_voiceunit(exx.zia, 0, 0)
    assert get_voice_agenda_net_ledger(sue_plan) == {}

    # WHEN
    sue_plan_settle_net_dict = get_voice_agenda_net_ledger(sue_plan, cashout=True)

    # THEN
    print(f"{sue_plan_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        exx.bob: -216666667,
        exx.yao: 316666667,
        exx.xio: -100000000,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_plan_settle_net_dict.get(exx.yao) != None
    assert sue_plan_settle_net_dict.get(exx.bob) != None
    assert sue_plan_settle_net_dict.get(exx.xio) != None
    assert sue_plan_settle_net_dict.get(exx.zia) is None
    assert sue_plan_settle_net_dict == example_bud_net_dict


def test_get_credit_ledger_ReturnsObj_Scenario0_No_voiceunits():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    # WHEN / THEN
    assert get_credit_ledger(sue_plan) == {}


def test_get_credit_ledger_ReturnsObj_Scenario1_voiceunits_Exist():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    bob_voice_cred_lumen = 11
    yao_voice_cred_lumen = 13
    xio_voice_cred_lumen = 17
    sue_plan.add_voiceunit(exx.yao, yao_voice_cred_lumen)
    sue_plan.add_voiceunit(exx.bob, bob_voice_cred_lumen)
    sue_plan.add_voiceunit(exx.xio, xio_voice_cred_lumen)

    # WHEN
    sue_credit_ledger = get_credit_ledger(sue_plan)

    # THEN
    print(f"{sue_credit_ledger=}")
    print("")
    expected_sue_credit_ledger = {
        exx.bob: bob_voice_cred_lumen,
        exx.yao: yao_voice_cred_lumen,
        exx.xio: xio_voice_cred_lumen,
    }
    print(f"{expected_sue_credit_ledger=}")
    assert sue_credit_ledger.get(exx.yao) != None
    assert sue_credit_ledger.get(exx.bob) != None
    assert sue_credit_ledger.get(exx.xio) != None
    assert sue_credit_ledger.get(exx.zia) is None
    assert sue_credit_ledger == expected_sue_credit_ledger
