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
from src.ch18_world_etl.etl_sqlstr import (
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    IDEA_STAGEBLE_DEL_DIMENS,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    create_all_idea_tables,
    create_sound_and_heard_tables,
    get_idea_stageble_put_dimens,
)
from src.ch18_world_etl.etl_table import create_prime_tablename
from src.ref.keywords import Ch18Keywords as kw


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
    idea_config = get_filtered_idea_config({kw.belief, kw.moment, kw.nabu})
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
    idea_config = get_filtered_idea_config({kw.belief, kw.moment, kw.nabu})
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
