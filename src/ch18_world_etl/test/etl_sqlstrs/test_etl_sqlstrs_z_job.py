from sqlite3 import connect as sqlite3_connect
from src.ch00_py.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_db_tables,
)
from src.ch07_plan_logic.plan_config import get_plan_config_dict
from src.ch17_idea.idea_config import get_idea_sqlite_types
from src.ch17_idea.idea_db_tool import get_default_sorted_list
from src.ch18_world_etl.etl_sqlstr import (
    create_job_tables,
    create_prime_tablename as prime_table,
    get_job_create_table_sqlstrs,
)
from src.ref.keywords import Ch18Keywords as kw


def test_get_job_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_job_create_table_sqlstrs()

    # THEN
    s_types = get_idea_sqlite_types()
    plan_config = get_plan_config_dict()
    for x_dimen in plan_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = plan_config.get(x_dimen)

        job_table = prime_table(x_dimen, kw.job, None)
        job_cols = {kw.moment_rope, kw.plan_name}
        job_cols.update(set(x_config.get(kw.jkeys).keys()))
        job_cols.update(set(x_config.get(kw.jvalues).keys()))
        job_cols = get_default_sorted_list(job_cols)
        expected_create_sqlstr = get_create_table_sqlstr(job_table, job_cols, s_types)
        job_dimen_abbr = x_config.get("abbreviation").upper()
        print(
            f'CREATE_JOB_{job_dimen_abbr.upper()}_SQLSTR= """{expected_create_sqlstr}"""'
        )
        # print(f'"{job_table}": CREATE_JOB_{job_dimen_abbr}_SQLSTR,')
        assert create_table_sqlstrs.get(job_table) == expected_create_sqlstr


def test_create_job_tables_CreatesTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        assert len(get_db_tables(cursor)) == 0

        plnmemb_job_table = prime_table(kw.plan_person_membership, kw.job, None)
        plnprsn_job_table = prime_table(kw.plan_personunit, kw.job, None)
        plngrou_job_table = prime_table(kw.plan_groupunit, kw.job, None)
        plnawar_job_table = prime_table(kw.plan_keg_awardunit, kw.job, None)
        plnfact_job_table = prime_table(kw.plan_keg_factunit, kw.job, None)
        plnheal_job_table = prime_table(kw.plan_keg_healerunit, kw.job, None)
        plncase_job_table = prime_table(kw.plan_keg_reason_caseunit, kw.job, None)
        planares_job_table = prime_table(kw.plan_keg_reasonunit, kw.job, None)
        plnlabo_job_table = prime_table(kw.plan_keg_partyunit, kw.job, None)
        plnkegg_job_table = prime_table(kw.plan_kegunit, kw.job, None)
        plnunit_job_table = prime_table(kw.planunit, kw.job, None)
        # plnmemb_job_table = f"{kw.plan_person_membership}_job"
        # plnprsn_job_table = f"{kw.plan_personunit}_job"
        # plngrou_job_table = f"{kw.plan_groupunit}_job"
        # plnawar_job_table = f"{kw.plan_keg_awardunit}_job"
        # plnfact_job_table = f"{kw.plan_keg_factunit}_job"
        # plnheal_job_table = f"{kw.plan_keg_healerunit}_job"
        # plncase_job_table = f"{kw.plan_keg_reason_caseunit}_job"
        # planares_job_table = f"{kw.plan_keg_reasonunit}_job"
        # plnlabo_job_table = f"{kw.plan_keg_partyunit}_job"
        # plnkegg_job_table = f"{kw.plan_kegunit}_job"
        # plnunit_job_table = f"{kw.planunit}_job"

        assert db_table_exists(cursor, plnmemb_job_table) is False
        assert db_table_exists(cursor, plnprsn_job_table) is False
        assert db_table_exists(cursor, plngrou_job_table) is False
        assert db_table_exists(cursor, plnawar_job_table) is False
        assert db_table_exists(cursor, plnfact_job_table) is False
        assert db_table_exists(cursor, plnheal_job_table) is False
        assert db_table_exists(cursor, plncase_job_table) is False
        assert db_table_exists(cursor, planares_job_table) is False
        assert db_table_exists(cursor, plnlabo_job_table) is False
        assert db_table_exists(cursor, plnkegg_job_table) is False
        assert db_table_exists(cursor, plnunit_job_table) is False

        # WHEN
        create_job_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, plnmemb_job_table)
        assert db_table_exists(cursor, plnprsn_job_table)
        assert db_table_exists(cursor, plngrou_job_table)
        assert db_table_exists(cursor, plnawar_job_table)
        assert db_table_exists(cursor, plnfact_job_table)
        assert db_table_exists(cursor, plnheal_job_table)
        assert db_table_exists(cursor, plncase_job_table)
        assert db_table_exists(cursor, planares_job_table)
        assert db_table_exists(cursor, plnlabo_job_table)
        assert db_table_exists(cursor, plnkegg_job_table)
        assert db_table_exists(cursor, plnunit_job_table)
        assert len(get_db_tables(cursor)) == 11
