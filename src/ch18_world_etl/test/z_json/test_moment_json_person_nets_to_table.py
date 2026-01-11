from sqlite3 import connect as sqlite3_connect
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch00_py.file_toolbox import save_json
from src.ch09_plan_lesson._ref.ch09_path import create_moment_json_path
from src.ch11_bud.bud_main import tranbook_shop
from src.ch14_moment.moment_main import momentunit_shop
from src.ch18_world_etl.etl_main import (
    etl_moment_json_person_nets_to_moment_person_nets_table,
    insert_tranunit_persons_net,
)
from src.ch18_world_etl.etl_sqlstr import CREATE_MOMENT_PERSON_NETS_SQLSTR
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_insert_tranunit_persons_net_PopulatesDatabase():
    # ESTABLISH
    a23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    a23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    a23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    a23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        moment_person_nets_tablename = kw.moment_person_nets
        cursor.execute(CREATE_MOMENT_PERSON_NETS_SQLSTR)
        assert get_row_count(cursor, moment_person_nets_tablename) == 0

        # WHEN
        insert_tranunit_persons_net(cursor, a23_tranbook)

        # THEN
        assert get_row_count(cursor, moment_person_nets_tablename) == 2
        select_sqlstr = f"SELECT moment_label, plan_name, {kw.plan_net_amount} FROM {moment_person_nets_tablename}"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [
            (exx.a23, exx.bob, t55_bob_amount),
            (exx.a23, exx.yao, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]


def test_etl_moment_json_person_nets_to_moment_person_nets_table_PopulatesDatabase(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, mstr_dir)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_moment.add_paypurchase(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    a23_moment.add_paypurchase(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    a23_moment.add_paypurchase(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    a23_moment.add_paypurchase(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    a23_json_path = create_moment_json_path(mstr_dir, exx.a23)
    save_json(a23_json_path, None, a23_moment.to_dict())

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        moment_person_nets_tablename = kw.moment_person_nets
        assert not db_table_exists(cursor, moment_person_nets_tablename)

        # WHEN
        etl_moment_json_person_nets_to_moment_person_nets_table(cursor, mstr_dir)

        # THEN
        assert get_row_count(cursor, moment_person_nets_tablename) == 2
        select_sqlstr = f"SELECT moment_label, plan_name, {kw.plan_net_amount} FROM {moment_person_nets_tablename}"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [
            (exx.a23, exx.bob, t55_bob_amount),
            (exx.a23, exx.yao, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]
