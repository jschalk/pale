from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor
from src.ch00_py.db_toolbox import create_insert_query
from src.ch18_world_etl._ref.ch18_semantic_types import (
    FaceName,
    FactNum,
    MomentRope,
    PersonName,
    ReasonNum,
    RopeTerm,
    SparkInt,
    TimeNum,
)
from src.ch18_world_etl.etl_sqlstr import create_prime_tablename as prime_tbl
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def insert_nabtime_h_agg_otx_inx_time(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_face_name: FaceName,
    x_moment_rope: MomentRope,
    x_otx_time: TimeNum,
    x_inx_time: TimeNum,
):
    nabtime_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
    select_sqlstr = f"""INSERT INTO {nabtime_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.otx_time}
, {kw.inx_time}
)
VALUES
  ({x_spark_num}, '{x_face_name}', '{x_moment_rope}', {x_otx_time}, {x_inx_time})
;
"""
    cursor.execute(select_sqlstr)


def select_nabtime_h_agg_otx_inx_time(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_rope: MomentRope,
) -> list[tuple]:
    nabtime_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_rope}
, {kw.otx_time}
, {kw.inx_time}
FROM {nabtime_h_agg_tablename}
WHERE {kw.spark_num} == {x_spark_num} and {kw.moment_rope} == '{x_moment_rope}'
"""
    cursor.execute(select_sqlstr)
    return cursor.fetchall()


def insert_mmtunit_special_c400_number(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_face_name: FaceName,
    x_moment_rope: MomentRope,
    c400_number: int,
):
    mmtunit_h_agg_tablename = prime_tbl(kw.momentunit, "h", "agg")
    select_sqlstr = f"""INSERT INTO {mmtunit_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.c400_number}
)
VALUES
  ({x_spark_num}, '{x_face_name}', '{x_moment_rope}', {c400_number})
;
"""
    cursor.execute(select_sqlstr)


def insert_mmtoffi_special_offi_time_otx(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_face_name: FaceName,
    x_moment_rope: MomentRope,
    offi_time_otx: int,
):
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    select_sqlstr = f"""INSERT INTO {mmtoffi_h_agg_tablename} (
  {kw.spark_num}
, {kw.face_name}
, {kw.moment_rope}
, {kw.offi_time}_otx
)
VALUES
  ({x_spark_num}, '{x_face_name}', '{x_moment_rope}', {offi_time_otx})
;
"""
    cursor.execute(select_sqlstr)


def select_mmtoffi_special_offi_time_inx(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_rope: MomentRope,
) -> list[tuple]:
    mmtoffi_h_agg_tablename = prime_tbl(kw.moment_timeoffi, "h", "agg")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_rope}
, {kw.offi_time}_otx
, {kw.offi_time}_inx
FROM {mmtoffi_h_agg_tablename}
WHERE {kw.spark_num} == {x_spark_num} and {kw.moment_rope} == '{x_moment_rope}'
"""
    cursor.execute(select_sqlstr)
    return cursor.fetchall()


def insert_prncase_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_person_name: PersonName,
    x_plan_rope: RopeTerm,
    x_reason_context: RopeTerm,
    x_reason_state: RopeTerm,
    x_reason_lower: ReasonNum,
    x_reason_upper: ReasonNum,
) -> list[tuple]:
    prncase_tbl = prime_tbl(kw.person_plan_reason_caseunit, "h", "agg", "put")
    values_dict = {
        kw.spark_num: x_spark_num,
        "person_name": x_person_name,
        "plan_rope": x_plan_rope,
        kw.reason_context: x_reason_context,
        kw.reason_state: x_reason_state,
        f"{kw.reason_upper}_otx": x_reason_upper,
        f"{kw.reason_lower}_otx": x_reason_lower,
    }
    insert_sqlstr = create_insert_query(cursor, prncase_tbl, values_dict)
    cursor.execute(insert_sqlstr)


@dataclass
class PRNCASEHEARDAGG:
    spark_num: SparkInt
    person_name: PersonName
    plan_rope: RopeTerm
    reason_context: RopeTerm
    reason_state: RopeTerm
    reason_lower_otx: float
    reason_lower_inx: float
    reason_upper_otx: float
    reason_upper_inx: float
    reason_divisor: int
    context_plan_close: float
    context_plan_denom: float
    context_plan_morph: float
    inx_epoch_diff: int


def select_prncase_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_person_name: PersonName,
    x_plan_rope: RopeTerm,
    x_reason_context: RopeTerm,
    x_reason_state: RopeTerm,
) -> list[PRNCASEHEARDAGG]:
    x_dimen = kw.person_plan_reason_caseunit
    prncase_h_agg_tablename = prime_tbl(x_dimen, "h", "agg", "put")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.person_name}
, {kw.plan_rope}
, {kw.reason_context}
, {kw.reason_state}
, {kw.reason_lower}_otx
, {kw.reason_lower}_inx
, {kw.reason_upper}_otx
, {kw.reason_upper}_inx
, {kw.reason_divisor}
, context_plan_close
, context_plan_denom
, context_plan_morph
, inx_epoch_diff
FROM {prncase_h_agg_tablename}
WHERE {kw.spark_num} = {x_spark_num} 
    AND {kw.person_name} = '{x_person_name}'
    AND {kw.plan_rope} = '{x_plan_rope}'
    AND {kw.reason_context} = '{x_reason_context}'
    AND {kw.reason_state} = '{x_reason_state}'
;
"""
    cursor.execute(select_sqlstr)
    prncase_heard_aggs = []
    for row in cursor.fetchall():
        x_prncase_h_agg = PRNCASEHEARDAGG(
            spark_num=row[0],
            person_name=row[1],
            plan_rope=row[2],
            reason_context=row[3],
            reason_state=row[4],
            reason_lower_otx=row[5],
            reason_lower_inx=row[6],
            reason_upper_otx=row[7],
            reason_upper_inx=row[8],
            reason_divisor=row[9],
            context_plan_close=row[10],
            context_plan_denom=row[11],
            context_plan_morph=row[12],
            inx_epoch_diff=row[13],
        )
        prncase_heard_aggs.append(x_prncase_h_agg)
    return prncase_heard_aggs


def insert_prnfact_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_rope: MomentRope,
    x_person_name: PersonName,
    x_plan_rope: RopeTerm,
    x_fact_context: RopeTerm,
    x_fact_state: RopeTerm,
    x_fact_upper: FactNum,
    x_fact_lower: FactNum,
) -> list[tuple]:
    pass


def select_prnfact_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_rope: MomentRope,
    x_person_name: PersonName,
    x_plan_rope: RopeTerm,
    x_fact_context: RopeTerm,
) -> list[tuple]:
    pass


def insert_prnplan_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_rope: MomentRope,
    x_person_name: PersonName,
    x_plan_rope: RopeTerm,
    x_denom: int,
) -> list[tuple]:
    pass
