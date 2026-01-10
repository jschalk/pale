from src.ch01_py.file_toolbox import set_dir
from src.ch07_plan_logic.plan_main import PlanUnit, planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import create_plan_dir_path
from src.ch09_plan_lesson.lesson_filehandler import gut_file_exists, save_gut_file
from src.ch10_plan_listen.keep_tool import job_file_exists, open_job_file, save_job_file
from src.ch14_moment.moment_main import momentunit_shop
from src.ch14_moment.test._util.ch14_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import ExampleStrs as exx


def test_MomentUnit_rotate_job_ReturnsObj_Scenario1(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.sue)
    a23_moment.create_init_job_from_guts(exx.sue)
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.sue)

    # WHEN
    sue_job = a23_moment.rotate_job(exx.sue)

    # THEN
    example_plan = planunit_shop(exx.sue, exx.a23)
    assert sue_job.moment_label == example_plan.moment_label
    assert sue_job.plan_name == example_plan.plan_name


def test_MomentUnit_rotate_job_ReturnsObj_Scenario2_EmptyPersonsCause_inallocable_person_debt_lumen(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    init_sue_job = planunit_shop(exx.sue, exx.a23)
    init_sue_job.add_personunit(exx.yao)
    init_sue_job.add_personunit(exx.bob)
    init_sue_job.add_personunit(exx.zia)
    save_job_file(moment_mstr_dir, init_sue_job)
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.sue)
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.yao) is False
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.bob) is False
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.zia) is False

    # WHEN
    rotated_sue_job = a23_moment.rotate_job(exx.sue)

    # THEN method should wipe over job plan
    assert rotated_sue_job.person_exists(exx.bob)
    assert rotated_sue_job.to_dict() != init_sue_job.to_dict()
    assert init_sue_job.get_person(exx.bob).inallocable_person_debt_lumen == 0
    assert rotated_sue_job.get_person(exx.bob).inallocable_person_debt_lumen == 1


def a23_job(plan_name: str) -> PlanUnit:
    moment_mstr_dir = get_temp_dir()
    return open_job_file(moment_mstr_dir, exx.a23, plan_name)


def test_MomentUnit_rotate_job_ReturnsObj_Scenario3_job_ChangesFromRotation(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    init_sue_job = planunit_shop(exx.sue, exx.a23)
    init_sue_job.add_personunit(exx.yao)
    init_yao_job = planunit_shop(exx.yao, exx.a23)
    init_yao_job.add_personunit(exx.bob)
    init_bob_job = planunit_shop(exx.bob, exx.a23)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_keg(clean_rope, pledge=True)
    save_job_file(moment_mstr_dir, init_sue_job)
    save_job_file(moment_mstr_dir, init_yao_job)
    save_job_file(moment_mstr_dir, init_bob_job)
    assert len(a23_job(exx.sue).get_agenda_dict()) == 0
    assert len(a23_job(exx.yao).get_agenda_dict()) == 0
    assert len(a23_job(exx.bob).get_agenda_dict()) == 1

    # WHEN / THEN
    assert len(a23_moment.rotate_job(exx.sue).get_agenda_dict()) == 0
    assert len(a23_moment.rotate_job(exx.yao).get_agenda_dict()) == 1
    assert len(a23_moment.rotate_job(exx.bob).get_agenda_dict()) == 0


def test_MomentUnit_rotate_job_ReturnsObj_Scenario4_job_SelfReferenceWorks(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    init_bob_job = planunit_shop(exx.bob, exx.a23)
    init_bob_job.add_personunit(exx.bob)
    init_sue_job = planunit_shop(exx.sue, exx.a23)
    init_sue_job.add_personunit(exx.yao)
    init_yao_job = planunit_shop(exx.yao, exx.a23)
    init_yao_job.add_personunit(exx.bob)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_keg(clean_rope, pledge=True)
    save_job_file(moment_mstr_dir, init_sue_job)
    save_job_file(moment_mstr_dir, init_yao_job)
    save_job_file(moment_mstr_dir, init_bob_job)
    assert len(a23_job(exx.bob).get_agenda_dict()) == 1
    assert len(a23_job(exx.sue).get_agenda_dict()) == 0
    assert len(a23_job(exx.yao).get_agenda_dict()) == 0

    # WHEN / THEN
    assert len(a23_moment.rotate_job(exx.bob).get_agenda_dict()) == 1
    assert len(a23_moment.rotate_job(exx.sue).get_agenda_dict()) == 0
    assert len(a23_moment.rotate_job(exx.yao).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario0_init_job_IsCreated(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    bob_gut = planunit_shop(exx.bob, exx.a23)
    save_gut_file(moment_mstr_dir, bob_gut)
    sue_dir = create_plan_dir_path(moment_mstr_dir, exx.a23, exx.sue)
    set_dir(sue_dir)
    assert gut_file_exists(moment_mstr_dir, exx.a23, exx.bob)
    assert gut_file_exists(moment_mstr_dir, exx.a23, exx.sue) is False
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.bob) is False
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.sue) is False

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert gut_file_exists(moment_mstr_dir, exx.a23, exx.bob)
    assert gut_file_exists(moment_mstr_dir, exx.a23, exx.sue)
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.bob)
    assert job_file_exists(moment_mstr_dir, exx.a23, exx.sue)


def test_MomentUnit_generate_all_jobs_Scenario1_jobs_rotated(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, job_listen_rotations=1)
    bob_gut = planunit_shop(exx.bob, exx.a23)
    bob_gut.add_personunit(exx.bob)
    bob_gut.add_personunit(exx.sue)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_keg(clean_rope, pledge=True)

    sue_gut = planunit_shop(exx.sue, exx.a23)
    sue_gut.add_personunit(exx.sue)
    sue_gut.add_personunit(exx.bob)
    yao_gut = planunit_shop(exx.yao, exx.a23)
    yao_gut.add_personunit(exx.sue)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.bob)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.sue)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.yao)

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob).get_agenda_dict()) == 1
    assert len(a23_job(exx.sue).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario2_jobs_rotated_InSortedOrder(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, job_listen_rotations=1)
    bob_gut = planunit_shop(exx.bob, exx.a23)
    bob_gut.add_personunit(exx.bob)
    bob_gut.add_personunit(exx.sue)

    sue_gut = planunit_shop(exx.sue, exx.a23)
    sue_gut.add_personunit(exx.sue)
    sue_gut.add_personunit(exx.bob)
    sue_gut.add_personunit(exx.yao)

    yao_gut = planunit_shop(exx.yao, exx.a23)
    yao_gut.add_personunit(exx.sue)
    yao_gut.add_personunit(exx.yao)
    yao_gut.add_personunit(exx.zia)

    zia_gut = planunit_shop(exx.zia, exx.a23)
    zia_gut.add_personunit(exx.zia)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_keg(clean_rope, pledge=True)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    save_gut_file(moment_mstr_dir, zia_gut)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.bob)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.sue)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.yao)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.zia)

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob).get_agenda_dict()) == 0
    assert len(a23_job(exx.sue).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao).get_agenda_dict()) == 1
    assert len(a23_job(exx.zia).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario3_job_listen_rotation_AffectsJobs(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir, job_listen_rotations=1)
    bob_gut = planunit_shop(exx.bob, exx.a23)
    bob_gut.add_personunit(exx.bob)
    bob_gut.add_personunit(exx.sue)

    sue_gut = planunit_shop(exx.sue, exx.a23)
    sue_gut.add_personunit(exx.sue)
    sue_gut.add_personunit(exx.bob)
    sue_gut.add_personunit(exx.yao)

    yao_gut = planunit_shop(exx.yao, exx.a23)
    yao_gut.add_personunit(exx.sue)
    yao_gut.add_personunit(exx.yao)
    yao_gut.add_personunit(exx.zia)

    zia_gut = planunit_shop(exx.zia, exx.a23)
    zia_gut.add_personunit(exx.zia)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_keg(clean_rope, pledge=True)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    save_gut_file(moment_mstr_dir, zia_gut)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.bob)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.sue)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.yao)
    assert not job_file_exists(moment_mstr_dir, exx.a23, exx.zia)
    assert a23_moment.job_listen_rotations == 1

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob).get_agenda_dict()) == 0
    assert len(a23_job(exx.sue).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao).get_agenda_dict()) == 1
    assert len(a23_job(exx.zia).get_agenda_dict()) == 1

    # WHEN
    a23_moment.job_listen_rotations = 2
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(exx.bob).get_agenda_dict()) == 1
    assert len(a23_job(exx.sue).get_agenda_dict()) == 1
    assert len(a23_job(exx.yao).get_agenda_dict()) == 1
    assert len(a23_job(exx.zia).get_agenda_dict()) == 1
