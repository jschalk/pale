from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch00_py.file_toolbox import (
    create_path,
    delete_dir,
    get_dir_file_strs,
    get_json_filename,
    open_file,
    open_json,
    save_file,
    set_dir,
)
from src.ch09_plan_lesson.lasso import lassounit_shop
from src.ch09_plan_lesson.lesson_filehandler import (
    lessonfilehandler_shop,
    open_gut_file,
    save_gut_file,
)
from src.ch09_plan_lesson.lesson_main import init_lesson_id, lessonunit_shop
from src.ch09_plan_lesson.test._util.ch09_env import (
    get_temp_dir as env_dir,
    temp_dir_setup,
)
from src.ch09_plan_lesson.test._util.ch09_examples import (
    get_atom_example_kegunit_knee,
    get_sue_lessonunit,
    sue_1planatoms_lessonunit,
    sue_2planatoms_lessonunit,
    sue_3planatoms_lessonunit,
    sue_4planatoms_lessonunit,
)
from src.ref.keywords import ExampleStrs as exx


def test_LessonFileHandler_get_max_lesson_file_number_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)

    # WHEN / THEN
    delete_dir(sue_lessonfilehandler.lessons_dir)
    assert sue_lessonfilehandler.get_max_lesson_file_number() is None
    assert sue_lessonfilehandler._get_next_lesson_file_number() == init_lesson_id()
    assert sue_lessonfilehandler._get_next_lesson_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(
        sue_lessonfilehandler.lessons_dir,
        sue_lessonfilehandler.lesson_filename(six_int),
        "x",
    )

    # WHEN / THEN
    assert sue_lessonfilehandler.get_max_lesson_file_number() == six_int
    assert sue_lessonfilehandler._get_next_lesson_file_number() == 7


def test_LessonFileHandler_lesson_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    assert sue_lessonfilehandler.hub_lesson_file_exists(None) is False
    assert sue_lessonfilehandler.hub_lesson_file_exists(0) is False
    six_int = 6
    print(f"{sue_lessonfilehandler.lesson_file_path(six_int)=}")
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int) is False

    # WHEN
    save_file(
        sue_lessonfilehandler.lessons_dir,
        sue_lessonfilehandler.lesson_filename(six_int),
        "x",
    )

    # THEN
    assert sue_lessonfilehandler.hub_lesson_file_exists(None) is False
    assert sue_lessonfilehandler.hub_lesson_file_exists(0) is False
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int)


def test_LessonFileHandler_save_lesson_file_SaveCorrectObj(temp_dir_setup):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_lesson2_path = create_path(sue_lessonfilehandler.lessons_dir, two_filename)
    sue_lesson6_path = create_path(sue_lessonfilehandler.lessons_dir, six_filename)
    print(f"{sue_lesson2_path=}")
    print(f"{sue_lesson6_path=}")
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=two_int,
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )
    assert sue_lessonfilehandler.hub_lesson_file_exists(two_int) is False
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int) is False

    # WHEN
    sue_lessonfilehandler.save_lesson_file(sue_lessonunit, correct_invalid_attrs=False)

    # THEN
    assert sue_lessonfilehandler.hub_lesson_file_exists(two_int)
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int) is False
    two_file_dict = open_json(sue_lessonfilehandler.lessons_dir, two_filename)
    assert two_file_dict == sue_lessonunit.get_deltametric_dict()


def test_LessonFileHandler_save_lesson_file_RaisesErrorIfLessonUnit_atoms_dir_IsWrong(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    x_lesson_id = 6
    six_filename = get_json_filename(x_lesson_id)
    sue_lesson0_path = create_path(sue_lessonfilehandler.lessons_dir, six_filename)
    print(f"{sue_lesson0_path=}")
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=x_lesson_id,
        atoms_dir="src\\incorrect_directory",
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lessonfilehandler.save_lesson_file(
            sue_lessonunit, correct_invalid_attrs=False
        )
    expected_exception_str = f"LessonUnit file cannot be saved because lessonunit.atoms_dir is incorrect: {sue_lessonunit.atoms_dir}. It must be {sue_lessonfilehandler.atoms_dir}."
    assert str(excinfo.value) == expected_exception_str


def test_LessonFileHandler_save_lesson_file_RaisesErrorIfLessonUnit_lessons_dir_IsWrong(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    x_lesson_id = 6
    six_filename = get_json_filename(x_lesson_id)
    sue_lesson0_path = create_path(sue_lessonfilehandler.lessons_dir, six_filename)
    print(f"{sue_lesson0_path=}")
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=x_lesson_id,
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir="src\\incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lessonfilehandler.save_lesson_file(
            sue_lessonunit, correct_invalid_attrs=False
        )
    expected_exception_str = f"LessonUnit file cannot be saved because lessonunit.lessons_dir is incorrect: {sue_lessonunit.lessons_dir}. It must be {sue_lessonfilehandler.lessons_dir}."
    assert str(excinfo.value) == expected_exception_str


def test_LessonFileHandler_save_lesson_file_RaisesErrorIfLessonUnit_plan_name_IsWrong(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    x_lesson_id = 6
    six_filename = get_json_filename(x_lesson_id)
    sue_lesson0_path = create_path(sue_lessonfilehandler.lessons_dir, six_filename)
    print(f"{sue_lesson0_path=}")
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.bob,
        _lesson_id=x_lesson_id,
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lessonfilehandler.save_lesson_file(
            sue_lessonunit, correct_invalid_attrs=False
        )
    expected_exception_str = f"LessonUnit file cannot be saved because lessonunit.plan_name is incorrect: {sue_lessonunit.plan_name}. It must be {exx.sue}."
    assert str(excinfo.value) == expected_exception_str


def test_LessonFileHandler_save_lesson_file_RaisesErrorIf_replace_IsFalse(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    x_lesson_id = 0
    six_filename = get_json_filename(x_lesson_id)
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=x_lesson_id,
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )
    saved_lessonunit = sue_lessonfilehandler.save_lesson_file(sue_lessonunit)

    print(f"{sue_lessonfilehandler.lesson_file_path(x_lesson_id)=}")
    assert sue_lessonfilehandler.hub_lesson_file_exists(x_lesson_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_lessonfilehandler.save_lesson_file(
            saved_lessonunit, replace=False, correct_invalid_attrs=False
        )
    expected_exception_str = (
        f"LessonUnit file {six_filename} exists and cannot be saved over."
    )
    assert str(excinfo.value) == expected_exception_str


def test_LessonFileHandler_validate_lessonunit_ReturnsObjWithAttributesFixed(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_lesson2_path = create_path(sue_lessonfilehandler.lessons_dir, two_filename)
    print(f"{sue_lesson2_path=}")

    # WHEN
    invalid_sue_lessonunit = lessonunit_shop(
        plan_name="Bob",
        _lesson_id=sue_lessonfilehandler._get_next_lesson_file_number() - 5,
        atoms_dir=create_path(sue_lessonfilehandler.atoms_dir, "swimming"),
        lessons_dir=create_path(sue_lessonfilehandler.atoms_dir, "swimming"),
    )
    valid_lessonunit = sue_lessonfilehandler.validate_lessonunit(invalid_sue_lessonunit)

    # THEN
    assert valid_lessonunit.atoms_dir == sue_lessonfilehandler.atoms_dir
    assert valid_lessonunit.lessons_dir == sue_lessonfilehandler.lessons_dir
    assert (
        valid_lessonunit._lesson_id
        == sue_lessonfilehandler._get_next_lesson_file_number()
    )
    correct_sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=sue_lessonfilehandler._get_next_lesson_file_number(),
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )
    assert valid_lessonunit == correct_sue_lessonunit


def test_LessonFileHandler_save_lesson_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    next_int = sue_lessonfilehandler._get_next_lesson_file_number()
    next_filename = get_json_filename(next_int)
    sue_lesson2_path = create_path(sue_lessonfilehandler.lessons_dir, next_filename)
    print(f"{sue_lesson2_path=}")
    assert sue_lessonfilehandler.hub_lesson_file_exists(next_int) is False

    # WHEN
    invalid_sue_lessonunit = lessonunit_shop(
        plan_name="Bob",
        _lesson_id=sue_lessonfilehandler._get_next_lesson_file_number() - 5,
        atoms_dir=create_path(sue_lessonfilehandler.atoms_dir, "swimming"),
        lessons_dir=create_path(sue_lessonfilehandler.atoms_dir, "swimming"),
    )
    sue_lessonfilehandler.save_lesson_file(invalid_sue_lessonunit)

    # THEN
    assert sue_lessonfilehandler.hub_lesson_file_exists(next_int)
    two_file_json = open_file(sue_lessonfilehandler.lessons_dir, next_filename)


def test_LessonFileHandler_default_lessonunit_ReturnsObjWithCorrect_lesson_id_WhenNoLessonFilesExist(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)

    # WHEN
    delete_dir(sue_lessonfilehandler.lessons_dir)
    sue_lessonunit = sue_lessonfilehandler._default_lessonunit()

    # THEN
    assert sue_lessonunit.plan_name == exx.sue
    assert sue_lessonunit._lesson_id == init_lesson_id()
    assert sue_lessonunit._lesson_id == 0
    assert (
        sue_lessonunit._lesson_id
        == sue_lessonfilehandler._get_next_lesson_file_number()
    )
    assert sue_lessonunit.face_name is None
    assert sue_lessonunit.atoms_dir == sue_lessonfilehandler.atoms_dir
    assert sue_lessonunit.lessons_dir == sue_lessonfilehandler.lessons_dir


def test_LessonFileHandler_default_lessonunit_ReturnsObjWithCorrect_lesson_id_WhenLessonFilesExist(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    delete_dir(sue_lessonfilehandler.lessons_dir)

    zero_lessonunit = get_sue_lessonunit()
    zero_lessonunit._lesson_id = sue_lessonfilehandler._get_next_lesson_file_number()
    zero_lessonunit.atoms_dir = sue_lessonfilehandler.atoms_dir
    zero_lessonunit.lessons_dir = sue_lessonfilehandler.lessons_dir
    sue_lessonfilehandler.save_lesson_file(zero_lessonunit)

    # WHEN
    sue_lessonunit = sue_lessonfilehandler._default_lessonunit()

    # THEN
    assert sue_lessonunit.plan_name == exx.sue
    assert sue_lessonunit._lesson_id == init_lesson_id() + 1
    assert sue_lessonunit._lesson_id == 1
    assert (
        sue_lessonunit._lesson_id
        == sue_lessonfilehandler._get_next_lesson_file_number()
    )
    assert sue_lessonunit.face_name is None
    assert sue_lessonunit.atoms_dir == sue_lessonfilehandler.atoms_dir
    assert sue_lessonunit.lessons_dir == sue_lessonfilehandler.lessons_dir


def test_LessonFileHandler_get_lessonunit_ReturnsObjWhenFilesDoesExist(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    x0_lessonunit = sue_lessonfilehandler._default_lessonunit()
    x0_lessonunit.set_face(exx.yao)
    sue_lessonfilehandler.save_lesson_file(x0_lessonunit)
    x1_lessonunit = sue_lessonfilehandler._default_lessonunit()
    x1_lessonunit.set_face(exx.bob)
    sue_lessonfilehandler.save_lesson_file(x1_lessonunit)

    # WHEN
    y0_lessonunit = sue_lessonfilehandler.get_lessonunit(x0_lessonunit._lesson_id)
    y1_lessonunit = sue_lessonfilehandler.get_lessonunit(x1_lessonunit._lesson_id)

    # THEN
    assert y0_lessonunit is not None
    assert y1_lessonunit is not None
    assert exx.yao in y0_lessonunit.face_name
    assert exx.bob not in y0_lessonunit.face_name
    assert exx.bob in y1_lessonunit.face_name


def test_LessonFileHandler_get_lessonunit_RaisesExceptionWhenFileDoesNotExist(
    temp_dir_setup,
):
    # sourcery skip: extract-duplicate-method, inline-variable, move-assign-in-block
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    x0_lessonunit = sue_lessonfilehandler._default_lessonunit()
    x0_lessonunit.set_face(exx.yao)
    sue_lessonfilehandler.save_lesson_file(x0_lessonunit)
    x1_lessonunit = sue_lessonfilehandler._default_lessonunit()
    x1_lessonunit.set_face(exx.bob)
    sue_lessonfilehandler.save_lesson_file(x1_lessonunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_lessonfilehandler.get_lessonunit(six_file_number)
    assertion_failure_str = f"LessonUnit file_number {six_file_number} does not exist."
    assert str(excinfo.value) == assertion_failure_str


def test_LessonFileHandler_del_lesson_file_DeleteslessonjsonAndNotPlanAtomjsons(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    six_int = 6
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=six_int,
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )
    sue_lessonunit._plandelta.set_planatom(get_atom_example_kegunit_knee())
    zero_int = 0
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int) is False
    assert sue_lessonfilehandler.h_atom_file_exists(zero_int) is False

    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    sue_lessonfilehandler.save_lesson_file(sue_lessonunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_lessonfilehandler.atoms_dir)}")
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int)
    assert sue_lessonfilehandler.h_atom_file_exists(zero_int)

    # WHEN
    sue_lessonfilehandler._del_lesson_file(sue_lessonunit._lesson_id)

    # THEN
    assert sue_lessonfilehandler.hub_lesson_file_exists(six_int) is False
    assert sue_lessonfilehandler.h_atom_file_exists(zero_int)


def test_LessonFileHandler_save_lesson_file_CanCreateAndModify3lessonunits(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    delete_dir(sue_lessonfilehandler.lessons_dir)
    delete_dir(sue_lessonfilehandler.atoms_dir)
    set_dir(sue_lessonfilehandler.lessons_dir)
    set_dir(sue_lessonfilehandler.atoms_dir)
    assert len(get_dir_file_strs(sue_lessonfilehandler.lessons_dir)) == 0
    assert len(get_dir_file_strs(sue_lessonfilehandler.atoms_dir)) == 0

    # WHEN
    sue_lessonfilehandler.save_lesson_file(sue_2planatoms_lessonunit())
    sue_lessonfilehandler.save_lesson_file(sue_3planatoms_lessonunit())
    sue_lessonfilehandler.save_lesson_file(sue_4planatoms_lessonunit())

    # THEN
    assert len(get_dir_file_strs(sue_lessonfilehandler.lessons_dir)) == 3
    assert len(get_dir_file_strs(sue_lessonfilehandler.atoms_dir)) == 9


def test_LessonFileHandler_save_lesson_file_ReturnsValidObj(temp_dir_setup):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    sue2_lessonunit = sue_2planatoms_lessonunit()
    sue2_lessonunit.atoms_dir = create_path(sue_lessonfilehandler.atoms_dir, "swimming")
    sue2_lessonunit.lessons_dir = create_path(
        sue_lessonfilehandler.atoms_dir, "swimming"
    )
    sue2_lessonunit.plan_name = "Bob"
    sue2_lessonunit._lesson_id = (
        sue_lessonfilehandler._get_next_lesson_file_number() - 5
    )
    prev_sue2_lessonunit = copy_deepcopy(sue2_lessonunit)

    # WHEN
    valid_lessonunit = sue_lessonfilehandler.save_lesson_file(sue2_lessonunit)

    # THEN
    assert valid_lessonunit.lessons_dir != prev_sue2_lessonunit.lessons_dir
    assert valid_lessonunit.lessons_dir == sue_lessonfilehandler.lessons_dir
    assert valid_lessonunit.atoms_dir == sue_lessonfilehandler.atoms_dir
    assert valid_lessonunit._lesson_id != prev_sue2_lessonunit._lesson_id


def test_LessonFileHandler_create_save_lesson_file_SaveCorrectObj(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    two_int = 2
    three_int = 3
    print(f"{sue_lessonfilehandler.lesson_file_path(two_int)=}")
    print(f"{sue_lessonfilehandler.lesson_file_path(three_int)=}")
    sue_lessonunit = lessonunit_shop(
        plan_name=exx.sue,
        _lesson_id=two_int,
        atoms_dir=sue_lessonfilehandler.atoms_dir,
        lessons_dir=sue_lessonfilehandler.lessons_dir,
    )
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    sue_lessonfilehandler.save_lesson_file(sue_lessonunit, correct_invalid_attrs=False)
    assert sue_lessonfilehandler.hub_lesson_file_exists(two_int)
    assert sue_lessonfilehandler.hub_lesson_file_exists(three_int) is False

    # WHEN
    before_plan = sue_lessonfilehandler.default_gut_plan()
    after_plan = copy_deepcopy(before_plan)
    after_plan.add_personunit(exx.bob)
    sue_lessonfilehandler.create_save_lesson_file(before_plan, after_plan)

    # THEN
    assert sue_lessonfilehandler.hub_lesson_file_exists(three_int)


def test_LessonFileHandler_merge_any_lessons_ReturnsObjThatIsEqual(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    save_gut_file(env_dir(), sue_lessonfilehandler.default_gut_plan())
    a23_lasso = lassounit_shop(exx.a23)
    gut_plan = open_gut_file(env_dir(), a23_lasso, exx.sue)
    gut_plan.last_lesson_id is None

    # WHEN
    new_plan = sue_lessonfilehandler._merge_any_lessons(gut_plan)

    # THEN
    assert new_plan == gut_plan


def test_LessonFileHandler_merge_any_lessons_ReturnsObj_WithSinglelessonModifies_1atom(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    sue_lessonfilehandler.save_lesson_file(sue_1planatoms_lessonunit())
    save_gut_file(env_dir(), sue_lessonfilehandler.default_gut_plan())
    a23_lasso = lassounit_shop(exx.a23)
    gut_plan = open_gut_file(env_dir(), a23_lasso, exx.sue)
    print(f"{gut_plan.moment_rope=}")
    print(f"{sue_lessonfilehandler.moment_rope=}")
    sports_str = "sports"
    sports_rope = gut_plan.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_plan.make_rope(sports_rope, knee_str)
    assert gut_plan.keg_exists(sports_rope) is False

    # WHEN
    new_plan = sue_lessonfilehandler._merge_any_lessons(gut_plan)

    # THEN
    assert new_plan != gut_plan
    assert new_plan.keg_exists(sports_rope)


def test_LessonFileHandler_merge_any_lessons_ReturnsObj_WithSinglelessonModifies_2atoms(
    temp_dir_setup,
):
    # ESTABLISH
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), exx.a23, exx.sue)
    sue_lessonfilehandler.save_lesson_file(sue_2planatoms_lessonunit())
    save_gut_file(env_dir(), sue_lessonfilehandler.default_gut_plan())
    a23_lasso = lassounit_shop(exx.a23)
    gut_plan = open_gut_file(env_dir(), a23_lasso, exx.sue)
    print(f"{gut_plan.moment_rope=}")
    sports_str = "sports"
    sports_rope = gut_plan.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_plan.make_rope(sports_rope, knee_str)
    assert gut_plan.keg_exists(sports_rope) is False
    assert gut_plan.keg_exists(knee_rope) is False

    # WHEN
    new_plan = sue_lessonfilehandler._merge_any_lessons(gut_plan)

    # THEN
    assert new_plan != gut_plan
    assert new_plan.keg_exists(sports_rope)
    assert new_plan.keg_exists(knee_rope)
