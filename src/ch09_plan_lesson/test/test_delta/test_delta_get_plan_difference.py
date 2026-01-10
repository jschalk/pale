from copy import deepcopy as copy_deepcopy
from src.ch01_py.dict_toolbox import get_empty_list_if_None, get_from_nested_dict
from src.ch03_person.group import awardunit_shop
from src.ch03_person.person import personunit_shop
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import get_planunit_with_4_levels
from src.ch09_plan_lesson.delta import PlanDelta, plandelta_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def print_planatom_keys(x_plandelta: PlanDelta):
    for x_planatom in get_delete_planatom_list(x_plandelta):
        print(f"DELETE {x_planatom.dimen} {list(x_planatom.jkeys.values())}")
    for x_planatom in get_update_planatom_list(x_plandelta):
        print(f"UPDATE {x_planatom.dimen} {list(x_planatom.jkeys.values())}")
    for x_planatom in get_insert_planatom_list(x_plandelta):
        print(f"INSERT {x_planatom.dimen} {list(x_planatom.jkeys.values())}")


def get_delete_planatom_list(x_plandelta: PlanDelta) -> list:
    return get_empty_list_if_None(x_plandelta._get_crud_planatoms_list().get(kw.DELETE))


def get_insert_planatom_list(x_plandelta: PlanDelta):
    return get_empty_list_if_None(x_plandelta._get_crud_planatoms_list().get(kw.INSERT))


def get_update_planatom_list(x_plandelta: PlanDelta):
    return get_empty_list_if_None(x_plandelta._get_crud_planatoms_list().get(kw.UPDATE))


def get_planatom_total_count(x_plandelta: PlanDelta) -> int:
    return (
        len(get_delete_planatom_list(x_plandelta))
        + len(get_insert_planatom_list(x_plandelta))
        + len(get_update_planatom_list(x_plandelta))
    )


def test_PlanDelta_create_planatoms_EmptyPlans():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    sue_plandelta = plandelta_shop()
    assert sue_plandelta.planatoms == {}

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(sue_plan, sue_plan)

    # THEN
    assert sue_plandelta.planatoms == {}


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_personunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    after_sue_plan = copy_deepcopy(before_sue_plan)
    xio_person_cred_lumen = 33
    xio_person_debt_lumen = 44
    xio_personunit = personunit_shop(
        exx.xio, xio_person_cred_lumen, xio_person_debt_lumen
    )
    after_sue_plan.set_personunit(xio_personunit, auto_set_membership=False)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    assert len(sue_plandelta.planatoms.get(kw.INSERT).get(kw.plan_personunit)) == 1
    sue_insert_dict = sue_plandelta.planatoms.get(kw.INSERT)
    sue_personunit_dict = sue_insert_dict.get(kw.plan_personunit)
    xio_planatom = sue_personunit_dict.get(exx.xio)
    assert xio_planatom.get_value(kw.person_name) == exx.xio
    assert xio_planatom.get_value("person_cred_lumen") == xio_person_cred_lumen
    assert xio_planatom.get_value("person_debt_lumen") == xio_person_debt_lumen

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_personunit_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit("Yao")
    before_sue_plan.add_personunit("Zia")

    after_sue_plan = copy_deepcopy(before_sue_plan)

    before_sue_plan.add_personunit(exx.xio)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    xio_planatom = get_from_nested_dict(
        sue_plandelta.planatoms,
        [kw.DELETE, kw.plan_personunit, exx.xio],
    )
    assert xio_planatom.get_value(kw.person_name) == exx.xio

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    print_planatom_keys(sue_plandelta)
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_personunit_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    after_sue_plan = copy_deepcopy(before_sue_plan)
    before_sue_plan.add_personunit(exx.xio)
    xio_person_cred_lumen = 33
    xio_person_debt_lumen = 44
    after_sue_plan.add_personunit(exx.xio, xio_person_cred_lumen, xio_person_debt_lumen)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    x_keylist = [kw.UPDATE, kw.plan_personunit, exx.xio]
    xio_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert xio_planatom.get_value(kw.person_name) == exx.xio
    assert xio_planatom.get_value("person_cred_lumen") == xio_person_cred_lumen
    assert xio_planatom.get_value("person_debt_lumen") == xio_person_debt_lumen

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_PlanUnit_simple_attrs_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    after_sue_plan = copy_deepcopy(before_sue_plan)
    x_planunit_tally = 55
    x_fund_pool = 8000000
    x_fund_grain = 8
    x_respect_grain = 5
    x_max_tree_traverse = 66
    x_credor_respect = 770
    x_debtor_respect = 880
    after_sue_plan.tally = x_planunit_tally
    after_sue_plan.fund_pool = x_fund_pool
    after_sue_plan.fund_grain = x_fund_grain
    after_sue_plan.respect_grain = x_respect_grain
    after_sue_plan.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_plan.set_credor_respect(x_credor_respect)
    after_sue_plan.set_debtor_respect(x_debtor_respect)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    x_keylist = [kw.UPDATE, kw.planunit]
    xio_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert xio_planatom.get_value(kw.max_tree_traverse) == x_max_tree_traverse
    assert xio_planatom.get_value(kw.credor_respect) == x_credor_respect
    assert xio_planatom.get_value(kw.debtor_respect) == x_debtor_respect
    assert xio_planatom.get_value(kw.tally) == x_planunit_tally
    assert xio_planatom.get_value(kw.fund_pool) == x_fund_pool
    assert xio_planatom.get_value(kw.fund_grain) == x_fund_grain
    assert xio_planatom.get_value(kw.respect_grain) == x_respect_grain

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_person_membership_insert():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    after_sue_plan = copy_deepcopy(before_sue_plan)
    temp_yao_personunit = personunit_shop(exx.yao)
    temp_zia_personunit = personunit_shop(exx.zia)
    after_sue_plan.set_personunit(temp_yao_personunit, auto_set_membership=False)
    after_sue_plan.set_personunit(temp_zia_personunit, auto_set_membership=False)
    after_yao_personunit = after_sue_plan.get_person(exx.yao)
    after_zia_personunit = after_sue_plan.get_person(exx.zia)
    zia_run_credit_w = 77
    zia_run_debt_w = 88
    after_zia_personunit.add_membership(exx.run, zia_run_credit_w, zia_run_debt_w)
    print(f"{after_sue_plan.get_personunit_group_titles_dict()=}")

    # WHEN
    sue_plandelta = plandelta_shop()
    print(f"{after_sue_plan.get_person(exx.zia).memberships=}")
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)
    # print(f"{sue_plandelta.planatoms.get(kw.INSERT).keys()=}")
    # print(
    #     sue_plandelta.planatoms.get(kw.INSERT).get(kw.plan_person_membership).keys()
    # )

    # THEN
    x_keylist = [kw.INSERT, kw.plan_personunit, exx.yao]
    yao_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert yao_planatom.get_value(kw.person_name) == exx.yao

    x_keylist = [kw.INSERT, kw.plan_personunit, exx.zia]
    zia_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert zia_planatom.get_value(kw.person_name) == exx.zia
    print(f"\n{sue_plandelta.planatoms=}")
    # print(f"\n{zia_planatom=}")

    x_keylist = [kw.INSERT, kw.plan_person_membership, exx.zia, exx.run]
    run_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert run_planatom.get_value(kw.person_name) == exx.zia
    assert run_planatom.get_value(kw.group_title) == exx.run
    assert run_planatom.get_value(kw.group_cred_lumen) == zia_run_credit_w
    assert run_planatom.get_value(kw.group_debt_lumen) == zia_run_debt_w

    print_planatom_keys(sue_plandelta)
    print(f"{get_planatom_total_count(sue_plandelta)=}")
    assert len(get_delete_planatom_list(sue_plandelta)) == 0
    assert len(get_insert_planatom_list(sue_plandelta)) == 3
    assert len(get_delete_planatom_list(sue_plandelta)) == 0
    assert get_planatom_total_count(sue_plandelta) == 3


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_person_membership_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    before_sue_plan.add_personunit(exx.zia)
    before_xio_credit_w = 77
    before_xio_debt_w = 88
    before_xio_person = before_sue_plan.get_person(exx.xio)
    before_xio_person.add_membership(exx.run, before_xio_credit_w, before_xio_debt_w)
    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_xio_personunit = after_sue_plan.get_person(exx.xio)
    after_xio_credit_w = 55
    after_xio_debt_w = 66
    after_xio_personunit.add_membership(exx.run, after_xio_credit_w, after_xio_debt_w)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    # x_keylist = [kw.UPDATE, kw.plan_personunit, exx.xio]
    # xio_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    # assert xio_planatom.get_value(kw.person_name) == exx.xio
    # print(f"\n{sue_plandelta.planatoms=}")
    # print(f"\n{xio_planatom=}")

    x_keylist = [kw.UPDATE, kw.plan_person_membership, exx.xio, exx.run]
    xio_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert xio_planatom.get_value(kw.person_name) == exx.xio
    assert xio_planatom.get_value(kw.group_title) == exx.run
    assert xio_planatom.get_value(kw.group_cred_lumen) == after_xio_credit_w
    assert xio_planatom.get_value(kw.group_debt_lumen) == after_xio_debt_w

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_person_membership_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    before_sue_plan.add_personunit(exx.zia)
    before_sue_plan.add_personunit(exx.bob)
    before_xio_personunit = before_sue_plan.get_person(exx.xio)
    before_zia_personunit = before_sue_plan.get_person(exx.zia)
    before_bob_personunit = before_sue_plan.get_person(exx.bob)
    before_xio_personunit.add_membership(exx.run)
    before_zia_personunit.add_membership(exx.run)
    fly_str = ";flyers"
    before_xio_personunit.add_membership(fly_str)
    before_zia_personunit.add_membership(fly_str)
    before_bob_personunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_plan.get_personunit_group_titles_dict()

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_xio_personunit = after_sue_plan.get_person(exx.xio)
    after_zia_personunit = after_sue_plan.get_person(exx.zia)
    after_bob_personunit = after_sue_plan.get_person(exx.bob)
    after_xio_personunit.delete_membership(exx.run)
    after_zia_personunit.delete_membership(exx.run)
    after_bob_personunit.delete_membership(fly_str)
    after_group_titles_dict = after_sue_plan.get_personunit_group_titles_dict()
    assert len(before_group_titles_dict.get(fly_str)) == 3
    assert len(before_group_titles_dict.get(exx.run)) == 2
    assert len(after_group_titles_dict.get(fly_str)) == 2
    assert after_group_titles_dict.get(exx.run) is None

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    x_keylist = [kw.DELETE, kw.plan_person_membership, exx.bob, fly_str]
    xio_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert xio_planatom.get_value(kw.person_name) == exx.bob
    assert xio_planatom.get_value(kw.group_title) == fly_str

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    print_planatom_keys(sue_plandelta)
    assert len(get_delete_planatom_list(sue_plandelta)) == 3
    assert len(get_insert_planatom_list(sue_plandelta)) == 0
    assert len(get_update_planatom_list(sue_plandelta)) == 0
    assert get_planatom_total_count(sue_plandelta) == 3


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_plan.make_rope(ball_rope, street_str)
    before_sue_plan.set_keg_obj(kegunit_shop(street_str), ball_rope)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_plan.make_rope(sports_rope, disc_str)
    amy45_str = "amy45"
    before_sue_plan.set_l1_keg(kegunit_shop(amy45_str))
    before_sue_plan.set_keg_obj(kegunit_shop(disc_str), sports_rope)
    # create after without ball_keg and street_keg
    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_sue_plan.del_keg_obj(ball_rope)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    x_dimen = kw.plan_kegunit
    print(f"{sue_plandelta.planatoms.get(kw.DELETE).get(x_dimen).keys()=}")

    x_keylist = [kw.DELETE, kw.plan_kegunit, street_rope]
    street_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert street_planatom.get_value(kw.keg_rope) == street_rope

    x_keylist = [kw.DELETE, kw.plan_kegunit, ball_rope]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope

    print(f"{get_planatom_total_count(sue_plandelta)=}")
    assert get_planatom_total_count(sue_plandelta) == 2


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    street_str = "street ball"
    street_rope = before_sue_plan.make_rope(ball_rope, street_str)
    before_sue_plan.set_keg_obj(kegunit_shop(street_str), ball_rope)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    disc_str = "Ultimate Disc"
    disc_rope = after_sue_plan.make_rope(sports_rope, disc_str)
    after_sue_plan.set_keg_obj(kegunit_shop(disc_str), sports_rope)
    amy45_str = "amy45"
    amy_begin = 34
    amy_close = 78
    amy_star = 55
    amy_pledge = True
    amy_rope = after_sue_plan.make_l1_rope(amy45_str)
    after_sue_plan.set_l1_keg(
        kegunit_shop(
            amy45_str,
            begin=amy_begin,
            close=amy_close,
            star=amy_star,
            pledge=amy_pledge,
        )
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print_planatom_keys(sue_plandelta)

    x_keylist = [kw.INSERT, kw.plan_kegunit, disc_rope]
    street_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert street_planatom.get_value(kw.keg_rope) == disc_rope

    a45_rope = after_sue_plan.make_l1_rope(amy45_str)
    x_keylist = [kw.INSERT, kw.plan_kegunit, a45_rope]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == a45_rope
    assert ball_planatom.get_value(kw.begin) == amy_begin
    assert ball_planatom.get_value(kw.close) == amy_close
    assert ball_planatom.get_value(kw.star) == amy_star
    assert ball_planatom.get_value(kw.pledge) == amy_pledge

    assert get_planatom_total_count(sue_plandelta) == 2


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    amy45_str = "amy45"
    amy45_rope = before_sue_plan.make_l1_rope(amy45_str)
    before_amy_begin = 34
    before_amy_close = 78
    before_amy_star = 55
    before_amy_pledge = True
    amy_rope = before_sue_plan.make_l1_rope(amy45_str)
    before_sue_plan.set_l1_keg(
        kegunit_shop(
            amy45_str,
            begin=before_amy_begin,
            close=before_amy_close,
            star=before_amy_star,
            pledge=before_amy_pledge,
        )
    )

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_amy_begin = 99
    after_amy_close = 111
    after_amy_star = 22
    after_amy_pledge = False
    after_sue_plan.edit_keg_attr(
        amy_rope,
        begin=after_amy_begin,
        close=after_amy_close,
        star=after_amy_star,
        pledge=after_amy_pledge,
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print_planatom_keys(sue_plandelta)

    x_keylist = [kw.UPDATE, kw.plan_kegunit, amy45_rope]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == amy45_rope
    assert ball_planatom.get_value(kw.begin) == after_amy_begin
    assert ball_planatom.get_value(kw.close) == after_amy_close
    assert ball_planatom.get_value(kw.star) == after_amy_star
    assert ball_planatom.get_value(kw.pledge) == after_amy_pledge

    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_awardunit_delete():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.xio)
    before_sue_au.add_personunit(exx.zia)
    before_sue_au.add_personunit(exx.bob)
    xio_personunit = before_sue_au.get_person(exx.xio)
    zia_personunit = before_sue_au.get_person(exx.zia)
    bob_personunit = before_sue_au.get_person(exx.bob)
    xio_personunit.add_membership(exx.run)
    zia_personunit.add_membership(exx.run)
    fly_str = ";flyers"
    xio_personunit.add_membership(fly_str)
    zia_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_sue_au.set_keg_obj(kegunit_shop(disc_str), sports_rope)
    before_sue_au.edit_keg_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    before_sue_au.edit_keg_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    before_sue_au.edit_keg_attr(disc_rope, awardunit=awardunit_shop(exx.run))
    before_sue_au.edit_keg_attr(disc_rope, awardunit=awardunit_shop(fly_str))

    after_sue_plan = copy_deepcopy(before_sue_au)
    after_sue_plan.edit_keg_attr(disc_rope, awardunit_del=exx.run)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_au, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")

    x_keylist = [kw.DELETE, kw.plan_keg_awardunit, disc_rope, exx.run]
    run_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert run_planatom.get_value(kw.keg_rope) == disc_rope
    assert run_planatom.get_value(kw.awardee_title) == exx.run

    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_awardunit_insert():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.xio)
    before_sue_au.add_personunit(exx.zia)
    before_sue_au.add_personunit(exx.bob)
    xio_personunit = before_sue_au.get_person(exx.xio)
    zia_personunit = before_sue_au.get_person(exx.zia)
    bob_personunit = before_sue_au.get_person(exx.bob)
    xio_personunit.add_membership(exx.run)
    zia_personunit.add_membership(exx.run)
    fly_str = ";flyers"
    xio_personunit.add_membership(fly_str)
    zia_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_au.make_rope(sports_rope, disc_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_sue_au.set_keg_obj(kegunit_shop(disc_str), sports_rope)
    before_sue_au.edit_keg_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    before_sue_au.edit_keg_attr(disc_rope, awardunit=awardunit_shop(fly_str))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_keg_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    after_run_give_force = 44
    after_run_take_force = 66
    x_awardunit = awardunit_shop(exx.run, after_run_give_force, after_run_take_force)
    after_sue_au.edit_keg_attr(disc_rope, awardunit=x_awardunit)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")

    x_keylist = [kw.INSERT, kw.plan_keg_awardunit, disc_rope, exx.run]
    run_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert run_planatom.get_value(kw.keg_rope) == disc_rope
    assert run_planatom.get_value(kw.awardee_title) == exx.run
    assert run_planatom.get_value(kw.keg_rope) == disc_rope
    assert run_planatom.get_value(kw.awardee_title) == exx.run
    assert run_planatom.get_value(kw.give_force) == after_run_give_force
    assert run_planatom.get_value(kw.take_force) == after_run_take_force

    assert get_planatom_total_count(sue_plandelta) == 2


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_awardunit_update():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.xio)
    before_sue_au.add_personunit(exx.zia)
    xio_personunit = before_sue_au.get_person(exx.xio)
    xio_personunit.add_membership(exx.run)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_sue_au.edit_keg_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    run_awardunit = before_sue_au.get_keg_obj(ball_rope).awardunits.get(exx.run)

    after_sue_plan = copy_deepcopy(before_sue_au)
    after_give_force = 55
    after_take_force = 66
    after_sue_plan.edit_keg_attr(
        ball_rope,
        awardunit=awardunit_shop(
            awardee_title=exx.run,
            give_force=after_give_force,
            take_force=after_take_force,
        ),
    )
    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_au, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")

    x_keylist = [kw.UPDATE, kw.plan_keg_awardunit, ball_rope, exx.run]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.awardee_title) == exx.run
    assert ball_planatom.get_value(kw.give_force) == after_give_force
    assert ball_planatom.get_value(kw.take_force) == after_take_force
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_factunit_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    bend_str = "bendable"
    bend_rope = before_sue_plan.make_rope(knee_rope, bend_str)
    before_sue_plan.set_keg_obj(kegunit_shop(bend_str), knee_rope)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_plan.make_rope(knee_rope, damaged_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    before_sue_plan.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_fact_lower = 11
    before_fact_upper = 22
    before_fact = factunit_shop(
        knee_rope, bend_rope, before_fact_lower, before_fact_upper
    )
    before_sue_plan.edit_keg_attr(ball_rope, factunit=before_fact)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_fact_lower = 55
    after_fact_upper = 66
    knee_fact = factunit_shop(
        knee_rope, damaged_rope, after_fact_lower, after_fact_upper
    )
    after_sue_plan.edit_keg_attr(ball_rope, factunit=knee_fact)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")

    x_keylist = [kw.UPDATE, kw.plan_keg_factunit, ball_rope, knee_rope]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.fact_context) == knee_rope
    assert ball_planatom.get_value(kw.fact_state) == damaged_rope
    assert ball_planatom.get_value(kw.fact_lower) == after_fact_lower
    assert ball_planatom.get_value(kw.fact_upper) == after_fact_upper
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_factunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_plan.make_rope(knee_rope, damaged_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    before_sue_plan.set_keg_obj(kegunit_shop(damaged_str), knee_rope)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_fact_lower = 55
    after_fact_upper = 66
    after_fact = factunit_shop(
        knee_rope, damaged_rope, after_fact_lower, after_fact_upper
    )
    after_sue_plan.edit_keg_attr(ball_rope, factunit=after_fact)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [kw.INSERT, kw.plan_keg_factunit, ball_rope, knee_rope]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    print(f"{ball_planatom=}")
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.fact_context) == knee_rope
    assert ball_planatom.get_value(kw.fact_state) == damaged_rope
    assert ball_planatom.get_value(kw.fact_lower) == after_fact_lower
    assert ball_planatom.get_value(kw.fact_upper) == after_fact_upper
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_factunit_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_plan.make_rope(knee_rope, damaged_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    before_sue_plan.set_keg_obj(kegunit_shop(damaged_str), knee_rope)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    before_damaged_reason_lower = 55
    before_damaged_reason_upper = 66
    before_fact = factunit_shop(
        fact_context=knee_rope,
        fact_state=damaged_rope,
        fact_lower=before_damaged_reason_lower,
        fact_upper=before_damaged_reason_upper,
    )
    before_sue_plan.edit_keg_attr(ball_rope, factunit=before_fact)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [kw.DELETE, kw.plan_keg_factunit, ball_rope, knee_rope]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.fact_context) == knee_rope
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_reason_caseunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_plan.make_rope(knee_rope, damaged_str)
    before_sue_plan.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_plan.make_rope(knee_rope, bend_str)
    before_sue_plan.set_keg_obj(kegunit_shop(bend_str), knee_rope)
    before_sue_plan.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )

    after_sue_plan = copy_deepcopy(before_sue_plan)
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    after_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=damaged_reason_lower,
        reason_upper=damaged_reason_upper,
        reason_divisor=damaged_reason_divisor,
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.plan_keg_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.reason_context) == knee_rope
    assert ball_planatom.get_value(kw.reason_state) == damaged_rope
    assert ball_planatom.get_value(kw.reason_lower) == damaged_reason_lower
    assert ball_planatom.get_value(kw.reason_upper) == damaged_reason_upper
    assert ball_planatom.get_value(kw.reason_divisor) == damaged_reason_divisor
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_reason_caseunit_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_plan.make_rope(knee_rope, damaged_str)
    before_sue_plan.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_plan.make_rope(knee_rope, bend_str)
    before_sue_plan.set_keg_obj(kegunit_shop(bend_str), knee_rope)
    before_sue_plan.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    before_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=damaged_reason_lower,
        reason_upper=damaged_reason_upper,
        reason_divisor=damaged_reason_divisor,
    )
    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_sue_plan.edit_keg_attr(
        ball_rope,
        reason_del_case_reason_context=knee_rope,
        reason_del_case_reason_state=damaged_rope,
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.plan_keg_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.reason_context) == knee_rope
    assert ball_planatom.get_value(kw.reason_state) == damaged_rope
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_reason_caseunit_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_plan.make_rope(knee_rope, damaged_str)
    before_sue_plan.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    bend_str = "bend"
    bend_rope = before_sue_plan.make_rope(knee_rope, bend_str)
    before_sue_plan.set_keg_obj(kegunit_shop(bend_str), knee_rope)
    before_sue_plan.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=bend_rope
    )
    before_damaged_reason_lower = 111
    before_damaged_reason_upper = 777
    before_damaged_reason_divisor = 13
    before_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=before_damaged_reason_lower,
        reason_upper=before_damaged_reason_upper,
        reason_divisor=before_damaged_reason_divisor,
    )

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_damaged_reason_lower = 333
    after_damaged_reason_upper = 555
    after_damaged_reason_divisor = 78
    after_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_case=damaged_rope,
        reason_lower=after_damaged_reason_lower,
        reason_upper=after_damaged_reason_upper,
        reason_divisor=after_damaged_reason_divisor,
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.UPDATE,
        kw.plan_keg_reason_caseunit,
        ball_rope,
        knee_rope,
        damaged_rope,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.reason_context) == knee_rope
    assert ball_planatom.get_value(kw.reason_state) == damaged_rope
    assert ball_planatom.get_value(kw.reason_lower) == after_damaged_reason_lower
    assert ball_planatom.get_value(kw.reason_upper) == after_damaged_reason_upper
    assert ball_planatom.get_value(kw.reason_divisor) == after_damaged_reason_divisor
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_reasonunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_plan.make_rope(knee_rope, medical_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    before_sue_plan.set_keg_obj(kegunit_shop(medical_str), knee_rope)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_medical_active_requisite = False
    after_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=after_medical_active_requisite,
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.plan_keg_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)

    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value("reason_context") == medical_rope
    assert (
        ball_planatom.get_value(kw.active_requisite) == after_medical_active_requisite
    )
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_reasonunit_update():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_plan.make_rope(knee_rope, medical_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    before_sue_plan.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_medical_active_requisite = True
    before_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=before_medical_active_requisite,
    )

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_medical_active_requisite = False
    after_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=after_medical_active_requisite,
    )

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.UPDATE,
        kw.plan_keg_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value("reason_context") == medical_rope
    assert (
        ball_planatom.get_value(kw.active_requisite) == after_medical_active_requisite
    )
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_reasonunit_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_plan.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_plan.make_rope(knee_rope, medical_str)
    before_sue_plan.set_l1_keg(kegunit_shop(knee_str))
    before_sue_plan.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_medical_active_requisite = True
    before_sue_plan.edit_keg_attr(
        ball_rope,
        reason_context=medical_rope,
        reason_requisite_active=before_medical_active_requisite,
    )

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_ball_keg = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_keg.del_reasonunit_reason_context(medical_rope)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.plan_keg_reasonunit,
        ball_rope,
        medical_rope,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value("reason_context") == medical_rope
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_partyunit_insert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_ball_kegunit = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_kegunit.laborunit.add_party(exx.xio)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.plan_keg_partyunit,
        ball_rope,
        exx.xio,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.party_title) == exx.xio
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_partyunit_delete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_plan.get_keg_obj(ball_rope)
    before_ball_kegunit.laborunit.add_party(exx.xio)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_ball_kegunit = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_kegunit.laborunit.del_partyunit(exx.xio)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.plan_keg_partyunit,
        ball_rope,
        exx.xio,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.party_title) == exx.xio
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_healerunit_insert_KegUnitUpdate():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_ball_kegunit = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_kegunit.healerunit.set_healer_name(exx.xio)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.plan_keg_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist)
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.healer_name) == exx.xio
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_healerunit_insert_KegUnitInsert():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    after_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    after_ball_kegunit = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_kegunit.healerunit.set_healer_name(exx.xio)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.INSERT,
        kw.plan_keg_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_planatom = get_from_nested_dict(sue_plandelta.planatoms, x_keylist, True)
    assert ball_planatom
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.healer_name) == exx.xio
    assert get_planatom_total_count(sue_plandelta) == 3


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_healerunit_delete_KegUnitUpdate():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_plan.get_keg_obj(ball_rope)
    before_ball_kegunit.healerunit.set_healer_name(exx.xio)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_ball_kegunit = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_kegunit.healerunit.del_healer_name(exx.xio)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.plan_keg_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_planatom = get_from_nested_dict(
        sue_plandelta.planatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_planatom
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.healer_name) == exx.xio
    assert get_planatom_total_count(sue_plandelta) == 1


def test_PlanDelta_add_all_different_planatoms_Creates_PlanAtom_keg_healerunit_delete_KegUnitDelete():
    # ESTABLISH
    before_sue_plan = planunit_shop(exx.sue)
    before_sue_plan.add_personunit(exx.xio)
    sports_str = "sports"
    sports_rope = before_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_plan.make_rope(sports_rope, ball_str)
    before_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_plan.get_keg_obj(ball_rope)
    before_ball_kegunit.healerunit.set_healer_name(exx.xio)

    after_sue_plan = copy_deepcopy(before_sue_plan)
    after_sue_plan.del_keg_obj(ball_rope)

    # WHEN
    sue_plandelta = plandelta_shop()
    sue_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    # THEN
    print(f"{print_planatom_keys(sue_plandelta)=}")
    x_keylist = [
        kw.DELETE,
        kw.plan_keg_healerunit,
        ball_rope,
        exx.xio,
    ]
    ball_planatom = get_from_nested_dict(
        sue_plandelta.planatoms, x_keylist, if_missing_return_None=True
    )
    assert ball_planatom
    assert ball_planatom.get_value(kw.keg_rope) == ball_rope
    assert ball_planatom.get_value(kw.healer_name) == exx.xio
    assert get_planatom_total_count(sue_plandelta) == 2


def test_PlanDelta_add_all_planatoms_Creates_PlanAtoms():
    # ESTABLISH

    after_sue_plan = planunit_shop(exx.sue)
    temp_xio_personunit = personunit_shop(exx.xio)
    after_sue_plan.set_personunit(temp_xio_personunit, auto_set_membership=False)
    sports_str = "sports"
    sports_rope = after_sue_plan.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = after_sue_plan.make_rope(sports_rope, ball_str)
    after_sue_plan.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    after_ball_kegunit = after_sue_plan.get_keg_obj(ball_rope)
    after_ball_kegunit.laborunit.add_party(exx.xio)

    before_sue_plan = planunit_shop(exx.sue)
    sue1_plandelta = plandelta_shop()
    sue1_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)
    print(f"{sue1_plandelta.get_ordered_planatoms()}")
    assert len(sue1_plandelta.get_ordered_planatoms()) == 4

    # WHEN
    sue2_plandelta = plandelta_shop()
    sue2_plandelta.add_all_planatoms(after_sue_plan)

    # THEN
    assert len(sue2_plandelta.get_ordered_planatoms()) == 4
    assert sue2_plandelta == sue1_plandelta
