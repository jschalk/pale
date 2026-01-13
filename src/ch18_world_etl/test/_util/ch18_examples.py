from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import create_insert_query, get_row_count, get_table_columns
from src.ch00_py.dict_toolbox import get_empty_set_if_None
from src.ch05_reason.reason_main import caseunit_shop
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)
from src.ch18_world_etl._ref.ch18_semantic_types import (
    FaceName,
    FactNum,
    MomentLabel,
    PlanName,
    ReasonNum,
    RopeTerm,
    SparkInt,
    TimeNum,
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
    x_otx_time: TimeNum,
    x_inx_time: TimeNum,
):
    nabepoc_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
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
    nabepoc_h_agg_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")
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


def insert_plncase_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_plan_name: PlanName,
    x_keg_rope: RopeTerm,
    x_reason_context: RopeTerm,
    x_reason_state: RopeTerm,
    x_reason_lower: ReasonNum,
    x_reason_upper: ReasonNum,
) -> list[tuple]:
    plncase_tbl = prime_tbl(kw.plan_keg_reason_caseunit, "h", "agg", "put")
    values_dict = {
        "spark_num": x_spark_num,
        "moment_label": x_moment_label,
        "plan_name": x_plan_name,
        "keg_rope": x_keg_rope,
        "reason_context": x_reason_context,
        "reason_state": x_reason_state,
        "reason_upper_otx": x_reason_upper,
        "reason_lower_otx": x_reason_lower,
    }
    insert_sqlstr = create_insert_query(cursor, plncase_tbl, values_dict)
    cursor.execute(insert_sqlstr)


@dataclass
class PLNCASEHEARDAGG:
    spark_num: SparkInt
    moment_label: MomentLabel
    plan_name: PlanName
    keg_rope: RopeTerm
    reason_context: RopeTerm
    reason_state: RopeTerm
    reason_lower_otx: float
    reason_lower_inx: float
    reason_upper_otx: float
    reason_upper_inx: float
    reason_divisor: int
    context_keg_close: float
    context_keg_denom: float
    context_keg_morph: float
    inx_epoch_diff: int


def select_plncase_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_plan_name: PlanName,
    x_keg_rope: RopeTerm,
    x_reason_context: RopeTerm,
    x_reason_state: RopeTerm,
) -> list[PLNCASEHEARDAGG]:
    x_dimen = kw.plan_keg_reason_caseunit
    plncase_h_agg_tablename = prime_tbl(x_dimen, "h", "agg", "put")
    select_sqlstr = f"""SELECT 
  {kw.spark_num}
, {kw.moment_label}
, {kw.plan_name}
, {kw.keg_rope}
, {kw.reason_context}
, {kw.reason_state}
, {kw.reason_lower}_otx
, {kw.reason_lower}_inx
, {kw.reason_upper}_otx
, {kw.reason_upper}_inx
, {kw.reason_divisor}
, context_keg_close
, context_keg_denom
, context_keg_morph
, inx_epoch_diff
FROM {plncase_h_agg_tablename}
WHERE {kw.spark_num} = {x_spark_num} 
    AND {kw.moment_label} = '{x_moment_label}'
    AND {kw.plan_name} = '{x_plan_name}'
    AND {kw.keg_rope} = '{x_keg_rope}'
    AND {kw.reason_context} = '{x_reason_context}'
    AND {kw.reason_state} = '{x_reason_state}'
;
"""
    cursor.execute(select_sqlstr)
    plncase_heard_aggs = []
    for row in cursor.fetchall():
        x_plncase_h_agg = PLNCASEHEARDAGG(
            spark_num=row[0],
            moment_label=row[1],
            plan_name=row[2],
            keg_rope=row[3],
            reason_context=row[4],
            reason_state=row[5],
            reason_lower_otx=row[6],
            reason_lower_inx=row[7],
            reason_upper_otx=row[8],
            reason_upper_inx=row[9],
            reason_divisor=row[10],
            context_keg_close=row[11],
            context_keg_denom=row[12],
            context_keg_morph=row[13],
            inx_epoch_diff=row[14],
        )
        plncase_heard_aggs.append(x_plncase_h_agg)
    return plncase_heard_aggs


def insert_plnfact_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_plan_name: PlanName,
    x_keg_rope: RopeTerm,
    x_fact_context: RopeTerm,
    x_fact_state: RopeTerm,
    x_fact_upper: FactNum,
    x_fact_lower: FactNum,
) -> list[tuple]:
    pass


def select_plnfact_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_plan_name: PlanName,
    x_keg_rope: RopeTerm,
    x_fact_context: RopeTerm,
) -> list[tuple]:
    pass


def insert_plnkegg_special_h_agg(
    cursor: sqlite3_Cursor,
    x_spark_num: SparkInt,
    x_moment_label: MomentLabel,
    x_plan_name: PlanName,
    x_keg_rope: RopeTerm,
    x_denom: int,
) -> list[tuple]:
    pass
