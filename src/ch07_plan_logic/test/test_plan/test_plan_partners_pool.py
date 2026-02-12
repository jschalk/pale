from pytest import raises as pytest_raises
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_set_credor_respect_SetsAttr():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_plan.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_plan.credor_respect == x_credor_respect


def test_PlanUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_plan = planunit_shop(exx.zia)
    x_credor_respect = 23
    zia_plan.set_credor_respect(x_credor_respect)
    assert zia_plan.respect_grain == 1
    assert zia_plan.credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_credor_respect(new_credor_respect)

    # THEN
    assert (
        str(excinfo.value)
        == f"Plan '{exx.zia}' cannot set credor_respect='{new_credor_respect}'. It is not divisible byrespect_grain'{zia_plan.respect_grain}'"
    )


def test_PlanUnit_set_debtor_respect_SetsInt():
    # ESTABLISH
    zia_plan = planunit_shop(plan_name=exx.zia)
    zia_debtor_respect = 13
    assert zia_plan.debtor_respect != zia_debtor_respect

    # WHEN
    zia_plan.set_debtor_respect(zia_debtor_respect)
    # THEN
    assert zia_plan.debtor_respect == zia_debtor_respect


def test_PlanUnit_set_debtor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_plan = planunit_shop(exx.zia)
    x_debtor_respect = 23
    zia_plan.set_debtor_respect(x_debtor_respect)
    assert zia_plan.respect_grain == 1
    assert zia_plan.debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_debtor_respect(new_debtor_respect)

    # THEN
    assert (
        str(excinfo.value)
        == f"Plan '{exx.zia}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible byrespect_grain'{zia_plan.respect_grain}'"
    )


def test_PlanUnit_set_partner_respect_SetsAttrs():
    # ESTABLISH
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_plan = planunit_shop(exx.zia)
    zia_plan.set_credor_respect(old_credor_respect)
    zia_plan.set_debtor_respect(old_debtor_respect)
    zia_plan.set_fund_pool(old_fund_pool)
    assert zia_plan.credor_respect == old_credor_respect
    assert zia_plan.debtor_respect == old_debtor_respect
    assert zia_plan.fund_pool == old_fund_pool

    # WHEN
    new_partner_pool = 200
    zia_plan.set_partner_respect(new_partner_pool)

    # THEN
    assert zia_plan.credor_respect == new_partner_pool
    assert zia_plan.debtor_respect == new_partner_pool
    assert zia_plan.fund_pool == new_partner_pool
