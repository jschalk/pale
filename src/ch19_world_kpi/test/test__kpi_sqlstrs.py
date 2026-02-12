from src.ch18_world_etl.etl_sqlstr import create_prime_tablename
from src.ch19_world_kpi.kpi_sqlstr import (
    get_create_kpi001_sqlstr,
    get_create_kpi002_sqlstr,
)
from src.ref.keywords import Ch19Keywords as kw


def test_get_create_kpi001_sqlstr_ReturnsObj():
    # ESTABLISH
    prnkegg_str = kw.person_kegunit
    prnkegg_job = create_prime_tablename(prnkegg_str, "job", None)

    # WHEN
    kpi001_sqlstr = get_create_kpi001_sqlstr()

    # THEN
    expected_kpi001_sqlstr = f"""
CREATE TABLE {kw.moment_kpi001_partner_nets} AS
SELECT
  {kw.moment_partner_nets}.{kw.moment_rope}
, {kw.moment_partner_nets}.{kw.person_name}
, {kw.person_net_amount} AS {kw.net_funds}
, RANK() OVER (ORDER BY {kw.person_net_amount} DESC) AS {kw.fund_rank}
, IFNULL(SUM({prnkegg_job}.{kw.pledge}), 0) AS {kw.pledges_count}
FROM {kw.moment_partner_nets}
LEFT JOIN {prnkegg_job} ON
  {prnkegg_job}.{kw.moment_rope} = {kw.moment_partner_nets}.{kw.moment_rope}
  AND {prnkegg_job}.{kw.person_name} = {kw.moment_partner_nets}.{kw.person_name}
GROUP BY {kw.moment_partner_nets}.{kw.moment_rope}, {kw.moment_partner_nets}.{kw.person_name}
;
"""
    assert kpi001_sqlstr == expected_kpi001_sqlstr


def test_get_create_kpi002_sqlstr_ReturnsObj():
    # ESTABLISH
    prnkegg_str = kw.person_kegunit
    prnkegg_job = create_prime_tablename(prnkegg_str, "job", None)

    # WHEN
    kpi002_sqlstr = get_create_kpi002_sqlstr()

    # THEN
    expected_kpi002_sqlstr = f"""
CREATE TABLE {kw.moment_kpi002_person_pledges} AS
SELECT
  {kw.moment_rope}
, {kw.person_name}
, {kw.keg_rope}
, {kw.pledge}
, {kw.keg_active}
, {kw.task}
FROM {prnkegg_job}
WHERE {kw.pledge} == 1 AND {kw.keg_active} == 1
;
"""
    print(expected_kpi002_sqlstr)
    assert kpi002_sqlstr == expected_kpi002_sqlstr
