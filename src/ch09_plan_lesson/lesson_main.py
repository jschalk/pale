from dataclasses import dataclass
from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import (
    create_path,
    get_json_filename,
    open_json,
    save_json,
)
from src.ch07_plan_logic.plan_main import PlanUnit, get_default_first_label
from src.ch08_plan_atom.atom_main import PlanAtom, get_planatom_from_dict
from src.ch09_plan_lesson._ref.ch09_semantic_types import (
    FaceName,
    MomentLabel,
    PlanName,
)
from src.ch09_plan_lesson.delta import (
    PlanDelta,
    get_plandelta_from_ordered_dict,
    plandelta_shop,
)


class lesson_plan_conflict_Exception(Exception):
    pass


def init_lesson_id() -> int:
    return 0


def get_init_lesson_id_if_None(x_lesson_id: int = None) -> int:
    return init_lesson_id() if x_lesson_id is None else x_lesson_id


@dataclass
class LessonUnit:
    face_name: FaceName = None
    moment_label: MomentLabel = None
    plan_name: PlanName = None
    _lesson_id: int = None
    _plandelta: PlanDelta = None
    _delta_start: int = None
    lessons_dir: str = None
    atoms_dir: str = None
    spark_num: int = None
    """Represents a per moment_label/spark_num PlanDelta for a plan_name"""

    def set_face(self, x_face_name: FaceName):
        self.face_name = x_face_name

    def del_face(self):
        self.face_name = None

    def set_plandelta(self, x_plandelta: PlanDelta):
        self._plandelta = x_plandelta

    def del_plandelta(self):
        self._plandelta = plandelta_shop()

    def set_delta_start(self, x_delta_start: int):
        self._delta_start = get_init_lesson_id_if_None(x_delta_start)

    def planatom_exists(self, x_planatom: PlanAtom):
        return self._plandelta.c_planatom_exists(x_planatom)

    def get_step_dict(self) -> dict[str, any]:
        return {
            "face_name": self.face_name,
            "moment_label": self.moment_label,
            "plan_name": self.plan_name,
            "spark_num": self.spark_num,
            "delta": self._plandelta.get_ordered_planatoms(self._delta_start),
        }

    def get_serializable_step_dict(self) -> dict[str, dict]:
        total_dict = self.get_step_dict()
        total_dict["delta"] = self._plandelta.get_ordered_dict()
        return total_dict

    def get_delta_atom_numbers(self, lessonunit_dict: list[str]) -> int:
        delta_dict = lessonunit_dict.get("delta")
        return list(delta_dict.keys())

    def get_deltametric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "plan_name": x_dict.get("plan_name"),
            "face_name": x_dict.get("face_name"),
            "spark_num": x_dict.get("spark_num"),
            "delta_atom_numbers": self.get_delta_atom_numbers(x_dict),
        }

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: PlanAtom):
        x_filename = self._get_num_filename(atom_number)
        save_json(self.atoms_dir, x_filename, x_atom.to_dict())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(create_path(self.atoms_dir, x_filename))

    def _open_atom_file(self, atom_number: int) -> PlanAtom:
        x_dict = open_json(self.atoms_dir, self._get_num_filename(atom_number))
        return get_planatom_from_dict(x_dict)

    def _save_lesson_file(self):
        x_filename = self._get_num_filename(self._lesson_id)
        save_json(self.lessons_dir, x_filename, self.get_deltametric_dict())

    def lesson_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._lesson_id)
        return os_path_exists(create_path(self.lessons_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_planatoms = step_dict.get("delta")
        for order_int, planatom in ordered_planatoms.items():
            self._save_atom_file(order_int, planatom)

    def save_files(self):
        self._save_lesson_file()
        self._save_atom_files()

    def _create_plandelta_from_atom_files(self, atom_number_list: list) -> PlanDelta:
        x_plandelta = plandelta_shop()
        for atom_number in atom_number_list:
            x_planatom = self._open_atom_file(atom_number)
            x_plandelta.set_planatom(x_planatom)
        self._plandelta = x_plandelta

    def add_p_planatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        self._plandelta.add_planatom(dimen, crud_str, jkeys=jkeys, jvalues=jvalues)

    def get_lesson_edited_plan(self, before_plan: PlanUnit) -> PlanUnit:
        if (
            self.moment_label != before_plan.moment_label
            or self.plan_name != before_plan.plan_name
        ):
            raise lesson_plan_conflict_Exception(
                f"lesson plan conflict {self.moment_label} != {before_plan.moment_label} or {self.plan_name} != {before_plan.plan_name}"
            )
        return self._plandelta.get_atom_edited_plan(before_plan)

    def is_empty(self) -> bool:
        return self._plandelta.atoms_empty()


def lessonunit_shop(
    plan_name: PlanName,
    face_name: FaceName = None,
    moment_label: MomentLabel = None,
    _lesson_id: int = None,
    _plandelta: PlanDelta = None,
    _delta_start: int = None,
    lessons_dir: str = None,
    atoms_dir: str = None,
    spark_num: int = None,
) -> LessonUnit:
    _plandelta = plandelta_shop() if _plandelta is None else _plandelta
    moment_label = get_default_first_label() if moment_label is None else moment_label
    x_lessonunit = LessonUnit(
        face_name=face_name,
        plan_name=plan_name,
        moment_label=moment_label,
        _lesson_id=get_init_lesson_id_if_None(_lesson_id),
        _plandelta=_plandelta,
        lessons_dir=lessons_dir,
        atoms_dir=atoms_dir,
        spark_num=spark_num,
    )
    x_lessonunit.set_delta_start(_delta_start)
    return x_lessonunit


def create_lessonunit_from_files(
    lessons_dir: str,
    lesson_id: str,
    atoms_dir: str,
) -> LessonUnit:
    lesson_filename = get_json_filename(lesson_id)
    lesson_dict = open_json(lessons_dir, lesson_filename)
    x_plan_name = lesson_dict.get("plan_name")
    x_moment_label = lesson_dict.get("moment_label")
    x_face_name = lesson_dict.get("face_name")
    delta_atom_numbers_list = lesson_dict.get("delta_atom_numbers")
    x_lessonunit = lessonunit_shop(
        face_name=x_face_name,
        plan_name=x_plan_name,
        moment_label=x_moment_label,
        _lesson_id=lesson_id,
        atoms_dir=atoms_dir,
    )
    x_lessonunit._create_plandelta_from_atom_files(delta_atom_numbers_list)
    return x_lessonunit


def get_lessonunit_from_dict(lesson_dict: dict) -> LessonUnit:
    if lesson_dict.get("spark_num") is None:
        x_spark_num = None
    else:
        x_spark_num = int(lesson_dict.get("spark_num"))
    x_lessonunit = lessonunit_shop(
        face_name=lesson_dict.get("face_name"),
        plan_name=lesson_dict.get("plan_name"),
        moment_label=lesson_dict.get("moment_label"),
        _lesson_id=lesson_dict.get("lesson_id"),
        atoms_dir=lesson_dict.get("atoms_dir"),
        spark_num=x_spark_num,
    )
    x_plandelta = get_plandelta_from_ordered_dict(lesson_dict.get("delta"))
    x_lessonunit.set_plandelta(x_plandelta)
    return x_lessonunit
