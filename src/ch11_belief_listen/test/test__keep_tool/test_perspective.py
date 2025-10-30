from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ch09_belief_lesson.lesson_filehandler import lessonfilehandler_shop
from src.ch11_belief_listen.keep_tool import (
    get_dw_perspective_belief,
    get_perspective_belief,
    rj_perspective_belief,
    save_job_file,
    save_vision_belief,
)
from src.ch11_belief_listen.test._util.ch11_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_perspective_belief_ReturnsBeliefWith_belief_nameSetToLessonFileHandler_belief_name():
    # ESTABLISH
    bob_beliefunit = get_beliefunit_with_4_levels()
    bob_beliefunit.set_belief_name(exx.bob)

    # WHEN
    perspective_beliefunit = get_perspective_belief(bob_beliefunit, exx.sue)

    # THEN
    assert perspective_beliefunit.to_dict() != bob_beliefunit.to_dict()
    assert perspective_beliefunit.belief_name == exx.sue
    perspective_beliefunit.set_belief_name(exx.bob)
    assert perspective_beliefunit.to_dict() == bob_beliefunit.to_dict()


def test_get_dw_perspective_belief_ReturnsBeliefWith_belief_nameSetToLessonFileHandler_belief_name(
    temp_dir_setup,
):
    # ESTABLISH
    a23_str = "amy23"
    bob_beliefunit = get_beliefunit_with_4_levels()
    bob_beliefunit.set_belief_name(exx.bob)
    bob_lessonfilehandler = lessonfilehandler_shop(env_dir(), a23_str, exx.bob)
    save_job_file(bob_lessonfilehandler.moment_mstr_dir, bob_beliefunit)

    # WHEN
    perspective_beliefunit = get_dw_perspective_belief(
        env_dir(), a23_str, exx.bob, exx.sue
    )

    # THEN
    assert perspective_beliefunit.belief_name == exx.sue
    assert perspective_beliefunit.to_dict() != bob_beliefunit.to_dict()
    perspective_beliefunit.set_belief_name(exx.bob)
    assert perspective_beliefunit.to_dict() == bob_beliefunit.to_dict()


def test_rj_perspective_belief_ReturnsBeliefWith_belief_nameSetToLessonFileHandler_belief_name(
    temp_dir_setup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope("amy23", nation_str)
    iowa_rope = create_rope(nation_rope, "Iowa")
    a23_str = "amy23"

    yao_beliefunit = get_beliefunit_with_4_levels()
    yao_beliefunit.set_belief_name(exx.yao)

    save_vision_belief(
        moment_mstr_dir=env_dir(),
        moment_label=a23_str,
        healer_name=exx.bob,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        x_belief=yao_beliefunit,
    )

    # WHEN
    perspective_beliefunit = rj_perspective_belief(
        moment_mstr_dir=env_dir(),
        moment_label=a23_str,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        healer_name=exx.bob,
        speaker_id=exx.yao,
        perspective_id=exx.sue,
    )

    # THEN
    assert perspective_beliefunit.belief_name == exx.sue
    assert perspective_beliefunit.to_dict() != yao_beliefunit.to_dict()
    perspective_beliefunit.set_belief_name(exx.yao)
    assert perspective_beliefunit.to_dict() == yao_beliefunit.to_dict()
