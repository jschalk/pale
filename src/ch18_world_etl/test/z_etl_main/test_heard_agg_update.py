from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
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
from src.ch18_world_etl.etl_main import etl_heard_raw_tables_to_heard_agg_tables
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_insert_heard_agg_sqlstrs,
    get_update_epochtime_sqlstr,
)
from src.ch18_world_etl.etl_table import (
    etl_idea_category_config_dict,
    get_dimen_abbv7,
    get_etl_category_stages_dict,
    get_prime_columns,
    remove_inx_columns,
    remove_otx_columns,
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


def add_otx_inx_time(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_face_name: FaceName,
    x_moment_label: MomentLabel,
    x_otx_time: EpochTime,
    x_inx_time: EpochTime,
):
    nabepoc_h_agg_tablename = prime_tbl(kw.nabu_epochtime, "h", "agg")
    select_sqlstr = f"""INSERT INTO {nabepoc_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.otx_time}
, {kw.inx_time}
)
VALUES
  ({x_spark_num}, '{x_face_name}', '{x_moment_label}', {x_otx_time}, {x_inx_time})
;
"""
    cursor.execute(select_sqlstr)


def test_add_otx_inx_time_PopulatesTable_Scenario0():
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
        add_otx_inx_time(cursor, spark1, exx.sue, exx.a23, otx_time, inx_time)

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


def test_update_insert_heard_agg_sqlstrs_ReturnsObj_PopulatesTable_Scenario0_SingleRecord():
    # ESTABLISH
    spark1 = 1
    s1_otx_time = 44
    s1_inx_time = 55
    x200_offi_time = 200

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        add_otx_inx_time(cursor, spark1, exx.sue, exx.a23, s1_otx_time, s1_inx_time)
        mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
        print(f"{get_table_columns(cursor, mmtoffi_h_agg_tablename)=}")
        insert_into_clause = f"""INSERT INTO {mmtoffi_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.offi_time}_otx
)
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}', {x200_offi_time})
;
"""
        cursor.execute(insert_into_clause)
        select_offi_time_inx = f"""SELECT {kw.offi_time}_inx FROM {mmtoffi_h_agg_tablename} WHERE {kw.spark_num} == {spark1}"""
        assert cursor.execute(select_offi_time_inx).fetchone()[0] is None

        # WHEN
        mmtoffi_table = mmtoffi_h_agg_tablename
        update_mmtoffi_sql = get_update_epochtime_sqlstr(mmtoffi_table, kw.offi_time)
        cursor.execute(update_mmtoffi_sql)

        # THEN
        x211_offi_time = x200_offi_time + s1_otx_time - s1_inx_time
        assert cursor.execute(select_offi_time_inx).fetchone()[0] == x211_offi_time


def test_update_insert_heard_agg_sqlstrs_ReturnsObj_PopulatesTable_Scenario1_TwoRecords():
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    s1_otx_time = 44
    s1_inx_time = 55
    s1_offi_time_otx = 200
    s3_otx_time = 400
    s3_inx_time = 550
    s3_offi_time_otx = 2000

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        add_otx_inx_time(cursor, spark1, exx.sue, exx.a23, s1_otx_time, s1_inx_time)
        add_otx_inx_time(cursor, spark3, exx.sue, exx.a23, s3_otx_time, s3_inx_time)
        mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
        print(f"{get_table_columns(cursor, mmtoffi_h_agg_tablename)=}")
        insert_into_clause = f"""INSERT INTO {mmtoffi_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.offi_time}_otx
)
VALUES
  ({spark1}, '{exx.sue}', '{exx.a23}', {s1_offi_time_otx})
, ({spark3}, '{exx.sue}', '{exx.a23}', {s3_offi_time_otx})
;
"""
        cursor.execute(insert_into_clause)
        select_s1_offi_time_inx = f"""SELECT {kw.offi_time}_inx FROM {mmtoffi_h_agg_tablename} WHERE {kw.spark_num} == {spark1}"""
        select_s3_offi_time_inx = f"""SELECT {kw.offi_time}_inx FROM {mmtoffi_h_agg_tablename} WHERE {kw.spark_num} == {spark3}"""
        assert cursor.execute(select_s1_offi_time_inx).fetchone()[0] is None
        assert cursor.execute(select_s3_offi_time_inx).fetchone()[0] is None

        # WHEN
        mmtoffi_table = mmtoffi_h_agg_tablename
        update_mmtoffi_sql = get_update_epochtime_sqlstr(mmtoffi_table, kw.offi_time)
        cursor.execute(update_mmtoffi_sql)

        # THEN
        s1_offi_time_inx = s1_offi_time_otx + s1_otx_time - s1_inx_time
        s3_offi_time_inx = s3_offi_time_otx + s3_otx_time - s3_inx_time
        assert cursor.execute(select_s1_offi_time_inx).fetchone()[0] == s1_offi_time_inx
        assert cursor.execute(select_s3_offi_time_inx).fetchone()[0] == s3_offi_time_inx


# def check_insert_sqlstr_exists(
#     dimen: str,
#     insert_heard_agg_sqlstrs: dict,
#     stage_dict: dict,
#     put_del: str = None,
# ):
#     raw_tablename = prime_tbl(dimen, "h", "raw", put_del)
#     agg_tablename = prime_tbl(dimen, "h", "agg", put_del)

#     # print(f"{raw_tablename=} {agg_tablename=}")
#     # print(f"{stage_dict=}")
#     config_dict = etl_idea_category_config_dict()
#     raw_keylist = ["h", "raw", put_del] if put_del else ["h", "raw"]
#     agg_keylist = ["h", "agg", put_del] if put_del else ["h", "agg"]
#     p_agg_columns = get_prime_columns(dimen, agg_keylist, config_dict)
#     p_raw_columns = get_prime_columns(dimen, raw_keylist, config_dict)
#     if stage_dict.get("exclude_otx_from_insert"):
#         p_raw_columns = remove_otx_columns(p_raw_columns)
#         p_agg_columns = remove_inx_columns(p_agg_columns)
#     exclude_from_insert = stage_dict.get("exclude_from_insert")
#     exclude_from_insert = set(get_empty_set_if_None(exclude_from_insert))
#     p_raw_columns -= exclude_from_insert
#     p_raw_columns = get_default_sorted_list(p_raw_columns)
#     p_agg_columns = get_default_sorted_list(p_agg_columns)

#     raw_columns_str = ", ".join(p_raw_columns)
#     agg_columns_str = ", ".join(p_agg_columns)
#     expected_table2table_agg_insert_sqlstr = f"""
# INSERT INTO {agg_tablename} ({agg_columns_str})
# SELECT {raw_columns_str}
# FROM {raw_tablename}
# GROUP BY {raw_columns_str}
# """
#     dimen_abbv7 = get_dimen_abbv7(dimen)
#     if put_del:
#         variable_name = (
#             f"{dimen_abbv7.upper()}_HEARD_AGG_{put_del.upper()}_INSERT_SQLSTR"
#         )
#     else:
#         variable_name = f"{dimen_abbv7.upper()}_HEARD_AGG_INSERT_SQLSTR"

#     # print(f'"{agg_tablename}": {variable_name},')
#     print(f'{variable_name} = """{expected_table2table_agg_insert_sqlstr}"""')
#     gen_sqlstr = insert_heard_agg_sqlstrs.get(agg_tablename)
#     # print(f"{expected_table2table_agg_insert_sqlstr=}")
#     # print(f"                            {gen_sqlstr=}")
#     assert gen_sqlstr == expected_table2table_agg_insert_sqlstr


# def test_get_insert_heard_agg_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     insert_heard_agg_sqlstrs = get_insert_heard_agg_sqlstrs()

#     # THEN
#     h_str = "h"
#     agg_str = "agg"
#     agg_sqlstrs = insert_heard_agg_sqlstrs
#     etl_idea_category_config = etl_idea_category_config_dict()
#     with sqlite3_connect(":memory:") as moment_db_conn:
#         cursor = moment_db_conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         for idea_category, category_dict in etl_idea_category_config.items():
#             category_config = get_idea_config_dict(idea_category)
#             if h_dict := category_dict.get("stages").get(h_str):
#                 agg_dict = h_dict.get(agg_str)
#                 # print(f"{idea_category=}")
#                 if agg_dict.get("del") is None:
#                     for dimen in sorted(category_config.keys()):
#                         check_insert_sqlstr_exists(dimen, agg_sqlstrs, agg_dict)
#                 if agg_dict.get("del") is not None:
#                     del_dict = agg_dict.get("del")
#                     for dimen in sorted(category_config.keys()):
#                         check_insert_sqlstr_exists(dimen, agg_sqlstrs, del_dict, "del")
#                 if agg_dict.get("put") is not None:
#                     put_dict = agg_dict.get("put")
#                     for dimen in sorted(category_config.keys()):
#                         check_insert_sqlstr_exists(dimen, agg_sqlstrs, put_dict, "put")
#     # gen_heard_agg_tablenames = set(insert_heard_agg_sqlstrs.keys())
#     # assert gen_heard_agg_tablenames.issubset()


# def test_etl_heard_raw_tables_to_heard_agg_tables_PopulatesTable_Scenario0():
#     # ESTABLISH
#     yao_inx = "Yaoito"
#     spark1 = 1
#     spark2 = 2
#     spark5 = 5
#     spark7 = 7
#     x44_credit = 44
#     x55_credit = 55
#     x22_debt = 22
#     x66_debt = 66

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         blfvoce_h_raw_put_tablename = prime_tbl(kw.belief_voiceunit, "h", "raw", "put")
#         print(f"{get_table_columns(cursor, blfvoce_h_raw_put_tablename)=}")
#         insert_into_clause = f"""INSERT INTO {blfvoce_h_raw_put_tablename} (
#   {kw.spark_num}
# , {kw.face_name}_inx
# , {kw.moment_label}_inx
# , {kw.belief_name}_inx
# , {kw.voice_name}_inx
# , {kw.voice_cred_lumen}
# , {kw.voice_debt_lumen}
# )
# VALUES
#   ({spark1}, '{exx.sue}', '{exx.a23}','{exx.yao}', '{yao_inx}', {x44_credit}, {x22_debt})
# , ({spark2}, '{exx.yao}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
# , ({spark5}, '{exx.sue}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x22_debt})
# , ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
# , ({spark7}, '{exx.bob}', '{exx.a23}','{exx.bob}', '{exx.bob}', {x55_credit}, {x66_debt})
# ;
# """
#         cursor.execute(insert_into_clause)
#         assert get_row_count(cursor, blfvoce_h_raw_put_tablename) == 5
#         blfvoce_h_agg_put_tablename = prime_tbl(kw.belief_voiceunit, "h", "agg", "put")
#         assert get_row_count(cursor, blfvoce_h_agg_put_tablename) == 0

#         # WHEN
#         etl_heard_raw_tables_to_heard_agg_tables(cursor)

#         # THEN
#         assert get_row_count(cursor, blfvoce_h_agg_put_tablename) == 4
#         select_sqlstr = f"""SELECT {kw.spark_num}
# , {kw.face_name}
# , {kw.moment_label}
# , {kw.belief_name}
# , {kw.voice_name}
# , {kw.voice_cred_lumen}
# , {kw.voice_debt_lumen}
# FROM {blfvoce_h_agg_put_tablename}
# """
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (spark1, exx.sue, exx.a23, exx.yao, yao_inx, 44.0, 22.0),
#             (spark2, exx.yao, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
#             (spark5, exx.sue, exx.a23, exx.bob, exx.bob, 55.0, 22.0),
#             (spark7, exx.bob, exx.a23, exx.bob, exx.bob, 55.0, 66.0),
#         ]
