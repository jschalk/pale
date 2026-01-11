from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch17_idea.idea_config import idea_format_00021_plan_personunit_v0_0_0
from src.ch17_idea.idea_db_tool import open_csv
from src.ch17_idea.idea_main import get_idearef_obj, save_idea_csv
from src.ch17_idea.test._util.ch17_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_open_csv_ReturnsObjWhenFileExists(temp_dir_setup):
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
    j1_ideaname = idea_format_00021_plan_personunit_v0_0_0()
    name_filename = f"{exx.sue}_person_example_01.csv"
    save_idea_csv(j1_ideaname, sue_planunit, get_temp_dir(), name_filename)

    # WHEN
    person_dataframe = open_csv(get_temp_dir(), name_filename)

    # THEN
    array_headers = list(person_dataframe.columns)
    person_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == person_idearef.get_headers_list()
    assert person_dataframe.loc[0, kw.moment_label] == amy_moment_label
    assert person_dataframe.loc[0, kw.plan_name] == sue_planunit.plan_name
    assert person_dataframe.loc[0, kw.person_name] == exx.bob
    assert person_dataframe.loc[0, kw.person_cred_lumen] == bob_person_cred_lumen
    assert person_dataframe.loc[0, kw.person_debt_lumen] == bob_person_debt_lumen

    assert person_dataframe.loc[1, kw.moment_label] == amy_moment_label
    assert person_dataframe.loc[1, kw.plan_name] == sue_planunit.plan_name
    assert person_dataframe.loc[1, kw.person_name] == exx.sue
    assert person_dataframe.loc[1, kw.person_cred_lumen] == sue_person_cred_lumen
    assert person_dataframe.loc[1, kw.person_debt_lumen] == sue_person_debt_lumen

    assert person_dataframe.loc[2, kw.moment_label] == amy_moment_label
    assert person_dataframe.loc[2, kw.plan_name] == sue_planunit.plan_name
    assert person_dataframe.loc[2, kw.person_name] == exx.yao
    assert person_dataframe.loc[2, kw.person_cred_lumen] == yao_person_cred_lumen
    assert person_dataframe.loc[2, kw.person_debt_lumen] == yao_person_debt_lumen

    assert len(person_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(temp_dir_setup):
    # ESTABLISH
    name_filename = f"{exx.sue}_person_example_77.csv"

    # WHEN
    person_dataframe = open_csv(get_temp_dir(), name_filename)

    # THEN
    assert person_dataframe is None
