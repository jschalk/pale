from src.ch04_rope.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch07_plan_logic.plan_main import PlanUnit, kegunit_shop, planunit_shop
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch09_plan_lesson.lesson_filehandler import (
    LessonFileHandler,
    lessonfilehandler_shop,
)
from src.ch09_plan_lesson.test._util.ch09_examples import get_texas_rope
from src.ch10_plan_listen.test._util.ch10_env import get_temp_dir
from src.ref.keywords import Ch10Keywords as kw, ExampleStrs as exx


def ch10_example_moment_rope() -> str:
    return ";Buzz;"


def eat_str() -> str:
    return "eat"


def hungry_str() -> str:
    return "hungry"


def full_str() -> str:
    return "full"


def run_str() -> str:
    return "run"


def a23_casa_rope() -> RopeTerm:
    return create_rope(exx.a23, exx.casa)


def a23_cuisine_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), exx.cuisine)


def a23_eat_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), eat_str())


def a23_hungry_rope() -> RopeTerm:
    return create_rope(a23_eat_rope(), hungry_str())


def a23_full_rope() -> RopeTerm:
    return create_rope(a23_eat_rope(), full_str())


def a23_clean_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), exx.clean)


def a23_run_rope() -> RopeTerm:
    return create_rope(a23_casa_rope(), run_str())


def get_example_zia_speaker() -> PlanUnit:
    zia_speaker = planunit_shop(exx.zia, exx.a23)
    zia_speaker.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    zia_speaker.set_keg_obj(kegunit_shop(hungry_str()), a23_eat_rope())
    zia_speaker.set_keg_obj(kegunit_shop(full_str()), a23_eat_rope())
    zia_speaker.add_personunit(exx.yao, person_debt_lumen=12)
    cuisine_kegunit = zia_speaker.get_keg_obj(a23_cuisine_rope())
    cuisine_kegunit.laborunit.add_party(exx.yao)
    zia_speaker.edit_keg_attr(
        a23_cuisine_rope(), reason_context=a23_eat_rope(), reason_case=a23_hungry_rope()
    )
    zia_speaker.add_fact(a23_eat_rope(), a23_full_rope())
    zia_speaker.set_person_respect(100)
    return zia_speaker


def get_example_bob_speaker() -> PlanUnit:
    bob_speaker = planunit_shop(exx.bob, exx.a23)
    bob_speaker.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    bob_speaker.set_keg_obj(kegunit_shop(hungry_str()), a23_eat_rope())
    bob_speaker.set_keg_obj(kegunit_shop(full_str()), a23_eat_rope())
    bob_speaker.add_personunit(exx.yao, person_debt_lumen=12)
    cuisine_kegunit = bob_speaker.get_keg_obj(a23_cuisine_rope())
    cuisine_kegunit.laborunit.add_party(exx.yao)
    bob_speaker.edit_keg_attr(
        a23_cuisine_rope(), reason_context=a23_eat_rope(), reason_case=a23_hungry_rope()
    )
    bob_speaker.add_fact(a23_eat_rope(), a23_hungry_rope())
    bob_speaker.set_person_respect(100)
    return bob_speaker


def get_example_yao_speaker() -> PlanUnit:
    yao_speaker = planunit_shop(exx.yao, exx.a23)
    yao_speaker.add_personunit(exx.yao, person_debt_lumen=12)
    yao_speaker.add_personunit(exx.zia, person_debt_lumen=36)
    yao_speaker.add_personunit(exx.bob, person_debt_lumen=48)
    yao_speaker.set_person_respect(100)
    yao_speaker.set_keg_obj(kegunit_shop(exx.cuisine, pledge=True), a23_casa_rope())
    yao_speaker.set_keg_obj(kegunit_shop(hungry_str()), a23_eat_rope())
    yao_speaker.set_keg_obj(kegunit_shop(full_str()), a23_eat_rope())
    cuisine_kegunit = yao_speaker.get_keg_obj(a23_cuisine_rope())
    cuisine_kegunit.laborunit.add_party(exx.yao)
    yao_speaker.edit_keg_attr(
        a23_cuisine_rope(), reason_context=a23_eat_rope(), reason_case=a23_hungry_rope()
    )
    yao_speaker.add_fact(a23_eat_rope(), a23_hungry_rope())
    return yao_speaker


def get_texas_lessonfilehandler() -> LessonFileHandler:
    moment_lasso = lassounit_shop(ch10_example_moment_rope())
    return lessonfilehandler_shop(get_temp_dir(), moment_lasso, plan_name="Sue")


def get_dakota_rope() -> RopeTerm:
    moment_rope = ch10_example_moment_rope()
    nation_str = "nation"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_rope_from_labels([moment_rope, nation_str, usa_str, dakota_str])


def get_dakota_lessonfilehandler() -> LessonFileHandler:
    moment_lasso = lassounit_shop(ch10_example_moment_rope())
    return lessonfilehandler_shop(get_temp_dir(), moment_lasso, plan_name="Sue")


def get_fund_breakdown_plan() -> PlanUnit:
    sue_plan = planunit_shop(plan_name="Sue")

    casa_rope = sue_plan.make_l1_rope(exx.casa)
    cat_str = "cat situation"
    cat_rope = sue_plan.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_y_str = "hungry"
    clean_str = "cleaning"
    clean_rope = sue_plan.make_rope(casa_rope, clean_str)
    sweep_str = "sweep floor"
    dish_str = "clean dishes"
    sue_plan.set_l1_keg(kegunit_shop(exx.casa, star=30))
    sue_plan.set_keg_obj(kegunit_shop(cat_str, star=30), casa_rope)
    sue_plan.set_keg_obj(kegunit_shop(hun_n_str, star=30), cat_rope)
    sue_plan.set_keg_obj(kegunit_shop(hun_y_str, star=30), cat_rope)
    sue_plan.set_keg_obj(kegunit_shop(clean_str, star=30), casa_rope)
    sue_plan.set_keg_obj(kegunit_shop(sweep_str, star=30, pledge=True), clean_rope)
    sue_plan.set_keg_obj(kegunit_shop(dish_str, star=30, pledge=True), clean_rope)

    cat_str = "cat have dinner"
    sue_plan.set_l1_keg(kegunit_shop(cat_str, star=30, pledge=True))

    return sue_plan
