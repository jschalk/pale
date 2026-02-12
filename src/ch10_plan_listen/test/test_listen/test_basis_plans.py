from src.ch01_allot.allot import default_pool_num, validate_pool_num
from src.ch02_partner.partner import RespectNum
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch10_plan_listen.basis_plan import (
    create_empty_plan_from_plan,
    create_listen_basis,
    get_default_job,
)
from src.ref.keywords import ExampleStrs as exx


def test_create_empty_plan_from_plan_ReturnsObj():
    # ESTABLISH
    mana_grain_float = 0.7
    yao_gut = planunit_shop(exx.yao, knot=exx.slash, mana_grain=mana_grain_float)
    yao_gut.set_l1_keg(kegunit_shop("Iowa"))
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_gut.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    zia_irrational_partner_debt_lumen = 11
    zia_inallocable_partner_debt_lumen = 22
    duty_zia_partnerunit = yao_gut.get_partner(exx.zia)
    duty_zia_partnerunit.add_irrational_partner_debt_lumen(
        zia_irrational_partner_debt_lumen
    )
    duty_zia_partnerunit.add_inallocable_partner_debt_lumen(
        zia_inallocable_partner_debt_lumen
    )
    zia_partnerunit = yao_gut.get_partner(exx.zia)
    zia_partnerunit.add_membership(f"{exx.slash}swimmers")
    yao_gut.set_credor_respect(zia_credor_pool)
    yao_gut.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_vision = create_empty_plan_from_plan(yao_gut, x_plan_name=exx.zia)

    # THEN
    assert yao_empty_vision.plan_name != yao_gut.plan_name
    assert yao_empty_vision.plan_name == exx.zia
    assert yao_empty_vision.moment_rope == yao_gut.moment_rope
    assert yao_empty_vision.last_lesson_id is None
    assert yao_empty_vision.get_partnerunits_dict() == {}
    assert yao_empty_vision.knot == yao_gut.knot
    assert yao_empty_vision.fund_pool == yao_gut.fund_pool
    assert yao_empty_vision.fund_grain == yao_gut.fund_grain
    assert yao_empty_vision.respect_grain == yao_gut.respect_grain
    assert yao_empty_vision.mana_grain == yao_gut.mana_grain
    assert yao_empty_vision.credor_respect != yao_gut.credor_respect
    assert yao_empty_vision.credor_respect == RespectNum(validate_pool_num())
    assert yao_empty_vision.debtor_respect != yao_gut.debtor_respect
    assert yao_empty_vision.debtor_respect == RespectNum(validate_pool_num())
    yao_empty_vision.cashout()
    assert yao_empty_vision.partners == {}


def test_create_listen_basis_ReturnsObj():
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao, knot=exx.slash)
    yao_duty.set_l1_keg(kegunit_shop("Iowa"))
    zia_partner_cred_lumen = 47
    zia_partner_debt_lumen = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_partnerunit(exx.zia, zia_partner_cred_lumen, zia_partner_debt_lumen)
    zia_irrational_partner_debt_lumen = 11
    zia_inallocable_partner_debt_lumen = 22
    duty_zia_partnerunit = yao_duty.get_partner(exx.zia)
    duty_zia_partnerunit.add_irrational_partner_debt_lumen(
        zia_irrational_partner_debt_lumen
    )
    duty_zia_partnerunit.add_inallocable_partner_debt_lumen(
        zia_inallocable_partner_debt_lumen
    )
    zia_partnerunit = yao_duty.get_partner(exx.zia)
    zia_partnerunit.add_membership(f"{exx.slash}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_vision = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_vision.plan_name == yao_duty.plan_name
    assert yao_basis_vision.moment_rope == yao_duty.moment_rope
    assert yao_basis_vision.last_lesson_id == yao_duty.last_lesson_id
    assert yao_basis_vision.get_partnerunits_dict() == yao_duty.get_partnerunits_dict()
    assert yao_basis_vision.knot == yao_duty.knot
    assert yao_basis_vision.fund_pool == yao_duty.fund_pool
    assert yao_basis_vision.fund_grain == yao_duty.fund_grain
    assert yao_basis_vision.respect_grain == yao_duty.respect_grain
    assert yao_basis_vision.credor_respect == yao_duty.credor_respect
    assert yao_basis_vision.debtor_respect == yao_duty.debtor_respect
    yao_basis_vision.cashout()
    assert len(yao_basis_vision._keg_dict) != len(yao_duty._keg_dict)
    assert len(yao_basis_vision._keg_dict) == 1
    vision_zia_partnerunit = yao_basis_vision.get_partner(exx.zia)
    assert (
        yao_basis_vision.get_partnerunits_dict().keys()
        == yao_duty.get_partnerunits_dict().keys()
    )
    assert vision_zia_partnerunit.irrational_partner_debt_lumen == 0
    assert vision_zia_partnerunit.inallocable_partner_debt_lumen == 0


def test_get_default_job_ReturnsObj():
    # ESTABLISH
    x_fund_pool = 99000
    x_fund_grain = 80
    x_respect_grain = 5
    sue_partner_pool = 800
    last_lesson_id = 7
    sue_max_tree_traverse = 9
    sue_planunit = planunit_shop(
        exx.sue, exx.a23_slash, exx.slash, x_fund_pool, x_fund_grain, x_respect_grain
    )
    sue_planunit.set_last_lesson_id(last_lesson_id)
    sue_planunit.add_partnerunit(exx.bob, 3, 4)
    bob_partnerunit = sue_planunit.get_partner(exx.bob)
    bob_partnerunit.add_membership(f"{exx.slash}swimmers")
    sue_planunit.set_partner_respect(sue_partner_pool)
    sue_planunit.set_l1_keg(kegunit_shop(exx.casa))
    sue_planunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_job = get_default_job(sue_planunit)

    # THEN
    default_job.cashout()
    assert default_job.plan_name == sue_planunit.plan_name
    assert default_job.plan_name == exx.sue
    assert default_job.moment_rope == sue_planunit.moment_rope
    assert default_job.moment_rope == exx.a23_slash
    assert default_job.knot == exx.slash
    assert default_job.fund_pool == sue_partner_pool
    assert default_job.fund_grain == x_fund_grain
    assert default_job.respect_grain == x_respect_grain
    assert default_job.credor_respect == RespectNum(default_pool_num())
    assert default_job.debtor_respect == RespectNum(default_pool_num())
    assert default_job.max_tree_traverse == sue_max_tree_traverse
    assert len(default_job.get_partnerunits_dict()) == 1
    assert len(default_job._keg_dict) == 1
