from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_row_count, get_table_columns
from src.ch01_py.dict_toolbox import get_empty_set_if_None
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import get_default_sorted_list, get_idea_config_dict
from src.ch18_world_etl._ref.ch18_semantic_types import (
    BeliefName,
    EpochTime,
    FaceName,
    MomentLabel,
    SparkInt,
)
from src.ch18_world_etl.etl_sqlstr import create_sound_and_heard_tables
from src.ch18_world_etl.etl_table import create_prime_tablename as prime_tbl
from src.ch18_world_etl.test._util.ch18_examples import (
    insert_mmtoffi_special_offi_time_otx,
    insert_mmtunit_special_c400_number,
    insert_nabepoc_h_agg_otx_inx_time,
    select_mmtoffi_special_offi_time_inx,
    select_nabepoc_h_agg_otx_inx_time,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO create function that updates all nabuable otx fields.
# identify the change
#
# update semantic_type: ContextNum belief_plan_reason_caseunit_h_agg_put reason_lower, reason_upper
# update semantic_type: ContextNum belief_plan_factunit_h_agg_put fact_lower, fact_upper
# update semantic_type: EpochTime moment_paybook_h_agg tran_time
# update semantic_type: EpochTime moment_budunit_h_agg bud_time
# update semantic_type: EpochTime moment_timeh_agg time


def test_insert_nabepoc_h_agg_otx_inx_time_PopulatesTable_Scenario0():
    # ESTABLISH
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        nabepoc_h_agg_tablename = prime_tbl(kw.nabu_epochtime, "h", "agg")
        otx_time = 5
        inx_time = 8
        assert get_row_count(cursor, nabepoc_h_agg_tablename) == 0

        # WHEN
        insert_nabepoc_h_agg_otx_inx_time(
            cursor, spark1, exx.sue, exx.a23, otx_time, inx_time
        )

        # THEN
        assert get_row_count(cursor, nabepoc_h_agg_tablename) == 1
        select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.otx_time}
, {kw.inx_time}
FROM {nabepoc_h_agg_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [(spark1, exx.sue, exx.a23, otx_time, inx_time)]


def test_select_nabepoc_h_agg_otx_inx_time_PopulatesTable_Scenario0():
    # ESTABLISH
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        nabepoc_h_agg_tablename = prime_tbl(kw.nabu_epochtime, "h", "agg")
        otx_time = 5
        inx_time = 8
        assert not select_nabepoc_h_agg_otx_inx_time(cursor, spark1, exx.a23)

        # WHEN
        insert_nabepoc_h_agg_otx_inx_time(
            cursor, spark1, exx.sue, exx.a23, otx_time, inx_time
        )

        # THEN
        expected_rows = [(spark1, exx.a23, otx_time, inx_time)]
        gen_rows = select_nabepoc_h_agg_otx_inx_time(cursor, spark1, exx.a23)
        assert gen_rows == expected_rows


def test_insert_mmtunit_special_c400_number_PopulatesTable_Scenario0():
    # ESTABLISH
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
        x_c400_number = 5
        assert get_row_count(cursor, mmtunit_h_agg_tablename) == 0

        # WHEN
        insert_mmtunit_special_c400_number(
            cursor, spark1, exx.sue, exx.a23, x_c400_number
        )

        # THEN
        assert get_row_count(cursor, mmtunit_h_agg_tablename) == 1
        select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.c400_number}
FROM {mmtunit_h_agg_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [(spark1, exx.sue, exx.a23, x_c400_number)]


def test_insert_mmtoffi_special_offi_time_otx_PopulatesTable_Scenario0():
    # ESTABLISH
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
        x_offi_time_otx = 5
        assert get_row_count(cursor, mmtoffi_h_agg_tablename) == 0

        # WHEN
        insert_mmtoffi_special_offi_time_otx(
            cursor, spark1, exx.sue, exx.a23, x_offi_time_otx
        )

        # THEN
        assert get_row_count(cursor, mmtoffi_h_agg_tablename) == 1
        select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.offi_time}_otx
FROM {mmtoffi_h_agg_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [(spark1, exx.sue, exx.a23, x_offi_time_otx)]


def test_select_mmtoffi_special_offi_time_inx_PopulatesTable_Scenario0():
    # ESTABLISH
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
        x_offi_time_otx = 5
        assert not select_mmtoffi_special_offi_time_inx(cursor, spark1, exx.a23)

        # WHEN
        insert_mmtoffi_special_offi_time_otx(
            cursor, spark1, exx.sue, exx.a23, x_offi_time_otx
        )

        # THEN
        expected_rows = [(spark1, exx.a23, x_offi_time_otx, None)]
        assert select_mmtoffi_special_offi_time_inx(cursor, spark1, exx.a23)
        select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.offi_time}_otx
FROM {mmtoffi_h_agg_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [(spark1, exx.sue, exx.a23, x_offi_time_otx)]
