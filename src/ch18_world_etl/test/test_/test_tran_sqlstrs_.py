from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    required_columns_exist,
)
from src.ch08_belief_atom.atom_config import get_delete_key_name
from src.ch17_idea.idea_config import (
    get_idea_config_dict,
    get_idea_numbers,
    get_idea_sqlite_types,
)
from src.ch17_idea.idea_db_tool import (
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.ch18_world_etl.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    IDEA_STAGEBLE_DEL_DIMENS,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    create_all_idea_tables,
    create_prime_tablename,
    create_sound_and_heard_tables,
    get_idea_stageble_put_dimens,
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
    nbuepch_dimen = "nabu_epochtime"
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
    blflabo_s_agg_table = create_prime_tablename("BLFLABO", "s", agg_str, put_str)
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
    nbuepch_s_agg_table = create_prime_tablename("nbuepch", "s", agg_str)
    trlname_s_agg_table = create_prime_tablename("trlname", "s", agg_str)
    trllabe_s_agg_table = create_prime_tablename("trllabe", "s", agg_str)
    trlrope_s_agg_table = create_prime_tablename("trlrope", "s", agg_str)
    trltitl_s_agg_table = create_prime_tablename("trltitl", "s", agg_str)
    trltitl_h_agg_table = create_prime_tablename("trltitl", "h", agg_str)
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
    assert nbuepch_s_agg_table == f"{nbuepch_dimen}_s_agg"
    assert trlname_s_agg_table == f"{trlname_dimen}_s_agg"
    assert trllabe_s_agg_table == f"{trllabe_dimen}_s_agg"
    assert trlrope_s_agg_table == f"{trlrope_dimen}_s_agg"
    assert trltitl_s_agg_table == f"{trltitl_dimen}_s_agg"
    assert trltitl_h_agg_table == f"{trltitl_dimen}_h_agg"
    assert trltitl_s_raw_table == f"{trltitl_dimen}_s_raw"
    assert trltitl_s_val_table == f"{trltitl_dimen}_s_vld"
    assert trlcore_s_raw_table == f"{trlcore_dimen}_s_raw"
    assert trlcore_s_agg_table == f"{trlcore_dimen}_s_agg"
    assert blfvoce_job_table == f"{blfvoce_dimen}_job"
    assert blfgrou_job_table == f"{blfgrou_dimen}_job"
    assert x_blfvoce_raw == "belief_voiceunit_raw"


def test_create_all_idea_tables_CreatesMomentRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        for idea_number in idea_numbers:
            assert db_table_exists(cursor, f"{idea_number}_raw") is False

        # WHEN
        create_all_idea_tables(cursor)

        # THEN
        for idea_number in idea_numbers:
            print(f"{idea_number} checking...")
            assert db_table_exists(cursor, f"{idea_number}_raw")


def test_get_idea_stageble_put_dimens_HasAll_idea_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(kw.idea_category) != kw.translate
        # if dimen_config.get(kw.idea_category) == "moment"
    }
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_sound_and_heard_tables(cursor)

        idea_raw2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        expected_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get(kw.jkeys).keys())
            dimen_value_columns = set(dimen_config.get(kw.jvalues).keys())
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_raw")
                expected_stagable = dimen_key_columns.issubset(src_columns)
                if idea_number == "br00036":
                    print(f"{x_dimen} {idea_number} checking... {src_columns}")
                src_tablename = f"{idea_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_stagable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    expected_idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    existing_value_col = src_cols_set & (dimen_value_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    # print(
                    #     f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
                    # )
                    generated_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""

    idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
    print(expected_idea_stagable_dimens)
    assert idea_dimen_combo_checked_count == 738
    assert idea_raw2dimen_count == 111
    assert get_idea_stageble_put_dimens() == expected_idea_stagable_dimens


def test_IDEA_STAGEBLE_DEL_DIMENS_HasAll_idea_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(kw.idea_category) != kw.translate
        # if dimen_config.get(kw.idea_category) == "moment"
    }
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_sound_and_heard_tables(cursor)

        idea_raw2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        x_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get(kw.jkeys).keys())
            dimen_key_columns = get_default_sorted_list(dimen_key_columns)
            dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
            dimen_key_columns = set(dimen_key_columns)
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_raw")
                expected_stagable = dimen_key_columns.issubset(src_columns)
                src_tablename = f"{idea_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_stagable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    x_idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    print(
                        f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}"
                    )
                    generated_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""
    expected_idea_stagable_dimens = {
        x_idea_number: stagable_dimens
        for x_idea_number, stagable_dimens in x_idea_stagable_dimens.items()
        if stagable_dimens != []
    }
    idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
    print(f"{expected_idea_stagable_dimens=}")
    assert idea_dimen_combo_checked_count == 738
    assert idea_raw2dimen_count == 10
    assert IDEA_STAGEBLE_DEL_DIMENS == expected_idea_stagable_dimens


def test_CREATE_MOMENT_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS {kw.moment_ote1_agg} (
  {kw.moment_label} TEXT
, {kw.belief_name} TEXT
, {kw.spark_num} INTEGER
, {kw.bud_time} INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_MOMENT_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# TODO create test to prove this insert should grab minimun spark_num instead of just spark_num
# TODO create test to prove this insert should never grab when error message is not null in source table
def test_INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR_Exists():
    # ESTABLISH
    momentbud_h_raw_tablename = create_prime_tablename(kw.moment_budunit, "h", "raw")
    expected_INSERT_sqlstr = f"""
INSERT INTO {kw.moment_ote1_agg} ({kw.moment_label}, {kw.belief_name}, {kw.spark_num}, {kw.bud_time})
SELECT {kw.moment_label}, {kw.belief_name}, {kw.spark_num}, {kw.bud_time}
FROM (
    SELECT 
      {kw.moment_label}_inx {kw.moment_label}
    , {kw.belief_name}_inx {kw.belief_name}
    , {kw.spark_num}
    , {kw.bud_time}
    FROM {momentbud_h_raw_tablename}
    GROUP BY {kw.moment_label}_inx, {kw.belief_name}_inx, {kw.spark_num}, {kw.bud_time}
)
ORDER BY {kw.moment_label}, {kw.belief_name}, {kw.spark_num}, {kw.bud_time}
;
"""
    # WHEN / THEN
    assert INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR == expected_INSERT_sqlstr


def test_CREATE_MOMENT_VOICE_NETS_SQLSTR_Exists():
    # ESTABLISH
    sqlite_types = get_idea_sqlite_types()
    sqlite_types[kw.belief_net_amount] = "REAL"
    expected_create_table_sqlstr = get_create_table_sqlstr(
        tablename=kw.moment_voice_nets,
        columns_list=[
            kw.moment_label,
            kw.belief_name,
            kw.belief_net_amount,
        ],
        column_types=sqlite_types,
    )

    # WHEN / THEN
    assert CREATE_MOMENT_VOICE_NETS_SQLSTR == expected_create_table_sqlstr
