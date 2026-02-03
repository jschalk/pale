from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_update_heard_agg_timenum_sqlstr,
    get_update_heard_agg_timenum_sqlstrs,
    get_update_plncase_context_keg_sqlstr,
    get_update_plncase_inx_epoch_diff_sqlstr,
    get_update_plncase_range_sqlstr,
    get_update_plnfact_context_keg_sqlstr,
    get_update_plnfact_inx_epoch_diff_sqlstr,
    get_update_plnfact_range_sqlstr,
    update_heard_agg_timenum_columns,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO create function that updates all nabuable otx fields.
# identify the change
# update semantic_type: ReasonNum plan_keg_reason_caseunit_h_agg_put reason_lower, reason_upper
# update semantic_type: ReasonNum plan_keg_factunit_h_agg_put fact_lower, fact_upper


def test_get_update_plncase_inx_epoch_diff_sqlstr_ReturnsObj():
    # ESTABLISH
    plncase_tablename = prime_tbl(kw.plncase, "h", "agg", "put")
    nabtime_tablename = prime_tbl(kw.nabu_timenum, "h", "agg")

    # WHEN
    update_sqlstr = get_update_plncase_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabtime_tablename}
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
    plnfact_tablename = prime_tbl(kw.plnfact, "h", "agg", "put")
    nabtime_tablename = prime_tbl(kw.nabtime, "h", "agg")

    # WHEN
    update_sqlstr = get_update_plnfact_inx_epoch_diff_sqlstr()

    # THEN
    assert update_sqlstr
    expected_update_sqlstr = f"""
WITH spark_inx_epoch_diff AS (
    SELECT 
      spark_num
    , otx_time - inx_time AS inx_epoch_diff
    FROM {nabtime_tablename}
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
    SELECT {kw.spark_num}, {kw.close}, {kw.denom}, {kw.morph}
    FROM {plnkegg_tablename}
    GROUP BY {kw.spark_num}, {kw.close}, {kw.denom}, {kw.morph}
)
UPDATE {plncase_tablename}
SET 
  context_keg_close = spark_plnkegg.{kw.close}
, context_keg_denom = spark_plnkegg.{kw.denom}
, context_keg_morph = spark_plnkegg.{kw.morph}
FROM spark_plnkegg
WHERE {plncase_tablename}.spark_num IN (SELECT spark_num FROM spark_plnkegg)
;
"""
    print(expected_update_sqlstr)
    assert update_sqlstr == expected_update_sqlstr


def test_get_update_plnfact_context_keg_sqlstr_ReturnsObj():
    # ESTABLISH
    plnfact_tablename = prime_tbl(kw.plnfact, "h", "agg", "put")
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
    plnfact_tablename = prime_tbl(kw.plnfact, "h", "agg", "put")

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
