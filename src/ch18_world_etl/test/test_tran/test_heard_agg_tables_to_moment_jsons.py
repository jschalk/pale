from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import create_select_query, db_table_exists, get_row_count
from src.ch01_py.file_toolbox import open_json
from src.ch09_belief_lesson._ref.ch09_path import create_moment_json_path
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch14_moment.moment_main import get_momentunit_from_dict
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.tran_sqlstrs import (
    create_prime_tablename,
    get_dimen_abbv7,
    get_moment_heard_select1_sqlstrs,
)
from src.ch18_world_etl.transformers import (
    create_sound_and_heard_tables,
    etl_heard_agg_tables_to_moment_jsons,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_moment_heard_select1_sqlstrs_ReturnsObj_HasAllKeys():
    # ESTABLISH

    # WHEN
    fu2_select_sqlstrs = get_moment_heard_select1_sqlstrs(exx.a23)

    # THEN
    assert fu2_select_sqlstrs
    expected_fu2_select_dimens = set(get_moment_dimens())
    assert set(fu2_select_sqlstrs.keys()) == expected_fu2_select_dimens


def test_get_moment_heard_select1_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH

    # WHEN
    fu2_select_sqlstrs = get_moment_heard_select1_sqlstrs(moment_label=exx.a23)

    # THEN
    gen_mmtpayy_sqlstr = fu2_select_sqlstrs.get(kw.moment_paybook)
    gen_momentbud_sqlstr = fu2_select_sqlstrs.get(kw.moment_budunit)
    gen_mmthour_sqlstr = fu2_select_sqlstrs.get(kw.moment_epoch_hour)
    gen_mmtmont_sqlstr = fu2_select_sqlstrs.get(kw.moment_epoch_month)
    gen_mmtweek_sqlstr = fu2_select_sqlstrs.get(kw.moment_epoch_weekday)
    gen_mmtoffi_sqlstr = fu2_select_sqlstrs.get(kw.moment_timeoffi)
    gen_momentunit_sqlstr = fu2_select_sqlstrs.get(kw.momentunit)
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        mmtpayy_abbv7 = get_dimen_abbv7(kw.moment_paybook)
        momentbud_abbv7 = get_dimen_abbv7(kw.moment_budunit)
        mmthour_abbv7 = get_dimen_abbv7(kw.moment_epoch_hour)
        mmtmont_abbv7 = get_dimen_abbv7(kw.moment_epoch_month)
        mmtweek_abbv7 = get_dimen_abbv7(kw.moment_epoch_weekday)
        mmtoffi_abbv7 = get_dimen_abbv7(kw.moment_timeoffi)
        momentunit_abbv7 = get_dimen_abbv7(kw.momentunit)
        mmtpayy_h_agg = create_prime_tablename(mmtpayy_abbv7, "h", "agg")
        momentbud_h_agg = create_prime_tablename(momentbud_abbv7, "h", "agg")
        mmthour_h_agg = create_prime_tablename(mmthour_abbv7, "h", "agg")
        mmtmont_h_agg = create_prime_tablename(mmtmont_abbv7, "h", "agg")
        mmtweek_h_agg = create_prime_tablename(mmtweek_abbv7, "h", "agg")
        mmtoffi_h_agg = create_prime_tablename(mmtoffi_abbv7, "h", "agg")
        momentunit_h_agg = create_prime_tablename(momentunit_abbv7, "h", "agg")
        where_dict = {kw.moment_label: exx.a23}
        mmtpayy_sql = create_select_query(cursor, mmtpayy_h_agg, [], where_dict, True)
        momentbud_sql = create_select_query(
            cursor, momentbud_h_agg, [], where_dict, True
        )
        mmthour_sql = create_select_query(cursor, mmthour_h_agg, [], where_dict, True)
        mmtmont_sql = create_select_query(cursor, mmtmont_h_agg, [], where_dict, True)
        mmtweek_sql = create_select_query(cursor, mmtweek_h_agg, [], where_dict, True)
        mmtoffi_sql = create_select_query(cursor, mmtoffi_h_agg, [], where_dict, True)
        momentunit_sql = create_select_query(
            cursor, momentunit_h_agg, [], where_dict, True
        )
        mmtpayy_sqlstr_ref = f"{mmtpayy_abbv7.upper()}_FU2_SELECT_SQLSTR"
        momentbud_sqlstr_ref = f"{momentbud_abbv7.upper()}_FU2_SELECT_SQLSTR"
        mmthour_sqlstr_ref = f"{mmthour_abbv7.upper()}_FU2_SELECT_SQLSTR"
        mmtmont_sqlstr_ref = f"{mmtmont_abbv7.upper()}_FU2_SELECT_SQLSTR"
        mmtweek_sqlstr_ref = f"{mmtweek_abbv7.upper()}_FU2_SELECT_SQLSTR"
        mmtoffi_sqlstr_ref = f"{mmtoffi_abbv7.upper()}_FU2_SELECT_SQLSTR"
        momentunit_sqlstr_ref = f"{momentunit_abbv7.upper()}_FU2_SELECT_SQLSTR"
        qa23_str = "'amy23'"
        blank = ""
        print(f"""{mmtpayy_sqlstr_ref} = "{mmtpayy_sql.replace(qa23_str, blank)}" """)
        print(
            f"""{momentbud_sqlstr_ref} = "{momentbud_sql.replace(qa23_str, blank)}" """
        )
        print(f"""{mmthour_sqlstr_ref} = "{mmthour_sql.replace(qa23_str, blank)}" """)
        print(f"""{mmtmont_sqlstr_ref} = "{mmtmont_sql.replace(qa23_str, blank)}" """)
        print(f"""{mmtweek_sqlstr_ref} = "{mmtweek_sql.replace(qa23_str, blank)}" """)
        print(f"""{mmtoffi_sqlstr_ref} = "{mmtoffi_sql.replace(qa23_str, blank)}" """)
        print(
            f"""{momentunit_sqlstr_ref} = "{momentunit_sql.replace(qa23_str, blank)}" """
        )
        assert gen_mmtpayy_sqlstr == mmtpayy_sql
        assert gen_momentbud_sqlstr == momentbud_sql
        assert gen_mmthour_sqlstr == mmthour_sql
        assert gen_mmtmont_sqlstr == mmtmont_sql
        assert gen_mmtweek_sqlstr == mmtweek_sql
        assert gen_mmtoffi_sqlstr == mmtoffi_sql
        assert gen_momentunit_sqlstr == momentunit_sql
        static_example_sqlstr = f"SELECT {kw.moment_label}, {kw.epoch_label}, {kw.c400_number}, {kw.yr1_jan1_offset}, {kw.monthday_index}, {kw.fund_grain}, {kw.mana_grain}, {kw.respect_grain}, {kw.knot}, {kw.job_listen_rotations} FROM momentunit_h_agg WHERE moment_label = '{exx.a23}'"
        assert gen_momentunit_sqlstr == static_example_sqlstr


def test_etl_heard_agg_tables_to_moment_jsons_Scenario0_CreateFilesWithOnlyMomentLabel(
    temp_dir_setup,
):
    # ESTABLISH
    amy45_str = "amy45"
    moment_mstr_dir = get_temp_dir()
    momentunit_h_agg_tablename = create_prime_tablename(kw.momentunit, "h", "agg")
    print(f"{momentunit_h_agg_tablename=}")

    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {momentunit_h_agg_tablename} ({kw.moment_label})
VALUES ('{exx.a23}'), ('{amy45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, momentunit_h_agg_tablename) == 2

        amy23_json_path = create_moment_json_path(moment_mstr_dir, exx.a23)
        amy45_json_path = create_moment_json_path(moment_mstr_dir, amy45_str)
        print(f"{amy23_json_path=}")
        print(f"{amy45_json_path=}")
        assert os_path_exists(amy23_json_path) is False
        assert os_path_exists(amy45_json_path) is False

        # WHEN
        etl_heard_agg_tables_to_moment_jsons(cursor, moment_mstr_dir)

    # THEN
    assert os_path_exists(amy23_json_path)
    assert os_path_exists(amy45_json_path)
    amy23_moment = get_momentunit_from_dict(open_json(amy23_json_path))
    amy45_moment = get_momentunit_from_dict(open_json(amy45_json_path))
    assert amy23_moment.moment_label == exx.a23
    assert amy45_moment.moment_label == amy45_str
