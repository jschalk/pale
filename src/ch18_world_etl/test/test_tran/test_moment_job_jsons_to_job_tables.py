from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count
from src.ch01_py.file_toolbox import save_json
from src.ch03_voice.group import awardunit_shop
from src.ch03_voice.labor import laborunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_lesson._ref.ch09_path import (
    create_job_path,
    create_moment_json_path,
)
from src.ch10_belief_listen.keep_tool import save_job_file
from src.ch14_moment.moment_main import momentunit_shop
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.tran_sqlstrs import create_prime_tablename as prime_table
from src.ch18_world_etl.transformers import etl_moment_job_jsons_to_job_tables
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario0(
    temp_dir_setup,
):  # sourcery skip: extract-method
    # ESTABLISH
    m23_moment_mstr_dir = get_temp_dir()
    m23_str = "music23"
    sue_belief = beliefunit_shop(exx.sue, exx.a23)
    sue_belief.add_voiceunit(exx.sue)
    sue_belief.add_voiceunit(exx.bob)
    sue_belief.get_voice(exx.bob).add_membership(exx.run)
    casa_rope = sue_belief.make_l1_rope("casa")
    situation_rope = sue_belief.make_l1_rope(kw.reason_active)
    clean_rope = sue_belief.make_rope(situation_rope, "clean")
    dirty_rope = sue_belief.make_rope(situation_rope, "dirty")
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    sue_belief.add_plan(dirty_rope)
    sue_belief.edit_plan_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_belief.edit_plan_attr(casa_rope, awardunit=awardunit_shop(exx.run))
    sue_belief.edit_plan_attr(casa_rope, healerunit=healerunit_shop({exx.bob}))
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(exx.sue)
    sue_belief.edit_plan_attr(casa_rope, laborunit=sue_laborunit)
    sue_belief.add_fact(situation_rope, clean_rope)
    print(f"{sue_belief.get_plan_obj(casa_rope).laborunit=}")
    print(f"{sue_belief.get_plan_obj(casa_rope).to_dict()=}")
    save_job_file(m23_moment_mstr_dir, sue_belief)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        blfmemb_job_table = prime_table("blfmemb", kw.job, None)
        blfvoce_job_table = prime_table("blfvoce", kw.job, None)
        blfgrou_job_table = prime_table("blfgrou", kw.job, None)
        blfawar_job_table = prime_table("blfawar", kw.job, None)
        blffact_job_table = prime_table("blffact", kw.job, None)
        blfheal_job_table = prime_table("blfheal", kw.job, None)
        blfcase_job_table = prime_table("blfcase", kw.job, None)
        blfreas_job_table = prime_table("blfreas", kw.job, None)
        blflabo_job_table = prime_table("blflabo", kw.job, None)
        blfplan_job_table = prime_table("blfplan", kw.job, None)
        blfunit_job_table = prime_table("beliefunit", kw.job, None)
        assert not db_table_exists(cursor, blfunit_job_table)
        assert not db_table_exists(cursor, blfplan_job_table)
        assert not db_table_exists(cursor, blfvoce_job_table)
        assert not db_table_exists(cursor, blfmemb_job_table)
        assert not db_table_exists(cursor, blfgrou_job_table)
        assert not db_table_exists(cursor, blfawar_job_table)
        assert not db_table_exists(cursor, blffact_job_table)
        assert not db_table_exists(cursor, blfheal_job_table)
        assert not db_table_exists(cursor, blfreas_job_table)
        assert not db_table_exists(cursor, blfcase_job_table)
        assert not db_table_exists(cursor, blflabo_job_table)

        # WHEN
        etl_moment_job_jsons_to_job_tables(cursor, m23_moment_mstr_dir)

        # THEN
        assert get_row_count(cursor, blfunit_job_table) == 1
        assert get_row_count(cursor, blfplan_job_table) == 5
        assert get_row_count(cursor, blfvoce_job_table) == 2
        assert get_row_count(cursor, blfmemb_job_table) == 3
        assert get_row_count(cursor, blfgrou_job_table) == 3
        assert get_row_count(cursor, blfawar_job_table) == 1
        assert get_row_count(cursor, blffact_job_table) == 1
        assert get_row_count(cursor, blfheal_job_table) == 1
        assert get_row_count(cursor, blfreas_job_table) == 1
        assert get_row_count(cursor, blfcase_job_table) == 1
        assert get_row_count(cursor, blflabo_job_table) == 1


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
    bob_job = beliefunit_shop(bob_inx, exx.a23)
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
        blfvoce_job_tablename = prime_table("blfvoce", kw.job, None)
        assert not db_table_exists(cursor, blfvoce_job_tablename)

        # WHEN
        etl_moment_job_jsons_to_job_tables(cursor, moment_mstr_dir)

        # THEN
        assert get_row_count(cursor, blfvoce_job_tablename) == 3
        rows = cursor.execute(f"SELECT * FROM {blfvoce_job_tablename}").fetchall()
        print(rows)
        assert rows == [
            (
                "Amy23",
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
                "Amy23",
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
                "Amy23",
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
