from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_plan_logic.test._util.ch07_examples import get_planunit_with_4_levels
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch09_plan_lesson.lesson_filehandler import lessonfilehandler_shop
from src.ch10_plan_listen.keep_tool import (
    get_dw_perspective_plan,
    get_perspective_plan,
    rj_perspective_plan,
    save_job_file,
    save_vision_plan,
)
from src.ch10_plan_listen.test._util.ch10_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_perspective_plan_ReturnsPlanWith_plan_nameSetToLessonFileHandler_plan_name():
    # ESTABLISH
    bob_planunit = get_planunit_with_4_levels()
    bob_planunit.set_plan_name(exx.bob)

    # WHEN
    perspective_planunit = get_perspective_plan(bob_planunit, exx.sue)

    # THEN
    assert perspective_planunit.to_dict() != bob_planunit.to_dict()
    assert perspective_planunit.plan_name == exx.sue
    perspective_planunit.set_plan_name(exx.bob)
    assert perspective_planunit.to_dict() == bob_planunit.to_dict()


def test_get_dw_perspective_plan_ReturnsPlanWith_plan_nameSetToLessonFileHandler_plan_name(
    temp_dir_setup,
):
    # ESTABLISH
    bob_planunit = get_planunit_with_4_levels()
    bob_planunit.set_plan_name(exx.bob)
    a23_lasso = lassounit_shop(exx.a23)
    bob_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_lasso, exx.bob)
    save_job_file(bob_lessonfilehandler.moment_mstr_dir, bob_planunit)

    # WHEN
    perspective_planunit = get_dw_perspective_plan(env_dir(), exx.a23, exx.bob, exx.sue)

    # THEN
    assert perspective_planunit.plan_name == exx.sue
    assert perspective_planunit.to_dict() != bob_planunit.to_dict()
    perspective_planunit.set_plan_name(exx.bob)
    assert perspective_planunit.to_dict() == bob_planunit.to_dict()


def test_rj_perspective_plan_ReturnsPlanWith_plan_nameSetToLessonFileHandler_plan_name(
    temp_dir_setup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(exx.a23, nation_str)
    iowa_rope = create_rope(nation_rope, "Iowa")

    yao_planunit = get_planunit_with_4_levels()
    yao_planunit.set_plan_name(exx.yao)

    save_vision_plan(
        moment_mstr_dir=env_dir(),
        moment_rope=exx.a23,
        healer_name=exx.bob,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        x_plan=yao_planunit,
    )

    # WHEN
    perspective_planunit = rj_perspective_plan(
        moment_mstr_dir=env_dir(),
        moment_rope=exx.a23,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        healer_name=exx.bob,
        speaker_id=exx.yao,
        perspective_id=exx.sue,
    )

    # THEN
    assert perspective_planunit.plan_name == exx.sue
    assert perspective_planunit.to_dict() != yao_planunit.to_dict()
    perspective_planunit.set_plan_name(exx.yao)
    assert perspective_planunit.to_dict() == yao_planunit.to_dict()
