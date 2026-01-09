from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch01_py.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_empty_list_if_None,
)
from src.ch02_allot.allot import allot_scale
from src.ch05_reason.reason_main import (
    FactUnit,
    get_dict_from_factunits,
    get_factunits_from_dict,
)
from src.ch07_plan_logic.plan_main import (
    PlanUnit,
    get_planunit_from_dict,
    planunit_shop,
)
from src.ch07_plan_logic.plan_tool import (
    clear_factunits_from_plan,
    get_credit_ledger,
    get_plan_root_facts_dict as get_facts_dict,
    get_voice_mandate_ledger,
)
from src.ch11_bud._ref.ch11_semantic_types import (
    FundNum,
    ManaGrain,
    PlanName,
    RopeTerm,
    SparkInt,
)

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[PlanName] = None
    spark_num: SparkInt = None
    celldepth: int = None
    bud_plan_name: PlanName = None
    mana_grain: ManaGrain = None
    quota: float = None
    mandate: float = None
    planadjust: PlanUnit = None
    planspark_facts: dict[RopeTerm, FactUnit] = None
    found_facts: dict[RopeTerm, FactUnit] = None
    boss_facts: dict[RopeTerm, FactUnit] = None
    reason_contexts: set[RopeTerm] = None
    _voice_mandate_ledger: dict[PlanName, FundNum] = None

    def get_cell_plan_name(self) -> PlanName:
        return self.bud_plan_name if self.ancestors == [] else self.ancestors[-1]

    def eval_planspark(self, x_plan: PlanUnit):
        if not x_plan:
            self.planadjust = None
            self.planspark_facts = {}
            self.reason_contexts = set()
        else:
            self._load_existing_planspark(x_plan)

    def _load_existing_planspark(self, x_plan: PlanUnit):
        self.reason_contexts = x_plan.get_reason_contexts()
        self.planspark_facts = get_factunits_from_dict(get_facts_dict(x_plan))
        y_plan = copy_deepcopy(x_plan)
        clear_factunits_from_plan(y_plan)
        y_plan.cashout()
        self.planadjust = y_plan

    def get_plansparks_credit_ledger(self) -> dict[PlanName, float]:
        return {} if self.planadjust is None else get_credit_ledger(self.planadjust)

    def get_plansparks_quota_ledger(self) -> dict[PlanName, float]:
        if not self.planadjust:
            return None
        credit_ledger = self.get_plansparks_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.mana_grain)

    def set_planspark_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.planspark_facts = get_factunits_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.found_facts = get_factunits_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.planspark_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def add_other_facts_to_boss_facts(self):
        for x_fact in self.found_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)
        for x_fact in self.planspark_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_contexts(self):
        to_delete_planspark_fact_keys = set(self.planspark_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_planspark_fact_keys.difference_update(self.reason_contexts)
        to_delete_found_fact_keys.difference_update(self.reason_contexts)
        to_delete_boss_fact_keys.difference_update(self.reason_contexts)
        for planspark_fact_key in to_delete_planspark_fact_keys:
            self.planspark_facts.pop(planspark_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_planadjust_facts(self):
        for fact in self.planspark_facts.values():
            self.planadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.found_facts.values():
            self.planadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.boss_facts.values():
            self.planadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )

    def _set_voice_mandate_ledger(self):
        self.planadjust.set_fund_pool(self.mandate)
        self._voice_mandate_ledger = get_voice_mandate_ledger(self.planadjust, True)

    def calc_voice_mandate_ledger(self):
        self.reason_contexts = self.planadjust.get_reason_contexts()
        self.filter_facts_by_reason_contexts()
        self.set_planadjust_facts()
        self._set_voice_mandate_ledger()

    def to_dict(self) -> dict[str, str | dict]:
        """Returns dict that is serializable to JSON."""

        if not self.planadjust:
            self.planadjust = planunit_shop(self.get_cell_plan_name())
        return {
            "ancestors": self.ancestors,
            "spark_num": self.spark_num,
            "celldepth": self.celldepth,
            "bud_plan_name": self.bud_plan_name,
            "mana_grain": self.mana_grain,
            "quota": self.quota,
            "mandate": self.mandate,
            "planadjust": self.planadjust.to_dict(),
            "planspark_facts": get_dict_from_factunits(self.planspark_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }


def cellunit_shop(
    bud_plan_name: PlanName,
    ancestors: list[PlanName] = None,
    spark_num: SparkInt = None,
    celldepth: int = None,
    mana_grain: ManaGrain = None,
    quota: float = None,
    planadjust: PlanUnit = None,
    planspark_facts: dict[RopeTerm, FactUnit] = None,
    found_facts: dict[RopeTerm, FactUnit] = None,
    boss_facts: dict[RopeTerm, FactUnit] = None,
    mandate: float = None,
) -> CellUnit:
    if quota is None:
        quota = CELLNODE_QUOTA_DEFAULT
    if mandate is None:
        mandate = CELLNODE_QUOTA_DEFAULT
    if planadjust is None:
        planadjust = planunit_shop(bud_plan_name)
    reason_contexts = planadjust.get_reason_contexts() if planadjust else set()
    if planadjust:
        planadjust = copy_deepcopy(planadjust)
        clear_factunits_from_plan(planadjust)

    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        spark_num=spark_num,
        celldepth=get_0_if_None(celldepth),
        bud_plan_name=bud_plan_name,
        mana_grain=get_1_if_None(mana_grain),
        quota=quota,
        mandate=mandate,
        planadjust=planadjust,
        planspark_facts=get_empty_dict_if_None(planspark_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        reason_contexts=reason_contexts,
        _voice_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    bud_plan_name = x_dict.get("bud_plan_name")
    ancestors = x_dict.get("ancestors")
    spark_num = x_dict.get("spark_num")
    celldepth = x_dict.get("celldepth")
    mana_grain = x_dict.get("mana_grain")
    quota = x_dict.get("quota")
    mandate = x_dict.get("mandate")
    planadjust_dict = x_dict.get("planadjust")
    if planadjust_dict:
        planadjust_obj = get_planunit_from_dict(planadjust_dict)
    else:
        planadjust_obj = None
    planspark_fact_dict = get_empty_dict_if_None(x_dict.get("planspark_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    planspark_facts = get_factunits_from_dict(planspark_fact_dict)
    found_facts = get_factunits_from_dict(found_fact_dict)
    boss_facts = get_factunits_from_dict(boss_fact_dict)
    return cellunit_shop(
        bud_plan_name=bud_plan_name,
        ancestors=ancestors,
        spark_num=spark_num,
        celldepth=celldepth,
        mana_grain=mana_grain,
        quota=quota,
        planadjust=planadjust_obj,
        planspark_facts=planspark_facts,
        found_facts=found_facts,
        boss_facts=boss_facts,
        mandate=mandate,
    )


def create_child_cellunits(parent_cell: CellUnit) -> list[CellUnit]:
    parent_cell.calc_voice_mandate_ledger()
    x_list = []
    for child_plan_name in sorted(parent_cell._voice_mandate_ledger):
        child_mandate = parent_cell._voice_mandate_ledger.get(child_plan_name)
        if child_mandate > 0 and parent_cell.celldepth > 0:
            child_ancestors = copy_deepcopy(parent_cell.ancestors)
            child_ancestors.append(child_plan_name)
            boss_facts = get_factunits_from_dict(get_facts_dict(parent_cell.planadjust))
            child_cell = cellunit_shop(
                bud_plan_name=parent_cell.bud_plan_name,
                ancestors=child_ancestors,
                spark_num=parent_cell.spark_num,
                celldepth=parent_cell.celldepth - 1,
                mana_grain=parent_cell.mana_grain,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list
