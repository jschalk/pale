from src.ch18_world_etl.etl_sqlstr import create_prime_tablename
from src.ch19_world_kpi.kpi_sqlstr import (
    get_create_kpi001_sqlstr,
    get_create_kpi002_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw


def test_get_create_kpi001_sqlstr_ReturnsObj():
    # ESTABLISH
    blfkegg_str = kw.plan_kegunit
    blfkegg_job = create_prime_tablename(blfkegg_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_create_kpi001_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {kw.moment_kpi001_voice_nets} AS
SELECT
  {kw.moment_voice_nets}.{kw.moment_label}
, {kw.moment_voice_nets}.{kw.plan_name}
, {kw.plan_net_amount} AS {kw.bnet_funds}
, RANK() OVER (ORDER BY {kw.plan_net_amount} DESC) AS {kw.fund_rank}
, IFNULL(SUM({blfkegg_job}.{kw.pledge}), 0) AS {kw.pledges_count}
FROM {kw.moment_voice_nets}
LEFT JOIN {blfkegg_job} ON
  {blfkegg_job}.{kw.moment_label} = {kw.moment_voice_nets}.{kw.moment_label}
  AND {blfkegg_job}.{kw.plan_name} = {kw.moment_voice_nets}.{kw.plan_name}
GROUP BY {kw.moment_voice_nets}.{kw.moment_label}, {kw.moment_voice_nets}.{kw.plan_name}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_create_kpi002_sqlstr_ReturnsObj():
    # ESTABLISH
    blfkegg_str = kw.plan_kegunit
    blfkegg_job = create_prime_tablename(blfkegg_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_create_kpi002_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {kw.moment_kpi002_plan_pledges} AS
SELECT
  {kw.moment_label}
, {kw.plan_name}
, {kw.keg_rope}
, {kw.pledge}
, {kw.keg_active}
, {kw.task}
FROM {blfkegg_job}
WHERE {kw.pledge} == 1 AND {kw.keg_active} == 1
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
