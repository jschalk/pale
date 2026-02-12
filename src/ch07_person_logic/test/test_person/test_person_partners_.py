from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch02_partner.partner import partnerunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_partnerunit_SetsAttr():
    # ESTABLISH
    yao_partnerunit = partnerunit_shop(exx.yao)
    yao_partnerunit.add_membership(exx.yao)
    deepcopy_yao_partnerunit = copy_deepcopy(yao_partnerunit)
    bob_person = personunit_shop("Bob", knot=exx.slash)

    # WHEN
    bob_person.set_partnerunit(yao_partnerunit)

    # THEN
    assert bob_person.partners.get(exx.yao).groupmark == exx.slash
    x_partners = {yao_partnerunit.partner_name: deepcopy_yao_partnerunit}
    assert bob_person.partners != x_partners
    deepcopy_yao_partnerunit.groupmark = bob_person.knot
    assert bob_person.partners == x_partners


def test_PersonUnit_set_partner_DoesNotSet_partner_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_person = personunit_shop("Yao", respect_grain=x_respect_grain)

    # WHEN
    yao_person.set_partnerunit(partnerunit_shop(exx.zia), auto_set_membership=False)

    # THEN
    assert yao_person.get_partner(exx.zia).get_membership(exx.zia) is None


def test_PersonUnit_set_partner_DoesSet_partner_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_person = personunit_shop("Yao", respect_grain=x_respect_grain)

    # WHEN
    yao_person.set_partnerunit(partnerunit_shop(exx.zia))

    # THEN
    zia_zia_membership = yao_person.get_partner(exx.zia).get_membership(exx.zia)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_lumen == 1
    assert zia_zia_membership.group_debt_lumen == 1


def test_PersonUnit_set_partner_DoesNotOverRide_partner_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_person = personunit_shop("Yao", respect_grain=x_respect_grain)
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_partnerunit = partnerunit_shop(exx.zia)
    zia_partnerunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_person.set_partnerunit(zia_partnerunit)

    # THEN
    zia_ohio_membership = yao_person.get_partner(exx.zia).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_lumen == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_lumen == zia_ohio_debt_w
    zia_zia_membership = yao_person.get_partner(exx.zia).get_membership(exx.zia)
    assert zia_zia_membership is None


def test_PersonUnit_add_partnerunit_Sets_partners():
    # ESTABLISH
    x_respect_grain = 6
    yao_person = personunit_shop("Yao", respect_grain=x_respect_grain)

    # WHEN
    yao_person.add_partnerunit(exx.zia, partner_cred_lumen=13, partner_debt_lumen=8)
    yao_person.add_partnerunit(exx.sue, partner_debt_lumen=5)
    yao_person.add_partnerunit(exx.xio, partner_cred_lumen=17)

    # THEN
    assert len(yao_person.partners) == 3
    assert len(yao_person.get_partnerunit_group_titles_dict()) == 3
    assert yao_person.partners.get(exx.xio).partner_cred_lumen == 17
    assert yao_person.partners.get(exx.sue).partner_debt_lumen == 5
    assert yao_person.partners.get(exx.xio).respect_grain == x_respect_grain


def test_PersonUnit_partner_exists_ReturnsObj():
    # ESTABLISH
    bob_person = personunit_shop("Bob")

    # WHEN / THEN
    assert bob_person.partner_exists(exx.yao) is False

    # ESTABLISH
    bob_person.add_partnerunit(exx.yao)

    # WHEN / THEN
    assert bob_person.partner_exists(exx.yao)


def test_PersonUnit_set_partner_Creates_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    before_zia_credit = 7
    before_zia_debt = 17
    yao_person.add_partnerunit(exx.zia, before_zia_credit, before_zia_debt)
    zia_partnerunit = yao_person.get_partner(exx.zia)
    zia_membership = zia_partnerunit.get_membership(exx.zia)
    assert zia_membership.group_cred_lumen != before_zia_credit
    assert zia_membership.group_debt_lumen != before_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_person.set_partnerunit(
        partnerunit_shop(exx.zia, after_zia_credit, after_zia_debt)
    )

    # THEN
    assert zia_membership.group_cred_lumen != after_zia_credit
    assert zia_membership.group_debt_lumen != after_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1


def test_PersonUnit_edit_partner_RaiseExceptionWhenPartnerDoesNotExist():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    zia_partner_cred_lumen = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_person.edit_partnerunit(exx.zia, partner_cred_lumen=zia_partner_cred_lumen)

    # THEN
    assert str(excinfo.value) == f"PartnerUnit '{exx.zia}' does not exist."


def test_PersonUnit_edit_partner_UpdatesObj():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    old_zia_partner_cred_lumen = 55
    old_zia_partner_debt_lumen = 66
    yao_person.set_partnerunit(
        partnerunit_shop(
            exx.zia,
            old_zia_partner_cred_lumen,
            old_zia_partner_debt_lumen,
        )
    )
    zia_partnerunit = yao_person.get_partner(exx.zia)
    assert zia_partnerunit.partner_cred_lumen == old_zia_partner_cred_lumen
    assert zia_partnerunit.partner_debt_lumen == old_zia_partner_debt_lumen

    # WHEN
    new_zia_partner_cred_lumen = 22
    new_zia_partner_debt_lumen = 33
    yao_person.edit_partnerunit(
        partner_name=exx.zia,
        partner_cred_lumen=new_zia_partner_cred_lumen,
        partner_debt_lumen=new_zia_partner_debt_lumen,
    )

    # THEN
    assert zia_partnerunit.partner_cred_lumen == new_zia_partner_cred_lumen
    assert zia_partnerunit.partner_debt_lumen == new_zia_partner_debt_lumen


def test_PersonUnit_get_partner_ReturnsObj():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    yao_person.add_partnerunit(exx.zia)
    yao_person.add_partnerunit(exx.sue)

    # WHEN
    zia_partner = yao_person.get_partner(exx.zia)
    sue_partner = yao_person.get_partner(exx.sue)

    # THEN
    assert zia_partner == yao_person.partners.get(exx.zia)
    assert sue_partner == yao_person.partners.get(exx.sue)
