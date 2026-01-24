from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch04_rope.rope import create_rope
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch13_time.test._util.ch13_examples import (
    add_time_creg_kegunit,
    add_time_five_kegunit,
)
from src.ch17_idea.idea_config import (
    idea_format_00013_kegunit_v0_0_0,
    idea_format_00019_kegunit_v0_0_0,
    idea_format_00020_plan_person_membership_v0_0_0,
    idea_format_00021_plan_personunit_v0_0_0,
)
from src.ch17_idea.idea_main import create_idea_df, get_idearef_obj, save_idea_csv
from src.ch17_idea.test._util.ch17_env import idea_moments_dir, temp_dir_setup
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_create_idea_df_Arg_idea_format_00021_plan_personunit_v0_0_0():
    # ESTABLISH
    sue_person_cred_lumen = 11
    bob_person_cred_lumen = 13
    yao_person_cred_lumen = 41
    sue_person_debt_lumen = 23
    bob_person_debt_lumen = 29
    yao_person_debt_lumen = 37
    amy_moment_rope = create_rope("amy56")
    sue_planunit = planunit_shop(exx.sue, amy_moment_rope)
    sue_planunit.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    sue_planunit.add_personunit(exx.bob, bob_person_cred_lumen, bob_person_debt_lumen)
    sue_planunit.add_personunit(exx.yao, yao_person_cred_lumen, yao_person_debt_lumen)

    # WHEN
    x_idea_name = idea_format_00021_plan_personunit_v0_0_0()
    person_dataframe = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(person_dataframe.columns)
    person_idearef = get_idearef_obj(x_idea_name)
    assert array_headers == person_idearef.get_headers_list()
    assert person_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert person_dataframe.loc[0, kw.plan_name] == sue_planunit.plan_name
    assert person_dataframe.loc[0, kw.person_name] == exx.bob
    assert person_dataframe.loc[0, kw.person_debt_lumen] == bob_person_debt_lumen
    assert person_dataframe.loc[0, kw.person_cred_lumen] == bob_person_cred_lumen

    assert person_dataframe.loc[1, kw.moment_rope] == amy_moment_rope
    assert person_dataframe.loc[1, kw.plan_name] == sue_planunit.plan_name
    assert person_dataframe.loc[1, kw.person_name] == exx.sue
    assert person_dataframe.loc[1, kw.person_debt_lumen] == sue_person_debt_lumen
    assert person_dataframe.loc[1, kw.person_cred_lumen] == sue_person_cred_lumen

    assert person_dataframe.loc[2, kw.moment_rope] == amy_moment_rope
    assert person_dataframe.loc[2, kw.plan_name] == sue_planunit.plan_name
    assert person_dataframe.loc[2, kw.person_name] == exx.yao
    assert person_dataframe.loc[2, kw.person_debt_lumen] == yao_person_debt_lumen
    assert person_dataframe.loc[2, kw.person_cred_lumen] == yao_person_cred_lumen

    assert len(person_dataframe) == 3


def test_create_idea_df_Arg_idea_format_00020_plan_person_membership_v0_0_0():
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_planunit = planunit_shop(exx.sue, amy_moment_rope)
    sue_planunit.add_personunit(exx.sue)
    sue_planunit.add_personunit(exx.bob)
    sue_planunit.add_personunit(exx.yao)
    iowa_str = ";Iowa"
    sue_iowa_credit_w = 37
    bob_iowa_credit_w = 43
    yao_iowa_credit_w = 51
    sue_iowa_debt_w = 57
    bob_iowa_debt_w = 61
    yao_iowa_debt_w = 67
    ohio_str = ";Ohio"
    yao_ohio_credit_w = 73
    yao_ohio_debt_w = 67
    sue_personunit = sue_planunit.get_person(exx.sue)
    bob_personunit = sue_planunit.get_person(exx.bob)
    yao_personunit = sue_planunit.get_person(exx.yao)
    sue_personunit.add_membership(iowa_str, sue_iowa_credit_w, sue_iowa_debt_w)
    bob_personunit.add_membership(iowa_str, bob_iowa_credit_w, bob_iowa_debt_w)
    yao_personunit.add_membership(iowa_str, yao_iowa_credit_w, yao_iowa_debt_w)
    yao_personunit.add_membership(ohio_str, yao_ohio_credit_w, yao_ohio_debt_w)

    # WHEN
    x_idea_name = idea_format_00020_plan_person_membership_v0_0_0()
    membership_dataframe = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(membership_dataframe.columns)
    person_idearef = get_idearef_obj(x_idea_name)
    print(f"{len(membership_dataframe)=}")
    assert len(membership_dataframe) == 10
    assert array_headers == person_idearef.get_headers_list()
    assert membership_dataframe.loc[0, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[0, kw.plan_name] == sue_planunit.plan_name
    assert membership_dataframe.loc[0, kw.person_name] == exx.bob
    assert membership_dataframe.loc[0, kw.group_title] == iowa_str
    assert membership_dataframe.loc[0, kw.group_cred_lumen] == bob_iowa_credit_w
    assert membership_dataframe.loc[0, kw.group_debt_lumen] == bob_iowa_debt_w

    assert membership_dataframe.loc[3, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[3, kw.plan_name] == sue_planunit.plan_name
    assert membership_dataframe.loc[3, kw.person_name] == exx.sue
    assert membership_dataframe.loc[3, kw.group_title] == iowa_str
    assert membership_dataframe.loc[3, kw.group_cred_lumen] == sue_iowa_credit_w
    assert membership_dataframe.loc[3, kw.group_debt_lumen] == sue_iowa_debt_w

    assert membership_dataframe.loc[4, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[4, kw.plan_name] == sue_planunit.plan_name
    assert membership_dataframe.loc[4, kw.person_name] == exx.sue
    assert membership_dataframe.loc[4, kw.group_title] == exx.sue
    assert membership_dataframe.loc[4, kw.group_cred_lumen] == 1
    assert membership_dataframe.loc[4, kw.group_debt_lumen] == 1

    assert membership_dataframe.loc[7, kw.moment_rope] == amy_moment_rope
    assert membership_dataframe.loc[7, kw.plan_name] == sue_planunit.plan_name
    assert membership_dataframe.loc[7, kw.person_name] == exx.yao
    assert membership_dataframe.loc[7, kw.group_title] == ohio_str
    assert membership_dataframe.loc[7, kw.group_cred_lumen] == yao_ohio_credit_w
    assert membership_dataframe.loc[7, kw.group_debt_lumen] == yao_ohio_debt_w
    assert len(membership_dataframe) == 10


def test_create_idea_df_Arg_idea_format_00013_kegunit_v0_0_0():
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_planunit = planunit_shop(exx.sue, amy_moment_rope)
    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_planunit.set_l1_keg(kegunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_planunit.make_rope(casa_rope, exx.clean)
    sue_planunit.set_keg_obj(kegunit_shop(exx.clean, pledge=True), casa_rope)

    # WHEN
    x_idea_name = idea_format_00013_kegunit_v0_0_0()
    kegunit_format = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(kegunit_format.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()

    assert kegunit_format.loc[0, kw.plan_name] == sue_planunit.plan_name
    assert kegunit_format.loc[0, kw.pledge] == ""
    assert kegunit_format.loc[0, kw.moment_rope] == amy_moment_rope
    assert kegunit_format.loc[0, kw.keg_rope] == casa_rope
    assert kegunit_format.loc[0, kw.star] == casa_star

    assert kegunit_format.loc[1, kw.plan_name] == sue_planunit.plan_name
    assert kegunit_format.loc[1, kw.pledge] == "Yes"
    assert kegunit_format.loc[1, kw.moment_rope] == amy_moment_rope
    assert kegunit_format.loc[1, kw.keg_rope] == clean_rope
    assert kegunit_format.loc[1, kw.star] == 1
    assert len(kegunit_format) == 2


def test_save_idea_csv_Arg_idea_format_00019_kegunit_v0_0_0():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue", create_rope("amy56"))
    sue_planunit = add_time_creg_kegunit(sue_planunit)
    sue_planunit = add_time_five_kegunit(sue_planunit)
    x_idea_name = idea_format_00019_kegunit_v0_0_0()

    # WHEN
    # name_filename = f"{exx.sue}_kegunit_example_00019.csv"
    # csv_example_path = create_path(idea_moments_dir(), name_filename)
    # save_idea_csv(x_idea_name, sue_planunit, get_temp_dir(), name_filename)
    idea_df = create_idea_df(sue_planunit, x_idea_name)

    # THEN
    array_headers = list(idea_df.columns)
    assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
    # for x_array_header in array_headers:
    #     print(f"{x_array_header=}")


def test_save_idea_csv_Arg_idea_format_00021_plan_personunit_v0_0_0_SaveToCSV(
    temp_dir_setup,
):
    # ESTABLISH
    sue_person_cred_lumen = 11
    bob_person_cred_lumen = 13
    yao_person_cred_lumen = 41
    sue_person_debt_lumen = 23
    bob_person_debt_lumen = 29
    yao_person_debt_lumen = 37
    amy_moment_rope = create_rope("amy56")
    sue_planunit = planunit_shop(exx.sue, amy_moment_rope)
    sue_planunit.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    sue_planunit.add_personunit(exx.bob, bob_person_cred_lumen, bob_person_debt_lumen)
    sue_planunit.add_personunit(exx.yao, yao_person_cred_lumen, yao_person_debt_lumen)
    j1_ideaname = idea_format_00021_plan_personunit_v0_0_0()
    name_filename = f"{exx.sue}_person_example_00.csv"
    csv_example_path = create_path(idea_moments_dir(), name_filename)
    print(f"{csv_example_path}")
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(j1_ideaname, sue_planunit, idea_moments_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue1_name_example_csv = """spark_num,face_name,moment_rope,plan_name,person_name,person_cred_lumen,person_debt_lumen
,,;amy56;,Sue,Bob,13,29
,,;amy56;,Sue,Sue,11,23
,,;amy56;,Sue,Yao,41,37
"""
    idea_file_str = open_file(idea_moments_dir(), name_filename)
    print(f"      {idea_file_str=}")
    print(f"{sue1_name_example_csv=}")
    assert idea_file_str == sue1_name_example_csv

    # WHEN
    sue_planunit.add_personunit(exx.zia)
    save_idea_csv(j1_ideaname, sue_planunit, idea_moments_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
    sue2_person_example_csv = """spark_num,face_name,moment_rope,plan_name,person_name,person_cred_lumen,person_debt_lumen
,,;amy56;,Sue,Bob,13,29
,,;amy56;,Sue,Sue,11,23
,,;amy56;,Sue,Yao,41,37
,,;amy56;,Sue,Zia,1,1
"""
    assert open_file(idea_moments_dir(), name_filename) == sue2_person_example_csv


def test_save_idea_csv_Arg_idea_format_00013_kegunit_v0_0_0(
    temp_dir_setup,
):
    # ESTABLISH
    amy_moment_rope = create_rope("amy56")
    sue_planunit = planunit_shop(exx.sue, amy_moment_rope)
    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    casa_star = 31
    sue_planunit.set_l1_keg(kegunit_shop(exx.casa, star=casa_star))
    clean_rope = sue_planunit.make_rope(casa_rope, exx.clean)
    sue_planunit.set_keg_obj(kegunit_shop(exx.clean, pledge=True), casa_rope)
    x_idea_name = idea_format_00013_kegunit_v0_0_0()
    kegunit_format = create_idea_df(sue_planunit, x_idea_name)
    name_filename = f"{exx.sue}_kegunit_example_000.csv"
    csv_example_path = create_path(idea_moments_dir(), name_filename)
    assert not os_path_exists(csv_example_path)

    # WHEN
    save_idea_csv(x_idea_name, sue_planunit, idea_moments_dir(), name_filename)

    # THEN
    assert os_path_exists(csv_example_path)
