from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch00_py.file_toolbox import create_path
from src.ch09_plan_lesson._ref.ch09_path import (
    MOMENT_FILENAME,
    create_atoms_dir_path,
    create_gut_path,
    create_job_path,
    create_lessons_dir_path,
    create_moment_dir_path,
    create_moment_json_path,
    create_moment_plans_dir_path,
    create_plan_dir_path,
)
from src.ch09_plan_lesson.test._util.ch09_env import get_temp_dir
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_create_moment_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_a23_dir_path = create_moment_dir_path(x_moment_mstr_dir, exx.a23)

    # THEN
    moments_dir = create_path(x_moment_mstr_dir, "moments")
    expected_a23_path = create_path(moments_dir, exx.a23)
    assert gen_a23_dir_path == expected_a23_path


def test_create_moment_json_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_a23_json_path = create_moment_json_path(x_moment_mstr_dir, exx.a23)

    # THEN
    moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_path = create_path(moments_dir, exx.a23)
    expected_a23_json_path = create_path(a23_path, MOMENT_FILENAME)
    assert gen_a23_json_path == expected_a23_json_path


def test_create_moment_plans_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_plans_dir = create_moment_plans_dir_path(x_moment_mstr_dir, exx.a23)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    expected_plans_dir = create_path(amy23_dir, "plans")
    assert gen_plans_dir == expected_plans_dir


def test_create_plan_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    sue_dir = create_plan_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    expected_sue_dir = create_path(plans_dir, exx.sue)
    assert sue_dir == expected_sue_dir


def test_create_atoms_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    atoms_dir = create_atoms_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    expected_atoms_dir = create_path(sue_dir, "atoms")
    assert atoms_dir == expected_atoms_dir


def test_create_lessons_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    lessons_dir = create_lessons_dir_path(x_moment_mstr_dir, exx.a23, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, exx.a23)
    plans_dir = create_path(amy23_dir, "plans")
    sue_dir = create_path(plans_dir, exx.sue)
    expected_lessons_dir = create_path(sue_dir, "lessons")
    assert lessons_dir == expected_lessons_dir


def test_create_gut_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_a23_e3_plan_path = create_gut_path(x_moment_mstr_dir, exx.a23, exx.bob)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, exx.a23)
    a23_plans_dir = create_path(a23_dir, "plans")
    a23_bob_dir = create_path(a23_plans_dir, exx.bob)
    a23_bob_gut_dir = create_path(a23_bob_dir, kw.gut)
    expected_a23_bob_gut_json_path = create_path(a23_bob_gut_dir, f"{exx.bob}.json")
    # plan_filename = "plan.json"
    # expected_a23_e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    assert gen_a23_e3_plan_path == expected_a23_bob_gut_json_path


def test_create_job_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()

    # WHEN
    gen_a23_e3_plan_path = create_job_path(x_moment_mstr_dir, exx.a23, exx.bob)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, exx.a23)
    a23_plans_dir = create_path(a23_dir, "plans")
    a23_bob_dir = create_path(a23_plans_dir, exx.bob)
    a23_bob_job_dir = create_path(a23_bob_dir, kw.job)
    expected_a23_bob_job_json_path = create_path(a23_bob_job_dir, f"{exx.bob}.json")
    # plan_filename = "plan.json"
    # expected_a23_e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    assert gen_a23_e3_plan_path == expected_a23_bob_job_json_path


LINUX_OS = platform_system() == "Linux"


def test_create_moment_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_dir_path("moment_mstr_dir", kw.moment_label)
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_dir_path) == doc_str


def test_create_moment_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_json_path("moment_mstr_dir", moment_label=kw.moment_label)
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_json_path) == doc_str


def test_create_moment_plans_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_plans_dir_path(
        "moment_mstr_dir", moment_label=kw.moment_label
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_plans_dir_path) == doc_str


def test_create_plan_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_plan_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_plan_dir_path) == doc_str


def test_create_atoms_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_atoms_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_atoms_dir_path) == doc_str


def test_create_lessons_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_lessons_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_lessons_dir_path) == doc_str


def test_create_gut_path_HasDocString():
    # ESTABLISH
    doc_str = create_gut_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_gut_path)=}")
    print(inspect_getdoc(create_gut_path))
    assert LINUX_OS or inspect_getdoc(create_gut_path) == doc_str


def test_create_job_path_HasDocString():
    # ESTABLISH
    doc_str = create_job_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        plan_name=kw.plan_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_job_path) == doc_str
