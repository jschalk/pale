from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_row_count, get_table_columns
from src.ch18_world_etl.etl_main import etl_sound_vld_tables_to_heard_raw_tables
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_insert_into_heard_raw_sqlstrs,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_insert_into_heard_raw_sqlstrs_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    yao_inx = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        planavoice_s_vld_put_tablename = prime_tbl(kw.plan_voiceunit, "s", "vld", "put")
        print(f"{get_table_columns(cursor, planavoice_s_vld_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {planavoice_s_vld_put_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.plan_name}
, {kw.voice_name}
, {kw.voice_cred_lumen}
, {kw.voice_debt_lumen}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, planavoice_s_vld_put_tablename) == 4
        blfawar_h_raw_put_tablename = prime_tbl(kw.plan_voiceunit, "h", "raw", "put")
        assert get_row_count(cursor, blfawar_h_raw_put_tablename) == 0

        # WHEN
        sqlstr = get_insert_into_heard_raw_sqlstrs().get(blfawar_h_raw_put_tablename)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, blfawar_h_raw_put_tablename) == 4
        select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}_otx
, {kw.moment_label}_otx
, {kw.plan_name}_otx
, {kw.voice_name}_otx
, {kw.voice_cred_lumen}
, {kw.voice_debt_lumen}
FROM {blfawar_h_raw_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
            (2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
        ]


def test_etl_sound_vld_tables_to_heard_raw_tables_Scenario0_AddRowsToTable():
    # ESTABLISH
    yao_inx = "Yaoito"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blfvoce_s_vld_put_tablename = prime_tbl(kw.plan_voiceunit, "s", "vld", "put")
        print(f"{get_table_columns(cursor, blfvoce_s_vld_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {blfvoce_s_vld_put_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.plan_name}
, {kw.voice_name}
, {kw.voice_cred_lumen}
, {kw.voice_debt_lumen}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, blfvoce_s_vld_put_tablename) == 4
        blfvoce_h_raw_put_tablename = prime_tbl(kw.plan_voiceunit, "h", "raw", "put")
        assert get_row_count(cursor, blfvoce_h_raw_put_tablename) == 0

        # WHEN
        etl_sound_vld_tables_to_heard_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, blfvoce_h_raw_put_tablename) == 4
        select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}_otx
, {kw.moment_label}_otx
, {kw.plan_name}_otx
, {kw.voice_name}_otx
, {kw.voice_cred_lumen}
, {kw.voice_debt_lumen}
FROM {blfvoce_h_raw_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
            (2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
        ]


def test_etl_sound_vld_tables_to_heard_raw_tables_Scenario1_Populates_inx_Columns():
    # ESTABLISH
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blfvoce_s_vld_put_tablename = prime_tbl(kw.plan_voiceunit, "s", "vld", "put")
        print(f"{get_table_columns(cursor, blfvoce_s_vld_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {blfvoce_s_vld_put_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.plan_name}
, {kw.voice_name}
, {kw.voice_cred_lumen}
, {kw.voice_debt_lumen}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{exx.yao}', {x44_credit}, {x22_debt})
, ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
, ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, blfvoce_s_vld_put_tablename) == 4
        blfvoce_h_raw_put_tablename = prime_tbl(kw.plan_voiceunit, "h", "raw", "put")
        assert get_row_count(cursor, blfvoce_h_raw_put_tablename) == 0

        # WHEN
        etl_sound_vld_tables_to_heard_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, blfvoce_h_raw_put_tablename) == 4
        select_sqlstr = f"""SELECT {kw.spark_num}
, {kw.face_name}_inx
, {kw.moment_label}_inx
, {kw.plan_name}_inx
, {kw.voice_name}_inx
, {kw.voice_cred_lumen}
, {kw.voice_debt_lumen}
FROM {blfvoce_h_raw_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, exx.sue, exx.a23, exx.yao, exx.yao, 44.0, 22.0),
            (2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
            (7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
        ]
