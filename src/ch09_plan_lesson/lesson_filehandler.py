from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import (
    create_path,
    delete_dir,
    get_dict_from_json,
    get_dir_file_strs,
    get_integer_filenames,
    get_json_filename,
    get_max_file_number,
    open_json,
    save_json,
)
from src.ch01_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch04_rope.rope import LassoUnit, lassounit_shop, validate_labelterm
from src.ch07_plan_logic.plan_main import (
    PlanUnit,
    get_planunit_from_dict,
    planunit_shop,
)
from src.ch08_plan_atom.atom_main import (
    PlanAtom,
    get_planatom_from_dict,
    modify_plan_with_planatom,
)
from src.ch09_plan_lesson._ref.ch09_path import (
    create_atoms_dir_path,
    create_gut_path,
    create_lessons_dir_path,
)
from src.ch09_plan_lesson._ref.ch09_semantic_types import (
    KnotTerm,
    LabelTerm,
    MomentRope,
    PlanName,
    RopeTerm,
    default_knot_if_None,
)
from src.ch09_plan_lesson.lesson_main import (
    LessonUnit,
    create_lessonunit_from_files,
    get_init_lesson_id_if_None,
    init_lesson_id,
    lessonunit_shop,
)


def save_plan_file(dest_dir: str, filename: str = None, planunit: PlanUnit = None):
    save_json(dest_dir, filename, planunit.to_dict())


def open_plan_file(dest_dir: str, filename: str = None) -> PlanUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return get_planunit_from_dict(open_json(dest_dir, filename))


def save_gut_file(moment_mstr_dir: str, planunit: PlanUnit):
    moment_lasso = lassounit_shop(planunit.moment_rope, planunit.knot)
    gut_path = create_gut_path(moment_mstr_dir, moment_lasso, planunit.plan_name)
    save_plan_file(gut_path, None, planunit)


def open_gut_file(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> PlanUnit:
    gut_path = create_gut_path(moment_mstr_dir, moment_lasso, plan_name)
    gut_plan = open_plan_file(gut_path)
    if gut_plan:
        gut_plan.moment_rope = moment_lasso.rope
    return gut_plan


def gut_file_exists(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> bool:
    gut_path = create_gut_path(moment_mstr_dir, moment_lasso, plan_name)
    return os_path_exists(gut_path)


class SaveLessonFileException(Exception):
    pass


class LessonFileMissingException(Exception):
    pass


@dataclass
class LessonFileHandler:
    plan_name: PlanName = None
    moment_mstr_dir: str = None
    moment_rope: MomentRope = None
    knot: KnotTerm = None
    fund_pool: float = None
    fund_grain: float = None
    respect_grain: float = None
    mana_grain: float = None
    atoms_dir: str = None
    lessons_dir: str = None

    def set_dir_attrs(self):
        mstr_dir = self.moment_mstr_dir
        plan_name = self.plan_name
        moment_lasso = lassounit_shop(self.moment_rope, self.knot)
        self.atoms_dir = create_atoms_dir_path(mstr_dir, moment_lasso, plan_name)
        self.lessons_dir = create_lessons_dir_path(mstr_dir, moment_lasso, plan_name)

    def default_gut_plan(self) -> PlanUnit:
        x_planunit = planunit_shop(
            plan_name=self.plan_name,
            moment_rope=self.moment_rope,
            knot=self.knot,
            fund_pool=self.fund_pool,
            fund_grain=self.fund_grain,
            respect_grain=self.respect_grain,
            mana_grain=self.mana_grain,
        )
        x_planunit.last_lesson_id = init_lesson_id()
        return x_planunit

    # lesson methods
    def get_max_atom_file_number(self) -> int:
        return get_max_file_number(self.atoms_dir)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_filename(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        "Returns path: _atoms_dir/atom_number.json"
        return create_path(self.atoms_dir, self.atom_filename(atom_number))

    def _save_valid_atom_file(self, x_atom: PlanAtom, file_number: int):
        save_json(
            self.atoms_dir,
            self.atom_filename(file_number),
            x_atom.to_dict(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: PlanAtom):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def h_atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_plan_from_atom_files(self) -> PlanUnit:
        x_plan = planunit_shop(self.plan_name, self.moment_rope)
        if self.h_atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = get_dir_file_strs(self.atoms_dir, delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_json_str = x_atom_files.get(x_atom_filename)
                x_dict = get_dict_from_json(x_json_str)
                x_atom = get_planatom_from_dict(x_dict)
                modify_plan_with_planatom(x_plan, x_atom)
        return x_plan

    def get_max_lesson_file_number(self) -> int:
        return get_max_file_number(self.lessons_dir)

    def _get_next_lesson_file_number(self) -> int:
        max_file_number = self.get_max_lesson_file_number()
        init_lesson_id = get_init_lesson_id_if_None()
        return init_lesson_id if max_file_number is None else max_file_number + 1

    def lesson_filename(self, lesson_id: int) -> str:
        return get_json_filename(lesson_id)

    def lesson_file_path(self, lesson_id: int) -> str:
        """Returns path: _lessons/lesson_id.json"""

        lesson_filename = self.lesson_filename(lesson_id)
        return create_path(self.lessons_dir, lesson_filename)

    def hub_lesson_file_exists(self, lesson_id: int) -> bool:
        return os_path_exists(self.lesson_file_path(lesson_id))

    def validate_lessonunit(self, x_lessonunit: LessonUnit) -> LessonUnit:
        if x_lessonunit.atoms_dir != self.atoms_dir:
            x_lessonunit.atoms_dir = self.atoms_dir
        if x_lessonunit.lessons_dir != self.lessons_dir:
            x_lessonunit.lessons_dir = self.lessons_dir
        if x_lessonunit._lesson_id != self._get_next_lesson_file_number():
            x_lessonunit._lesson_id = self._get_next_lesson_file_number()
        if x_lessonunit.plan_name != self.plan_name:
            x_lessonunit.plan_name = self.plan_name
        if x_lessonunit._delta_start != self._get_next_atom_file_number():
            x_lessonunit._delta_start = self._get_next_atom_file_number()
        return x_lessonunit

    def save_lesson_file(
        self,
        x_lesson: LessonUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> LessonUnit:
        if correct_invalid_attrs:
            x_lesson = self.validate_lessonunit(x_lesson)

        if x_lesson.atoms_dir != self.atoms_dir:
            raise SaveLessonFileException(
                f"LessonUnit file cannot be saved because lessonunit.atoms_dir is incorrect: {x_lesson.atoms_dir}. It must be {self.atoms_dir}."
            )
        if x_lesson.lessons_dir != self.lessons_dir:
            raise SaveLessonFileException(
                f"LessonUnit file cannot be saved because lessonunit.lessons_dir is incorrect: {x_lesson.lessons_dir}. It must be {self.lessons_dir}."
            )
        if x_lesson.plan_name != self.plan_name:
            raise SaveLessonFileException(
                f"LessonUnit file cannot be saved because lessonunit.plan_name is incorrect: {x_lesson.plan_name}. It must be {self.plan_name}."
            )
        lesson_filename = self.lesson_filename(x_lesson._lesson_id)
        if not replace and self.hub_lesson_file_exists(x_lesson._lesson_id):
            raise SaveLessonFileException(
                f"LessonUnit file {lesson_filename} exists and cannot be saved over."
            )
        x_lesson.save_files()
        return x_lesson

    def _del_lesson_file(self, lesson_id: int):
        delete_dir(self.lesson_file_path(lesson_id))

    def _default_lessonunit(self) -> LessonUnit:
        return lessonunit_shop(
            plan_name=self.plan_name,
            _lesson_id=self._get_next_lesson_file_number(),
            atoms_dir=self.atoms_dir,
            lessons_dir=self.lessons_dir,
        )

    def create_save_lesson_file(self, before_plan: PlanUnit, after_plan: PlanUnit):
        new_lessonunit = self._default_lessonunit()
        new_plandelta = new_lessonunit._plandelta
        new_plandelta.add_all_different_planatoms(before_plan, after_plan)
        self.save_lesson_file(new_lessonunit)

    def get_lessonunit(self, lesson_id: int) -> LessonUnit:
        if self.hub_lesson_file_exists(lesson_id) is False:
            raise LessonFileMissingException(
                f"LessonUnit file_number {lesson_id} does not exist."
            )
        x_lessons_dir = self.lessons_dir
        x_atoms_dir = self.atoms_dir
        return create_lessonunit_from_files(x_lessons_dir, lesson_id, x_atoms_dir)

    def _merge_any_lessons(self, x_plan: PlanUnit) -> PlanUnit:
        lessons_dir = self.lessons_dir
        lesson_ints = get_integer_filenames(lessons_dir, x_plan.last_lesson_id)
        if len(lesson_ints) == 0:
            return copy_deepcopy(x_plan)

        for lesson_int in lesson_ints:
            x_lesson = self.get_lessonunit(lesson_int)
            new_plan = x_lesson._plandelta.get_atom_edited_plan(x_plan)
        return new_plan

    def _create_initial_lesson_files_from_default(self):
        x_lessonunit = lessonunit_shop(
            plan_name=self.plan_name,
            _lesson_id=get_init_lesson_id_if_None(),
            lessons_dir=self.lessons_dir,
            atoms_dir=self.atoms_dir,
        )
        x_lessonunit._plandelta.add_all_different_planatoms(
            before_plan=self.default_gut_plan(),
            after_plan=self.default_gut_plan(),
        )
        x_lessonunit.save_files()

    def _create_gut_from_lessons(self):
        x_plan = self._merge_any_lessons(self.default_gut_plan())
        save_gut_file(self.moment_mstr_dir, x_plan)

    def _create_initial_lesson_and_gut_files(self):
        self._create_initial_lesson_files_from_default()
        self._create_gut_from_lessons()

    def _create_initial_lesson_files_from_gut(self):
        x_lessonunit = self._default_lessonunit()
        moment_lasso = lassounit_shop(self.moment_rope)
        x_lessonunit._plandelta.add_all_different_planatoms(
            before_plan=self.default_gut_plan(),
            after_plan=open_gut_file(
                self.moment_mstr_dir, moment_lasso, self.plan_name
            ),
        )
        x_lessonunit.save_files()

    def initialize_lesson_gut_files(self):
        moment_lasso = lassounit_shop(self.moment_rope)
        x_gut_file_exists = gut_file_exists(
            self.moment_mstr_dir, moment_lasso, self.plan_name
        )
        lesson_file_exists = self.hub_lesson_file_exists(init_lesson_id())
        if x_gut_file_exists is False and lesson_file_exists is False:
            self._create_initial_lesson_and_gut_files()
        elif x_gut_file_exists is False and lesson_file_exists:
            self._create_gut_from_lessons()
        elif x_gut_file_exists and lesson_file_exists is False:
            self._create_initial_lesson_files_from_gut()

    def append_lessons_to_gut_file(self) -> PlanUnit:
        moment_lasso = lassounit_shop(self.moment_rope)
        gut_plan = open_gut_file(self.moment_mstr_dir, moment_lasso, self.plan_name)
        gut_plan = self._merge_any_lessons(gut_plan)
        save_gut_file(self.moment_mstr_dir, gut_plan)
        return gut_plan


def lessonfilehandler_shop(
    moment_mstr_dir: str,
    moment_rope: MomentRope,
    plan_name: PlanName = None,
    knot: KnotTerm = None,
    fund_pool: float = None,
    fund_grain: float = None,
    respect_grain: float = None,
    mana_grain: float = None,
) -> LessonFileHandler:
    x_lessonfilehandler = LessonFileHandler(
        moment_mstr_dir=moment_mstr_dir,
        moment_rope=moment_rope,
        plan_name=validate_labelterm(plan_name, knot),
        knot=default_knot_if_None(knot),
        fund_pool=validate_pool_num(fund_pool),
        fund_grain=default_grain_num_if_None(fund_grain),
        respect_grain=default_grain_num_if_None(respect_grain),
        mana_grain=default_grain_num_if_None(mana_grain),
    )
    x_lessonfilehandler.set_dir_attrs()
    return x_lessonfilehandler
