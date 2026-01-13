from sqlite3 import connect as sqlite3_connect
from src.ch00_py.db_toolbox import get_row_count, get_table_columns
from src.ch00_py.dict_toolbox import get_empty_set_if_None
from src.ch05_reason.reason_main import caseunit_shop
from src.ch13_time.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_plan,
)
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import get_default_sorted_list, get_idea_config_dict
from src.ch18_world_etl._ref.ch18_semantic_types import (
    FaceName,
    MomentLabel,
    PlanName,
    SparkInt,
    TimeNum,
)
from src.ch18_world_etl.etl_config import create_prime_tablename as prime_tbl
from src.ch18_world_etl.etl_sqlstr import create_sound_and_heard_tables
from src.ch18_world_etl.test._util.ch18_examples import (
    insert_mmtoffi_special_offi_time_otx,
    insert_mmtunit_special_c400_number,
    insert_nabepoc_h_agg_otx_inx_time,
    insert_plncase_special_h_agg,
    select_mmtoffi_special_offi_time_inx,
    select_nabepoc_h_agg_otx_inx_time,
    select_plncase_special_h_agg,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO create function that updates all nabuable otx fields.
# identify the change
#
# update semantic_type: ReasonNum plan_keg_reason_caseunit_h_agg_put reason_lower, reason_upper
# update semantic_type: ReasonNum plan_keg_factunit_h_agg_put fact_lower, fact_upper
# update semantic_type: TimeNum moment_paybook_h_agg tran_time
# update semantic_type: TimeNum moment_budunit_h_agg bud_time
# update semantic_type: TimeNum moment_timeh_agg time


def test_insert_nabepoc_h_agg_otx_inx_time_PopulatesTable_Scenario0():
    # ESTABLISH
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        nabepoc_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
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
        nabepoc_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
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
        assert select_mmtoffi_special_offi_time_inx(cursor, spark1, exx.a23)
        gen_rows = select_mmtoffi_special_offi_time_inx(cursor, spark1, exx.a23)
        expected_rows = [(spark1, exx.a23, x_offi_time_otx, None)]
        assert gen_rows == expected_rows
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


def test_insert_plncase_special_h_agg_PopulatesTable_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        plncase_h_agg = prime_tbl(kw.plan_keg_reason_caseunit, "h", "agg", "put")
        spark1 = 1
        s1_reason_upper = 500
        s1_reason_lower = 600
        assert get_row_count(cursor, plncase_h_agg) == 0

        # WHEN
        insert_plncase_special_h_agg(
            cursor=cursor,
            x_spark_num=spark1,
            x_moment_label=exx.sue,
            x_plan_name=exx.a23,
            x_keg_rope=wx.clean_rope,
            x_reason_context=wx.day_rope,
            x_reason_state=wx.days_rope,
            x_reason_lower=s1_reason_lower,
            x_reason_upper=s1_reason_upper,
        )

        # THEN
        assert get_row_count(cursor, plncase_h_agg) == 1
        select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_label}
, {kw.plan_name}
, {kw.keg_rope}
, {kw.reason_context}
, {kw.reason_state}
, {kw.reason_upper}_otx
, {kw.reason_lower}_otx
FROM {plncase_h_agg}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        expected_row = (
            spark1,
            exx.sue,
            exx.a23,
            wx.clean_rope,
            wx.day_rope,
            wx.days_rope,
            s1_reason_upper,
            s1_reason_lower,
        )
        assert rows == [expected_row]


def test_select_plncase_special_h_agg_PopulatesTable_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        plncase_h_agg = prime_tbl(kw.plan_keg_reason_caseunit, "h", "agg", "put")
        spark1 = 1
        s1_reason_upper = 500
        s1_reason_lower = 600
        insert_plncase_special_h_agg(
            cursor=cursor,
            x_spark_num=spark1,
            x_moment_label=exx.a23,
            x_plan_name=exx.sue,
            x_keg_rope=wx.clean_rope,
            x_reason_context=wx.day_rope,
            x_reason_state=wx.days_rope,
            x_reason_lower=s1_reason_lower,
            x_reason_upper=s1_reason_upper,
        )

        # WHEN
        gen_rows = select_plncase_special_h_agg(
            cursor=cursor,
            x_spark_num=spark1,
            x_moment_label=exx.a23,
            x_plan_name=exx.sue,
            x_keg_rope=wx.clean_rope,
            x_reason_context=wx.day_rope,
            x_reason_state=wx.days_rope,
        )

        # THEN
        assert gen_rows
        gen_row0 = gen_rows[0]
        assert gen_row0.spark_num == spark1
        assert gen_row0.moment_label == exx.a23
        assert gen_row0.plan_name == exx.sue
        assert gen_row0.keg_rope == wx.clean_rope
        assert gen_row0.reason_context == wx.day_rope
        assert gen_row0.reason_state == wx.days_rope
        assert gen_row0.reason_lower_otx == s1_reason_lower
        assert not gen_row0.reason_lower_inx
        assert gen_row0.reason_upper_otx == s1_reason_upper
        assert not gen_row0.reason_lower_inx
        print(f"{gen_rows=}")
        print(f"{[gen_row0]=}")
        assert get_row_count(cursor, plncase_h_agg) == 1
        select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_label}
, {kw.plan_name}
, {kw.keg_rope}
, {kw.reason_context}
, {kw.reason_state}
, {kw.reason_lower}_otx
, {kw.reason_upper}_otx
FROM {plncase_h_agg}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        expected_row = (
            spark1,
            exx.a23,
            exx.sue,
            wx.clean_rope,
            wx.day_rope,
            wx.days_rope,
            s1_reason_lower,
            s1_reason_upper,
        )
        assert rows == [expected_row]


# def insert_plncase_special_h_agg(
#     cursor: sqlite3_Cursor,
#     x_spark_num: SparkInt,
#     x_moment_label: MomentLabel,
#     x_plan_name: PlanName,
#     x_keg_rope: RopeTerm,
#     x_reason_context: RopeTerm,
#     x_reason_state: RopeTerm,
#     x_reason_lower: ReasonNum,
#     x_reason_upper: ReasonNum,
# ) -> list[tuple]:
#     pass


# def select_plncase_special_h_agg(
#     cursor: sqlite3_Cursor,
#     x_spark_num: SparkInt,
#     x_moment_label: MomentLabel,
#     x_plan_name: PlanName,
#     x_keg_rope: RopeTerm,
#     x_reason_context: RopeTerm,
#     x_reason_state: RopeTerm,
# ) -> list[tuple]:
#     pass


# def insert_plnfact_special_h_agg(
#     cursor: sqlite3_Cursor,
#     x_spark_num: SparkInt,
#     x_moment_label: MomentLabel,
#     x_plan_name: PlanName,
#     x_keg_rope: RopeTerm,
#     x_fact_context: RopeTerm,
#     x_fact_state: RopeTerm,
#     x_fact_upper: FactNum,
#     x_fact_lower: FactNum,
# ) -> list[tuple]:
#     pass


# def select_plnfact_special_h_agg(
#     cursor: sqlite3_Cursor,
#     x_spark_num: SparkInt,
#     x_moment_label: MomentLabel,
#     x_plan_name: PlanName,
#     x_keg_rope: RopeTerm,
#     x_fact_context: RopeTerm,
# ) -> list[tuple]:
#     pass


# def insert_plnkegg_special_h_agg(
#     cursor: sqlite3_Cursor,
#     x_spark_num: SparkInt,
#     x_moment_label: MomentLabel,
#     x_plan_name: PlanName,
#     x_keg_rope: RopeTerm,
#     x_denom: int,
# ) -> list[tuple]:
#     pass
