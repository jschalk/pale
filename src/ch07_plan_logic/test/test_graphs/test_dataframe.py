from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_report import (
    get_plan_agenda_dataframe,
    get_plan_personunits_dataframe,
)
from src.ch07_plan_logic.test._util.ch07_examples import planunit_v001_with_large_agenda
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_get_plan_personunits_dataframe_ReturnsDataFrame():
    # ESTABLISH
    luca_plan = planunit_shop()
    luca_plan.set_credor_respect(500)
    luca_plan.set_debtor_respect(400)
    yao_person_cred_lumen = 66
    yao_person_debt_lumen = 77
    luca_plan.add_personunit(exx.yao, yao_person_cred_lumen, yao_person_debt_lumen)
    sue_person_cred_lumen = 434
    sue_person_debt_lumen = 323
    luca_plan.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)

    # WHEN
    x_df = get_plan_personunits_dataframe(luca_plan)

    # THEN
    personunit_colums = {
        kw.person_name,
        "person_cred_lumen",
        "person_debt_lumen",
        "memberships",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
    assert x_df.shape[0] == 2


def test_get_plan_personunits_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    luca_plan = planunit_shop()

    # WHEN
    x_df = get_plan_personunits_dataframe(luca_plan)

    # THEN
    personunit_colums = {
        kw.person_name,
        "person_cred_lumen",
        "person_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
    assert x_df.shape[0] == 0


def test_get_plan_agenda_dataframe_ReturnsDataFrame():
    # ESTABLISH
    yao_plan = planunit_v001_with_large_agenda()
    assert len(yao_plan.get_agenda_dict()) == 69

    # WHEN
    x_df = get_plan_agenda_dataframe(yao_plan)
    print(x_df)

    # THEN
    personunit_colums = {
        kw.plan_name,
        "fund_ratio",
        kw.keg_label,
        kw.parent_rope,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
    assert x_df.shape[0] == 69


def test_get_plan_agenda_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    assert len(yao_plan.get_agenda_dict()) == 0

    # WHEN
    x_df = get_plan_agenda_dataframe(yao_plan)
    print(x_df)

    # THEN
    personunit_colums = {
        kw.plan_name,
        "fund_ratio",
        kw.keg_label,
        kw.parent_rope,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
