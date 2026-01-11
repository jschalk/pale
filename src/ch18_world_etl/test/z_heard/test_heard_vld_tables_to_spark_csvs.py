from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch00_py.file_toolbox import create_path, open_file
from src.ch11_bud._ref.ch11_path import create_plan_spark_dir_path
from src.ch18_world_etl.etl_main import etl_heard_vld_to_spark_plan_csvs
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename,
    create_sound_and_heard_tables,
)
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_etl_heard_vld_to_spark_plan_csvs_PopulatesPlanPulabelTables(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    spark3 = 3
    spark7 = 7
    yao_person_cred_lumen5 = 5
    sue_person_cred_lumen7 = 7
    put_agg_tablename = create_prime_tablename(kw.plan_personunit, "h", "vld", "put")
    put_agg_csv = f"{put_agg_tablename}.csv"
    x_moment_mstr_dir = get_temp_dir()
    a23_bob_e3_dir = create_plan_spark_dir_path(
        x_moment_mstr_dir, exx.a23, bob_inx, spark3
    )
    a23_bob_e7_dir = create_plan_spark_dir_path(
        x_moment_mstr_dir, exx.a23, bob_inx, spark7
    )
    a23_e3_plnprsn_put_path = create_path(a23_bob_e3_dir, put_agg_csv)
    a23_e7_plnprsn_put_path = create_path(a23_bob_e7_dir, put_agg_csv)

    with sqlite3_connect(":memory:") as plan_db_conn:
        cursor = plan_db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {put_agg_tablename} ({kw.spark_num},{kw.face_name},{kw.moment_label},{kw.plan_name},{kw.person_name},{kw.person_cred_lumen})
VALUES
  ({spark3},'{sue_inx}','{exx.a23}','{bob_inx}','{yao_inx}',{yao_person_cred_lumen5})
, ({spark7},'{sue_inx}','{exx.a23}','{bob_inx}','{yao_inx}',{yao_person_cred_lumen5})
, ({spark7},'{sue_inx}','{exx.a23}','{bob_inx}','{sue_inx}',{sue_person_cred_lumen7})
;
"""
        print(insert_raw_sqlstr)
        cursor.execute(insert_raw_sqlstr)
        assert os_path_exists(a23_e3_plnprsn_put_path) is False
        assert os_path_exists(a23_e7_plnprsn_put_path) is False

        # WHEN
        etl_heard_vld_to_spark_plan_csvs(cursor, x_moment_mstr_dir)

        # THEN
        assert os_path_exists(a23_e3_plnprsn_put_path)
        assert os_path_exists(a23_e7_plnprsn_put_path)
        e3_put_csv = open_file(a23_e3_plnprsn_put_path)
        e7_put_csv = open_file(a23_e7_plnprsn_put_path)
        print(f"{e3_put_csv=}")
        print(f"{e7_put_csv=}")
        expected_e3_put_csv = """spark_num,face_name,moment_label,plan_name,person_name,person_cred_lumen,person_debt_lumen
3,Suzy,Amy23,Bobby,Bobby,5.0,
"""
        expected_e7_put_csv = """spark_num,face_name,moment_label,plan_name,person_name,person_cred_lumen,person_debt_lumen
7,Suzy,Amy23,Bobby,Bobby,5.0,
7,Suzy,Amy23,Bobby,Suzy,7.0,
"""
        assert e3_put_csv == expected_e3_put_csv
        assert e7_put_csv == expected_e7_put_csv
