from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    required_columns_exist,
)
from src.ch08_belief_atom.atom_config import get_delete_key_name
from src.ch17_idea.idea_config import (
    get_filtered_idea_config,
    get_idea_config_dict,
    get_idea_numbers,
    get_idea_sqlite_types,
)
from src.ch17_idea.idea_db_tool import (
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ch18_world_etl.etl_table import (
    ALL_DIMEN_ABBV7,
    create_prime_tablename,
    get_all_dimen_columns_set,
)
from src.ref.keywords import Ch18Keywords as kw


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())
    x_set = {len(dimen) for dimen in ALL_DIMEN_ABBV7}
    assert x_set == {7}


def test_create_prime_tablename_ReturnsObj_Scenario0_ExpectedReturns():
    # ESTABLISH
    blfunit_dimen = kw.beliefunit
    blfvoce_dimen = kw.belief_voiceunit
    blfmemb_dimen = kw.belief_voice_membership
    blfgrou_dimen = kw.belief_groupunit
    blfplan_dimen = kw.belief_planunit
    blfawar_dimen = kw.belief_plan_awardunit
    blfreas_dimen = kw.belief_plan_reasonunit
    blfcase_dimen = kw.belief_plan_reason_caseunit
    blflabo_dimen = kw.belief_plan_partyunit
    blfheal_dimen = kw.belief_plan_healerunit
    blffact_dimen = kw.belief_plan_factunit
    mmtunit_dimen = kw.momentunit
    mmtpayy_dimen = kw.moment_paybook
    mmtbudd_dimen = kw.moment_budunit
    mmthour_dimen = kw.moment_epoch_hour
    mmtmont_dimen = kw.moment_epoch_month
    mmtweek_dimen = kw.moment_epoch_weekday
    mmtoffi_dimen = kw.moment_timeoffi
    nabepoc_dimen = kw.nabu_epochtime
    trlname_dimen = kw.translate_name
    trllabe_dimen = kw.translate_label
    trlrope_dimen = kw.translate_rope
    trltitl_dimen = kw.translate_title
    trlcore_dimen = kw.translate_core
    raw_str = "raw"
    agg_str = "agg"
    vld_str = "vld"
    put_str = "put"
    del_str = "del"

    # WHEN
    blfunit_s_agg_table = create_prime_tablename("beliefunit", "s", agg_str, put_str)
    blfvoce_s_agg_table = create_prime_tablename("blfvoce", "s", agg_str, put_str)
    blfmemb_s_agg_table = create_prime_tablename("blfmemb", "s", agg_str, put_str)
    blfplan_s_agg_table = create_prime_tablename("blfplan", "s", agg_str, put_str)
    blfawar_s_agg_table = create_prime_tablename("blfawar", "s", agg_str, put_str)
    blfreas_s_agg_table = create_prime_tablename("blfreas", "s", agg_str, put_str)
    blfcase_s_agg_table = create_prime_tablename("blfcase", "s", agg_str, put_str)
    blflabo_s_agg_table = create_prime_tablename("blflabo", "s", agg_str, put_str)
    blfheal_s_agg_table = create_prime_tablename("blfheal", "s", agg_str, put_str)
    blffact_s_agg_table = create_prime_tablename("blffact", "s", agg_str, put_str)
    blffact_s_del_table = create_prime_tablename("blffact", "s", agg_str, del_str)
    mmtunit_s_agg_table = create_prime_tablename("mmtunit", "s", agg_str)
    mmtpayy_s_agg_table = create_prime_tablename("mmtpayy", "s", agg_str)
    mmtbudd_s_agg_table = create_prime_tablename("mmtbudd", "s", agg_str)
    mmthour_s_agg_table = create_prime_tablename("mmthour", "s", agg_str)
    mmtmont_s_agg_table = create_prime_tablename("mmtmont", "s", agg_str)
    mmtweek_s_agg_table = create_prime_tablename("mmtweek", "s", agg_str)
    mmtoffi_s_agg_table = create_prime_tablename("mmtoffi", "s", agg_str)
    nabepoc_s_agg_table = create_prime_tablename("nabepoc", "s", agg_str)
    trlname_s_agg_table = create_prime_tablename("trlname", "s", agg_str)
    trllabe_s_agg_table = create_prime_tablename("trllabe", "s", agg_str)
    trlrope_s_agg_table = create_prime_tablename("trlrope", "s", agg_str)
    trltitl_s_agg_table = create_prime_tablename("trltitl", "s", agg_str)
    trltitl_h_vld_table = create_prime_tablename("trltitl", "h", vld_str)
    trltitl_s_raw_table = create_prime_tablename("trltitl", "s", raw_str)
    trltitl_s_val_table = create_prime_tablename("trltitl", "s", vld_str)
    trlcore_s_raw_table = create_prime_tablename("trlcore", "s", raw_str)
    trlcore_s_agg_table = create_prime_tablename("trlcore", "s", agg_str)
    blfvoce_job_table = create_prime_tablename("blfvoce", kw.job, None)
    x_blfvoce_raw = create_prime_tablename("blfvoce", "k", raw_str)
    blfgrou_job_table = create_prime_tablename("blfgrou", kw.job, None)

    # THEN
    assert blfunit_s_agg_table == f"{blfunit_dimen}_s_put_agg"
    assert blfvoce_s_agg_table == f"{blfvoce_dimen}_s_put_agg"
    assert blfmemb_s_agg_table == f"{blfmemb_dimen}_s_put_agg"
    assert blfplan_s_agg_table == f"{blfplan_dimen}_s_put_agg"
    assert blfawar_s_agg_table == f"{blfawar_dimen}_s_put_agg"
    assert blfreas_s_agg_table == f"{blfreas_dimen}_s_put_agg"
    assert blfcase_s_agg_table == f"{blfcase_dimen}_s_put_agg"
    assert blflabo_s_agg_table == f"{blflabo_dimen}_s_put_agg"
    assert blfheal_s_agg_table == f"{blfheal_dimen}_s_put_agg"
    assert blffact_s_agg_table == f"{blffact_dimen}_s_put_agg"
    assert blffact_s_del_table == f"{blffact_dimen}_s_del_agg"
    assert mmtunit_s_agg_table == f"{mmtunit_dimen}_s_agg"
    assert mmtpayy_s_agg_table == f"{mmtpayy_dimen}_s_agg"
    assert mmtbudd_s_agg_table == f"{mmtbudd_dimen}_s_agg"
    assert mmthour_s_agg_table == f"{mmthour_dimen}_s_agg"
    assert mmtmont_s_agg_table == f"{mmtmont_dimen}_s_agg"
    assert mmtweek_s_agg_table == f"{mmtweek_dimen}_s_agg"
    assert mmtoffi_s_agg_table == f"{mmtoffi_dimen}_s_agg"
    assert nabepoc_s_agg_table == f"{nabepoc_dimen}_s_agg"
    assert trlname_s_agg_table == f"{trlname_dimen}_s_agg"
    assert trllabe_s_agg_table == f"{trllabe_dimen}_s_agg"
    assert trlrope_s_agg_table == f"{trlrope_dimen}_s_agg"
    assert trltitl_s_agg_table == f"{trltitl_dimen}_s_agg"
    assert trltitl_h_vld_table == f"{trltitl_dimen}_h_vld"
    assert trltitl_s_raw_table == f"{trltitl_dimen}_s_raw"
    assert trltitl_s_val_table == f"{trltitl_dimen}_s_vld"
    assert trlcore_s_raw_table == f"{trlcore_dimen}_s_raw"
    assert trlcore_s_agg_table == f"{trlcore_dimen}_s_agg"
    assert blfvoce_job_table == f"{blfvoce_dimen}_job"
    assert blfgrou_job_table == f"{blfgrou_dimen}_job"
    assert x_blfvoce_raw == "belief_voiceunit_raw"


def test_get_all_dimen_columns_set_ReturnsObj_Scenario0_idea_config_Dimens():
    # ESTABLISH
    for x_dimen in get_idea_config_dict().keys():
        # WHEN
        dimen_columns = get_all_dimen_columns_set(x_dimen)

        # THEN
        dimen_idea_config = get_idea_config_dict().get(x_dimen)
        expected_columns = set(dimen_idea_config.get(kw.jkeys).keys())
        expected_columns.update(set(dimen_idea_config.get(kw.jvalues).keys()))
        assert dimen_columns == expected_columns


def test_get_all_dimen_columns_set_ReturnsObj_Scenario1_translate_core_Dimens():
    # ESTABLISH / WHEN
    translate_core_columns = get_all_dimen_columns_set(kw.translate_core)

    # THEN
    expected_columns = {kw.face_name, kw.otx_knot, kw.inx_knot, kw.unknown_str}
    assert translate_core_columns == expected_columns


# TODO create tests for these functions
# def get_del_dimen_columns_set(x_dimen: str) -> list[str]:
# def create_translate_sound_raw_table_sqlstr(x_dimen):
# def create_translate_sound_agg_table_sqlstr(x_dimen):
# def create_translate_sound_vld_table_sqlstr(x_dimen):
# def create_translate_core_raw_table_sqlstr(x_dimen):
# def create_moment_sound_agg_table_sqlstr(x_dimen):
# def create_moment_sound_vld_table_sqlstr(x_dimen):
# def create_moment_heard_raw_table_sqlstr(x_dimen):
# def create_moment_heard_vld_table_sqlstr(x_dimen: str):
# def create_prime_table_sqlstr(x_dimen: str) -> str:
