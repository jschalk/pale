from src.ch00_py.file_toolbox import (
    create_directory_path,
    create_path,
    get_json_filename,
)
from src.ch04_rope.rope import get_all_rope_labels, rebuild_rope
from src.ch10_plan_listen._ref.ch10_semantic_types import (
    KnotTerm,
    LabelTerm,
    MomentLabel,
    PlanName,
)


def treasury_filename() -> str:
    return "treasury.db"


def create_keeps_dir_path(
    moment_mstr_dir: str, moment_label: LabelTerm, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    plans_dir = create_path(moment_dir, "plans")
    plan_dir = create_path(plans_dir, plan_name)
    return create_path(plan_dir, "keeps")


class _keep_ropeMissingException(Exception):
    pass


def create_keep_rope_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\kegroot\\level1_label"""
    if keep_rope is None:
        raise _keep_ropeMissingException(
            f"'{plan_name}' cannot save to keep_path because it does not have keep_rope."
        )

    keep_root = "kegroot"
    keep_rope = rebuild_rope(keep_rope, moment_label, keep_root)
    x_list = get_all_rope_labels(keep_rope, knot)
    keep_sub_path = create_directory_path(x_list=[*x_list])
    keeps_dir = create_keeps_dir_path(moment_mstr_dir, moment_label, plan_name)
    return create_path(keeps_dir, keep_sub_path)


def create_keep_dutys_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\level1\\dutys"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, "dutys")


def create_keep_duty_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
    duty_plan: PlanName,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\level1\\dutys\\duty_plan.json"""
    x_dutys_path = create_keep_dutys_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    return create_path(x_dutys_path, get_json_filename(duty_plan))


def create_keep_visions_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\level1\\visions"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, "visions")


def create_keep_grades_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\level1\\grades"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, "grades")


def create_keep_grade_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
    grade_plan_name: PlanName,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\level1\\grades\\grade_plan_name.json"""
    x_keep_path = create_keep_grades_path(
        moment_mstr_dir, plan_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, get_json_filename(grade_plan_name))


def create_treasury_db_path(
    moment_mstr_dir: str,
    plan_name: PlanName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: KnotTerm,
) -> str:
    "Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\keeps\\level1\\treasury.db"
    keep_path = create_keep_rope_path(
        moment_mstr_dir=moment_mstr_dir,
        plan_name=plan_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return create_path(keep_path, treasury_filename())
