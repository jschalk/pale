from src.ch07_plan_logic.plan_main import PlanUnit, planunit_shop
from src.ch10_plan_listen._ref.ch10_semantic_types import PlanName


def create_empty_plan_from_plan(
    ref_plan: PlanUnit, x_plan_name: PlanName = None
) -> PlanUnit:
    x_plan_name = ref_plan.plan_name if x_plan_name is None else x_plan_name
    x_knot = ref_plan.knot
    x_fund_pool = ref_plan.fund_pool
    x_fund_grain = ref_plan.fund_grain
    x_respect_grain = ref_plan.respect_grain
    x_mana_grain = ref_plan.mana_grain
    return planunit_shop(
        plan_name=x_plan_name,
        moment_rope=ref_plan.moment_rope,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )


def create_listen_basis(x_plan: PlanUnit) -> PlanUnit:
    x_listen = create_empty_plan_from_plan(x_plan, x_plan.plan_name)
    x_listen.partners = x_plan.partners
    x_listen.set_max_tree_traverse(x_plan.max_tree_traverse)
    if x_plan.credor_respect is not None:
        x_listen.set_credor_respect(x_plan.credor_respect)
    if x_plan.debtor_respect is not None:
        x_listen.set_debtor_respect(x_plan.debtor_respect)
    for x_partnerunit in x_listen.partners.values():
        x_partnerunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: PlanUnit) -> PlanUnit:
    default_job = create_listen_basis(gut)
    default_job.last_lesson_id = gut.last_lesson_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
