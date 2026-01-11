from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch02_person.person import personunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_set_personunit_SetsAttr():
    # ESTABLISH
    yao_personunit = personunit_shop(exx.yao)
    yao_personunit.add_membership(exx.yao)
    deepcopy_yao_personunit = copy_deepcopy(yao_personunit)
    bob_plan = planunit_shop("Bob", knot=exx.slash)

    # WHEN
    bob_plan.set_personunit(yao_personunit)

    # THEN
    assert bob_plan.persons.get(exx.yao).groupmark == exx.slash
    x_persons = {yao_personunit.person_name: deepcopy_yao_personunit}
    assert bob_plan.persons != x_persons
    deepcopy_yao_personunit.groupmark = bob_plan.knot
    assert bob_plan.persons == x_persons


def test_PlanUnit_set_person_DoesNotSet_person_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_plan = planunit_shop("Yao", respect_grain=x_respect_grain)

    # WHEN
    yao_plan.set_personunit(personunit_shop(exx.zia), auto_set_membership=False)

    # THEN
    assert yao_plan.get_person(exx.zia).get_membership(exx.zia) is None


def test_PlanUnit_set_person_DoesSet_person_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_plan = planunit_shop("Yao", respect_grain=x_respect_grain)

    # WHEN
    yao_plan.set_personunit(personunit_shop(exx.zia))

    # THEN
    zia_zia_membership = yao_plan.get_person(exx.zia).get_membership(exx.zia)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_lumen == 1
    assert zia_zia_membership.group_debt_lumen == 1


def test_PlanUnit_set_person_DoesNotOverRide_person_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_plan = planunit_shop("Yao", respect_grain=x_respect_grain)
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_personunit = personunit_shop(exx.zia)
    zia_personunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_plan.set_personunit(zia_personunit)

    # THEN
    zia_ohio_membership = yao_plan.get_person(exx.zia).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_lumen == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_lumen == zia_ohio_debt_w
    zia_zia_membership = yao_plan.get_person(exx.zia).get_membership(exx.zia)
    assert zia_zia_membership is None


def test_PlanUnit_add_personunit_Sets_persons():
    # ESTABLISH
    x_respect_grain = 6
    yao_plan = planunit_shop("Yao", respect_grain=x_respect_grain)

    # WHEN
    yao_plan.add_personunit(exx.zia, person_cred_lumen=13, person_debt_lumen=8)
    yao_plan.add_personunit(exx.sue, person_debt_lumen=5)
    yao_plan.add_personunit(exx.xio, person_cred_lumen=17)

    # THEN
    assert len(yao_plan.persons) == 3
    assert len(yao_plan.get_personunit_group_titles_dict()) == 3
    assert yao_plan.persons.get(exx.xio).person_cred_lumen == 17
    assert yao_plan.persons.get(exx.sue).person_debt_lumen == 5
    assert yao_plan.persons.get(exx.xio).respect_grain == x_respect_grain


def test_PlanUnit_person_exists_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")

    # WHEN / THEN
    assert bob_plan.person_exists(exx.yao) is False

    # ESTABLISH
    bob_plan.add_personunit(exx.yao)

    # WHEN / THEN
    assert bob_plan.person_exists(exx.yao)


def test_PlanUnit_set_person_Creates_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    before_zia_credit = 7
    before_zia_debt = 17
    yao_plan.add_personunit(exx.zia, before_zia_credit, before_zia_debt)
    zia_personunit = yao_plan.get_person(exx.zia)
    zia_membership = zia_personunit.get_membership(exx.zia)
    assert zia_membership.group_cred_lumen != before_zia_credit
    assert zia_membership.group_debt_lumen != before_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_plan.set_personunit(personunit_shop(exx.zia, after_zia_credit, after_zia_debt))

    # THEN
    assert zia_membership.group_cred_lumen != after_zia_credit
    assert zia_membership.group_debt_lumen != after_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1


def test_PlanUnit_edit_person_RaiseExceptionWhenPersonDoesNotExist():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    zia_person_cred_lumen = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_plan.edit_personunit(exx.zia, person_cred_lumen=zia_person_cred_lumen)

    # THEN
    assert str(excinfo.value) == f"PersonUnit '{exx.zia}' does not exist."


def test_PlanUnit_edit_person_UpdatesObj():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    old_zia_person_cred_lumen = 55
    old_zia_person_debt_lumen = 66
    yao_plan.set_personunit(
        personunit_shop(
            exx.zia,
            old_zia_person_cred_lumen,
            old_zia_person_debt_lumen,
        )
    )
    zia_personunit = yao_plan.get_person(exx.zia)
    assert zia_personunit.person_cred_lumen == old_zia_person_cred_lumen
    assert zia_personunit.person_debt_lumen == old_zia_person_debt_lumen

    # WHEN
    new_zia_person_cred_lumen = 22
    new_zia_person_debt_lumen = 33
    yao_plan.edit_personunit(
        person_name=exx.zia,
        person_cred_lumen=new_zia_person_cred_lumen,
        person_debt_lumen=new_zia_person_debt_lumen,
    )

    # THEN
    assert zia_personunit.person_cred_lumen == new_zia_person_cred_lumen
    assert zia_personunit.person_debt_lumen == new_zia_person_debt_lumen


def test_PlanUnit_get_person_ReturnsObj():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    yao_plan.add_personunit(exx.zia)
    yao_plan.add_personunit(exx.sue)

    # WHEN
    zia_person = yao_plan.get_person(exx.zia)
    sue_person = yao_plan.get_person(exx.sue)

    # THEN
    assert zia_person == yao_plan.persons.get(exx.zia)
    assert sue_person == yao_plan.persons.get(exx.sue)
