from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch01_py.db_toolbox import create_insert_query, get_row_count, get_table_columns
from src.ch01_py.dict_toolbox import get_empty_set_if_None
from src.ch05_reason.reason_main import caseunit_shop
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)
from src.ch18_world_etl._ref.ch18_semantic_types import (
    BeliefName,
    CotoNum,
    EpochTime,
    FaceName,
    MomentLabel,
    RopeTerm,
    SparkInt,
)
from src.ch18_world_etl.etl_config import (
    etl_idea_category_config_dict,
    get_dimen_abbv7,
    get_etl_category_stages_dict,
    get_prime_columns,
    remove_inx_columns,
    remove_otx_columns,
)
from src.ch18_world_etl.etl_main import etl_heard_raw_tables_to_heard_agg_tables
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def insert_nabepoc_h_agg_otx_inx_time(
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


def select_nabepoc_h_agg_otx_inx_time(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
) -> list[tuple]:
    nabepoc_h_agg_tablename = prime_tbl(kw.nabu_epochtime, "h", "agg")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_label}
, {kw.otx_time}
, {kw.inx_time}
FROM {nabepoc_h_agg_tablename}
WHERE {kw.spark_num} == {x_spark_num} and {kw.moment_label} == '{x_moment_label}'
"""
    cursor.execute(select_sqlstr)
    return cursor.fetchall()


def insert_mmtunit_special_c400_number(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_face_name: FaceName,
    x_moment_label: MomentLabel,
    c400_number: int,
):
    mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
    select_sqlstr = f"""INSERT INTO {mmtunit_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.c400_number}
)
VALUES
  ({x_spark_num}, '{x_face_name}', '{x_moment_label}', {c400_number})
;
"""
    cursor.execute(select_sqlstr)


def insert_mmtoffi_special_offi_time_otx(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_face_name: FaceName,
    x_moment_label: MomentLabel,
    offi_time_otx: int,
):
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    select_sqlstr = f"""INSERT INTO {mmtoffi_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_label}
, {kw.offi_time}_otx
)
VALUES
  ({x_spark_num}, '{x_face_name}', '{x_moment_label}', {offi_time_otx})
;
"""
    cursor.execute(select_sqlstr)


def select_mmtoffi_special_offi_time_inx(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
) -> list[tuple]:
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_label}
, {kw.offi_time}_otx
, {kw.offi_time}_inx
FROM {mmtoffi_h_agg_tablename}
WHERE {kw.spark_num} == {x_spark_num} and {kw.moment_label} == '{x_moment_label}'
"""
    cursor.execute(select_sqlstr)
    return cursor.fetchall()


def insert_blfcase_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_belief_name: BeliefName,
    x_plan_rope: RopeTerm,
    x_reason_context: RopeTerm,
    x_reason_state: RopeTerm,
    x_reason_lower: CotoNum,
    x_reason_upper: CotoNum,
) -> list[tuple]:
    blfcase_tbl = prime_tbl(kw.belief_plan_reason_caseunit, "h", "agg", "put")
    values_dict = {
        "spark_num": x_spark_num,
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "plan_rope": x_plan_rope,
        "reason_context": x_reason_context,
        "reason_state": x_reason_state,
        "reason_upper_otx": x_reason_upper,
        "reason_lower_otx": x_reason_lower,
    }
    insert_sqlstr = create_insert_query(cursor, blfcase_tbl, values_dict)
    cursor.execute(insert_sqlstr)


@dataclass
class BLFCASEHEARDAGG:
    spark_num: SparkInt
    moment_label: MomentLabel
    belief_name: BeliefName
    plan_rope: RopeTerm
    reason_context: RopeTerm
    reason_state: RopeTerm
    reason_lower_otx: float
    reason_lower_inx: float
    reason_upper_otx: float
    reason_upper_inx: float
    reason_divisor: int


def select_blfcase_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_belief_name: BeliefName,
    x_plan_rope: RopeTerm,
    x_reason_context: RopeTerm,
    x_reason_state: RopeTerm,
) -> list[BLFCASEHEARDAGG]:
    x_dimen = kw.belief_plan_reason_caseunit
    blfcase_h_agg_tablename = prime_tbl(x_dimen, "h", "agg", "put")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_label}
, {kw.belief_name}
, {kw.plan_rope}
, {kw.reason_context}
, {kw.reason_state}
, {kw.reason_lower}_otx
, {kw.reason_lower}_inx
, {kw.reason_upper}_otx
, {kw.reason_upper}_inx
, {kw.reason_divisor}
FROM {blfcase_h_agg_tablename}
WHERE {kw.spark_num} = {x_spark_num} 
    AND {kw.moment_label} = '{x_moment_label}'
    AND {kw.belief_name} = '{x_belief_name}'
    AND {kw.plan_rope} = '{x_plan_rope}'
    AND {kw.reason_context} = '{x_reason_context}'
    AND {kw.reason_state} = '{x_reason_state}'
;
"""
    cursor.execute(select_sqlstr)
    blfcase_heard_aggs = []
    for row in cursor.fetchall():
        x_blfcase_h_agg = BLFCASEHEARDAGG(
            spark_num=row[0],
            moment_label=row[1],
            belief_name=row[2],
            plan_rope=row[3],
            reason_context=row[4],
            reason_state=row[5],
            reason_lower_otx=row[6],
            reason_lower_inx=row[7],
            reason_upper_otx=row[8],
            reason_upper_inx=row[9],
            reason_divisor=row[10],
        )
        blfcase_heard_aggs.append(x_blfcase_h_agg)
    return blfcase_heard_aggs


def insert_blffact_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_belief_name: BeliefName,
    x_plan_rope: RopeTerm,
    x_fact_context: RopeTerm,
    x_fact_state: RopeTerm,
    x_fact_upper: CotoNum,
    x_fact_lower: CotoNum,
) -> list[tuple]:
    pass


def select_blffact_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_belief_name: BeliefName,
    x_plan_rope: RopeTerm,
    x_fact_context: RopeTerm,
) -> list[tuple]:
    pass


def insert_blfplan_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_belief_name: BeliefName,
    x_plan_rope: RopeTerm,
    x_denom: int,
) -> list[tuple]:
    pass
