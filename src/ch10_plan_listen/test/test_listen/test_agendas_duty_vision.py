from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch09_plan_lesson.lesson_filehandler import lessonfilehandler_shop
from src.ch10_plan_listen.keep_tool import save_duty_plan, save_vision_plan
from src.ch10_plan_listen.listen_main import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
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
    a23_run_rope,
    get_dakota_lessonfilehandler,
    get_dakota_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    run_str,
)
from src.ref.keywords import ExampleStrs as exx


def test_listen_to_agenda_duty_vision_agenda_AddstasksTovision_PlanWhenNo_partyunitIsSet(
    temp_dir_setup,
):
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao, exx.a23)
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    zia_pool = 87
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_duty.set_person_respect(zia_pool)

    zia_vision = planunit_shop(exx.zia, exx.a23)
    zia_vision.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_personunit(exx.yao, person_debt_lumen=12)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.yao)
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        zia_vision,
    )
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_keg_dict())=}")
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_AddstasksTovision_Plan(
    temp_dir_setup,
):
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao, exx.a23)
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    zia_pool = 87
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_duty.set_person_respect(zia_pool)

    zia_vision = planunit_shop(exx.zia, exx.a23)
    zia_vision.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_personunit(exx.yao, person_debt_lumen=12)
    clean_kegunit = zia_vision.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_vision.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.yao)
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        zia_vision,
    )

    # zia_file_path = create_path(visions_path, exx.zia}.json")
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_keg_dict())=}")
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_AddstasksTovisionPlanWithDetailsDecidedBy_person_debt_lumen(
    temp_dir_setup,
):
    # ESTABLISH
    zia_vision = get_example_zia_speaker()
    bob_vision = get_example_bob_speaker()
    bob_vision.edit_keg_attr(
        a23_cuisine_rope(),
        reason_del_case_reason_context=a23_eat_rope(),
        reason_del_case_reason_state=a23_hungry_rope(),
    )
    bob_cuisine_kegunit = bob_vision.get_keg_obj(a23_cuisine_rope())
    zia_cuisine_kegunit = zia_vision.get_keg_obj(a23_cuisine_rope())
    assert bob_cuisine_kegunit != zia_cuisine_kegunit
    assert len(zia_cuisine_kegunit.reasonunits) == 1
    assert len(bob_cuisine_kegunit.reasonunits) == 0
    sue_dakota_lessonfilehandler = get_dakota_lessonfilehandler()
    save_vision_plan(
        sue_dakota_lessonfilehandler.moment_mstr_dir,
        sue_dakota_lessonfilehandler.plan_name,
        sue_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        sue_dakota_lessonfilehandler.knot,
        zia_vision,
    )
    save_vision_plan(
        sue_dakota_lessonfilehandler.moment_mstr_dir,
        sue_dakota_lessonfilehandler.plan_name,
        sue_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        sue_dakota_lessonfilehandler.knot,
        bob_vision,
    )

    yao_duty = get_example_yao_speaker()
    save_duty_plan(
        moment_mstr_dir=sue_dakota_lessonfilehandler.moment_mstr_dir,
        plan_name=sue_dakota_lessonfilehandler.plan_name,
        moment_rope=sue_dakota_lessonfilehandler.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_plan=yao_duty,
    )
    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.keg_exists(a23_cuisine_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(
        new_yao_job1, sue_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert new_yao_job1.keg_exists(a23_cuisine_rope())
    new_cuisine_keg = new_yao_job1.get_keg_obj(a23_cuisine_rope())
    zia_personunit = new_yao_job1.get_person(exx.zia)
    bob_personunit = new_yao_job1.get_person(exx.bob)
    assert zia_personunit.person_debt_lumen < bob_personunit.person_debt_lumen
    assert new_cuisine_keg.get_reasonunit(a23_eat_rope()) is None

    yao_zia_person_debt_lumen = 15
    yao_bob_person_debt_lumen = 5
    yao_duty.add_personunit(exx.zia, None, yao_zia_person_debt_lumen)
    yao_duty.add_personunit(exx.bob, None, yao_bob_person_debt_lumen)
    yao_duty.set_person_respect(100)
    new_yao_job2 = create_listen_basis(yao_duty)
    assert new_yao_job2.keg_exists(a23_cuisine_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(
        new_yao_job2, sue_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert new_yao_job2.keg_exists(a23_cuisine_rope())
    new_cuisine_keg = new_yao_job2.get_keg_obj(a23_cuisine_rope())
    zia_personunit = new_yao_job2.get_person(exx.zia)
    bob_personunit = new_yao_job2.get_person(exx.bob)
    assert zia_personunit.person_debt_lumen > bob_personunit.person_debt_lumen
    zia_eat_reasonunit = zia_cuisine_kegunit.get_reasonunit(a23_eat_rope())
    assert new_cuisine_keg.get_reasonunit(a23_eat_rope()) == zia_eat_reasonunit


def test_listen_to_agenda_duty_vision_agenda_ProcessesIrrationalPlan(
    temp_dir_setup,
):
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao, exx.a23)
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    sue_person_cred_lumen = 57
    sue_person_debt_lumen = 51
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_duty.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    yao_pool = 92
    yao_duty.set_person_respect(yao_pool)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.yao)
    save_duty_plan(
        moment_mstr_dir=yao_dakota_lessonfilehandler.moment_mstr_dir,
        plan_name=yao_dakota_lessonfilehandler.plan_name,
        moment_rope=yao_dakota_lessonfilehandler.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_plan=yao_duty,
    )

    zia_vision = planunit_shop(exx.zia, exx.a23)
    zia_vision.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_personunit(exx.yao, person_debt_lumen=12)
    clean_kegunit = zia_vision.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_vision.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        zia_vision,
    )

    sue_vision = planunit_shop(exx.sue)
    sue_vision.set_max_tree_traverse(5)
    zia_vision.add_personunit(exx.yao, person_debt_lumen=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_vision.make_l1_rope(vacuum_str)
    sue_vision.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = sue_vision.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)

    egg_str = "egg first"
    egg_rope = sue_vision.make_l1_rope(egg_str)
    sue_vision.set_l1_keg(kegunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_vision.make_l1_rope(chicken_str)
    sue_vision.set_l1_keg(kegunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_vision.edit_keg_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_vision.edit_keg_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        sue_vision,
    )

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN irrational plan is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_personunit = new_yao_vision.get_person(exx.zia)
    sue_personunit = new_yao_vision.get_person(exx.sue)
    print(f"{sue_personunit.person_debt_lumen=}")
    print(f"{sue_personunit.irrational_person_debt_lumen=}")
    assert zia_personunit.irrational_person_debt_lumen == 0
    assert sue_personunit.irrational_person_debt_lumen == 51


def test_listen_to_agenda_duty_vision_agenda_ProcessesMissingDebtorvisionPlan(
    temp_dir_setup,
):
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao, exx.a23)
    zia_person_cred_lumen = 47
    sue_person_cred_lumen = 57
    zia_person_debt_lumen = 41
    sue_person_debt_lumen = 51
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_duty.add_personunit(exx.sue, sue_person_cred_lumen, sue_person_debt_lumen)
    yao_pool = 92
    yao_duty.set_person_respect(yao_pool)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.yao)
    save_duty_plan(
        moment_mstr_dir=yao_dakota_lessonfilehandler.moment_mstr_dir,
        plan_name=yao_dakota_lessonfilehandler.plan_name,
        moment_rope=yao_dakota_lessonfilehandler.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_plan=yao_duty,
    )

    zia_vision = planunit_shop(exx.zia, exx.a23)
    zia_vision.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_personunit(exx.yao, person_debt_lumen=12)
    clean_kegunit = zia_vision.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_vision.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.yao)
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        zia_vision,
    )

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN irrational plan is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_personunit = new_yao_vision.get_person(exx.zia)
    sue_personunit = new_yao_vision.get_person(exx.sue)
    print(f"{sue_personunit.person_debt_lumen=}")
    print(f"{sue_personunit.inallocable_person_debt_lumen=}")
    assert zia_personunit.inallocable_person_debt_lumen == 0
    assert sue_personunit.inallocable_person_debt_lumen == 51


def test_listen_to_agenda_duty_vision_agenda_ListensToPlan_duty_AndNotPlan_vision(
    temp_dir_setup,
):
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao, exx.a23)
    yao_person_cred_lumen = 57
    yao_person_debt_lumen = 51
    yao_duty.add_personunit(exx.yao, yao_person_cred_lumen, yao_person_debt_lumen)
    zia_person_cred_lumen = 47
    zia_person_debt_lumen = 41
    yao_duty.add_personunit(exx.zia, zia_person_cred_lumen, zia_person_debt_lumen)
    yao_pool = 87
    yao_duty.set_person_respect(yao_pool)
    # save yao without task to dutys
    yao_dakota_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.yao)
    save_duty_plan(
        moment_mstr_dir=yao_dakota_lessonfilehandler.moment_mstr_dir,
        plan_name=yao_dakota_lessonfilehandler.plan_name,
        moment_rope=yao_dakota_lessonfilehandler.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_plan=yao_duty,
    )

    # Save Zia to visions
    zia_vision = planunit_shop(exx.zia, exx.a23)
    zia_vision.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    zia_vision.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_vision.add_personunit(exx.yao, person_debt_lumen=12)
    clean_kegunit = zia_vision.get_keg_obj(a23_clean_rope())
    cuisine_kegunit = zia_vision.get_keg_obj(a23_cuisine_rope())
    clean_kegunit.laborunit.add_party(exx.yao)
    cuisine_kegunit.laborunit.add_party(exx.yao)
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        zia_vision,
    )

    # save yao with task to visions
    yao_old_vision = planunit_shop(exx.yao, exx.a23)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_vision.make_l1_rope(vacuum_str)
    yao_old_vision.set_l1_keg(kegunit_shop(vacuum_str, pledge=True))
    vacuum_kegunit = yao_old_vision.get_keg_obj(vacuum_rope)
    vacuum_kegunit.laborunit.add_party(exx.yao)
    save_vision_plan(
        yao_dakota_lessonfilehandler.moment_mstr_dir,
        yao_dakota_lessonfilehandler.plan_name,
        yao_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        yao_dakota_lessonfilehandler.knot,
        yao_old_vision,
    )

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(
        new_yao_vision, yao_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN irrational plan is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_GetsAgendaFromSrcPlanNotSpeakerSelf(
    temp_dir_setup,
):
    # ESTABLISH
    # yao_duty has task run_rope
    # yao_vision has task a23_clean_rope
    # yao_new_vision fact_states yao_duty task run_rope and not a23_clean_rope
    yao_duty = get_example_yao_speaker()
    assert yao_duty.keg_exists(a23_run_rope()) is False
    assert yao_duty.keg_exists(a23_clean_rope()) is False
    yao_duty.set_keg_obj(kegunit_shop(run_str(), pledge=True), a23_casa_rope())
    sue_dakota_lessonfilehandler = get_dakota_lessonfilehandler()
    save_duty_plan(
        moment_mstr_dir=sue_dakota_lessonfilehandler.moment_mstr_dir,
        plan_name=sue_dakota_lessonfilehandler.plan_name,
        moment_rope=sue_dakota_lessonfilehandler.moment_rope,
        keep_rope=get_dakota_rope(),
        knot=None,
        duty_plan=yao_duty,
    )
    yao_old_vision = get_example_yao_speaker()
    assert yao_old_vision.keg_exists(a23_run_rope()) is False
    assert yao_old_vision.keg_exists(a23_clean_rope()) is False
    yao_old_vision.set_keg_obj(kegunit_shop(exx.clean, pledge=True), a23_casa_rope())
    save_vision_plan(
        sue_dakota_lessonfilehandler.moment_mstr_dir,
        sue_dakota_lessonfilehandler.plan_name,
        sue_dakota_lessonfilehandler.moment_rope,
        get_dakota_rope(),
        sue_dakota_lessonfilehandler.knot,
        yao_old_vision,
    )

    yao_new_vision = create_listen_basis(yao_duty)
    assert yao_new_vision.keg_exists(a23_run_rope()) is False
    assert yao_new_vision.keg_exists(a23_clean_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(
        yao_new_vision, sue_dakota_lessonfilehandler, get_dakota_rope()
    )

    # THEN
    assert yao_new_vision.keg_exists(a23_clean_rope()) is False
    assert yao_new_vision.keg_exists(a23_run_rope())
