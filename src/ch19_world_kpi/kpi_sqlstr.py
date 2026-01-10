def get_create_kpi001_sqlstr() -> str:
    """
    Returns the SQL string for creating the KPI001 person nets table.
    """
    return """
CREATE TABLE moment_kpi001_person_nets AS
SELECT
  moment_person_nets.moment_label
, moment_person_nets.plan_name
, plan_net_amount AS bnet_funds
, RANK() OVER (ORDER BY plan_net_amount DESC) AS fund_rank
, IFNULL(SUM(plan_kegunit_job.pledge), 0) AS pledges_count
FROM moment_person_nets
LEFT JOIN plan_kegunit_job ON
  plan_kegunit_job.moment_label = moment_person_nets.moment_label
  AND plan_kegunit_job.plan_name = moment_person_nets.plan_name
GROUP BY moment_person_nets.moment_label, moment_person_nets.plan_name
;
"""


def get_create_kpi002_sqlstr() -> str:
    return """
CREATE TABLE moment_kpi002_plan_pledges AS
SELECT
  moment_label
, plan_name
, keg_rope
, pledge
, keg_active
, task
FROM plan_kegunit_job
WHERE pledge == 1 AND keg_active == 1
;
"""
