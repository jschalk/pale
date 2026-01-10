from src.ch03_person.group import awardunit_shop
from src.ch05_reason.reason_main import factunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch09_plan_lesson.delta import plandelta_shop
from src.ch09_plan_lesson.test._util.ch09_examples import get_plandelta_example1
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_PlanDelta_get_edited_plan_ReturnsObj_SimplestScenario():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()

    # WHEN
    sue_tally = 55
    before_sue_planunit = planunit_shop(exx.sue, tally=sue_tally)
    after_sue_planunit = ex1_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    assert after_sue_planunit.tally == sue_tally
    assert after_sue_planunit == before_sue_planunit


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnitSimpleAttrs():
    # ESTABLISH
    sue_plandelta = plandelta_shop()

    sue_tally = 44
    before_sue_planunit = planunit_shop(exx.sue, tally=sue_tally)

    dimen = kw.planunit
    x_planatom = planatom_shop(dimen, kw.UPDATE)
    new1_value = 55
    new1_arg = kw.tally
    x_planatom.set_jvalue(new1_arg, new1_value)
    new2_value = 66
    new2_arg = kw.max_tree_traverse
    x_planatom.set_jvalue(new2_arg, new2_value)
    new3_value = 77
    new3_arg = kw.credor_respect
    x_planatom.set_jvalue(new3_arg, new3_value)
    new4_value = 88
    new4_arg = kw.debtor_respect
    x_planatom.set_jvalue(new4_arg, new4_value)
    new9_value = 55550000
    new9_arg = kw.fund_pool
    x_planatom.set_jvalue(new9_arg, new9_value)
    new8_value = 0.5555
    new8_arg = kw.fund_grain
    x_planatom.set_jvalue(new8_arg, new8_value)
    sue_plandelta.set_planatom(x_planatom)
    new6_value = 0.5
    new6_arg = kw.respect_grain
    x_planatom.set_jvalue(new6_arg, new6_value)
    sue_plandelta.set_planatom(x_planatom)
    new7_value = 0.025
    new7_arg = kw.mana_grain
    x_planatom.set_jvalue(new7_arg, new7_value)
    sue_plandelta.set_planatom(x_planatom)

    # WHEN
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    print(f"{sue_plandelta.planatoms.keys()=}")
    assert after_sue_planunit.max_tree_traverse == new2_value
    assert after_sue_planunit.credor_respect == new3_value
    assert after_sue_planunit.debtor_respect == new4_value
    assert after_sue_planunit.tally == new1_value
    assert after_sue_planunit.tally != before_sue_planunit.tally
    assert after_sue_planunit.fund_pool == new9_value
    assert after_sue_planunit.fund_pool != before_sue_planunit.fund_pool
    assert after_sue_planunit.fund_grain == new8_value
    assert after_sue_planunit.fund_grain != before_sue_planunit.fund_grain
    assert after_sue_planunit.respect_grain == new6_value
    assert after_sue_planunit.respect_grain != before_sue_planunit.respect_grain
    assert after_sue_planunit.mana_grain == new7_value
    assert after_sue_planunit.mana_grain != before_sue_planunit.mana_grain


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_person():
    # ESTABLISH
    sue_plandelta = plandelta_shop()

    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)

    dimen = kw.plan_personunit
    x_planatom = planatom_shop(dimen, kw.DELETE)
    x_planatom.set_jkey(kw.person_name, exx.zia)
    sue_plandelta.set_planatom(x_planatom)

    # WHEN
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    print(f"{sue_plandelta.planatoms=}")
    assert after_sue_planunit != before_sue_planunit
    assert after_sue_planunit.person_exists(exx.yao)
    assert after_sue_planunit.person_exists(exx.zia) is False


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_person():
    # ESTABLISH
    sue_plandelta = plandelta_shop()

    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    assert before_sue_planunit.person_exists(exx.yao)
    assert before_sue_planunit.person_exists(exx.zia) is False

    # WHEN
    dimen = kw.plan_personunit
    x_planatom = planatom_shop(dimen, kw.INSERT)
    x_planatom.set_jkey(kw.person_name, exx.zia)
    x_person_cred_lumen = 55
    x_person_debt_lumen = 66
    x_planatom.set_jvalue("person_cred_lumen", x_person_cred_lumen)
    x_planatom.set_jvalue("person_debt_lumen", x_person_debt_lumen)
    sue_plandelta.set_planatom(x_planatom)
    print(f"{sue_plandelta.planatoms.keys()=}")
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    yao_personunit = after_sue_planunit.get_person(exx.yao)
    zia_personunit = after_sue_planunit.get_person(exx.zia)
    assert yao_personunit is not None
    assert zia_personunit is not None
    assert zia_personunit.person_cred_lumen == x_person_cred_lumen
    assert zia_personunit.person_debt_lumen == x_person_debt_lumen


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_person():
    # ESTABLISH
    sue_plandelta = plandelta_shop()

    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    assert before_sue_planunit.get_person(exx.yao).person_cred_lumen == 1

    # WHEN
    dimen = kw.plan_personunit
    x_planatom = planatom_shop(dimen, kw.UPDATE)
    x_planatom.set_jkey(kw.person_name, exx.yao)
    yao_person_cred_lumen = 55
    x_planatom.set_jvalue("person_cred_lumen", yao_person_cred_lumen)
    sue_plandelta.set_planatom(x_planatom)
    print(f"{sue_plandelta.planatoms.keys()=}")
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    yao_person = after_sue_planunit.get_person(exx.yao)
    assert yao_person.person_cred_lumen == yao_person_cred_lumen


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)
    before_sue_planunit.add_personunit(exx.bob)
    yao_personunit = before_sue_planunit.get_person(exx.yao)
    zia_personunit = before_sue_planunit.get_person(exx.zia)
    bob_personunit = before_sue_planunit.get_person(exx.bob)
    yao_personunit.add_membership(exx.run)
    zia_personunit.add_membership(exx.run)
    fly_str = ";flyers"
    yao_personunit.add_membership(fly_str)
    zia_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)
    before_group_titles_dict = before_sue_planunit.get_personunit_group_titles_dict()
    assert len(before_group_titles_dict.get(exx.run)) == 2
    assert len(before_group_titles_dict.get(fly_str)) == 3

    # WHEN
    yao_planatom = planatom_shop(kw.plan_person_membership, kw.DELETE)
    yao_planatom.set_jkey(kw.group_title, exx.run)
    yao_planatom.set_jkey(kw.person_name, exx.yao)
    # print(f"{yao_planatom=}")
    zia_planatom = planatom_shop(kw.plan_person_membership, kw.DELETE)
    zia_planatom.set_jkey(kw.group_title, fly_str)
    zia_planatom.set_jkey(kw.person_name, exx.zia)
    # print(f"{zia_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(yao_planatom)
    sue_plandelta.set_planatom(zia_planatom)
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    after_group_titles_dict = after_sue_planunit.get_personunit_group_titles_dict()
    assert len(after_group_titles_dict.get(exx.run)) == 1
    assert len(after_group_titles_dict.get(fly_str)) == 2


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_membership():
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)
    before_sue_planunit.add_personunit(exx.bob)
    zia_personunit = before_sue_planunit.get_person(exx.zia)
    zia_personunit.add_membership(exx.run)
    before_group_titles = before_sue_planunit.get_personunit_group_titles_dict()
    assert len(before_group_titles.get(exx.run)) == 1

    # WHEN
    yao_planatom = planatom_shop(kw.plan_person_membership, kw.INSERT)
    yao_planatom.set_jkey(kw.group_title, exx.run)
    yao_planatom.set_jkey(kw.person_name, exx.yao)
    yao_run_group_cred_lumen = 17
    yao_planatom.set_jvalue(kw.group_cred_lumen, yao_run_group_cred_lumen)
    print(f"{yao_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(yao_planatom)
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    after_group_titles = after_sue_planunit.get_personunit_group_titles_dict()
    assert len(after_group_titles.get(exx.run)) == 2
    after_yao_personunit = after_sue_planunit.get_person(exx.yao)
    after_yao_run_membership = after_yao_personunit.get_membership(exx.run)
    assert after_yao_run_membership is not None
    assert after_yao_run_membership.group_cred_lumen == yao_run_group_cred_lumen


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_yao_personunit = before_sue_planunit.get_person(exx.yao)
    old_yao_run_group_cred_lumen = 3
    before_yao_personunit.add_membership(exx.run, old_yao_run_group_cred_lumen)
    yao_run_membership = before_yao_personunit.get_membership(exx.run)
    assert yao_run_membership.group_cred_lumen == old_yao_run_group_cred_lumen
    assert yao_run_membership.group_debt_lumen == 1

    # WHEN
    yao_planatom = planatom_shop(kw.plan_person_membership, kw.UPDATE)
    yao_planatom.set_jkey(kw.group_title, exx.run)
    yao_planatom.set_jkey(kw.person_name, exx.yao)
    new_yao_run_group_cred_lumen = 7
    new_yao_run_group_debt_lumen = 11
    yao_planatom.set_jvalue(kw.group_cred_lumen, new_yao_run_group_cred_lumen)
    yao_planatom.set_jvalue(kw.group_debt_lumen, new_yao_run_group_debt_lumen)
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(yao_planatom)
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    after_yao_personunit = after_sue_planunit.get_person(exx.yao)
    after_yao_run_membership = after_yao_personunit.get_membership(exx.run)
    assert after_yao_run_membership.group_cred_lumen == new_yao_run_group_cred_lumen
    assert after_yao_run_membership.group_debt_lumen == new_yao_run_group_debt_lumen


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_kegunit():
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_planunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_planunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_planunit.make_rope(sports_rope, disc_str)
    before_sue_planunit.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_sue_planunit.set_keg_obj(kegunit_shop(disc_str), sports_rope)
    delete_disc_planatom = planatom_shop(kw.plan_kegunit, kw.DELETE)
    delete_disc_planatom.set_jkey(kw.keg_rope, disc_rope)
    print(f"{disc_rope=}")
    delete_disc_planatom.set_jkey(kw.keg_rope, disc_rope)
    print(f"{delete_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(delete_disc_planatom)
    assert before_sue_planunit.keg_exists(ball_rope)
    assert before_sue_planunit.keg_exists(disc_rope)

    # WHEN
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    assert after_sue_planunit.keg_exists(ball_rope)
    assert after_sue_planunit.keg_exists(disc_rope) is False


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_kegunit():
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_planunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_planunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_planunit.make_rope(sports_rope, disc_str)
    before_sue_planunit.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    assert before_sue_planunit.keg_exists(ball_rope)
    assert before_sue_planunit.keg_exists(disc_rope) is False

    # WHEN
    # x_addin = 140
    x_gogo_want = 1000
    x_stop_want = 1700
    # x_denom = 17
    # x_numor = 10
    x_pledge = True
    insert_disc_planatom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    insert_disc_planatom.set_jkey(kw.keg_rope, disc_rope)
    # insert_disc_planatom.set_jvalue(kw.addin, x_addin)
    # insert_disc_planatom.set_jvalue(kw.begin, x_begin)
    # insert_disc_planatom.set_jvalue(kw.close, x_close)
    # insert_disc_planatom.set_jvalue(kw.denom, x_denom)
    # insert_disc_planatom.set_jvalue(kw.numor, x_numor)
    insert_disc_planatom.set_jvalue(kw.pledge, x_pledge)
    insert_disc_planatom.set_jvalue(kw.gogo_want, x_gogo_want)
    insert_disc_planatom.set_jvalue(kw.stop_want, x_stop_want)

    print(f"{insert_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(insert_disc_planatom)
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    assert after_sue_planunit.keg_exists(ball_rope)
    assert after_sue_planunit.keg_exists(disc_rope)
    disc_keg = after_sue_planunit.get_keg_obj(disc_rope)
    assert disc_keg.gogo_want == x_gogo_want
    assert disc_keg.stop_want == x_stop_want


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_kegunit_SimpleAttributes():
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_planunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_planunit.make_rope(sports_rope, ball_str)
    before_sue_planunit.set_keg_obj(kegunit_shop(ball_str), sports_rope)

    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    # x_numor = 10
    x_gogo_want = 1222
    x_stop_want = 1333
    x_pledge = True
    insert_disc_planatom = planatom_shop(kw.plan_kegunit, kw.UPDATE)
    insert_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    # insert_disc_planatom.set_jvalue(kw.addin, x_addin)
    insert_disc_planatom.set_jvalue(kw.begin, x_begin)
    insert_disc_planatom.set_jvalue(kw.close, x_close)
    # insert_disc_planatom.set_jvalue(kw.denom, x_denom)
    # insert_disc_planatom.set_jvalue(kw.numor, x_numor)
    insert_disc_planatom.set_jvalue(kw.pledge, x_pledge)
    insert_disc_planatom.set_jvalue(kw.gogo_want, x_gogo_want)
    insert_disc_planatom.set_jvalue(kw.stop_want, x_stop_want)

    print(f"{insert_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(insert_disc_planatom)
    assert before_sue_planunit.get_keg_obj(ball_rope).begin is None
    assert before_sue_planunit.get_keg_obj(ball_rope).close is None
    assert before_sue_planunit.get_keg_obj(ball_rope).pledge is False
    assert before_sue_planunit.get_keg_obj(ball_rope).gogo_want is None
    assert before_sue_planunit.get_keg_obj(ball_rope).stop_want is None

    # WHEN
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    assert after_sue_planunit.get_keg_obj(ball_rope).begin == x_begin
    assert after_sue_planunit.get_keg_obj(ball_rope).close == x_close
    assert after_sue_planunit.get_keg_obj(ball_rope).gogo_want == x_gogo_want
    assert after_sue_planunit.get_keg_obj(ball_rope).stop_want == x_stop_want
    assert after_sue_planunit.get_keg_obj(ball_rope).pledge


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_keg_awardunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)
    before_sue_planunit.add_personunit(exx.bob)
    yao_personunit = before_sue_planunit.get_person(exx.yao)
    zia_personunit = before_sue_planunit.get_person(exx.zia)
    bob_personunit = before_sue_planunit.get_person(exx.bob)
    yao_personunit.add_membership(exx.run)
    zia_personunit.add_membership(exx.run)
    fly_str = ";flyers"
    yao_personunit.add_membership(fly_str)
    zia_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)

    sports_str = "sports"
    sports_rope = before_sue_planunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_planunit.make_rope(sports_rope, ball_str)
    disc_str = "Ultimate Disc"
    disc_rope = before_sue_planunit.make_rope(sports_rope, disc_str)
    before_sue_planunit.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_sue_planunit.set_keg_obj(kegunit_shop(disc_str), sports_rope)
    before_sue_planunit.edit_keg_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    before_sue_planunit.edit_keg_attr(ball_rope, awardunit=awardunit_shop(fly_str))
    before_sue_planunit.edit_keg_attr(disc_rope, awardunit=awardunit_shop(exx.run))
    before_sue_planunit.edit_keg_attr(disc_rope, awardunit=awardunit_shop(fly_str))
    assert len(before_sue_planunit.get_keg_obj(ball_rope).awardunits) == 2
    assert len(before_sue_planunit.get_keg_obj(disc_rope).awardunits) == 2

    # WHEN
    delete_disc_planatom = planatom_shop(kw.plan_keg_awardunit, kw.DELETE)
    delete_disc_planatom.set_jkey(kw.keg_rope, disc_rope)
    delete_disc_planatom.set_jkey(kw.awardee_title, fly_str)
    print(f"{delete_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(delete_disc_planatom)
    after_sue_planunit = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    assert len(after_sue_planunit.get_keg_obj(ball_rope).awardunits) == 2
    assert len(after_sue_planunit.get_keg_obj(disc_rope).awardunits) == 1


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_keg_awardunit():
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)
    yao_personunit = before_sue_planunit.get_person(exx.yao)
    yao_personunit.add_membership(exx.run)

    sports_str = "sports"
    sports_rope = before_sue_planunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_planunit.make_rope(sports_rope, ball_str)
    before_sue_planunit.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_sue_planunit.edit_keg_attr(ball_rope, awardunit=awardunit_shop(exx.run))
    run_awardunit = before_sue_planunit.get_keg_obj(ball_rope).awardunits.get(exx.run)
    assert run_awardunit.give_force == 1
    assert run_awardunit.take_force == 1

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_planatom = planatom_shop(kw.plan_keg_awardunit, kw.UPDATE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.awardee_title, exx.run)
    update_disc_planatom.set_jvalue(kw.give_force, x_give_force)
    update_disc_planatom.set_jvalue(kw.take_force, x_take_force)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    run_awardunit = after_sue_au.get_keg_obj(ball_rope).awardunits.get(exx.run)
    print(f"{run_awardunit.give_force=}")
    assert run_awardunit.give_force == x_give_force
    assert run_awardunit.take_force == x_take_force


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_keg_awardunit():
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)
    yao_personunit = before_sue_planunit.get_person(exx.yao)
    yao_personunit.add_membership(exx.run)
    sports_str = "sports"
    sports_rope = before_sue_planunit.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_planunit.make_rope(sports_rope, ball_str)
    before_sue_planunit.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_keg = before_sue_planunit.get_keg_obj(ball_rope)
    assert before_ball_keg.awardunits.get(exx.run) is None

    # WHEN
    x_give_force = 55
    x_take_force = 66
    update_disc_planatom = planatom_shop(kw.plan_keg_awardunit, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.awardee_title, exx.run)
    update_disc_planatom.set_jvalue(kw.give_force, x_give_force)
    update_disc_planatom.set_jvalue(kw.take_force, x_take_force)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_keg.awardunits.get(exx.run) is not None


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_keg_factunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_keg.factunits == {}

    # WHEN
    damaged_fact_lower = 55
    damaged_fact_upper = 66
    update_disc_planatom = planatom_shop(kw.plan_keg_factunit, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_planatom.set_jvalue(kw.fact_state, damaged_rope)
    update_disc_planatom.set_jvalue(kw.fact_lower, damaged_fact_lower)
    update_disc_planatom.set_jvalue(kw.fact_upper, damaged_fact_upper)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_keg.factunits != {}
    assert after_ball_keg.factunits.get(knee_rope) is not None
    assert after_ball_keg.factunits.get(knee_rope).fact_context == knee_rope
    assert after_ball_keg.factunits.get(knee_rope).fact_state == damaged_rope
    assert after_ball_keg.factunits.get(knee_rope).fact_lower == damaged_fact_lower
    assert after_ball_keg.factunits.get(knee_rope).fact_upper == damaged_fact_upper


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_keg_factunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_sue_au.edit_keg_attr(
        ball_rope,
        factunit=factunit_shop(fact_context=knee_rope, fact_state=damaged_rope),
    )
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_keg.factunits != {}
    assert before_ball_keg.factunits.get(knee_rope) is not None

    # WHEN
    update_disc_planatom = planatom_shop(kw.plan_keg_factunit, kw.DELETE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.fact_context, knee_rope)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_keg.factunits == {}


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_keg_factunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_sue_au.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_knee_factunit = factunit_shop(knee_rope, damaged_rope)
    before_sue_au.edit_keg_attr(ball_rope, factunit=before_knee_factunit)
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_keg.factunits != {}
    assert before_ball_keg.factunits.get(knee_rope) is not None
    assert before_ball_keg.factunits.get(knee_rope).fact_state == damaged_rope
    assert before_ball_keg.factunits.get(knee_rope).fact_lower is None
    assert before_ball_keg.factunits.get(knee_rope).fact_upper is None

    # WHEN
    medical_fact_lower = 45
    medical_fact_upper = 77
    update_disc_planatom = planatom_shop(kw.plan_keg_factunit, kw.UPDATE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_planatom.set_jvalue(kw.fact_state, medical_rope)
    update_disc_planatom.set_jvalue(kw.fact_lower, medical_fact_lower)
    update_disc_planatom.set_jvalue(kw.fact_upper, medical_fact_upper)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_keg.factunits != {}
    assert after_ball_keg.factunits.get(knee_rope) is not None
    assert after_ball_keg.factunits.get(knee_rope).fact_state == medical_rope
    assert after_ball_keg.factunits.get(knee_rope).fact_lower == medical_fact_lower
    assert after_ball_keg.factunits.get(knee_rope).fact_upper == medical_fact_upper


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_keg_reason_caseunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_sue_au.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_keg.reasonunits != {}
    before_knee_reasonunit = before_ball_keg.get_reasonunit(knee_rope)
    assert before_knee_reasonunit is not None
    damaged_caseunit = before_knee_reasonunit.get_case(damaged_rope)
    assert damaged_caseunit.reason_state == damaged_rope
    assert damaged_caseunit.reason_lower is None
    assert damaged_caseunit.reason_upper is None
    assert damaged_caseunit.reason_divisor is None

    # WHEN
    damaged_reason_lower = 45
    damaged_reason_upper = 77
    damaged_reason_divisor = 3
    update_disc_planatom = planatom_shop(kw.plan_keg_reason_caseunit, kw.UPDATE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.reason_context, knee_rope)
    update_disc_planatom.set_jkey(kw.reason_state, damaged_rope)
    update_disc_planatom.set_jvalue(kw.reason_lower, damaged_reason_lower)
    update_disc_planatom.set_jvalue(kw.reason_upper, damaged_reason_upper)
    update_disc_planatom.set_jvalue(kw.reason_divisor, damaged_reason_divisor)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    after_knee_reasonunit = after_ball_keg.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    after_damaged_caseunit = after_knee_reasonunit.get_case(damaged_rope)
    assert after_damaged_caseunit.reason_state == damaged_rope
    assert after_damaged_caseunit.reason_lower == damaged_reason_lower
    assert after_damaged_caseunit.reason_upper == damaged_reason_upper
    assert after_damaged_caseunit.reason_divisor == damaged_reason_divisor


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_keg_reason_caseunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_sue_au.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_sue_au.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    before_knee_reasonunit = before_ball_keg.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_case(damaged_rope) is not None
    assert before_knee_reasonunit.get_case(medical_rope) is None

    # WHEN
    medical_reason_lower = 45
    medical_reason_upper = 77
    medical_reason_divisor = 3
    update_disc_planatom = planatom_shop(kw.plan_keg_reason_caseunit, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.reason_context, knee_rope)
    update_disc_planatom.set_jkey(kw.reason_state, medical_rope)
    update_disc_planatom.set_jvalue(kw.reason_lower, medical_reason_lower)
    update_disc_planatom.set_jvalue(kw.reason_upper, medical_reason_upper)
    update_disc_planatom.set_jvalue(kw.reason_divisor, medical_reason_divisor)
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    after_knee_reasonunit = after_ball_keg.get_reasonunit(knee_rope)
    after_medical_caseunit = after_knee_reasonunit.get_case(medical_rope)
    assert after_medical_caseunit is not None
    assert after_medical_caseunit.reason_state == medical_rope
    assert after_medical_caseunit.reason_lower == medical_reason_lower
    assert after_medical_caseunit.reason_upper == medical_reason_upper
    assert after_medical_caseunit.reason_divisor == medical_reason_divisor


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_keg_reason_caseunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    damaged_str = "damaged mcl"
    damaged_rope = before_sue_au.make_rope(knee_rope, damaged_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(damaged_str), knee_rope)
    before_sue_au.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_sue_au.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=damaged_rope
    )
    before_sue_au.edit_keg_attr(
        ball_rope, reason_context=knee_rope, reason_case=medical_rope
    )
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    before_knee_reasonunit = before_ball_keg.get_reasonunit(knee_rope)
    assert before_knee_reasonunit.get_case(damaged_rope) is not None
    assert before_knee_reasonunit.get_case(medical_rope) is not None

    # WHEN
    update_disc_planatom = planatom_shop(kw.plan_keg_reason_caseunit, kw.DELETE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.reason_context, knee_rope)
    update_disc_planatom.set_jkey(kw.reason_state, medical_rope)
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    after_knee_reasonunit = after_ball_keg.get_reasonunit(knee_rope)
    assert after_knee_reasonunit.get_case(damaged_rope) is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_keg_reasonunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_keg.get_reasonunit(knee_rope) is None

    # WHEN
    medical_active_requisite = True
    update_disc_planatom = planatom_shop(kw.plan_keg_reasonunit, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey("reason_context", knee_rope)
    update_disc_planatom.set_jvalue(
        kw.active_requisite,
        medical_active_requisite,
    )
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    after_knee_reasonunit = after_ball_keg.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None
    assert after_knee_reasonunit.active_requisite == medical_active_requisite


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_update_keg_reasonunit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_str = "get medical attention"
    medical_rope = before_sue_au.make_rope(knee_rope, medical_str)
    before_medical_active_requisite = False
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.set_keg_obj(kegunit_shop(medical_str), knee_rope)
    before_sue_au.edit_keg_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_requisite_active=before_medical_active_requisite,
    )
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    before_ball_reasonunit = before_ball_keg.get_reasonunit(knee_rope)
    assert before_ball_reasonunit is not None
    assert before_ball_reasonunit.active_requisite == before_medical_active_requisite

    # WHEN
    after_medical_active_requisite = True
    update_disc_planatom = planatom_shop(kw.plan_keg_reasonunit, kw.UPDATE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey("reason_context", knee_rope)
    update_disc_planatom.set_jvalue(
        kw.active_requisite,
        after_medical_active_requisite,
    )
    # print(f"{update_disc_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    after_knee_reasonunit = after_ball_keg.get_reasonunit(knee_rope)
    assert after_knee_reasonunit is not None
    assert after_knee_reasonunit.get_case(medical_rope) is None
    assert after_knee_reasonunit.active_requisite == after_medical_active_requisite


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_keg_reasonunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    knee_str = "knee"
    knee_rope = before_sue_au.make_l1_rope(knee_str)
    medical_active_requisite = False
    before_sue_au.set_l1_keg(kegunit_shop(knee_str))
    before_sue_au.edit_keg_attr(
        ball_rope,
        reason_context=knee_rope,
        reason_requisite_active=medical_active_requisite,
    )
    before_ball_keg = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_keg.get_reasonunit(knee_rope) is not None

    # WHEN
    update_disc_planatom = planatom_shop(kw.plan_keg_reasonunit, kw.DELETE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey("reason_context", knee_rope)
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_keg = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_keg.get_reasonunit(knee_rope) is None


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_keg_partyunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_kegunit.laborunit.partys == {}

    # WHEN
    update_disc_planatom = planatom_shop(kw.plan_keg_partyunit, kw.INSERT)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.party_title, exx.yao)
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_kegunit = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_kegunit.laborunit.partys != set()
    assert after_ball_kegunit.laborunit.get_partyunit(exx.yao) is not None


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_keg_partyunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_au.get_keg_obj(ball_rope)
    before_ball_kegunit.laborunit.add_party(exx.yao)
    assert before_ball_kegunit.laborunit.partys != set()
    assert before_ball_kegunit.laborunit.get_partyunit(exx.yao) is not None

    # WHEN
    update_disc_planatom = planatom_shop(kw.plan_keg_partyunit, kw.DELETE)
    update_disc_planatom.set_jkey(kw.keg_rope, ball_rope)
    update_disc_planatom.set_jkey(kw.party_title, exx.yao)
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(update_disc_planatom)
    print(f"{before_sue_au.get_keg_obj(ball_rope).laborunit=}")
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_kegunit = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_kegunit.laborunit.partys == {}


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_insert_keg_healerunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_au.get_keg_obj(ball_rope)
    assert before_ball_kegunit.healerunit._healer_names == set()
    assert not before_ball_kegunit.healerunit.healer_name_exists(exx.yao)

    # WHEN
    x_planatom = planatom_shop(kw.plan_keg_healerunit, kw.INSERT)
    x_planatom.set_jkey(kw.keg_rope, ball_rope)
    x_planatom.set_jkey(kw.healer_name, exx.yao)
    print(f"{x_planatom=}")
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(x_planatom)
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_kegunit = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_kegunit.healerunit._healer_names != set()
    assert after_ball_kegunit.healerunit.healer_name_exists(exx.yao)


def test_PlanDelta_get_edited_plan_ReturnsObj_PlanUnit_delete_keg_healerunit():
    # ESTABLISH
    before_sue_au = planunit_shop(exx.sue)
    before_sue_au.add_personunit(exx.yao)
    sports_str = "sports"
    sports_rope = before_sue_au.make_l1_rope(sports_str)
    ball_str = "basketball"
    ball_rope = before_sue_au.make_rope(sports_rope, ball_str)
    before_sue_au.set_keg_obj(kegunit_shop(ball_str), sports_rope)
    before_ball_kegunit = before_sue_au.get_keg_obj(ball_rope)
    before_ball_kegunit.healerunit.set_healer_name(exx.yao)
    assert before_ball_kegunit.healerunit._healer_names != set()
    assert before_ball_kegunit.healerunit.healer_name_exists(exx.yao)

    # WHEN
    x_planatom = planatom_shop(kw.plan_keg_healerunit, kw.DELETE)
    x_planatom.set_jkey(kw.keg_rope, ball_rope)
    x_planatom.set_jkey(kw.healer_name, exx.yao)
    sue_plandelta = plandelta_shop()
    sue_plandelta.set_planatom(x_planatom)
    print(f"{before_sue_au.get_keg_obj(ball_rope).laborunit=}")
    after_sue_au = sue_plandelta.get_atom_edited_plan(before_sue_au)

    # THEN
    after_ball_kegunit = after_sue_au.get_keg_obj(ball_rope)
    assert after_ball_kegunit.healerunit._healer_names == set()
    assert not after_ball_kegunit.healerunit.healer_name_exists(exx.yao)


def test_PlanDelta_get_plandelta_example1_ContainsPlanAtoms():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    before_sue_planunit = planunit_shop(exx.sue)
    before_sue_planunit.add_personunit(exx.yao)
    before_sue_planunit.add_personunit(exx.zia)
    before_sue_planunit.add_personunit(exx.bob)
    yao_personunit = before_sue_planunit.get_person(exx.yao)
    zia_personunit = before_sue_planunit.get_person(exx.zia)
    bob_personunit = before_sue_planunit.get_person(exx.bob)
    yao_personunit.add_membership(exx.run)
    zia_personunit.add_membership(exx.run)
    fly_str = ";flyers"
    yao_personunit.add_membership(fly_str)
    bob_personunit.add_membership(fly_str)
    assert before_sue_planunit.tally != 55
    assert before_sue_planunit.max_tree_traverse != 66
    assert before_sue_planunit.credor_respect != 77
    assert before_sue_planunit.debtor_respect != 88
    assert before_sue_planunit.person_exists(exx.yao)
    assert before_sue_planunit.person_exists(exx.zia)
    assert yao_personunit.get_membership(fly_str) is not None
    assert bob_personunit.get_membership(fly_str) is not None

    # WHEN
    ex1_plandelta = get_plandelta_example1()
    after_sue_planunit = ex1_plandelta.get_atom_edited_plan(before_sue_planunit)

    # THEN
    assert after_sue_planunit.tally == 55
    assert after_sue_planunit.max_tree_traverse == 66
    assert after_sue_planunit.credor_respect == 77
    assert after_sue_planunit.debtor_respect == 88
    assert after_sue_planunit.person_exists(exx.yao)
    assert after_sue_planunit.person_exists(exx.zia) is False
