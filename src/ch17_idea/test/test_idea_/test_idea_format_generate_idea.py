from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import planunit_v001
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch17_idea.idea_config import (
    idea_format_00013_kegunit_v0_0_0,
    idea_format_00021_plan_personunit_v0_0_0,
)
from src.ch17_idea.idea_main import create_idea_df, get_idearef_obj, make_plandelta
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_make_plandelta_Arg_idea_format_00021_plan_personunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_person_cred_lumen = 11
    bob_person_cred_lumen = 13
    yao_person_cred_lumen = 41
    sue_person_debt_lumen = 23
    bob_person_debt_lumen = 29
    yao_person_debt_lumen = 37
    amy_moment_label = "amy56"
    sue_planunit = planunit_shop(exx.sue, amy_moment_label)
    sue_planunit.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    sue_planunit.add_personunit(exx.bob, bob_person_cred_lumen, bob_person_debt_lumen)
    sue_planunit.add_personunit(exx.yao, yao_person_cred_lumen, yao_person_debt_lumen)
    x_idea_name = idea_format_00021_plan_personunit_v0_0_0()
    person_dataframe = create_idea_df(sue_planunit, x_idea_name)
    print(f"{person_dataframe.columns=}")
    person_csv = person_dataframe.to_csv(index=False)

    # WHEN
    sue_person_plandelta = make_plandelta(person_csv)

    # THEN
    assert sue_person_plandelta
    sue_planatom = planatom_shop(kw.plan_personunit, kw.INSERT)
    sue_planatom.set_arg(kw.person_name, exx.sue)
    sue_planatom.set_arg(kw.person_cred_lumen, sue_person_cred_lumen)
    sue_planatom.set_arg(kw.person_debt_lumen, sue_person_debt_lumen)
    sue_planatom.set_atom_order()
    bob_planatom = planatom_shop(kw.plan_personunit, kw.INSERT)
    bob_planatom.set_arg(kw.person_name, exx.bob)
    bob_planatom.set_arg(kw.person_cred_lumen, bob_person_cred_lumen)
    bob_planatom.set_arg(kw.person_debt_lumen, bob_person_debt_lumen)
    bob_planatom.set_atom_order()
    # print(f"{sue_person_plandelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_person_plandelta.planatoms.get(kw.INSERT).get(kw.plan_personunit).get(exx.sue)=}"
    # )
    print(f"{sue_planatom=}")
    assert sue_person_plandelta.c_planatom_exists(sue_planatom)
    assert sue_person_plandelta.c_planatom_exists(bob_planatom)
    assert len(sue_person_plandelta.get_ordered_planatoms()) == 3


# def test_make_plandelta_Arg_idea_format_00020_plan_person_membership_v0_0_0():
#     # ESTABLISH
#     exx.bob = "Bob"
#     exx.yao = "Yao"
#     amy_moment_label = "amy56"
#     sue_planunit = planunit_shop(exx.sue, amy_moment_label)
#     sue_planunit.add_personunit(exx.sue)
#     sue_planunit.add_personunit(exx.bob)
#     sue_planunit.add_personunit(exx.yao)
#     iowa_str = ";Iowa"
#     sue_iowa_group_cred_lumen = 37
#     bob_iowa_group_cred_lumen = 43
#     yao_iowa_group_cred_lumen = 51
#     sue_iowa_group_debt_lumen = 57
#     bob_iowa_group_debt_lumen = 61
#     yao_iowa_group_debt_lumen = 67
#     ohio_str = ";Ohio"
#     yao_ohio_group_cred_lumen = 73
#     yao_ohio_group_debt_lumen = 67
#     sue_personunit = sue_planunit.get_person(exx.sue)
#     bob_personunit = sue_planunit.get_person(exx.bob)
#     yao_personunit = sue_planunit.get_person(exx.yao)
#     sue_personunit.add_membership(iowa_str, sue_iowa_group_cred_lumen, sue_iowa_group_debt_lumen)
#     bob_personunit.add_membership(iowa_str, bob_iowa_group_cred_lumen, bob_iowa_group_debt_lumen)
#     yao_personunit.add_membership(iowa_str, yao_iowa_group_cred_lumen, yao_iowa_group_debt_lumen)
#     yao_personunit.add_membership(ohio_str, yao_ohio_group_cred_lumen, yao_ohio_group_debt_lumen)
#     x_idea_name = idea_format_00020_plan_person_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_planunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_plandelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_planatom = planatom_shop(kw.plan_person_membership, kw.INSERT)
#     bob_iowa_planatom = planatom_shop(kw.plan_person_membership, kw.INSERT)
#     yao_iowa_planatom = planatom_shop(kw.plan_person_membership, kw.INSERT)
#     yao_ohio_planatom = planatom_shop(kw.plan_person_membership, kw.INSERT)
#     sue_iowa_planatom.set_arg(kw.group_title, iowa_str)
#     bob_iowa_planatom.set_arg(kw.group_title, iowa_str)
#     yao_iowa_planatom.set_arg(kw.group_title, iowa_str)
#     yao_ohio_planatom.set_arg(kw.group_title, ohio_str)
#     sue_iowa_planatom.set_arg(kw.person_name, exx.sue)
#     bob_iowa_planatom.set_arg(kw.person_name, exx.bob)
#     yao_iowa_planatom.set_arg(kw.person_name, exx.yao)
#     yao_ohio_planatom.set_arg(kw.person_name, exx.yao)
#     sue_iowa_planatom.set_arg(kw.group_cred_lumen, sue_iowa_group_cred_lumen)
#     bob_iowa_planatom.set_arg(kw.group_cred_lumen, bob_iowa_group_cred_lumen)
#     yao_iowa_planatom.set_arg(kw.group_cred_lumen, yao_iowa_group_cred_lumen)
#     yao_ohio_planatom.set_arg(kw.group_cred_lumen, yao_ohio_group_cred_lumen)
#     sue_iowa_planatom.set_arg(kw.group_debt_lumen, sue_iowa_group_debt_lumen)
#     bob_iowa_planatom.set_arg(kw.group_debt_lumen, bob_iowa_group_debt_lumen)
#     yao_iowa_planatom.set_arg(kw.group_debt_lumen, yao_iowa_group_debt_lumen)
#     yao_ohio_planatom.set_arg(kw.group_debt_lumen, yao_ohio_group_debt_lumen)
#     bob_iowa_planatom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_planatoms()[2]=}")
#     # print(f"{sue_iowa_planatom=}")
#     assert len(membership_changunit.get_ordered_planatoms()) == 10
#     assert membership_changunit.get_ordered_planatoms()[0] == bob_iowa_planatom
#     assert membership_changunit.planatom_exists(sue_iowa_planatom)
#     assert membership_changunit.planatom_exists(bob_iowa_planatom)
#     assert membership_changunit.planatom_exists(yao_iowa_planatom)
#     assert membership_changunit.planatom_exists(yao_ohio_planatom)
#     assert len(membership_changunit.get_ordered_planatoms()) == 10


def test_make_plandelta_Arg_idea_format_00013_kegunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    amy_moment_label = "amy56"
    sue_planunit = planunit_shop(exx.sue, amy_moment_label)
    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_planunit.set_l1_keg(kegunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_planunit.make_rope(casa_rope, exx.clean)
    sue_planunit.set_keg_obj(kegunit_shop(exx.clean, pledge=True), casa_rope)
    x_idea_name = idea_format_00013_kegunit_v0_0_0()
    kegunit_dataframe = create_idea_df(sue_planunit, x_idea_name)
    kegunit_csv = kegunit_dataframe.to_csv(index=False)

    # WHEN
    kegunit_changunit = make_plandelta(kegunit_csv)

    # THEN
    casa_planatom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    casa_planatom.set_arg(kw.keg_rope, casa_rope)
    casa_planatom.set_arg(kw.pledge, False)
    casa_planatom.set_arg(kw.star, casa_star)
    print(f"{casa_planatom=}")
    assert casa_planatom.get_value(kw.star) == casa_star
    clean_planatom = planatom_shop(kw.plan_kegunit, kw.INSERT)
    clean_planatom.set_arg(kw.keg_rope, clean_rope)
    clean_planatom.set_arg(kw.pledge, True)
    clean_planatom.set_arg(kw.star, 1)
    assert kegunit_changunit.c_planatom_exists(casa_planatom)
    assert kegunit_changunit.c_planatom_exists(clean_planatom)
    assert len(kegunit_changunit.get_ordered_planatoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_kegunit_v0_0_0_Scenario_planunit_v001(
    run_big_tests,
):
    # sourcery skip: no-conditionals-in-tests
    if run_big_tests:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_kegunit_v0_0_0()

        # WHEN
        kegunit_format = create_idea_df(planunit_v001(), x_idea_name)

        # THEN
        array_headers = list(kegunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(kegunit_format) == 251
