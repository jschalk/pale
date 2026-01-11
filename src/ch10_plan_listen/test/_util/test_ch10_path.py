from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from pytest import raises as pytest_raises
from src.ch00_py.file_toolbox import create_path, get_json_filename
from src.ch04_rope.rope import create_rope, create_rope_from_labels
from src.ch10_plan_listen._ref.ch10_path import (
    create_keep_duty_path,
    create_keep_dutys_path,
    create_keep_grade_path,
    create_keep_grades_path,
    create_keep_rope_path,
    create_keep_visions_path,
    create_keeps_dir_path,
    create_treasury_db_path,
    treasury_filename,
)
from src.ch10_plan_listen.test._util.ch10_env import get_temp_dir
from src.ref.keywords import Ch10Keywords as kw, ExampleStrs as exx

LINUX_OS = platform_system() == "Linux"


def test_treasury_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert treasury_filename() == "treasury.db"


def test_create_keeps_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    keeps_dir = create_keeps_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    expected_keeps_dir = create_path(sue_dir, "keeps")
    assert keeps_dir == expected_keeps_dir


def test_create_keep_rope_path_ReturnsObj_Scenario0_SimpleRope():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )

    # THEN
    keeps_dir = create_keeps_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)
    keep_amy23_dir = create_path(keeps_dir, exx.a23)
    expected_keep_casa_dir = create_path(keep_amy23_dir, exx.casa)
    assert keep_casa_path == expected_keep_casa_dir


def test_create_keep_rope_path_ReturnsObj_Scenario1_MoreTestsForRopePathCreation():
    # ESTABLISH
    peru_str = "peru"
    moment_mstr_dir = get_temp_dir()
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    texas_rope = create_rope_from_labels([peru_str, texas_str])
    dallas_rope = create_rope_from_labels([peru_str, texas_str, dallas_str])
    elpaso_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str])
    kern_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str, kern_str])

    # WHEN
    # texas_path = create_keep_rope_path(sue_lessonfilehandler, texas_rope)
    texas_path = create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=texas_rope,
        knot=None,
    )
    # dallas_path = createdallas_path_keep_rope_path(sue_lessonfilehandler, dallas_rope)
    dallas_path = create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=dallas_rope,
        knot=None,
    )
    # elpaso_path = create_keep_rope_path(sue_lessonfilehandler, elpaso_rope)
    elpaso_path = create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=elpaso_rope,
        knot=None,
    )
    # kern_path = create_keep_rope_path(sue_lessonfilehandler, kern_rope)
    kern_path = create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=kern_rope,
        knot=None,
    )

    # THEN
    keeps_dir = create_keeps_dir_path(moment_mstr_dir, peru_str, exx.sue)
    kegroot_dir = create_path(keeps_dir, peru_str)
    print(f"{kern_rope=}")
    print(f"{kegroot_dir=}")
    assert texas_path == create_path(kegroot_dir, texas_str)
    assert dallas_path == create_path(texas_path, dallas_str)
    assert elpaso_path == create_path(texas_path, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)

    # WHEN / THEN
    diff_root_texas_rope = create_rope_from_labels([peru_str, texas_str])
    diff_root_dallas_rope = create_rope_from_labels([peru_str, texas_str, dallas_str])
    diff_root_elpaso_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str])
    assert texas_path == create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=diff_root_texas_rope,
        knot=None,
    )
    assert dallas_path == create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=diff_root_dallas_rope,
        knot=None,
    )
    assert elpaso_path == create_keep_rope_path(
        moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=peru_str,
        keep_rope=diff_root_elpaso_rope,
        knot=None,
    )


def test_create_keep_rope_path_RaisesError_Scenarion2_keep_rope_DoesNotExist():
    # ESTABLISH

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_keep_rope_path("dir", exx.bob, exx.a23, None, None)
    assertion_fail_str = (
        f"'{exx.bob}' cannot save to keep_path because it does not have keep_rope."
    )
    assert str(excinfo.value) == assertion_fail_str


def test_create_keep_dutys_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_keep_dutys_path(
        moment_mstr_dir=x_moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "dutys")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keep_duty_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=x_moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=exx.a23,
        keep_rope=casa_rope,
        knot=None,
        duty_plan=exx.bob,
    )

    # THEN
    keep_dutys_path = create_keep_dutys_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    bob_filename = get_json_filename(exx.bob)
    expected_keep_duty_path = create_path(keep_dutys_path, bob_filename)
    assert gen_keep_duty_path == expected_keep_duty_path


def test_create_keep_grades_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_keep_grades_path(
        moment_mstr_dir=x_moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "grades")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keep_grade_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=exx.a23,
        keep_rope=casa_rope,
        knot=None,
        grade_plan_name=exx.bob,
    )

    # THEN
    keep_grades_path = create_keep_grades_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_grade_path = create_path(keep_grades_path, get_json_filename(exx.bob))
    assert gen_keep_grade_path == expected_grade_path


def test_create_keep_visions_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_keep_visions_path(
        moment_mstr_dir=x_moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "visions")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_treasury_db_path_ReturnsObj() -> None:
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    casa_rope = create_rope(exx.a23, exx.casa)

    # WHEN
    gen_keep_dutys_path = create_treasury_db_path(
        moment_mstr_dir=x_moment_mstr_dir,
        plan_name=exx.sue,
        moment_label=exx.a23,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_moment_mstr_dir, exx.sue, exx.a23, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "treasury.db")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keeps_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_keeps_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keeps_dir_path) == doc_str


def test_create_keep_rope_path_HasDocString() -> None:
    # ESTABLISH
    level1_label_str = "level1_label"
    level1_rope = create_rope(kw.kegroot, level1_label_str)
    doc_str = create_keep_rope_path(
        moment_mstr_dir="moment_mstr_dir",
        plan_name=kw.plan_name,
        moment_label=kw.moment_label,
        keep_rope=level1_rope,
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_rope_path) == doc_str


def test_create_keep_dutys_path_HasDocString() -> None:
    # ESTABLISH
    expected_doc_str = create_keep_dutys_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        keep_rope="kegroot;level1;leveln",
        knot=None,
    )
    expected_doc_str = f"Returns path: {expected_doc_str}"
    print(f"{expected_doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_dutys_path) == expected_doc_str


def test_create_keep_duty_path_HasDocString() -> None:
    # ESTABLISH
    duty_plan_str = "duty_plan"
    expected_doc_str = create_keep_duty_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        keep_rope="kegroot;level1;leveln",
        knot=None,
        duty_plan=duty_plan_str,
    )
    expected_doc_str = f"Returns path: {expected_doc_str}"
    print(f"{expected_doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_duty_path) == expected_doc_str


def test_create_keep_grades_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_keep_grades_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        keep_rope="kegroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"                             {doc_str=}")
    print(f"{inspect_getdoc(create_keep_grades_path)=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_grades_path) == doc_str


def test_create_keep_grade_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_keep_grade_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        keep_rope="kegroot;level1;leveln",
        knot=None,
        grade_plan_name="grade_plan_name",
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_keep_grade_path)=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_grade_path) == doc_str


def test_create_keep_visions_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_keep_visions_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        keep_rope="kegroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_visions_path) == doc_str


def test_create_treasury_db_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_treasury_db_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
        keep_rope="kegroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_treasury_db_path) == doc_str
