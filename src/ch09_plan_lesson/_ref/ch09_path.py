from src.ch01_py.file_toolbox import create_path
from src.ch09_plan_lesson._ref.ch09_semantic_types import MomentLabel, PlanName

MOMENT_FILENAME = "moment.json"


def create_moment_dir_path(moment_mstr_dir: str, moment_label: MomentLabel) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    return create_path(moments_dir, moment_label)


def create_moment_json_path(moment_mstr_dir: str, moment_label: MomentLabel) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\moment.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_label)
    return create_path(moment_path, "moment.json")


def create_moment_plans_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    return create_path(moment_dir, "plans")


def create_plan_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name"""

    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    plans_dir = create_path(moment_dir, "plans")
    return create_path(plans_dir, plan_name)


def create_atoms_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\atoms"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    plans_dir = create_path(moment_dir, "plans")
    plan_dir = create_path(plans_dir, plan_name)
    return create_path(plan_dir, "atoms")


def create_lessons_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\lessons"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    plans_dir = create_path(moment_dir, "plans")
    plan_dir = create_path(plans_dir, plan_name)
    return create_path(plan_dir, "lessons")


def create_gut_path(
    moment_mstr_dir: str, moment_label: MomentLabel, plan_name: PlanName
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\gut\\plan_name.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    plans_dir = create_path(moment_dir, "plans")
    plan_dir = create_path(plans_dir, plan_name)
    gut_dir = create_path(plan_dir, "gut")
    return create_path(gut_dir, f"{plan_name}.json")


def create_job_path(
    moment_mstr_dir: str, moment_label: MomentLabel, plan_name: PlanName
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\plans\\plan_name\\job\\plan_name.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    plans_dir = create_path(moment_dir, "plans")
    plan_dir = create_path(plans_dir, plan_name)
    job_dir = create_path(plan_dir, "job")
    return create_path(job_dir, f"{plan_name}.json")
