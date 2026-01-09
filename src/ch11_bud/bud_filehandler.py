from os import listdir as os_listdir
from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.ch01_py.dict_toolbox import get_empty_list_if_None
from src.ch01_py.file_toolbox import (
    create_path,
    get_dir_file_strs,
    open_json,
    save_json,
    set_dir,
)
from src.ch07_plan_logic.plan_main import PlanUnit, planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import (
    create_job_path,
    create_moment_plans_dir_path,
)
from src.ch09_plan_lesson.lesson_filehandler import open_plan_file, save_plan_file
from src.ch11_bud._ref.ch11_path import (
    CELLNODE_FILENAME,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_planspark_path,
    create_plantime_path,
)
from src.ch11_bud._ref.ch11_semantic_types import (
    EpochTime,
    LabelTerm,
    PlanName,
    RopeTerm,
    SparkInt,
)
from src.ch11_bud.bud_main import BudUnit, get_budunit_from_dict
from src.ch11_bud.cell_main import CellUnit, cellunit_get_from_dict, cellunit_shop


def get_planspark_obj(
    moment_mstr_dir: str,
    moment_label: LabelTerm,
    plan_name: PlanName,
    spark_num: int,
) -> PlanUnit:
    planspark_json_path = create_planspark_path(
        moment_mstr_dir, moment_label, plan_name, spark_num
    )
    return open_plan_file(planspark_json_path)


def collect_plan_spark_dir_sets(
    moment_mstr_dir: str, moment_label: LabelTerm
) -> dict[PlanName, set[SparkInt]]:
    x_dict = {}
    plans_dir = create_moment_plans_dir_path(moment_mstr_dir, moment_label)
    set_dir(plans_dir)
    for plan_name in os_listdir(plans_dir):
        plan_dir = create_path(plans_dir, plan_name)
        sparks_dir = create_path(plan_dir, "sparks")
        set_dir(sparks_dir)
        plan_sparks_dirs = {
            int(spark_num_dir)
            for spark_num_dir in os_listdir(sparks_dir)
            if os_path_isdir(create_path(sparks_dir, spark_num_dir))
        }
        x_dict[plan_name] = plan_sparks_dirs
    return x_dict


def get_plans_downhill_spark_nums(
    plan_sparks_sets: dict[PlanName, set[SparkInt]],
    downhill_plans: set[PlanName] = None,
    ref_spark_num: SparkInt = None,
) -> dict[PlanName, SparkInt]:
    x_dict = {}
    if downhill_plans:
        for plan_name in downhill_plans:
            if spark_set := plan_sparks_sets.get(plan_name):
                _add_downhill_spark_num(x_dict, spark_set, ref_spark_num, plan_name)
    else:
        for plan_name, spark_set in plan_sparks_sets.items():
            _add_downhill_spark_num(x_dict, spark_set, ref_spark_num, plan_name)
    return x_dict


def _add_downhill_spark_num(
    x_dict: dict[PlanName, SparkInt],
    spark_set: set[SparkInt],
    ref_spark_num: SparkInt,
    downhill_plan: PlanName,
):
    if spark_set:
        if ref_spark_num:
            if downhill_spark_nums := {ei for ei in spark_set if ei <= ref_spark_num}:
                x_dict[downhill_plan] = max(downhill_spark_nums)
        else:
            x_dict[downhill_plan] = max(spark_set)


def save_arbitrary_planspark(
    moment_mstr_dir: str,
    moment_label: str,
    plan_name: str,
    spark_num: int,
    voices: list[list] = None,
    facts: list[tuple[RopeTerm, RopeTerm, float, float]] = None,
) -> str:
    voices = get_empty_list_if_None(voices)
    facts = get_empty_list_if_None(facts)
    x_planunit = planunit_shop(plan_name, moment_label)
    for voice_list in voices:
        try:
            voice_cred_lumen = voice_list[1]
        except Exception:
            voice_cred_lumen = None
        x_planunit.add_voiceunit(voice_list[0], voice_cred_lumen)
    for fact_tup in facts:
        x_reason_context = fact_tup[0]
        x_fact_state = fact_tup[1]
        x_fact_lower = fact_tup[2]
        x_fact_upper = fact_tup[3]
        x_planunit.add_fact(
            x_reason_context, x_fact_state, x_fact_lower, x_fact_upper, True
        )
    x_planspark_path = create_planspark_path(
        moment_mstr_dir, moment_label, plan_name, spark_num
    )
    save_json(x_planspark_path, None, x_planunit.to_dict())
    return x_planspark_path


def cellunit_add_json_file(
    moment_mstr_dir: str,
    moment_label: str,
    time_plan_name: str,
    bud_time: int,
    spark_num: int,
    bud_ancestors: list[PlanName] = None,
    quota: int = None,
    celldepth: int = None,
    mana_grain: int = None,
):
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, time_plan_name, bud_time, bud_ancestors
    )
    x_cell = cellunit_shop(
        time_plan_name, bud_ancestors, spark_num, celldepth, mana_grain, quota
    )
    cellunit_save_to_dir(cell_dir, x_cell)


def cellunit_save_to_dir(dirpath: str, x_cell: CellUnit):
    save_json(dirpath, CELLNODE_FILENAME, x_cell.to_dict())


def cellunit_get_from_dir(dirpath: str) -> CellUnit:
    cell_json_path = create_path(dirpath, CELLNODE_FILENAME)
    if os_path_exists(cell_json_path):
        return cellunit_get_from_dict(open_json(cell_json_path))


def create_cell_voice_mandate_ledger_json(dirpath: str):
    if cell := cellunit_get_from_dir(dirpath):
        cell.calc_voice_mandate_ledger()
        save_json(dirpath, "cell_voice_mandate_ledger.json", cell._voice_mandate_ledger)


def save_bud_file(
    moment_mstr_dir: str,
    moment_label: str,
    plan_name: PlanName,
    x_bud: BudUnit = None,
):
    x_bud.calc_magnitude()
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, plan_name, x_bud.bud_time
    )
    save_json(bud_json_path, None, x_bud.to_dict(), replace=True)


def bud_file_exists(
    moment_mstr_dir: str,
    moment_label: str,
    plan_name: PlanName,
    x_bud_time: EpochTime = None,
) -> bool:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, plan_name, x_bud_time
    )
    return os_path_exists(bud_json_path)


def open_bud_file(
    moment_mstr_dir: str,
    moment_label: str,
    plan_name: PlanName,
    x_bud_time: EpochTime = None,
) -> BudUnit:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, plan_name, x_bud_time
    )
    if bud_file_exists(moment_mstr_dir, moment_label, plan_name, x_bud_time):
        return get_budunit_from_dict(open_json(bud_json_path))


class _save_valid_plantime_Exception(Exception):
    pass


def save_plantime_file(
    moment_mstr_dir: str,
    x_plantime: PlanUnit,
    x_bud_time: EpochTime = None,
):
    x_plantime.cashout()
    if x_plantime.rational is False:
        raise _save_valid_plantime_Exception(
            "PlanTime could not be saved PlanUnit.rational is False"
        )
    plantime_json_path = create_plantime_path(
        moment_mstr_dir,
        x_plantime.moment_label,
        x_plantime.plan_name,
        x_bud_time,
    )
    save_plan_file(plantime_json_path, None, x_plantime)


def plantime_file_exists(
    moment_mstr_dir: str,
    moment_label: str,
    plan_name: PlanName,
    x_bud_time: EpochTime = None,
) -> bool:
    plantime_json_path = create_plantime_path(
        moment_mstr_dir, moment_label, plan_name, x_bud_time
    )
    return os_path_exists(plantime_json_path)


def open_plantime_file(
    moment_mstr_dir: str,
    moment_label: str,
    plan_name: PlanName,
    x_bud_time: EpochTime = None,
) -> bool:
    plantime_json_path = create_plantime_path(
        moment_mstr_dir, moment_label, plan_name, x_bud_time
    )
    # if self.plantime_file_exists(x_bud_time):
    return open_plan_file(plantime_json_path)


def get_epochtime_dirs(
    moment_mstr_dir: str, moment_label: str, plan_name: PlanName
) -> list[EpochTime]:
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_label, plan_name)
    x_dict = get_dir_file_strs(buds_dir, include_dirs=True, include_files=False)
    return [int(x_epochtime) for x_epochtime in sorted(list(x_dict.keys()))]
