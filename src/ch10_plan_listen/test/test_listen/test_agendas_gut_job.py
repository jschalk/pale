from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import delete_dir
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import create_gut_path
from src.ch09_plan_lesson.lesson_filehandler import (
    lessonfilehandler_shop,
    save_gut_file,
)
from src.ch10_plan_listen.keep_tool import save_job_file
from src.ch10_plan_listen.listen_main import (
    create_listen_basis,
    listen_to_agendas_jobs_into_job,
)
from src.ch10_plan_listen.test._util.ch10_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ch10_plan_listen.test._util.ch10_examples import (
    a23_casa_rope,
    a23_clean_rope,
    a23_cuisine_rope,
    a23_eat_rope,
    a23_hungry_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_agendas_jobs_into_job_AddstasksToPlanWhenNo_partyunitIsSet(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    yao_gut = planunit_shop(exx.yao, exx.a23)
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    zia_pool = 87
    yao_gut.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.set_voice_respect(zia_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_job = planunit_shop(exx.zia, exx.a23)
    zia_job.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_voiceunit(exx.yao, voice_debt_lumen=12)
    save_job_file(moment_mstr_dir, zia_job)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_keg_dict())=}")
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddstasksToPlan(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    yao_gut = planunit_shop(exx.yao, exx.a23)
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    zia_pool = 87
    yao_gut.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.set_voice_respect(zia_pool)
    save_job_file(moment_mstr_dir, yao_gut)

    zia_job = planunit_shop(exx.zia, exx.a23)
    zia_job.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_voiceunit(exx.yao, voice_debt_lumen=12)
    clean_kegunit = zia_job.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_job.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_keg_dict())=}")
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddstasksToPlanWithDetailsDecidedBy_voice_debt_lumen(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    zia_job = get_example_zia_speaker()
    bob_job = get_example_bob_speaker()
    bob_job.edit_keg_attr(
        a23_cuisine_rope(),
        reason_del_case_reason_context=a23_eat_rope(),
        reason_del_case_reason_state=a23_hungry_rope(),
    )
    bob_cuisine_kegunit = bob_job.get_keg_obj(a23_cuisine_rope())
    zia_cuisine_kegunit = zia_job.get_keg_obj(a23_cuisine_rope())
    assert bob_cuisine_kegunit != zia_cuisine_kegunit
    assert len(zia_cuisine_kegunit.reasonunits) == 1
    assert len(bob_cuisine_kegunit.reasonunits) == 0
    save_job_file(moment_mstr_dir, zia_job)
    save_job_file(moment_mstr_dir, bob_job)

    yao_gut = get_example_yao_speaker()
    save_gut_file(moment_mstr_dir, yao_gut)

    new_yao_job1 = create_listen_basis(yao_gut)
    assert new_yao_job1.keg_exists(a23_cuisine_rope()) is False

    # WHEN
    yao_lessonfilehandler = lessonfilehandler_shop(moment_mstr_dir, exx.a23, exx.yao)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job1)

    # THEN
    assert new_yao_job1.keg_exists(a23_cuisine_rope())
    new_cuisine_keg = new_yao_job1.get_keg_obj(a23_cuisine_rope())
    zia_voiceunit = new_yao_job1.get_voice(exx.zia)
    bob_voiceunit = new_yao_job1.get_voice(exx.bob)
    assert zia_voiceunit.voice_debt_lumen < bob_voiceunit.voice_debt_lumen
    assert new_cuisine_keg.get_reasonunit(a23_eat_rope()) is None

    yao_zia_voice_debt_lumen = 15
    yao_bob_voice_debt_lumen = 5
    yao_gut.add_voiceunit(exx.zia, None, yao_zia_voice_debt_lumen)
    yao_gut.add_voiceunit(exx.bob, None, yao_bob_voice_debt_lumen)
    yao_gut.set_voice_respect(100)
    new_yao_job2 = create_listen_basis(yao_gut)
    assert new_yao_job2.keg_exists(a23_cuisine_rope()) is False

    # WHEN
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job2)

    # THEN
    assert new_yao_job2.keg_exists(a23_cuisine_rope())
    new_cuisine_keg = new_yao_job2.get_keg_obj(a23_cuisine_rope())
    zia_voiceunit = new_yao_job2.get_voice(exx.zia)
    bob_voiceunit = new_yao_job2.get_voice(exx.bob)
    assert zia_voiceunit.voice_debt_lumen > bob_voiceunit.voice_debt_lumen
    zia_eat_reasonunit = zia_cuisine_kegunit.get_reasonunit(a23_eat_rope())
    assert new_cuisine_keg.get_reasonunit(a23_eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_jobs_into_job_ProcessesIrrationalPlan(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    yao_gut = planunit_shop(exx.yao, exx.a23)
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    sue_voice_cred_lumen = 57
    sue_voice_debt_lumen = 51
    yao_gut.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_gut.set_voice_respect(yao_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_job = planunit_shop(exx.zia, exx.a23)
    zia_job.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_voiceunit(exx.yao, voice_debt_lumen=12)
    clean_kegunit = zia_job.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_job.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)

    sue_job = planunit_shop(exx.sue, exx.a23)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_voiceunit(exx.yao, voice_debt_lumen=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_job.make_l1_rope(vacuum_str)
    sue_job.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = sue_job.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_job.make_l1_rope(egg_str)
    sue_job.set_l1_keg(kegunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_job.make_l1_rope(chicken_str)
    sue_job.set_l1_keg(kegunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_job.edit_keg_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_job.edit_keg_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    save_job_file(moment_mstr_dir, sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN irrational plan is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_voiceunit = new_yao_job.get_voice(exx.zia)
    sue_voiceunit = new_yao_job.get_voice(exx.sue)
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.irrational_voice_debt_lumen=}")
    assert zia_voiceunit.irrational_voice_debt_lumen == 0
    assert sue_voiceunit.irrational_voice_debt_lumen == 51


def test_listen_to_agendas_jobs_into_job_ProcessesMissingDebtorPlan(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    yao_gut_path = create_gut_path(moment_mstr_dir, exx.a23, exx.yao)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = planunit_shop(exx.yao, exx.a23)
    zia_voice_cred_lumen = 47
    sue_voice_cred_lumen = 57
    zia_voice_debt_lumen = 41
    sue_voice_debt_lumen = 51
    yao_gut.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.add_voiceunit(exx.sue, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_gut.set_voice_respect(yao_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_job = planunit_shop(exx.zia, exx.a23)
    zia_job.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_voiceunit(exx.yao, voice_debt_lumen=12)
    clean_kegunit = zia_job.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_job.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN irrational plan is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_voiceunit = new_yao_job.get_voice(exx.zia)
    sue_voiceunit = new_yao_job.get_voice(exx.sue)
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.inallocable_voice_debt_lumen=}")
    assert zia_voiceunit.inallocable_voice_debt_lumen == 0
    assert sue_voiceunit.inallocable_voice_debt_lumen == 51


def test_listen_to_agendas_jobs_into_job_ListensToPlan_gut_AndNotPlan_job(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    yao_gut = planunit_shop(exx.yao, exx.a23)
    yao_voice_cred_lumen = 57
    yao_voice_debt_lumen = 51
    yao_gut.add_voiceunit(exx.yao, yao_voice_cred_lumen, yao_voice_debt_lumen)
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    yao_gut.add_voiceunit(exx.zia, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_pool = 87
    yao_gut.set_voice_respect(yao_pool)
    # save yao without task to dutys
    save_gut_file(moment_mstr_dir, yao_gut)

    # Save Zia to job
    zia_job = planunit_shop(exx.zia, exx.a23)
    zia_job.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_job.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_job.add_voiceunit(exx.yao, voice_debt_lumen=12)
    clean_kegunit = zia_job.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_job.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    save_job_file(moment_mstr_dir, zia_job)

    # save yao with task to dutys
    yao_old_job = planunit_shop(exx.yao, exx.a23)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_job.make_l1_rope(vacuum_str)
    yao_old_job.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = yao_old_job.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)
    save_job_file(moment_mstr_dir, yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(moment_mstr_dir, new_yao_job)

    # THEN irrational plan is ignored
    assert len(new_yao_job.get_agenda_dict()) != 2
    assert len(new_yao_job.get_agenda_dict()) == 3
