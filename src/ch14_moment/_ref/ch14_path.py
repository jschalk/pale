from src.ch00_py.file_toolbox import create_path
from src.ch11_bud._ref.ch11_path import create_bud_dir_path
from src.ch14_moment._ref.ch14_semantic_types import PlanName, RopeTerm

BUD_MANDATE_FILENAME = "bud_person_mandate_ledger.json"


def create_bud_person_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_rope: RopeTerm,
    plan_name: PlanName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\plans\\plan_name\\buds\n\\bud_time\\bud_person_mandate_ledger.json"""
    timenum_dir = create_bud_dir_path(moment_mstr_dir, moment_rope, plan_name, bud_time)
    return create_path(timenum_dir, "bud_person_mandate_ledger.json")
