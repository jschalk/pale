from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_db_tables, get_row_count
from src.ch18_world_etl.etl_sqlstr import (
    CREATE_JOB_PLNKEGG_SQLSTR,
    CREATE_MOMENT_PERSON_NETS_SQLSTR,
    create_prime_tablename,
)
from src.ch19_world_kpi.kpi_mstr import populate_kpi_bundle
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_populate_kpi_bundle_PopulatesTable_Scenario0_WithDefaultBundleID():
    # ESTABLISH
    yao_person_net = -55
    bob_person_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_PLNKEGG_SQLSTR)
        cursor.execute(CREATE_MOMENT_PERSON_NETS_SQLSTR)
        moment_person_nets_tablename = kw.moment_person_nets
        plnkegg_job_tablename = create_prime_tablename("PLNKEGG", "job", None)
        insert_sqlstr = f"""INSERT INTO {moment_person_nets_tablename} ({kw.moment_label}, {kw.plan_name}, {kw.plan_net_amount})
VALUES
  ('{exx.a23}', '{exx.bob}', {bob_person_net})
, ('{exx.a23}', '{exx.yao}', {yao_person_net})
"""
        cursor.execute(insert_sqlstr)
        assert db_table_exists(cursor, plnkegg_job_tablename)
        assert get_row_count(cursor, moment_person_nets_tablename) == 2
        moment_kpi001_tablename = kw.moment_kpi001_person_nets
        moment_kpi002_tablename = kw.moment_kpi002_plan_pledges
        assert not db_table_exists(cursor, moment_kpi001_tablename)
        assert not db_table_exists(cursor, moment_kpi002_tablename)

        # WHEN
        populate_kpi_bundle(cursor, kw.default_kpi_bundle)

        # THEN
        assert db_table_exists(cursor, moment_kpi001_tablename)
        assert db_table_exists(cursor, moment_kpi002_tablename)
        assert get_row_count(cursor, moment_kpi001_tablename) == 2
        assert get_row_count(cursor, moment_kpi002_tablename) == 0
        assert set(get_db_tables(db_conn).keys()) == {
            kw.moment_kpi001_person_nets,
            kw.moment_kpi002_plan_pledges,
            moment_person_nets_tablename,
            plnkegg_job_tablename,
        }


def test_populate_kpi_bundle_PopulatesTable_Scenario1_WithNoBundleID():
    # ESTABLISH
    yao_person_net = -55
    bob_person_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_PLNKEGG_SQLSTR)
        cursor.execute(CREATE_MOMENT_PERSON_NETS_SQLSTR)
        moment_person_nets_tablename = kw.moment_person_nets
        insert_sqlstr = f"""INSERT INTO {moment_person_nets_tablename} ({kw.moment_label}, {kw.plan_name}, {kw.plan_net_amount})
VALUES
  ('{exx.a23}', '{exx.bob}', {bob_person_net})
, ('{exx.a23}', '{exx.yao}', {yao_person_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, moment_person_nets_tablename) == 2
        moment_kpi001_person_nets_tablename = kw.moment_kpi001_person_nets
        assert not db_table_exists(cursor, moment_kpi001_person_nets_tablename)

        # WHEN
        populate_kpi_bundle(cursor)

        # THEN
        assert get_row_count(cursor, moment_kpi001_person_nets_tablename) == 2
        plnkegg_job_tablename = create_prime_tablename("PLNKEGG", "job", None)
        assert set(get_db_tables(db_conn).keys()) == {
            kw.moment_kpi001_person_nets,
            kw.moment_kpi002_plan_pledges,
            moment_person_nets_tablename,
            plnkegg_job_tablename,
        }
