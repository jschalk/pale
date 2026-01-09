from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import (
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
        job_cols = {kw.moment_label, kw.plan_name}
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

        blfmemb_job_table = prime_table(kw.plan_voice_membership, kw.job, None)
        blfvoce_job_table = prime_table(kw.plan_voiceunit, kw.job, None)
        blfgrou_job_table = prime_table(kw.plan_groupunit, kw.job, None)
        blfawar_job_table = prime_table(kw.plan_keg_awardunit, kw.job, None)
        blffact_job_table = prime_table(kw.plan_keg_factunit, kw.job, None)
        blfheal_job_table = prime_table(kw.plan_keg_healerunit, kw.job, None)
        blfcase_job_table = prime_table(kw.plan_keg_reason_caseunit, kw.job, None)
        planares_job_table = prime_table(kw.plan_keg_reasonunit, kw.job, None)
        blflabo_job_table = prime_table(kw.plan_keg_partyunit, kw.job, None)
        blfkegg_job_table = prime_table(kw.plan_kegunit, kw.job, None)
        blfunit_job_table = prime_table(kw.planunit, kw.job, None)
        # blfmemb_job_table = f"{kw.plan_voice_membership}_job"
        # blfvoce_job_table = f"{kw.plan_voiceunit}_job"
        # blfgrou_job_table = f"{kw.plan_groupunit}_job"
        # blfawar_job_table = f"{kw.plan_keg_awardunit}_job"
        # blffact_job_table = f"{kw.plan_keg_factunit}_job"
        # blfheal_job_table = f"{kw.plan_keg_healerunit}_job"
        # blfcase_job_table = f"{kw.plan_keg_reason_caseunit}_job"
        # planares_job_table = f"{kw.plan_keg_reasonunit}_job"
        # blflabo_job_table = f"{kw.plan_keg_partyunit}_job"
        # blfkegg_job_table = f"{kw.plan_kegunit}_job"
        # blfunit_job_table = f"{kw.planunit}_job"

        assert db_table_exists(cursor, blfmemb_job_table) is False
        assert db_table_exists(cursor, blfvoce_job_table) is False
        assert db_table_exists(cursor, blfgrou_job_table) is False
        assert db_table_exists(cursor, blfawar_job_table) is False
        assert db_table_exists(cursor, blffact_job_table) is False
        assert db_table_exists(cursor, blfheal_job_table) is False
        assert db_table_exists(cursor, blfcase_job_table) is False
        assert db_table_exists(cursor, planares_job_table) is False
        assert db_table_exists(cursor, blflabo_job_table) is False
        assert db_table_exists(cursor, blfkegg_job_table) is False
        assert db_table_exists(cursor, blfunit_job_table) is False

        # WHEN
        create_job_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, blfmemb_job_table)
        assert db_table_exists(cursor, blfvoce_job_table)
        assert db_table_exists(cursor, blfgrou_job_table)
        assert db_table_exists(cursor, blfawar_job_table)
        assert db_table_exists(cursor, blffact_job_table)
        assert db_table_exists(cursor, blfheal_job_table)
        assert db_table_exists(cursor, blfcase_job_table)
        assert db_table_exists(cursor, planares_job_table)
        assert db_table_exists(cursor, blflabo_job_table)
        assert db_table_exists(cursor, blfkegg_job_table)
        assert db_table_exists(cursor, blfunit_job_table)
        assert len(get_db_tables(cursor)) == 11
