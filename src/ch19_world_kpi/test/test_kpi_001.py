from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch04_rope.rope import create_rope
from src.ch18_world_etl.etl_sqlstr import (
    CREATE_JOB_BLFKEGG_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    create_prime_tablename,
)
from src.ch19_world_kpi.kpi_mstr import create_populate_kpi001_table
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_create_populate_kpi001_table_PopulatesTable_Scenario0_NoPledges():
    # ESTABLISH
    yao_voice_net = -55
    bob_voice_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_BLFKEGG_SQLSTR)
        cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
        moment_voice_nets_tablename = kw.moment_voice_nets
        insert_sqlstr = f"""INSERT INTO {moment_voice_nets_tablename} ({kw.moment_label}, {kw.plan_name}, {kw.plan_net_amount}) 
VALUES 
  ('{exx.a23}', '{exx.bob}', {bob_voice_net})
, ('{exx.a23}', '{exx.yao}', {yao_voice_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        moment_kpi001_voice_nets_tablename = kw.moment_kpi001_voice_nets
        assert not db_table_exists(cursor, moment_kpi001_voice_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

        # THEN
        assert get_table_columns(cursor, moment_kpi001_voice_nets_tablename) == [
            kw.moment_label,
            kw.plan_name,
            kw.bnet_funds,
            kw.fund_rank,
            kw.pledges_count,
        ]
        assert get_row_count(cursor, moment_kpi001_voice_nets_tablename)
        select_sqlstr = f"""
        SELECT 
  {kw.moment_label}
, {kw.plan_name}
, {kw.bnet_funds}
, {kw.fund_rank}
, {kw.pledges_count}
FROM {moment_kpi001_voice_nets_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (exx.a23, exx.bob, 600.0, 1, 0),
            (exx.a23, exx.yao, -55.0, 2, 0),
        ]


def test_create_populate_kpi001_table_PopulatesTable_Scenario1_1pledge():
    # ESTABLISH
    yao_voice_net = -55
    bob_voice_net = 600
    casa_rope = create_rope(exx.a23, "casa")

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
        moment_voice_nets_tablename = kw.moment_voice_nets
        insert_sqlstr = f"""INSERT INTO {moment_voice_nets_tablename} ({kw.moment_label}, {kw.plan_name}, {kw.plan_net_amount})
VALUES
  ('{exx.a23}', '{exx.bob}', {bob_voice_net})
, ('{exx.a23}', '{exx.yao}', {yao_voice_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2

        cursor.execute(CREATE_JOB_BLFKEGG_SQLSTR)
        job_blfkegg_tablename = create_prime_tablename("blfkegg", "job", None)
        insert_sqlstr = f"""
INSERT INTO {job_blfkegg_tablename} ({kw.moment_label}, {kw.plan_name}, {kw.keg_rope}, {kw.pledge})
VALUES ('{exx.a23}', '{exx.bob}', '{casa_rope}', 1)
"""
        cursor.execute(insert_sqlstr)
        moment_kpi001_voice_nets_tablename = kw.moment_kpi001_voice_nets
        assert not db_table_exists(cursor, moment_kpi001_voice_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

        # THEN
        assert get_row_count(cursor, moment_kpi001_voice_nets_tablename)
        select_sqlstr = f"""SELECT {kw.moment_label}, {kw.plan_name}, {kw.bnet_funds}, {kw.fund_rank}, {kw.pledges_count} FROM {moment_kpi001_voice_nets_tablename}"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (exx.a23, exx.bob, bob_voice_net, 1, 1),
            (exx.a23, exx.yao, yao_voice_net, 2, 0),
        ]
