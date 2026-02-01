from src.ch04_rope.rope import LabelTerm, RopeTerm, create_rope
from src.ch07_plan_logic.plan_main import PlanUnit, kegunit_shop, planunit_shop
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch09_plan_lesson.lesson_filehandler import (
    LessonFileHandler,
    gut_file_exists,
    lessonfilehandler_shop,
    save_gut_file,
)
from src.ch10_plan_listen.keep_tool import (
    get_vision_plan,
    job_file_exists,
    open_job_file,
    save_duty_plan,
    vision_file_exists,
)
from src.ch10_plan_listen.listen_main import (
    create_vision_file_from_duty_file,
    listen_to_plan_visions,
)
from src.ch10_plan_listen.test._util.ch10_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ch10_plan_listen.test._util.ch10_examples import (
    ch10_example_moment_rope,
    eat_str,
    full_str,
    get_texas_lessonfilehandler,
    get_texas_rope,
    hungry_str,
    run_str,
)
from src.ref.keywords import Ch10Keywords as kw, ExampleStrs as exx


def sanitation_str() -> str:
    return "sanitation"


def dirty_str() -> str:
    return "dirty"


def sweep_str() -> str:
    return "sweep"


def casa_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), exx.casa)


def cuisine_rope() -> RopeTerm:
    return create_rope(casa_rope(), exx.cuisine)


def eat_rope() -> RopeTerm:
    return create_rope(casa_rope(), eat_str())


def hungry_rope() -> RopeTerm:
    return create_rope(eat_rope(), hungry_str())


def full_rope() -> RopeTerm:
    return create_rope(eat_rope(), full_str())


def sanitation_rope() -> RopeTerm:
    return create_rope(casa_rope(), sanitation_str())


def clean_rope() -> RopeTerm:
    return create_rope(sanitation_rope(), exx.clean)


def dirty_rope() -> RopeTerm:
    return create_rope(sanitation_rope(), dirty_str())


def sweep_rope() -> RopeTerm:
    return create_rope(casa_rope(), sweep_str())


def run_rope() -> RopeTerm:
    return create_rope(casa_rope(), run_str())


def get_example_yao_plan() -> PlanUnit:
    yao_speaker = planunit_shop(exx.yao, ch10_example_moment_rope())
    yao_speaker.set_keg_obj(kegunit_shop(run_str()), casa_rope())
    yao_speaker.add_personunit(exx.yao, person_debt_lumen=10)
    yao_speaker.add_personunit(exx.zia, person_debt_lumen=30)
    yao_speaker.add_personunit(exx.bob, person_debt_lumen=40)
    yao_speaker.set_person_respect(80)
    return yao_speaker


def get_example_yao_vision1_speaker() -> PlanUnit:
    yao_speaker = get_example_yao_plan()
    yao_speaker.del_keg_obj(run_rope())
    yao_speaker.set_person_respect(40)
    yao_speaker.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), casa_rope())
    yao_speaker.set_keg_obj(kegunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_keg_obj(kegunit_shop(full_str()), eat_rope())
    cuisine_kegunit = yao_speaker.get_keg_obj(cuisine_rope())
    cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_speaker.edit_reason(cuisine_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())
    return yao_speaker


def get_example_yao_vision2_speaker() -> PlanUnit:
    yao_speaker = get_example_yao_plan()
    yao_speaker.del_keg_obj(run_rope())
    yao_speaker.set_person_respect(30)
    yao_speaker.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), casa_rope())
    yao_speaker.set_keg_obj(kegunit_shop(hungry_str()), eat_rope())
    yao_speaker.set_keg_obj(kegunit_shop(full_str()), eat_rope())
    cuisine_kegunit = yao_speaker.get_keg_obj(cuisine_rope())
    cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_speaker.edit_reason(cuisine_rope(), eat_rope(), hungry_rope())
    yao_speaker.add_fact(eat_rope(), hungry_rope())

    yao_speaker.set_keg_obj(kegunit_shop(sweep_str(), pledge=True), casa_rope())
    yao_speaker.set_keg_obj(kegunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_keg_obj(kegunit_shop(exx.clean), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_example_yao_vision3_speaker() -> PlanUnit:
    yao_speaker = get_example_yao_plan()
    yao_speaker.del_keg_obj(run_rope())
    yao_speaker.set_person_respect(10)
    yao_speaker.set_keg_obj(kegunit_shop(sweep_str(), pledge=True), casa_rope())
    yao_speaker.set_keg_obj(kegunit_shop(dirty_str()), sanitation_rope())
    yao_speaker.set_keg_obj(kegunit_shop(exx.clean), sanitation_rope())
    yao_speaker.edit_reason(sweep_rope(), sanitation_rope(), dirty_rope())
    yao_speaker.add_fact(sweep_rope(), dirty_rope())
    return yao_speaker


def get_usa_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), "USA")


def get_iowa_str() -> LabelTerm:
    return "Iowa"


def get_ohio_str() -> LabelTerm:
    return "Ohio"


def get_utah_str() -> LabelTerm:
    return "Utah"


def get_swim_str() -> LabelTerm:
    return "swim"


def get_location_str() -> LabelTerm:
    return "location"


def get_in_mer_str() -> LabelTerm:
    return "in_mer"


def get_on_land_str() -> LabelTerm:
    return "on_land"


def get_iowa_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_iowa_str())


def get_ohio_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_ohio_str())


def get_utah_rope() -> RopeTerm:
    return create_rope(get_usa_rope(), get_utah_str())


def get_swim_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), get_swim_str())


def get_location_rope() -> RopeTerm:
    return create_rope(ch10_example_moment_rope(), get_location_str())


def get_in_mer_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_in_mer_str())


def get_on_land_rope() -> RopeTerm:
    return create_rope(get_location_rope(), get_on_land_str())


def get_yao_ohio_lessonfilehandler() -> LessonFileHandler:
    yao_plan = get_example_yao_plan()
    return lessonfilehandler_shop(
        moment_mstr_dir=env_dir(),
        moment_rope=yao_plan.moment_rope,
        plan_name=yao_plan.plan_name,
    )


def get_yao_iowa_lessonfilehandler() -> LessonFileHandler:
    yao_plan = get_example_yao_plan()
    return lessonfilehandler_shop(
        moment_mstr_dir=env_dir(),
        moment_rope=yao_plan.moment_rope,
        plan_name=yao_plan.plan_name,
    )


def get_zia_utah_lessonfilehandler() -> LessonFileHandler:
    yao_plan = get_example_yao_plan()
    return lessonfilehandler_shop(
        moment_mstr_dir=env_dir(),
        moment_rope=yao_plan.moment_rope,
        plan_name="Zia",
    )


def get_example_yao_gut_with_3_healers():
    yao_gut = get_example_yao_plan()
    iowa_keg = kegunit_shop(get_iowa_str(), problem_bool=True)
    ohio_keg = kegunit_shop(get_ohio_str(), problem_bool=True)
    utah_keg = kegunit_shop(get_utah_str(), problem_bool=True)
    iowa_keg.healerunit.set_healer_name(get_yao_iowa_lessonfilehandler().plan_name)
    ohio_keg.healerunit.set_healer_name(get_yao_ohio_lessonfilehandler().plan_name)
    utah_keg.healerunit.set_healer_name(get_zia_utah_lessonfilehandler().plan_name)
    yao_gut.set_keg_obj(iowa_keg, get_usa_rope())
    yao_gut.set_keg_obj(ohio_keg, get_usa_rope())
    yao_gut.set_keg_obj(utah_keg, get_usa_rope())

    return yao_gut


def test_listen_to_plan_visions_Pipeline_Scenario1_yao_gut_CanOnlyReferenceItself(
    temp_dir_setup,
):
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    # yao0_gut with 3 debotors of different person_cred_lumens
    # yao_vision1 with 1 task, fact that doesn't make that task active
    # yao_vision2 with 2 tasks, one is equal fact that makes task active
    # yao_vision3 with 1 new task, fact stays with it
    moment_mstr_dir = env_dir()
    moment_rope = ch10_example_moment_rope()
    yao_gut0 = get_example_yao_gut_with_3_healers()
    yao_gut0.set_l1_keg(kegunit_shop(get_location_str()))
    yao_gut0.set_keg_obj(kegunit_shop(get_in_mer_str()), get_location_rope())
    yao_gut0.set_keg_obj(kegunit_shop(get_on_land_str()), get_location_rope())
    yao_gut0.set_l1_keg(kegunit_shop(get_swim_str(), pledge=True))
    yao_gut0.edit_reason(get_swim_rope(), get_location_rope(), get_in_mer_rope())
    yao_gut0.add_fact(get_location_rope(), get_in_mer_rope())
    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    yao_gut0.del_keg_obj(run_rope())
    assert yao_gut0._keep_dict.get(get_iowa_rope())
    assert yao_gut0._keep_dict.get(get_ohio_rope())
    assert yao_gut0._keep_dict.get(get_utah_rope())
    yao_gut0.cashout()
    assert len(yao_gut0._keep_dict) == 3
    # print(f"{yao_gut0._keg_dict.keys()=}")

    yao_vision1 = get_example_yao_vision1_speaker()
    yao_vision2 = get_example_yao_vision2_speaker()
    yao_vision3 = get_example_yao_vision3_speaker()
    yao_iowa_lessonfilehandler = get_yao_iowa_lessonfilehandler()
    yao_ohio_lessonfilehandler = get_yao_ohio_lessonfilehandler()
    zia_utah_lessonfilehandler = get_zia_utah_lessonfilehandler()
    # delete_dir(yao_iowa_lessonfilehandler.plans_dir())
    moment_lasso = lassounit_shop(moment_rope)
    assert gut_file_exists(moment_mstr_dir, moment_lasso, exx.yao) is False
    assert job_file_exists(moment_mstr_dir, moment_lasso, exx.yao) is False
    assert (
        vision_file_exists(
            yao_iowa_lessonfilehandler.moment_mstr_dir,
            yao_iowa_lessonfilehandler.plan_name,
            yao_iowa_lessonfilehandler.moment_rope,
            get_iowa_rope(),
            yao_iowa_lessonfilehandler.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            yao_ohio_lessonfilehandler.moment_mstr_dir,
            yao_ohio_lessonfilehandler.plan_name,
            yao_ohio_lessonfilehandler.moment_rope,
            get_ohio_rope(),
            yao_ohio_lessonfilehandler.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            zia_utah_lessonfilehandler.moment_mstr_dir,
            zia_utah_lessonfilehandler.plan_name,
            zia_utah_lessonfilehandler.moment_rope,
            get_utah_rope(),
            zia_utah_lessonfilehandler.knot,
            exx.yao,
        )
        is False
    )

    print(f"{yao_gut0.get_fact(get_location_rope())=}")
    save_gut_file(env_dir(), yao_gut0)
    assert gut_file_exists(moment_mstr_dir, moment_lasso, exx.yao)
    assert (
        vision_file_exists(
            yao_iowa_lessonfilehandler.moment_mstr_dir,
            yao_iowa_lessonfilehandler.plan_name,
            yao_iowa_lessonfilehandler.moment_rope,
            get_iowa_rope(),
            yao_iowa_lessonfilehandler.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            yao_ohio_lessonfilehandler.moment_mstr_dir,
            yao_ohio_lessonfilehandler.plan_name,
            yao_ohio_lessonfilehandler.moment_rope,
            get_ohio_rope(),
            yao_ohio_lessonfilehandler.knot,
            exx.yao,
        )
        is False
    )
    assert (
        vision_file_exists(
            zia_utah_lessonfilehandler.moment_mstr_dir,
            zia_utah_lessonfilehandler.plan_name,
            zia_utah_lessonfilehandler.moment_rope,
            get_utah_rope(),
            zia_utah_lessonfilehandler.knot,
            exx.yao,
        )
        is False
    )
    # WHEN / THEN
    assert job_file_exists(moment_mstr_dir, moment_lasso, exx.yao) is False
    listen_to_plan_visions(yao_iowa_lessonfilehandler, get_iowa_rope())
    assert job_file_exists(moment_mstr_dir, moment_lasso, exx.yao)

    yao_job = open_job_file(moment_mstr_dir, moment_lasso, exx.yao)
    yao_job.cashout()
    assert yao_job.persons.keys() == yao_gut0.persons.keys()
    assert yao_job.get_person(exx.yao).irrational_person_debt_lumen == 0
    yao_job_persons = yao_job.to_dict().get(kw.persons)
    yao_gut0_persons = yao_gut0.to_dict().get(kw.persons)
    yao_job_bob = yao_job_persons.get("Bob")
    yao_gut0_bob = yao_gut0_persons.get("Bob")
    print(f"{yao_job_bob=}")
    print(f"{yao_gut0_bob=}")
    assert yao_job_bob == yao_gut0_bob
    assert yao_job_persons.keys() == yao_gut0_persons.keys()
    assert yao_job_persons == yao_gut0_persons
    assert len(yao_job.to_dict().get(kw.persons)) == 3
    assert len(yao_job._keg_dict) == 4
    print(f"{yao_job._keg_dict.keys()=}")
    print(f"{yao_job.get_kegroot_factunits_dict().keys()=}")
    assert yao_job.keg_exists(cuisine_rope()) is False
    assert yao_job.keg_exists(clean_rope()) is False
    assert yao_job.keg_exists(run_rope()) is False
    assert yao_job.keg_exists(get_swim_rope())
    assert yao_job.keg_exists(get_in_mer_rope())
    assert yao_job.keg_exists(get_on_land_rope()) is False
    assert yao_job.get_fact(get_location_rope()) is not None
    assert yao_job.get_fact(get_location_rope()).fact_state == get_in_mer_rope()
    assert len(yao_job.get_agenda_dict()) == 1
    assert len(yao_job.kegroot.factunits) == 1
    assert yao_job != yao_gut0


def test_create_vision_file_from_duty_file_CreatesEmptyvision(temp_dir_setup):
    # ESTABLISH
    yao_duty = planunit_shop(exx.yao)
    sue_texas_lessonfilehandler = get_texas_lessonfilehandler()
    save_duty_plan(
        moment_mstr_dir=sue_texas_lessonfilehandler.moment_mstr_dir,
        plan_name=sue_texas_lessonfilehandler.plan_name,
        moment_rope=sue_texas_lessonfilehandler.moment_rope,
        keep_rope=get_texas_rope(),
        knot=None,
        duty_plan=yao_duty,
    )

    assert not (
        vision_file_exists(
            sue_texas_lessonfilehandler.moment_mstr_dir,
            sue_texas_lessonfilehandler.plan_name,
            sue_texas_lessonfilehandler.moment_rope,
            get_texas_rope(),
            sue_texas_lessonfilehandler.knot,
            exx.yao,
        )
    )

    # WHEN
    print(f"{sue_texas_lessonfilehandler.moment_rope=}")
    create_vision_file_from_duty_file(
        sue_texas_lessonfilehandler, exx.yao, get_texas_rope()
    )

    # THEN
    assert vision_file_exists(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.plan_name,
        sue_texas_lessonfilehandler.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.knot,
        exx.yao,
    )
    yao_vision = get_vision_plan(
        sue_texas_lessonfilehandler.moment_mstr_dir,
        sue_texas_lessonfilehandler.plan_name,
        sue_texas_lessonfilehandler.moment_rope,
        get_texas_rope(),
        sue_texas_lessonfilehandler.knot,
        exx.yao,
    )
    assert yao_vision.plan_name is not None
    assert yao_vision.plan_name == exx.yao
    assert yao_vision.to_dict() == yao_duty.to_dict()
