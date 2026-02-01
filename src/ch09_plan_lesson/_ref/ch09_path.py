from src.ch00_py.file_toolbox import create_path
from src.ch09_plan_lesson._ref.ch09_semantic_types import PlanName
from src.ch09_plan_lesson.lasso import LassoUnit

MOMENT_FILENAME = "moment.json"


def create_moment_dir_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    return create_path(moments_dir, moment_lasso.make_path())


def create_moment_json_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\moment.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_lasso.make_path())
    return create_path(moment_path, "moment.json")


def create_moment_plans_dir_path(moment_mstr_dir: str, moment_lasso: LassoUnit) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_lasso.make_path())
    return create_path(moment_dir, "plans")


def create_plan_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    return create_path(plans_dir, plan_name)


def create_atoms_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\atoms"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    plan_dir = create_path(plans_dir, plan_name)
    return create_path(plan_dir, "atoms")


def create_lessons_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\lessons"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    plan_dir = create_path(plans_dir, plan_name)
    return create_path(plan_dir, "lessons")


def create_gut_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\gut\\plan_name.json"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    plan_dir = create_path(plans_dir, plan_name)
    gut_dir = create_path(plan_dir, "gut")
    return create_path(gut_dir, f"{plan_name}.json")


def create_job_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\job\\plan_name.json"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    plan_dir = create_path(plans_dir, plan_name)
    job_dir = create_path(plan_dir, "job")
    return create_path(job_dir, f"{plan_name}.json")
