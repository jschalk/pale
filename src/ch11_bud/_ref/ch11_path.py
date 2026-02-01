from src.ch00_py.file_toolbox import create_path
from src.ch09_plan_lesson._ref.ch09_path import create_moment_plans_dir_path
from src.ch09_plan_lesson.lasso import LassoUnit
from src.ch11_bud._ref.ch11_semantic_types import PlanName

MOMENT_FILENAME = "moment.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_person_mandate_ledger.json"
PLANTIME_FILENAME = "plantime.json"
PLANSPARK_FILENAME = "plan.json"
SPARK_ALL_LESSON_FILENAME = "all_lesson.json"
SPARK_EXPRESSED_LESSON_FILENAME = "expressed_lesson.json"


def create_buds_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, plan_name: PlanName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    plan_dir = create_path(plans_dir, plan_name)
    return create_path(plan_dir, "buds")


def create_bud_dir_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time"""
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_lasso, plan_name)
    return create_path(buds_dir, bud_time)


def create_budunit_json_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time\\budunit.json"""
    timenum_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, bud_time
    )
    return create_path(timenum_dir, "budunit.json")


def create_plantime_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time\\plantime.json"""
    timenum_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, bud_time
    )
    return create_path(timenum_dir, "plantime.json")


def create_cell_dir_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    bud_time: int,
    bud_ancestors: list[PlanName],
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time\\ledger_plan1\\ledger_plan2\\ledger_plan3"""
    bud_celldepth_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_plan in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_plan)
    return bud_celldepth_dir


def create_cell_json_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    bud_time: int,
    bud_ancestors: list[PlanName] = None,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time\\ledger_plan1\\ledger_plan2\\ledger_plan3\\cell.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_person_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    bud_time: int,
    bud_ancestors: list[PlanName] = None,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time\\ledger_plan1\\ledger_plan2\\ledger_plan3\\cell_person_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_person_mandate_ledger.json")


def create_plan_spark_dir_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\sparks\\spark_num"""
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_lasso)
    moment_plan_dir = create_path(plans_dir, plan_name)
    moment_sparks_dir = create_path(moment_plan_dir, "sparks")
    return create_path(moment_sparks_dir, spark_num)


def create_plan_spark_csv_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    spark_num: int,
    filename: str,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\sparks\\spark_num\\filename.csv"""
    spark_dir = create_plan_spark_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, spark_num
    )
    return create_path(spark_dir, f"{filename}.csv")


def create_planspark_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\sparks\\spark_num\\plan.json"""
    plan_spark_dir_path = create_plan_spark_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, spark_num
    )
    plan_filename = "plan.json"
    return create_path(plan_spark_dir_path, plan_filename)


def create_spark_all_lesson_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\sparks\\spark_num\\all_lesson.json"""
    plan_spark_dir_path = create_plan_spark_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, spark_num
    )
    all_lesson_filename = "all_lesson.json"
    return create_path(plan_spark_dir_path, all_lesson_filename)


def create_spark_expressed_lesson_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    plan_name: PlanName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\sparks\\spark_num\\expressed_lesson.json"""
    plan_spark_dir_path = create_plan_spark_dir_path(
        moment_mstr_dir, moment_lasso, plan_name, spark_num
    )
    expressed_lesson_filename = "expressed_lesson.json"
    return create_path(plan_spark_dir_path, expressed_lesson_filename)
