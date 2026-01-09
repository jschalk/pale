from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import planunit_v001
from src.ch08_plan_atom.atom_main import planatom_shop
from src.ch17_idea.idea_config import (
    idea_format_00013_kegunit_v0_0_0,
    idea_format_00021_plan_voiceunit_v0_0_0,
)
from src.ch17_idea.idea_main import create_idea_df, get_idearef_obj, make_plandelta
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_make_plandelta_Arg_idea_format_00021_plan_voiceunit_v0_0_0():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_voice_cred_lumen = 11
    bob_voice_cred_lumen = 13
    yao_voice_cred_lumen = 41
    sue_voice_debt_lumen = 23
    bob_voice_debt_lumen = 29
    yao_voice_debt_lumen = 37
    amy_moment_label = "amy56"
    sue_planunit = planunit_shop(exx.sue, amy_moment_label)
    sue_planunit.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    sue_planunit.add_voiceunit(exx.bob, bob_voice_cred_lumen, bob_voice_debt_lumen)
    sue_planunit.add_voiceunit(exx.yao, yao_voice_cred_lumen, yao_voice_debt_lumen)
    x_idea_name = idea_format_00021_plan_voiceunit_v0_0_0()
    voice_dataframe = create_idea_df(sue_planunit, x_idea_name)
    print(f"{voice_dataframe.columns=}")
    voice_csv = voice_dataframe.to_csv(index=False)

    # WHEN
    sue_voice_plandelta = make_plandelta(voice_csv)

    # THEN
    assert sue_voice_plandelta
    sue_planatom = planatom_shop(kw.plan_voiceunit, kw.INSERT)
    sue_planatom.set_arg(kw.voice_name, exx.sue)
    sue_planatom.set_arg(kw.voice_cred_lumen, sue_voice_cred_lumen)
    sue_planatom.set_arg(kw.voice_debt_lumen, sue_voice_debt_lumen)
    sue_planatom.set_atom_order()
    bob_planatom = planatom_shop(kw.plan_voiceunit, kw.INSERT)
    bob_planatom.set_arg(kw.voice_name, exx.bob)
    bob_planatom.set_arg(kw.voice_cred_lumen, bob_voice_cred_lumen)
    bob_planatom.set_arg(kw.voice_debt_lumen, bob_voice_debt_lumen)
    bob_planatom.set_atom_order()
    # print(f"{sue_voice_plandelta.get_ordered_dict()=}")
    # print(
    #     f"{sue_voice_plandelta.planatoms.get(kw.INSERT).get(kw.plan_voiceunit).get(exx.sue)=}"
    # )
    print(f"{sue_planatom=}")
    assert sue_voice_plandelta.c_planatom_exists(sue_planatom)
    assert sue_voice_plandelta.c_planatom_exists(bob_planatom)
    assert len(sue_voice_plandelta.get_ordered_planatoms()) == 3


# def test_make_plandelta_Arg_idea_format_00020_plan_voice_membership_v0_0_0():
#     # ESTABLISH
#     exx.bob = "Bob"
#     exx.yao = "Yao"
#     amy_moment_label = "amy56"
#     sue_planunit = planunit_shop(exx.sue, amy_moment_label)
#     sue_planunit.add_voiceunit(exx.sue)
#     sue_planunit.add_voiceunit(exx.bob)
#     sue_planunit.add_voiceunit(exx.yao)
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
#     sue_voiceunit = sue_planunit.get_voice(exx.sue)
#     bob_voiceunit = sue_planunit.get_voice(exx.bob)
#     yao_voiceunit = sue_planunit.get_voice(exx.yao)
#     sue_voiceunit.add_membership(iowa_str, sue_iowa_group_cred_lumen, sue_iowa_group_debt_lumen)
#     bob_voiceunit.add_membership(iowa_str, bob_iowa_group_cred_lumen, bob_iowa_group_debt_lumen)
#     yao_voiceunit.add_membership(iowa_str, yao_iowa_group_cred_lumen, yao_iowa_group_debt_lumen)
#     yao_voiceunit.add_membership(ohio_str, yao_ohio_group_cred_lumen, yao_ohio_group_debt_lumen)
#     x_idea_name = idea_format_00020_plan_voice_membership_v0_0_0()
#     membership_dataframe = create_idea_df(sue_planunit, x_idea_name)
#     assert len(membership_dataframe) == 10
#     print(membership_dataframe)
#     membership_csv = membership_dataframe.to_csv(index=False)
#     print(f"{membership_csv=}")

#     # WHEN
#       membership_changunit = make_plandelta(membership_csv)

#     # THEN
#     assert membership_changunit
#     sue_iowa_planatom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
#     bob_iowa_planatom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
#     yao_iowa_planatom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
#     yao_ohio_planatom = planatom_shop(kw.plan_voice_membership, kw.INSERT)
#     sue_iowa_planatom.set_arg(kw.group_title, iowa_str)
#     bob_iowa_planatom.set_arg(kw.group_title, iowa_str)
#     yao_iowa_planatom.set_arg(kw.group_title, iowa_str)
#     yao_ohio_planatom.set_arg(kw.group_title, ohio_str)
#     sue_iowa_planatom.set_arg(kw.voice_name, exx.sue)
#     bob_iowa_planatom.set_arg(kw.voice_name, exx.bob)
#     yao_iowa_planatom.set_arg(kw.voice_name, exx.yao)
#     yao_ohio_planatom.set_arg(kw.voice_name, exx.yao)
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
