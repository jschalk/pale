from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import open_json, save_json
from src.ch07_plan_logic.plan_main import get_planunit_from_dict, planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import (
    create_gut_path,
    create_job_path,
    create_moment_json_path,
)
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch14_moment.moment_main import momentunit_shop
from src.ch18_world_etl.etl_main import etl_moment_guts_to_moment_jobs
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import ExampleStrs as exx


def test_etl_moment_guts_to_moment_jobs_SetsFiles_Scenario0(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    credit44 = 44
    credit77 = 77
    credit88 = 88
    moment_mstr_dir = get_temp_dir()
    bob_gut = planunit_shop(bob_inx, exx.a23)
    bob_gut.add_personunit(bob_inx, credit77)
    bob_gut.add_personunit(yao_inx, credit44)
    bob_gut.add_personunit(bob_inx, credit77)
    bob_gut.add_personunit(sue_inx, credit88)
    bob_gut.add_personunit(yao_inx, credit44)
    a23_lasso = lassounit_shop(exx.a23)
    a23_bob_gut_path = create_gut_path(moment_mstr_dir, a23_lasso, bob_inx)
    save_json(a23_bob_gut_path, None, bob_gut.to_dict())
    a23_bob_job_path = create_job_path(moment_mstr_dir, a23_lasso, bob_inx)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    save_json(
        moment_json_path, None, momentunit_shop(exx.a23, moment_mstr_dir).to_dict()
    )
    assert os_path_exists(moment_json_path)
    assert os_path_exists(a23_bob_gut_path)
    print(f"{a23_bob_gut_path=}")
    assert os_path_exists(a23_bob_job_path) is False

    # WHEN
    etl_moment_guts_to_moment_jobs(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_job_path)
    generated_job = get_planunit_from_dict(open_json(a23_bob_job_path))
    expected_job = planunit_shop(bob_inx, exx.a23)
    expected_job.add_personunit(bob_inx, credit77)
    expected_job.add_personunit(yao_inx, credit44)
    expected_job.add_personunit(bob_inx, credit77)
    expected_job.add_personunit(sue_inx, credit88)
    expected_job.add_personunit(yao_inx, credit44)
    # assert generated_job.get_person(sue_inx) == expected_job.get_person(sue_inx)
    # assert generated_job.get_person(bob_inx) == expected_job.get_person(bob_inx)
    # assert generated_job.get_person(yao_inx) == expected_job.get_person(yao_inx)
    assert generated_job.persons.keys() == expected_job.persons.keys()
    # assert generated_job.persons == expected_job.persons
    # assert generated_job.get_keg_dict() == expected_job.to_dict()
    # assert generated_job.to_dict() == expected_job.to_dict()
    # assert generated_job == expected_job
