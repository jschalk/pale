from pytest import raises as pytest_raises
from src.ch00_py.file_toolbox import create_path
from src.ch01_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch09_plan_lesson._ref.ch09_path import create_plan_dir_path
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch09_plan_lesson.lesson_filehandler import (
    LessonFileHandler,
    lessonfilehandler_shop,
)
from src.ch09_plan_lesson.test._util.ch09_env import get_temp_dir
from src.ref.keywords import ExampleStrs as exx


def test_LessonFileHandler_Exists():
    # ESTABLISH / WHEN
    x_lessonfilehandler = LessonFileHandler()

    # THEN
    assert not x_lessonfilehandler.moment_mstr_dir
    assert not x_lessonfilehandler.moment_rope
    assert not x_lessonfilehandler.plan_name
    assert not x_lessonfilehandler.knot
    assert not x_lessonfilehandler.fund_pool
    assert not x_lessonfilehandler.fund_grain
    assert not x_lessonfilehandler.respect_grain
    assert not x_lessonfilehandler.mana_grain
    assert not x_lessonfilehandler.atoms_dir
    assert not x_lessonfilehandler.lessons_dir


def test_lessonfilehandler_shop_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a45_str = "amy45"
    a45_rope = create_rope(a45_str, None, exx.slash)
    a45_lasso = lassounit_shop(a45_rope, exx.slash)
    x_fund_pool = 13000
    x_fund_grain = 13
    x_respect_grain = 9
    x_mana_grain = 3

    # WHEN
    x_lessonfilehandler = lessonfilehandler_shop(
        moment_mstr_dir=x_moment_mstr_dir,
        moment_rope=a45_rope,
        plan_name=exx.sue,
        knot=exx.slash,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )

    # THEN
    assert x_lessonfilehandler.moment_mstr_dir == x_moment_mstr_dir
    assert x_lessonfilehandler.moment_rope == a45_rope
    assert x_lessonfilehandler.plan_name == exx.sue
    assert x_lessonfilehandler.knot == exx.slash
    assert x_lessonfilehandler.fund_pool == x_fund_pool
    assert x_lessonfilehandler.fund_grain == x_fund_grain
    assert x_lessonfilehandler.respect_grain == x_respect_grain
    assert x_lessonfilehandler.mana_grain == x_mana_grain
    sue_dir = create_plan_dir_path(x_moment_mstr_dir, a45_lasso, exx.sue)
    assert x_lessonfilehandler.atoms_dir == create_path(sue_dir, "atoms")
    assert x_lessonfilehandler.lessons_dir == create_path(sue_dir, "lessons")


def test_lessonfilehandler_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()

    # WHEN
    sue_lessonfilehandler = lessonfilehandler_shop(moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    assert sue_lessonfilehandler.moment_mstr_dir == moment_mstr_dir
    assert sue_lessonfilehandler.moment_rope == exx.a23
    assert sue_lessonfilehandler.plan_name == exx.sue
    assert sue_lessonfilehandler.knot == default_knot_if_None()
    assert sue_lessonfilehandler.fund_pool == validate_pool_num()
    assert sue_lessonfilehandler.fund_grain == default_grain_num_if_None()
    assert sue_lessonfilehandler.respect_grain == default_grain_num_if_None()
    assert sue_lessonfilehandler.mana_grain == default_grain_num_if_None()


def test_lessonfilehandler_shop_RaisesErrorIf_plan_name_Contains_knot():
    # ESTABLISH
    bob_str = f"Bob{exx.slash}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        lessonfilehandler_shop(None, None, plan_name=bob_str, knot=exx.slash)
    assertion_fail_str = (
        f"'{bob_str}' must be a LabelTerm. Cannot contain knot: '{exx.slash}'"
    )
    assert str(excinfo.value) == assertion_fail_str
