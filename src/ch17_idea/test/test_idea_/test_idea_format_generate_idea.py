from src.ch04_rope.rope import create_rope
from src.ch06_keg.keg import kegunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import personunit_v001
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch17_idea.idea_config import (
    idea_format_00013_kegunit_v0_0_0,
    idea_format_00021_person_partnerunit_v0_0_0,
)
from src.ch17_idea.idea_main import create_idea_df, get_idearef_obj, make_persondelta
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_make_persondelta_Arg_idea_format_00021_person_partnerunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_partner_cred_lumen = 11
    bob_partner_cred_lumen = 13
    yao_partner_cred_lumen = 41
    sue_partner_debt_lumen = 23
    bob_partner_debt_lumen = 29
    yao_partner_debt_lumen = 37
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    sue_personunit.add_partnerunit(
        exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen
    )
    sue_personunit.add_partnerunit(
        exx.bob, bob_partner_cred_lumen, bob_partner_debt_lumen
    )
    sue_personunit.add_partnerunit(
        exx.yao, yao_partner_cred_lumen, yao_partner_debt_lumen
    )
    x_idea_name = idea_format_00021_person_partnerunit_v0_0_0()
    partner_dataframe = create_idea_df(sue_personunit, x_idea_name)
    print(f"{partner_dataframe.columns=}")
    partner_csv = partner_dataframe.to_csv(index=False)

    # WHEN
    sue_partner_persondelta = make_persondelta(partner_csv)

    # THEN
    assert sue_partner_persondelta
    sue_personatom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    sue_personatom.set_arg(kw.partner_name, exx.sue)
    sue_personatom.set_arg(kw.partner_cred_lumen, sue_partner_cred_lumen)
    sue_personatom.set_arg(kw.partner_debt_lumen, sue_partner_debt_lumen)
    sue_personatom.set_atom_order()
    bob_personatom = personatom_shop(kw.person_partnerunit, kw.INSERT)
    bob_personatom.set_arg(kw.partner_name, exx.bob)
    bob_personatom.set_arg(kw.partner_cred_lumen, bob_partner_cred_lumen)
    bob_personatom.set_arg(kw.partner_debt_lumen, bob_partner_debt_lumen)
    bob_personatom.set_atom_order()
    # print(f"{sue_partner_persondelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_partner_persondelta.personatoms.get(kw.INSERT).get(kw.person_partnerunit).get(exx.sue)=}"
    # )
    print(f"{sue_personatom=}")
    assert sue_partner_persondelta.c_personatom_exists(sue_personatom)
    assert sue_partner_persondelta.c_personatom_exists(bob_personatom)
    assert len(sue_partner_persondelta.get_ordered_personatoms()) == 3


# def test_make_persondelta_Arg_idea_format_00020_person_partner_membership_v0_0_0():
#     # ESTABLISH
#     exx.bob = "Bob"
#     exx.yao = "Yao"
#     amy_moment_rope = create_rope("amy56")
#     sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
#     sue_personunit.add_partnerunit(exx.sue)
#     sue_personunit.add_partnerunit(exx.bob)
#     sue_personunit.add_partnerunit(exx.yao)
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
#     sue_partnerunit = sue_personunit.get_partner(exx.sue)
#     bob_partnerunit = sue_personunit.get_partner(exx.bob)
#     yao_partnerunit = sue_personunit.get_partner(exx.yao)
#     sue_partnerunit.add_membership(iowa_str, sue_iowa_group_cred_lumen, sue_iowa_group_debt_lumen)
#     bob_partnerunit.add_membership(iowa_str, bob_iowa_group_cred_lumen, bob_iowa_group_debt_lumen)
#     yao_partnerunit.add_membership(iowa_str, yao_iowa_group_cred_lumen, yao_iowa_group_debt_lumen)
#     yao_partnerunit.add_membership(ohio_str, yao_ohio_group_cred_lumen, yao_ohio_group_debt_lumen)
#     x_idea_name = idea_format_00020_person_partner_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_personunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_persondelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_personatom = personatom_shop(kw.person_partner_membership, kw.INSERT)
#     bob_iowa_personatom = personatom_shop(kw.person_partner_membership, kw.INSERT)
#     yao_iowa_personatom = personatom_shop(kw.person_partner_membership, kw.INSERT)
#     yao_ohio_personatom = personatom_shop(kw.person_partner_membership, kw.INSERT)
#     sue_iowa_personatom.set_arg(kw.group_title, iowa_str)
#     bob_iowa_personatom.set_arg(kw.group_title, iowa_str)
#     yao_iowa_personatom.set_arg(kw.group_title, iowa_str)
#     yao_ohio_personatom.set_arg(kw.group_title, ohio_str)
#     sue_iowa_personatom.set_arg(kw.partner_name, exx.sue)
#     bob_iowa_personatom.set_arg(kw.partner_name, exx.bob)
#     yao_iowa_personatom.set_arg(kw.partner_name, exx.yao)
#     yao_ohio_personatom.set_arg(kw.partner_name, exx.yao)
#     sue_iowa_personatom.set_arg(kw.group_cred_lumen, sue_iowa_group_cred_lumen)
#     bob_iowa_personatom.set_arg(kw.group_cred_lumen, bob_iowa_group_cred_lumen)
#     yao_iowa_personatom.set_arg(kw.group_cred_lumen, yao_iowa_group_cred_lumen)
#     yao_ohio_personatom.set_arg(kw.group_cred_lumen, yao_ohio_group_cred_lumen)
#     sue_iowa_personatom.set_arg(kw.group_debt_lumen, sue_iowa_group_debt_lumen)
#     bob_iowa_personatom.set_arg(kw.group_debt_lumen, bob_iowa_group_debt_lumen)
#     yao_iowa_personatom.set_arg(kw.group_debt_lumen, yao_iowa_group_debt_lumen)
#     yao_ohio_personatom.set_arg(kw.group_debt_lumen, yao_ohio_group_debt_lumen)
#     bob_iowa_personatom.set_atom_order()
#     # print(f"{membership_changunit.get_ordered_personatoms()[2]=}")
#     # print(f"{sue_iowa_personatom=}")
#     assert len(membership_changunit.get_ordered_personatoms()) == 10
#     assert membership_changunit.get_ordered_personatoms()[0] == bob_iowa_personatom
#     assert membership_changunit.personatom_exists(sue_iowa_personatom)
#     assert membership_changunit.personatom_exists(bob_iowa_personatom)
#     assert membership_changunit.personatom_exists(yao_iowa_personatom)
#     assert membership_changunit.personatom_exists(yao_ohio_personatom)
#     assert len(membership_changunit.get_ordered_personatoms()) == 10


def test_make_persondelta_Arg_idea_format_00013_kegunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_personunit = personunit_shop(exx.sue, amy_moment_rope)
    casa_rope = sue_personunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_personunit.set_l1_keg(kegunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_personunit.make_rope(casa_rope, exx.clean)
    sue_personunit.set_keg_obj(kegunit_shop(exx.clean, pledge=True), casa_rope)
    x_idea_name = idea_format_00013_kegunit_v0_0_0()
    kegunit_dataframe = create_idea_df(sue_personunit, x_idea_name)
    kegunit_csv = kegunit_dataframe.to_csv(index=False)

    # WHEN
    kegunit_changunit = make_persondelta(kegunit_csv)

    # THEN
    casa_personatom = personatom_shop(kw.person_kegunit, kw.INSERT)
    casa_personatom.set_arg(kw.keg_rope, casa_rope)
    casa_personatom.set_arg(kw.pledge, False)
    casa_personatom.set_arg(kw.star, casa_star)
    print(f"{casa_personatom=}")
    assert casa_personatom.get_value(kw.star) == casa_star
    clean_personatom = personatom_shop(kw.person_kegunit, kw.INSERT)
    clean_personatom.set_arg(kw.keg_rope, clean_rope)
    clean_personatom.set_arg(kw.pledge, True)
    clean_personatom.set_arg(kw.star, 1)
    assert kegunit_changunit.c_personatom_exists(casa_personatom)
    assert kegunit_changunit.c_personatom_exists(clean_personatom)
    assert len(kegunit_changunit.get_ordered_personatoms()) == 2


def test_create_idea_df_Arg_idea_format_00013_kegunit_v0_0_0_Scenario_personunit_v001(
    run_big_tests,
):
    # sourcery skip: no-conditionals-in-tests
    if run_big_tests:
        # ESTABLISH / WHEN
        x_idea_name = idea_format_00013_kegunit_v0_0_0()

        # WHEN
        kegunit_format = create_idea_df(personunit_v001(), x_idea_name)

        # THEN
        array_headers = list(kegunit_format.columns)
        assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
        assert len(kegunit_format) == 251
