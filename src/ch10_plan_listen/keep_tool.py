from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch00_py.dict_toolbox import get_empty_set_if_None
from src.ch00_py.file_toolbox import (
    create_path,
    get_json_filename,
    open_json,
    save_json,
    set_dir,
)
from src.ch07_plan_logic.plan_main import PlanUnit, get_planunit_from_dict
from src.ch09_plan_lesson._ref.ch09_path import create_job_path
from src.ch09_plan_lesson.lesson_filehandler import (
    open_gut_file,
    open_plan_file,
    save_plan_file,
)
from src.ch10_plan_listen._ref.ch10_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_keep_visions_path,
    create_treasury_db_path,
)
from src.ch10_plan_listen._ref.ch10_semantic_types import (
    KnotTerm,
    LabelTerm,
    MomentLabel,
    PlanName,
    RopeTerm,
)


def job_file_exists(
    moment_mstr_dir: str, moment_label: str, plan_name: PlanName
) -> bool:
    job_path = create_job_path(moment_mstr_dir, moment_label, plan_name)
    return os_path_exists(job_path)


def save_job_file(moment_mstr_dir: str, planunit: PlanUnit):
    job_path = create_job_path(
        moment_mstr_dir, planunit.moment_label, planunit.plan_name
    )
    save_plan_file(job_path, None, planunit)


def open_job_file(
    moment_mstr_dir: str, moment_label: str, plan_name: PlanName
) -> PlanUnit:
    job_path = create_job_path(moment_mstr_dir, moment_label, plan_name)
    return open_plan_file(job_path)


def create_keep_path_dir_if_missing(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
):
    keep_path = create_keep_rope_path(
        moment_mstr_dir,
        plan_name,
        moment_label,
        keep_rope,
        knot,
    )
    set_dir(keep_path)


def treasury_db_file_exists(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> bool:
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        plan_name=plan_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return os_path_exists(treasury_db_path)


def create_treasury_db_file(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> None:
    create_keep_path_dir_if_missing(
        moment_mstr_dir=moment_mstr_dir,
        plan_name=plan_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        plan_name=plan_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    conn = sqlite3_connect(treasury_db_path)
    conn.close()


def save_duty_plan(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
    duty_plan: PlanUnit,
) -> None:
    duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        plan_name=plan_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
        duty_plan=duty_plan.plan_name,
    )
    save_json(duty_path, None, duty_plan.to_dict())


def get_duty_plan(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
    duty_plan_name: PlanName,
) -> PlanUnit:
    keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        plan_name=plan_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
        duty_plan=duty_plan_name,
    )
    if os_path_exists(keep_duty_path) is False:
        return None
    return get_planunit_from_dict(open_json(keep_duty_path))


def save_all_gut_dutys(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    plan_name: PlanName,
    keep_ropes: set[RopeTerm],
    knot: KnotTerm,
):
    gut = open_gut_file(moment_mstr_dir, moment_label, plan_name)
    for x_keep_rope in keep_ropes:
        save_duty_plan(
            moment_mstr_dir=moment_mstr_dir,
            plan_name=plan_name,
            moment_label=moment_label,
            keep_rope=x_keep_rope,
            knot=knot,
            duty_plan=gut,
        )


class get_keep_ropesException(Exception):
    pass


def get_keep_ropes(moment_mstr_dir, moment_label, plan_name) -> set[RopeTerm]:
    x_gut_plan = open_gut_file(moment_mstr_dir, moment_label, plan_name)
    x_gut_plan.cashout()
    if x_gut_plan.keeps_justified is False:
        x_str = f"Cannot get_keep_ropes from '{plan_name}' gut plan because 'PlanUnit.keeps_justified' is False."
        raise get_keep_ropesException(x_str)
    if x_gut_plan.keeps_buildable is False:
        x_str = f"Cannot get_keep_ropes from '{plan_name}' gut plan because 'PlanUnit.keeps_buildable' is False."
        raise get_keep_ropesException(x_str)
    plan_healer_dict = x_gut_plan._healers_dict.get(plan_name)
    if plan_healer_dict is None:
        return get_empty_set_if_None()
    keep_ropes = x_gut_plan._healers_dict.get(plan_name).keys()
    return get_empty_set_if_None(keep_ropes)


def get_perspective_plan(speaker: PlanUnit, listener_name: PlanName) -> PlanUnit:
    # get copy of plan without any metrics
    perspective_plan = get_planunit_from_dict(speaker.to_dict())
    perspective_plan.set_plan_name(listener_name)
    perspective_plan.cashout()
    return perspective_plan


def vision_file_exists(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    speaker_id: PlanName,
) -> bool:
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    file_path = create_path(keep_visions_path, get_json_filename(speaker_id))
    return os_path_exists(file_path)


def get_vision_plan(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    speaker_id: PlanName,
) -> PlanUnit:
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    if (
        vision_file_exists(
            moment_mstr_dir, plan_name, moment_label, keep_rope, knot, speaker_id
        )
        is False
    ):
        return None
    plan_dict = open_json(keep_visions_path, get_json_filename(speaker_id))
    return get_planunit_from_dict(plan_dict)


def get_dw_perspective_plan(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    speaker_id: PlanName,
    prespective_id: PlanName,
) -> PlanUnit:
    speaker_job = open_job_file(moment_mstr_dir, moment_label, speaker_id)
    return get_perspective_plan(speaker_job, prespective_id)


def rj_speaker_plan(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    healer_name: PlanName,
    speaker_id: PlanName,
) -> PlanUnit:
    return get_vision_plan(
        moment_mstr_dir=moment_mstr_dir,
        moment_label=moment_label,
        plan_name=healer_name,
        keep_rope=keep_rope,
        knot=knot,
        speaker_id=speaker_id,
    )


def rj_perspective_plan(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    healer_name: PlanName,
    speaker_id: PlanName,
    perspective_id: PlanName,
) -> PlanUnit:
    speaker_vision = rj_speaker_plan(
        moment_mstr_dir,
        moment_label,
        keep_rope,
        knot,
        healer_name,
        speaker_id,
    )
    return get_perspective_plan(speaker_vision, perspective_id)


def save_vision_plan(
    moment_mstr_dir: str,
    healer_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: KnotTerm,
    x_plan: PlanUnit,
) -> None:
    x_filename = get_json_filename(x_plan.plan_name)
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir,
        healer_name,
        moment_label,
        keep_rope,
        knot,
    )
    save_plan_file(keep_visions_path, x_filename, x_plan)
