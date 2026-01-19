from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_plan_logic.test._util.ch07_examples import get_planunit_with_4_levels
from src.ch10_plan_listen.keep_tool import (
    get_vision_plan,
    save_vision_plan,
    vision_file_exists,
)
from src.ch10_plan_listen.test._util.ch10_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ch10_plan_listen.test._util.ch10_examples import ch10_example_moment_rope
from src.ref.keywords import ExampleStrs as exx


def test_save_vision_plan_SavesFile(temp_dir_setup):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)

    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_plan_name(exx.bob)
    x_knot = default_knot_if_None()
    assert not vision_file_exists(
        env_dir(), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )

    # WHEN
    save_vision_plan(env_dir(), exx.sue, exx.a23, texas_rope, x_knot, bob_plan)

    # THEN
    assert vision_file_exists(env_dir(), exx.sue, exx.a23, texas_rope, x_knot, exx.bob)


def test_vision_file_exists_ReturnsBool(temp_dir_setup):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)

    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_plan_name(exx.bob)
    x_knot = default_knot_if_None()
    assert not (
        vision_file_exists(env_dir(), exx.sue, exx.a23, texas_rope, x_knot, exx.bob)
    )

    # WHEN
    save_vision_plan(env_dir(), exx.sue, exx.a23, texas_rope, x_knot, bob_plan)

    # THEN
    assert vision_file_exists(env_dir(), exx.sue, exx.a23, texas_rope, x_knot, exx.bob)


def test_get_vision_plan_reason_lowersFile(temp_dir_setup):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)

    bob_plan = get_planunit_with_4_levels()
    bob_plan.set_plan_name(exx.bob)
    x_knot = default_knot_if_None()
    save_vision_plan(env_dir(), exx.sue, exx.a23, texas_rope, x_knot, bob_plan)

    # WHEN
    bob_vision = get_vision_plan(
        env_dir(), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )

    # THEN
    assert bob_vision.to_dict() == bob_plan.to_dict()


def test_get_vision_plan_ReturnsNoneIfFileDoesNotExist(
    temp_dir_setup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope(ch10_example_moment_rope(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    x_knot = default_knot_if_None()

    # WHEN
    bob_vision = get_vision_plan(
        env_dir(), exx.sue, exx.a23, texas_rope, x_knot, exx.bob
    )

    # THEN
    assert not bob_vision
