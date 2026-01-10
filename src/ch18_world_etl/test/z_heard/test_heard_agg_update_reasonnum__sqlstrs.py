from sqlite3 import connect as sqlite3_connect
from src.ch06_keg.test._util.ch06_examples import get_range_attrs
from src.ch07_plan_logic.plan_tool import (
    plan_keg_factunit_exists,
    plan_keg_factunit_get_obj,
    plan_keg_reason_caseunit_exists,
    plan_keg_reason_caseunit_get_obj,
    plan_keg_reasonunit_get_obj,
    plan_kegunit_get_obj,
)
from src.ch13_epoch.epoch_main import (
    DEFAULT_EPOCH_LENGTH,
    add_epoch_kegunit,
    get_c400_constants,
)
from src.ch13_epoch.epoch_reason import set_epoch_cases_by_args_dict
from src.ch13_epoch.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_plan,
    get_lizzy9_config,
)
from src.ch15_nabu.nabu_config import get_nabu_config_dict
from src.ch17_idea.idea_config import get_dimens_with_idea_element
from src.ch18_world_etl.etl_nabu import (
    add_epoch_frame_to_db_planunit,
    add_frame_to_db_caseunit,
    add_frame_to_db_factunit,
    add_frame_to_db_planunit,
    add_frame_to_db_reasonunit,
)
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_update_heard_agg_epochtime_sqlstr,
    get_update_heard_agg_epochtime_sqlstrs,
    get_update_plncase_context_keg_sqlstr,
    get_update_plncase_inx_epoch_diff_sqlstr,
    get_update_plncase_range_sqlstr,
    get_update_plnfact_context_keg_sqlstr,
    get_update_plnfact_inx_epoch_diff_sqlstr,
    get_update_plnfact_range_sqlstr,
    update_heard_agg_epochtime_columns,
)
from src.ch18_world_etl.obj2db_plan import insert_h_agg_obj
from src.ch18_world_etl.test._util.ch18_examples import (
    insert_mmtoffi_special_offi_time_otx as insert_offi_time_otx,
    insert_mmtunit_special_c400_number as insert_c400_number,
    insert_nabepoc_h_agg_otx_inx_time as insert_otx_inx_time,
    insert_plncase_special_h_agg as insert_plncase,
    select_mmtoffi_special_offi_time_inx as select_offi_time_inx,
    select_plncase_special_h_agg as select_plncase,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO create function that updates all nabuable otx fields.
# identify the change
# update semantic_type: ReasonNum plan_keg_reason_caseunit_h_agg_put reason_lower, reason_upper
# update semantic_type: ReasonNum plan_keg_factunit_h_agg_put fact_lower, fact_upper


def test_get_update_plncase_inx_epoch_diff_sqlstr_ReturnsObj():
    # ESTABLISH
    plncase_tablename = prime_tbl(kw.plan_keg_reason_caseunit, "h", "agg", "put")
    nabepoc_tablename = prime_tbl(kw.nabu_epochtime, "h", "agg")

    # WHEN
    update_sqlstr = get_update_plncase_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabepoc_tablename}
    GROUP BY spark_num, otx_time, inx_time
)
UPDATE {plncase_tablename}
SET inx_epoch_diff = spark_inx_epoch_diff.inx_epoch_diff
FROM spark_inx_epoch_diff
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_plnfact_inx_epoch_diff_sqlstr_ReturnsObj():
    # ESTABLISH
    plnfact_tablename = prime_tbl(kw.plan_keg_factunit, "h", "agg", "put")
    nabepoc_tablename = prime_tbl(kw.nabu_epochtime, "h", "agg")

    # WHEN
    update_sqlstr = get_update_plnfact_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabepoc_tablename}
    GROUP BY spark_num, otx_time, inx_time
)
UPDATE {plnfact_tablename}
SET inx_epoch_diff = spark_inx_epoch_diff.inx_epoch_diff
FROM spark_inx_epoch_diff
WHERE {plnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_inx_epoch_diff)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_plncase_context_keg_sqlstr_ReturnsObj():
    # ESTABLISH
    plncase_tablename = prime_tbl(kw.plan_keg_reason_caseunit, "h", "agg", "put")
    plnkegg_tablename = prime_tbl(kw.plan_kegunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_plncase_context_keg_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_plnkegg AS (
    SELECT spark_num, close, denom, morph
    FROM {plnkegg_tablename}
    GROUP BY spark_num, close, denom, morph
)
UPDATE {plncase_tablename}
SET 
  context_keg_close = spark_plnkegg.close
, context_keg_denom = spark_plnkegg.denom
, context_keg_morph = spark_plnkegg.morph
FROM spark_plnkegg
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_plnkegg)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_plnfact_context_keg_sqlstr_ReturnsObj():
    # ESTABLISH
    plnfact_tablename = prime_tbl(kw.plan_keg_factunit, "h", "agg", "put")
    plnkegg_tablename = prime_tbl(kw.plan_kegunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_plnfact_context_keg_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_plnkegg AS (
    SELECT spark_num, close, denom, morph
    FROM {plnkegg_tablename}
    GROUP BY spark_num, close, denom, morph
)
UPDATE {plnfact_tablename}
SET 
  context_keg_close = spark_plnkegg.close
, context_keg_denom = spark_plnkegg.denom
, context_keg_morph = spark_plnkegg.morph
FROM spark_plnkegg
WHERE {plnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_plnkegg)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_plncase_range_sqlstr_ReturnsObj():
    # ESTABLISH
    plncase_tablename = prime_tbl(kw.plan_keg_reason_caseunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_plncase_range_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_plncase AS (
    SELECT 
      spark_num
    , IFNULL(reason_divisor, IFNULL(context_keg_close, context_keg_denom)) modulus
    , CASE WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_keg_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
    FROM {plncase_tablename}
    GROUP BY spark_num, reason_divisor, context_keg_close, context_keg_denom, context_keg_morph
)
UPDATE {plncase_tablename}
SET 
  reason_lower_inx = (reason_lower_otx + spark_plncase.calc_epoch_diff) % spark_plncase.modulus
, reason_upper_inx = (reason_upper_otx + spark_plncase.calc_epoch_diff) % spark_plncase.modulus
FROM spark_plncase
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_plncase)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_plnfact_range_sqlstr_ReturnsObj():
    # ESTABLISH
    plnfact_tablename = prime_tbl(kw.plan_keg_factunit, "h", "agg", "put")

    # WHEN
    update_sqlstr = get_update_plnfact_range_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_plnfact AS (
    SELECT 
      spark_num
    , IFNULL(reason_divisor, IFNULL(context_keg_close, context_keg_denom)) modulus
    , FACT WHEN morph = 1 THEN inx_epoch_diff / IFNULL(context_keg_denom, 1) ELSE inx_epoch_diff END calc_epoch_diff
    FROM {plnfact_tablename}
    GROUP BY spark_num, reason_divisor, context_keg_close, context_keg_denom, context_keg_morph
)
UPDATE {plnfact_tablename}
SET 
  reason_lower_inx = (reason_lower_otx + spark_plnfact.calc_epoch_diff) % spark_plnfact.modulus
, reason_upper_inx = (reason_upper_otx + spark_plnfact.calc_epoch_diff) % spark_plnfact.modulus
FROM spark_plnfact
WHERE {plnfact_tablename}.spark_num IN (SELECT spark_num FROM spark_plnfact)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr
