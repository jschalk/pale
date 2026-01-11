from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch02_person._ref.ch02_semantic_types import NameTerm
from src.ch02_person.person import (
    PersonUnit,
    default_groupmark_if_None,
    is_nameterm,
    personunit_shop,
    validate_nameterm,
)
from src.ref.keywords import Ch02Keywords as kw, ExampleStrs as exx


def test_is_nameterm_ReturnsObj():
    # ESTABLISH
    x_groupmark = default_groupmark_if_None()

    # WHEN / THEN
    assert is_nameterm("", groupmark=x_groupmark) is False
    assert is_nameterm("casa", groupmark=x_groupmark)
    assert not is_nameterm(f"ZZ{x_groupmark}casa", x_groupmark)
    assert not is_nameterm(NameTerm(f"ZZ{x_groupmark}casa"), x_groupmark)
    assert is_nameterm(NameTerm("YY"), x_groupmark)


def test_validate_nameterm_Scenario0_RaisesErrorWhenNotNameTerm():
    # ESTABLISH
    bob_str = "Bob, Tom"
    assert bob_str == validate_nameterm(bob_str, x_groupmark=exx.slash)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_nameterm(bob_str, x_groupmark=comma_str)

    # THEN
    assert (
        str(excinfo.value)
        == f"'{bob_str}' must be a NameTerm. Cannot contain GroupMark: '{comma_str}'"
    )


def test_validate_nameterm_Scenario1_RaisesErrorWhenNameTerm():
    # ESTABLISH
    bob_str = f"Bob{exx.slash}Tom"
    assert bob_str == validate_nameterm(
        bob_str, x_groupmark=exx.slash, not_nameterm_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        bob_str == validate_nameterm(
            bob_str, x_groupmark=comma_str, not_nameterm_required=True
        )

    # THEN
    assert (
        str(excinfo.value)
        == f"'{bob_str}' must not be a NameTerm. Must contain GroupMark: '{comma_str}'"
    )


def test_PersonUnit_Exists():
    # ESTABLISH

    # WHEN
    bob_personunit = PersonUnit(exx.bob)

    # THEN
    print(f"{exx.bob}")
    assert bob_personunit
    assert bob_personunit.person_name
    assert bob_personunit.person_name == exx.bob
    assert not bob_personunit.person_cred_lumen
    assert not bob_personunit.person_debt_lumen
    # calculated fields
    assert not bob_personunit.credor_pool
    assert not bob_personunit.debtor_pool
    assert not bob_personunit.memberships
    assert not bob_personunit.irrational_person_debt_lumen
    assert not bob_personunit.inallocable_person_debt_lumen
    assert not bob_personunit.fund_give
    assert not bob_personunit.fund_take
    assert not bob_personunit.fund_agenda_give
    assert not bob_personunit.fund_agenda_take
    assert not bob_personunit.groupmark
    assert not bob_personunit.respect_grain
    obj_attrs = set(bob_personunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_agenda_take,
        kw.fund_give,
        kw.fund_take,
        kw.inallocable_person_debt_lumen,
        kw.irrational_person_debt_lumen,
        kw.memberships,
        kw.respect_grain,
        kw.person_name,
        kw.groupmark,
        kw.person_cred_lumen,
        kw.person_debt_lumen,
    }


def test_PersonUnit_set_nameterm_SetsAttr():
    # ESTABLISH
    x_personunit = PersonUnit()

    # WHEN
    x_personunit.set_name(exx.bob)

    # THEN
    assert x_personunit.person_name == exx.bob


def test_PersonUnit_set_nameterm_RaisesErrorIfParameterContains_groupmark():
    # ESTABLISH
    texas_str = f"Texas{exx.slash}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_name=texas_str, groupmark=exx.slash)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' must be a NameTerm. Cannot contain {kw.GroupMark}: '{exx.slash}'"
    )


def test_personunit_shop_SetsAttributes():
    # ESTABLISH

    # WHEN
    yao_personunit = personunit_shop(person_name=exx.yao)

    # THEN
    assert yao_personunit.person_name == exx.yao
    assert yao_personunit.person_cred_lumen == 1
    assert yao_personunit.person_debt_lumen == 1
    # calculated fields
    assert yao_personunit.credor_pool == 0
    assert yao_personunit.debtor_pool == 0
    assert yao_personunit.memberships == {}
    assert yao_personunit.irrational_person_debt_lumen == 0
    assert yao_personunit.inallocable_person_debt_lumen == 0
    assert yao_personunit.fund_give == 0
    assert yao_personunit.fund_take == 0
    assert yao_personunit.fund_agenda_give == 0
    assert yao_personunit.fund_agenda_take == 0
    assert yao_personunit.fund_agenda_ratio_give == 0
    assert yao_personunit.fund_agenda_ratio_take == 0
    assert yao_personunit.groupmark == default_groupmark_if_None()
    assert yao_personunit.respect_grain == default_grain_num_if_None()


def test_personunit_shop_SetsAttributes_groupmark():
    # ESTABLISH

    # WHEN
    yao_personunit = personunit_shop("Yao", groupmark=exx.slash)

    # THEN
    assert yao_personunit.groupmark == exx.slash


def test_personunit_shop_SetsAttributes_respect_grain():
    # ESTABLISH
    respect_grain_float = 00.45

    # WHEN
    yao_personunit = personunit_shop("Yao", respect_grain=respect_grain_float)

    # THEN
    assert yao_personunit.respect_grain == respect_grain_float


def test_PersonUnit_set_respect_grain_SetsAttribute():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.respect_grain == 1

    # WHEN
    x_respect_grain = 5
    bob_personunit.set_respect_grain(x_respect_grain)

    # THEN
    assert bob_personunit.respect_grain == x_respect_grain


def test_PersonUnit_set_person_cred_lumen_SetsAttribute():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")

    # WHEN
    x_person_cred_lumen = 23
    bob_personunit.set_person_cred_lumen(x_person_cred_lumen)

    # THEN
    assert bob_personunit.person_cred_lumen == x_person_cred_lumen


def test_PersonUnit_set_person_debt_lumen_SetsAttribute():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")

    # WHEN
    x_person_debt_lumen = 23
    bob_personunit.set_person_debt_lumen(x_person_debt_lumen)

    # THEN
    assert bob_personunit.person_debt_lumen == x_person_debt_lumen


def test_PersonUnit_set_credor_person_debt_lumen_SetsAttr_Scenario0():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.person_cred_lumen == 1
    assert bob_personunit.person_debt_lumen == 1

    # WHEN
    bob_personunit.set_credor_person_debt_lumen(
        person_cred_lumen=23, person_debt_lumen=34
    )

    # THEN
    assert bob_personunit.person_cred_lumen == 23
    assert bob_personunit.person_debt_lumen == 34


def test_PersonUnit_set_credor_person_debt_lumen_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob", person_cred_lumen=45, person_debt_lumen=56)
    assert bob_personunit.person_cred_lumen == 45
    assert bob_personunit.person_debt_lumen == 56

    # WHEN
    bob_personunit.set_credor_person_debt_lumen(
        person_cred_lumen=None, person_debt_lumen=None
    )

    # THEN
    assert bob_personunit.person_cred_lumen == 45
    assert bob_personunit.person_debt_lumen == 56


def test_PersonUnit_set_credor_person_debt_lumen_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.person_cred_lumen == 1
    assert bob_personunit.person_debt_lumen == 1

    # WHEN
    bob_personunit.set_credor_person_debt_lumen(
        person_cred_lumen=None, person_debt_lumen=None
    )

    # THEN
    assert bob_personunit.person_cred_lumen == 1
    assert bob_personunit.person_debt_lumen == 1


def test_PersonUnit_add_irrational_person_debt_lumen_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.irrational_person_debt_lumen == 0

    # WHEN
    bob_int1 = 11
    bob_personunit.add_irrational_person_debt_lumen(bob_int1)

    # THEN
    assert bob_personunit.irrational_person_debt_lumen == bob_int1

    # WHEN
    bob_int2 = 22
    bob_personunit.add_irrational_person_debt_lumen(bob_int2)

    # THEN
    assert bob_personunit.irrational_person_debt_lumen == bob_int1 + bob_int2


def test_PersonUnit_add_inallocable_person_debt_lumen_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.inallocable_person_debt_lumen == 0

    # WHEN
    bob_int1 = 11
    bob_personunit.add_inallocable_person_debt_lumen(bob_int1)

    # THEN
    assert bob_personunit.inallocable_person_debt_lumen == bob_int1

    # WHEN
    bob_int2 = 22
    bob_personunit.add_inallocable_person_debt_lumen(bob_int2)

    # THEN
    assert bob_personunit.inallocable_person_debt_lumen == bob_int1 + bob_int2


def test_PersonUnit_reset_listen_calculated_attrs_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_personunit.add_irrational_person_debt_lumen(bob_int1)
    bob_personunit.add_inallocable_person_debt_lumen(bob_int2)
    assert bob_personunit.irrational_person_debt_lumen == bob_int1
    assert bob_personunit.inallocable_person_debt_lumen == bob_int2

    # WHEN
    bob_personunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_personunit.irrational_person_debt_lumen == 0
    assert bob_personunit.inallocable_person_debt_lumen == 0


def test_PersonUnit_clear_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit.fund_give = 0.27
    bob_personunit.fund_take = 0.37
    bob_personunit.fund_agenda_give = 0.41
    bob_personunit.fund_agenda_take = 0.51
    bob_personunit.fund_agenda_ratio_give = 0.433
    bob_personunit.fund_agenda_ratio_take = 0.533
    assert bob_personunit.fund_give == 0.27
    assert bob_personunit.fund_take == 0.37
    assert bob_personunit.fund_agenda_give == 0.41
    assert bob_personunit.fund_agenda_take == 0.51
    assert bob_personunit.fund_agenda_ratio_give == 0.433
    assert bob_personunit.fund_agenda_ratio_take == 0.533

    # WHEN
    bob_personunit.clear_fund_give_take()

    # THEN
    assert bob_personunit.fund_give == 0
    assert bob_personunit.fund_take == 0
    assert bob_personunit.fund_agenda_give == 0
    assert bob_personunit.fund_agenda_take == 0
    assert bob_personunit.fund_agenda_ratio_give == 0
    assert bob_personunit.fund_agenda_ratio_take == 0


def test_PersonUnit_add_fund_agenda_give_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit.fund_agenda_give = 0.41
    assert bob_personunit.fund_agenda_give == 0.41

    # WHEN
    bob_personunit.add_fund_agenda_give(0.3)

    # THEN
    assert bob_personunit.fund_agenda_give == 0.71


def test_PersonUnit_add_fund_agenda_take_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit.fund_agenda_take = 0.41
    assert bob_personunit.fund_agenda_take == 0.41

    # WHEN
    bob_personunit.add_fund_agenda_take(0.3)

    # THEN
    assert bob_personunit.fund_agenda_take == 0.71


def test_PersonUnit_add_person_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit.fund_give = 0.4106
    bob_personunit.fund_take = 0.1106
    bob_personunit.fund_agenda_give = 0.41
    bob_personunit.fund_agenda_take = 0.51
    assert bob_personunit.fund_agenda_give == 0.41
    assert bob_personunit.fund_agenda_take == 0.51

    # WHEN
    bob_personunit.add_person_fund_give_take(
        fund_give=0.33,
        fund_take=0.055,
        fund_agenda_give=0.3,
        fund_agenda_take=0.05,
    )

    # THEN
    assert bob_personunit.fund_give == 0.7406
    assert bob_personunit.fund_take == 0.1656
    assert bob_personunit.fund_agenda_give == 0.71
    assert bob_personunit.fund_agenda_take == 0.56


def test_PersonUnit_set_personunits_fund_agenda_ratios_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob", person_cred_lumen=15, person_debt_lumen=7)
    bob_personunit.fund_give = 0.4106
    bob_personunit.fund_take = 0.1106
    bob_personunit.fund_agenda_give = 0.041
    bob_personunit.fund_agenda_take = 0.051
    bob_personunit.fund_agenda_ratio_give = 0
    bob_personunit.fund_agenda_ratio_take = 0
    assert bob_personunit.fund_agenda_ratio_give == 0
    assert bob_personunit.fund_agenda_ratio_take == 0

    # WHEN
    bob_personunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0.2,
        fund_agenda_ratio_take_sum=0.5,
        personunits_person_cred_lumen_sum=20,
        personunits_person_debt_lumen_sum=14,
    )

    # THEN
    assert bob_personunit.fund_agenda_ratio_give == 0.205
    assert bob_personunit.fund_agenda_ratio_take == 0.102

    # WHEN
    bob_personunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        personunits_person_cred_lumen_sum=20,
        personunits_person_debt_lumen_sum=14,
    )

    # THEN
    assert bob_personunit.fund_agenda_ratio_give == 0.75
    assert bob_personunit.fund_agenda_ratio_take == 0.5
