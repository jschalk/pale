def get_create_kpi001_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 partner nets table.
    """
    return """
CREATE TABLE moment_kpi001_partner_nets AS
SELECT
  moment_partner_nets.moment_rope
, moment_partner_nets.plan_name
, plan_net_amount AS net_funds
, RANK() OVER (ORDER BY plan_net_amount DESC) AS fund_rank
, IFNULL(SUM(plan_kegunit_job.pledge), 0) AS pledges_count
FROM moment_partner_nets
LEFT JOIN plan_kegunit_job ON
  plan_kegunit_job.moment_rope = moment_partner_nets.moment_rope
  AND plan_kegunit_job.plan_name = moment_partner_nets.plan_name
GROUP BY moment_partner_nets.moment_rope, moment_partner_nets.plan_name
;
"""


def get_create_kpi002_sqlstr() -> str:
    return """
CREATE TABLE moment_kpi002_plan_pledges AS
SELECT
  moment_rope
, plan_name
, keg_rope
, pledge
, keg_active
, task
FROM plan_kegunit_job
WHERE pledge == 1 AND keg_active == 1
;
"""
