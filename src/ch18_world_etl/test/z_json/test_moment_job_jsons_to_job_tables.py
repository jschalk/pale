from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count
from src.ch01_py.file_toolbox import save_json
from src.ch03_voice.group import awardunit_shop
from src.ch03_voice.labor import laborunit_shop
from src.ch06_keg.healer import healerunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import create_job_path, create_moment_json_path
from src.ch10_plan_listen.keep_tool import save_job_file
from src.ch14_moment.moment_main import momentunit_shop
from src.ch18_world_etl.etl_main import etl_moment_job_jsons_to_job_tables
from src.ch18_world_etl.etl_sqlstr import create_prime_tablename as prime_table
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario0(
    temp_dir_setup,
):  # sourcery skip: extract-method
    # ESTABLISH
    m23_moment_mstr_dir = get_temp_dir()
    m23_str = "music23"
    sue_plan = planunit_shop(exx.sue, exx.a23)
    sue_plan.add_voiceunit(exx.sue)
    sue_plan.add_voiceunit(exx.bob)
    sue_plan.get_voice(exx.bob).add_membership(exx.run)
    casa_rope = sue_plan.make_l1_rope("casa")
    situation_rope = sue_plan.make_l1_rope(kw.reason_active)
    clean_rope = sue_plan.make_rope(situation_rope, "clean")
    dirty_rope = sue_plan.make_rope(situation_rope, "dirty")
    sue_plan.add_keg(casa_rope)
    sue_plan.add_keg(clean_rope)
    sue_plan.add_keg(dirty_rope)
    sue_plan.edit_keg_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_plan.edit_keg_attr(casa_rope, awardunit=awardunit_shop(exx.run))
    sue_plan.edit_keg_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(exx.sue)
    sue_plan.edit_keg_attr(casa_rope, laborunit=sue_laborunit)
    sue_plan.add_fact(situation_rope, clean_rope)
    print(f"{sue_plan.get_keg_obj(casa_rope).laborunit=}")
    print(f"{sue_plan.get_keg_obj(casa_rope).to_dict()=}")
    save_job_file(m23_moment_mstr_dir, sue_plan)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        plnmemb_job_table = prime_table("plnmemb", kw.job, None)
        plnvoce_job_table = prime_table("plnvoce", kw.job, None)
        plngrou_job_table = prime_table("plngrou", kw.job, None)
        plnawar_job_table = prime_table("plnawar", kw.job, None)
        plnfact_job_table = prime_table("plnfact", kw.job, None)
        plnheal_job_table = prime_table("plnheal", kw.job, None)
        plncase_job_table = prime_table("plncase", kw.job, None)
        plnreas_job_table = prime_table("plnreas", kw.job, None)
        plnlabo_job_table = prime_table("plnlabo", kw.job, None)
        plnkegg_job_table = prime_table("plnkegg", kw.job, None)
        plnunit_job_table = prime_table("plnunit", kw.job, None)
        assert not db_table_exists(cursor, plnunit_job_table)
        assert not db_table_exists(cursor, plnkegg_job_table)
        assert not db_table_exists(cursor, plnvoce_job_table)
        assert not db_table_exists(cursor, plnmemb_job_table)
        assert not db_table_exists(cursor, plngrou_job_table)
        assert not db_table_exists(cursor, plnawar_job_table)
        assert not db_table_exists(cursor, plnfact_job_table)
        assert not db_table_exists(cursor, plnheal_job_table)
        assert not db_table_exists(cursor, plnreas_job_table)
        assert not db_table_exists(cursor, plncase_job_table)
        assert not db_table_exists(cursor, plnlabo_job_table)

        # WHEN
        etl_moment_job_jsons_to_job_tables(cursor, m23_moment_mstr_dir)

        # THEN
        assert get_row_count(cursor, plnunit_job_table) == 1
        assert get_row_count(cursor, plnkegg_job_table) == 5
        assert get_row_count(cursor, plnvoce_job_table) == 2
        assert get_row_count(cursor, plnmemb_job_table) == 3
        assert get_row_count(cursor, plngrou_job_table) == 3
        assert get_row_count(cursor, plnawar_job_table) == 1
        assert get_row_count(cursor, plnfact_job_table) == 1
        assert get_row_count(cursor, plnheal_job_table) == 1
        assert get_row_count(cursor, plnreas_job_table) == 1
        assert get_row_count(cursor, plncase_job_table) == 1
        assert get_row_count(cursor, plnlabo_job_table) == 1


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario1(
    temp_dir_setup,
):  # sourcery skip: extract-method
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    credit44 = 44
    credit77 = 77
    credit88 = 88
    moment_mstr_dir = get_temp_dir()
    bob_job = planunit_shop(bob_inx, exx.a23)
    bob_job.add_voiceunit(bob_inx, credit77)
    bob_job.add_voiceunit(yao_inx, credit44)
    bob_job.add_voiceunit(bob_inx, credit77)
    bob_job.add_voiceunit(sue_inx, credit88)
    bob_job.add_voiceunit(yao_inx, credit44)
    save_job_file(moment_mstr_dir, bob_job)
    moment_json_path = create_moment_json_path(moment_mstr_dir, exx.a23)
    moment_dict = momentunit_shop(exx.a23, moment_mstr_dir).to_dict()
    save_json(moment_json_path, None, moment_dict)
    a23_bob_job_path = create_job_path(moment_mstr_dir, exx.a23, bob_inx)
    assert os_path_exists(moment_json_path)
    assert os_path_exists(a23_bob_job_path)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        plnvoce_job_tablename = prime_table("plnvoce", kw.job, None)
        assert not db_table_exists(cursor, plnvoce_job_tablename)

        # WHEN
        etl_moment_job_jsons_to_job_tables(cursor, moment_mstr_dir)

        # THEN
        assert get_row_count(cursor, plnvoce_job_tablename) == 3
        rows = cursor.execute(f"SELECT * FROM {plnvoce_job_tablename}").fetchall()
        print(rows)
        assert rows == [
            (
                exx.a23,
                "Bobby",
                "Bobby",
                77.0,
                1.0,
                ";",
                368421053.0,
                333333334.0,
                368421053.0,
                333333334.0,
                368421053.0,
                333333334.0,
                0.368421053,
                0.333333334,
                0.0,
                0.0,
            ),
            (
                exx.a23,
                "Bobby",
                "Suzy",
                88.0,
                1.0,
                ";",
                421052631.0,
                333333333.0,
                421052631.0,
                333333333.0,
                421052631.0,
                333333333.0,
                0.421052631,
                0.333333333,
                0.0,
                0.0,
            ),
            (
                exx.a23,
                "Bobby",
                "Yaoe",
                44.0,
                1.0,
                ";",
                210526316.0,
                333333333.0,
                210526316.0,
                333333333.0,
                210526316.0,
                333333333.0,
                0.210526316,
                0.333333333,
                0.0,
                0.0,
            ),
        ]
