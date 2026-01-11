from src.ch00_py.dict_toolbox import (
    create_csv,
    get_1_if_None,
    get_empty_str_if_None,
    modular_addition,
)
from src.ch01_allot.allot import allot_scale
from src.ch02_person.group import AwardUnit, MemberShip
from src.ch02_person.person import PersonUnit, calc_give_take_net
from src.ch04_rope.rope import get_unique_short_ropes, is_sub_rope
from src.ch05_reason.reason_main import (
    CaseUnit,
    FactUnit,
    ReasonUnit,
    get_factunits_from_dict,
)
from src.ch06_keg.keg import KegUnit
from src.ch07_plan_logic._ref.ch07_semantic_types import (
    FundNum,
    PersonName,
    RespectNum,
    RopeTerm,
)
from src.ch07_plan_logic.plan_main import PlanUnit


def planunit_exists(x_plan: PlanUnit) -> bool:
    return x_plan is not None


def plan_personunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_person_name = jkeys.get("person_name")
    return False if x_plan is None else x_plan.person_exists(x_person_name)


def plan_person_membership_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_person_name = jkeys.get("person_name")
    x_group_title = jkeys.get("group_title")
    return bool(
        plan_personunit_exists(x_plan, jkeys)
        and x_plan.get_person(x_person_name).membership_exists(x_group_title)
    )


def plan_kegunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("keg_rope")
    return False if x_plan is None else bool(x_plan.keg_exists(x_rope))


def plan_keg_awardunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_awardee_title = jkeys.get("awardee_title")
    x_rope = jkeys.get("keg_rope")
    return bool(
        plan_kegunit_exists(x_plan, jkeys)
        and x_plan.get_keg_obj(x_rope).awardunit_exists(x_awardee_title)
    )


def plan_keg_reasonunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("keg_rope")
    x_reason_context = jkeys.get("reason_context")
    return bool(
        plan_kegunit_exists(x_plan, jkeys)
        and x_plan.get_keg_obj(x_rope).reasonunit_exists(x_reason_context)
    )


def plan_keg_reason_caseunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("keg_rope")
    x_reason_context = jkeys.get("reason_context")
    x_reason_state = jkeys.get("reason_state")
    return bool(
        plan_keg_reasonunit_exists(x_plan, jkeys)
        and x_plan.get_keg_obj(x_rope)
        .get_reasonunit(x_reason_context)
        .case_exists(x_reason_state)
    )


def plan_keg_partyunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_party_title = jkeys.get("party_title")
    x_rope = jkeys.get("keg_rope")
    return bool(
        plan_kegunit_exists(x_plan, jkeys)
        and x_plan.get_keg_obj(x_rope).laborunit.partyunit_exists(x_party_title)
    )


def plan_keg_healerunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_healer_name = jkeys.get("healer_name")
    x_rope = jkeys.get("keg_rope")
    return bool(
        plan_kegunit_exists(x_plan, jkeys)
        and x_plan.get_keg_obj(x_rope).healerunit.healer_name_exists(x_healer_name)
    )


def plan_keg_factunit_exists(x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    x_rope = jkeys.get("keg_rope")
    x_fact_context = jkeys.get("fact_context")
    return bool(
        plan_kegunit_exists(x_plan, jkeys)
        and x_plan.get_keg_obj(x_rope).factunit_exists(x_fact_context)
    )


def plan_attr_exists(x_dimen: str, x_plan: PlanUnit, jkeys: dict[str, any]) -> bool:
    if x_dimen == "plan_person_membership":
        return plan_person_membership_exists(x_plan, jkeys)
    elif x_dimen == "plan_personunit":
        return plan_personunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_keg_awardunit":
        return plan_keg_awardunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_keg_factunit":
        return plan_keg_factunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_keg_healerunit":
        return plan_keg_healerunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_keg_reason_caseunit":
        return plan_keg_reason_caseunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_keg_reasonunit":
        return plan_keg_reasonunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_keg_partyunit":
        return plan_keg_partyunit_exists(x_plan, jkeys)
    elif x_dimen == "plan_kegunit":
        return plan_kegunit_exists(x_plan, jkeys)
    elif x_dimen == "planunit":
        return planunit_exists(x_plan)
    return True


def plan_personunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> PersonUnit:
    return x_plan.get_person(jkeys.get("person_name"))


def plan_person_membership_get_obj(
    x_plan: PlanUnit, jkeys: dict[str, any]
) -> MemberShip:
    x_person_name = jkeys.get("person_name")
    x_group_title = jkeys.get("group_title")
    return x_plan.get_person(x_person_name).get_membership(x_group_title)


def plan_kegunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> KegUnit:
    x_rope = jkeys.get("keg_rope")
    return x_plan.get_keg_obj(x_rope)


def plan_keg_awardunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> AwardUnit:
    x_rope = jkeys.get("keg_rope")
    x_awardee_title = jkeys.get("awardee_title")
    return x_plan.get_keg_obj(x_rope).get_awardunit(x_awardee_title)


def plan_keg_reasonunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> ReasonUnit:
    x_rope = jkeys.get("keg_rope")
    x_reason_context = jkeys.get("reason_context")
    return x_plan.get_keg_obj(x_rope).get_reasonunit(x_reason_context)


def plan_keg_reason_caseunit_get_obj(
    x_plan: PlanUnit, jkeys: dict[str, any]
) -> CaseUnit:
    """jkeys: keg_rope, reason_context, reason_state"""

    x_rope = jkeys.get("keg_rope")
    x_reason_context = jkeys.get("reason_context")
    x_reason_state = jkeys.get("reason_state")
    return (
        x_plan.get_keg_obj(x_rope)
        .get_reasonunit(x_reason_context)
        .get_case(x_reason_state)
    )


def plan_keg_factunit_get_obj(x_plan: PlanUnit, jkeys: dict[str, any]) -> FactUnit:
    x_rope = jkeys.get("keg_rope")
    x_fact_context = jkeys.get("fact_context")
    return x_plan.get_keg_obj(x_rope).factunits.get(x_fact_context)


def plan_get_obj(x_dimen: str, x_plan: PlanUnit, jkeys: dict[str, any]) -> any:
    if x_dimen == "planunit":
        return x_plan

    x_dimens = {
        "plan_personunit": plan_personunit_get_obj,
        "plan_person_membership": plan_person_membership_get_obj,
        "plan_kegunit": plan_kegunit_get_obj,
        "plan_keg_awardunit": plan_keg_awardunit_get_obj,
        "plan_keg_reasonunit": plan_keg_reasonunit_get_obj,
        "plan_keg_reason_caseunit": plan_keg_reason_caseunit_get_obj,
        "plan_keg_factunit": plan_keg_factunit_get_obj,
    }
    if x_func := x_dimens.get(x_dimen):
        return x_func(x_plan, jkeys)


def get_plan_person_agenda_award_array(
    x_plan: PlanUnit, cashout: bool = None
) -> list[list]:
    if cashout:
        x_plan.cashout()

    x_list = [
        [
            x_person.person_name,
            x_person.fund_agenda_take,
            x_person.fund_agenda_give,
        ]
        for x_person in x_plan.persons.values()
    ]
    x_list.sort(key=lambda y: y[0], reverse=False)
    return x_list


def get_plan_person_agenda_award_csv(x_plan: PlanUnit, cashout: bool = None) -> str:
    x_person_agenda_award_array = get_plan_person_agenda_award_array(x_plan, cashout)
    x_headers = ["person_name", "fund_agenda_take", "fund_agenda_give"]
    return create_csv(x_headers, x_person_agenda_award_array)


def get_person_mandate_ledger(
    x_plan: PlanUnit, cashout: bool = None
) -> dict[PersonName, FundNum]:
    if not x_plan:
        return {}
    if len(x_plan.persons) == 0:
        return {x_plan.plan_name: x_plan.fund_pool}

    if cashout:
        x_plan.cashout()
    plan_persons = x_plan.persons.values()
    mandates = {
        x_person.person_name: x_person.fund_agenda_give for x_person in plan_persons
    }
    mandate_sum = sum(mandates.values())
    if mandate_sum == 0:
        mandates = reset_mandates_to_minimum(mandates, x_plan.mana_grain)
    if mandate_sum != x_plan.fund_pool:
        mandates = allot_scale(mandates, x_plan.fund_pool, x_plan.fund_grain)
    return mandates


def reset_mandates_to_minimum(
    mandates: dict[PersonName, FundNum], mana_grain: FundNum
) -> dict[PersonName, FundNum]:
    """Reset all mandates to the minimum value (mana_grain)."""

    person_names = set(mandates.keys())
    for person_name in person_names:
        mandates[person_name] = mana_grain
    return mandates


def get_person_agenda_net_ledger(
    x_plan: PlanUnit, cashout: bool = None
) -> dict[PersonName, FundNum]:
    if cashout:
        x_plan.cashout()

    x_dict = {}
    for x_person in x_plan.persons.values():
        settle_net = calc_give_take_net(
            x_person.fund_agenda_give, x_person.fund_agenda_take
        )
        if settle_net != 0:
            x_dict[x_person.person_name] = settle_net
    return x_dict


def get_credit_ledger(x_plan: PlanUnit) -> dict[PersonUnit, RespectNum]:
    credit_ledger, debt_ledger = x_plan.get_credit_ledger_debt_ledger()
    return credit_ledger


def get_plan_root_facts_dict(
    x_plan: PlanUnit,
) -> dict[RopeTerm, dict[str,]]:
    return x_plan.get_kegroot_factunits_dict()


def set_factunits_to_plan(x_plan: PlanUnit, x_facts_dict: dict[RopeTerm, dict]):
    """Sets dict of FactUnits to PlanUnit kegroot"""
    factunits_dict = get_factunits_from_dict(x_facts_dict)
    missing_fact_reason_contexts = set(x_plan.get_missing_fact_reason_contexts().keys())
    not_missing_fact_reason_contexts = set(x_plan.get_kegroot_factunits_dict().keys())
    plan_fact_reason_contexts = not_missing_fact_reason_contexts.union(
        missing_fact_reason_contexts
    )
    for factunit in factunits_dict.values():
        if factunit.fact_context in plan_fact_reason_contexts:
            x_plan.add_fact(
                factunit.fact_context,
                factunit.fact_state,
                factunit.fact_lower,
                factunit.fact_upper,
                create_missing_kegs=True,
            )


def clear_factunits_from_plan(x_plan: PlanUnit):
    """Deletes all PlanUnit kegroot FactUnits"""
    for fact_reason_context in get_plan_root_facts_dict(x_plan).keys():
        x_plan.del_fact(fact_reason_context)


def plan_keg_reason_caseunit_set_obj(plan: PlanUnit, args: dict[str,]):
    """Wrapper for method that edit planunit keg nodes reasonunits.
    keg_rope: required jkeys
    reason_context: required jkeys
    reason_state: required jkeys
    reason_lower: optional jvalues
    reason_upper: optional jvalues
    reason_divisor: optional jvalues
    """
    keg_rope = args.get("keg_rope")
    reason_context = args.get("reason_context")
    reason_state = args.get("reason_state")
    reason_lower = args.get("reason_lower")
    reason_upper = args.get("reason_upper")
    reason_divisor = args.get("reason_divisor")
    plan.edit_keg_attr(
        keg_rope=keg_rope,
        reason_context=reason_context,
        reason_case=reason_state,
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
    )


def get_plan_unique_short_ropes(plan: PlanUnit) -> dict[RopeTerm, RopeTerm]:
    """Return dict of all keg_ropes and the shortest possible term for that Keg that is unique."""
    return get_unique_short_ropes(set(plan.get_keg_dict().keys()), plan.knot)


def add_frame_to_caseunit(
    x_case: CaseUnit,
    x_frame: int,
    context_keg_close: int,
    context_keg_denom: int,
    context_keg_morph: bool,
):
    """Given any case append number to caseunit reason_lower and reason_upper

    Step 0: calculate modulus:
        If it exists set to the caseunit's reason_divisor
        Else if it exists set to the context keg's close
        Elfe if it exists set to the context keg's denom
    Step 1: morph x_frame
        If context keg's morph is True then divide frame by context_keg_denom
    Step 2: define CaseUnit attrs
        Change CaseUnit's reason_lower and reason_upper range attrs by adding frame
        to each and use modulus to make result is not negative or more then modulus.


    """
    modulus = x_case.reason_divisor or context_keg_close or context_keg_denom
    if not context_keg_morph:
        x_frame //= get_1_if_None(context_keg_denom)
    x_case.reason_lower = modular_addition(x_case.reason_lower, x_frame, modulus)
    x_case.reason_upper = modular_addition(x_case.reason_upper, x_frame, modulus)


def add_frame_to_reasonunit(
    x_reason: ReasonUnit,
    x_int: int,
    context_keg_close: int,
    context_keg_denom: int,
    context_keg_morph: bool,
):
    for x_case in x_reason.cases.values():
        if x_case.reason_lower and x_case.reason_upper:
            add_frame_to_caseunit(
                x_case,
                x_int,
                context_keg_close,
                context_keg_denom,
                context_keg_morph,
            )


def add_frame_to_factunit(x_factunit: FactUnit, x_int: int, context_keg_close: int):
    if x_factunit.fact_lower and x_factunit.fact_upper:
        x_lower = modular_addition(x_factunit.fact_lower, x_int, context_keg_close)
        x_upper = modular_addition(x_factunit.fact_upper, x_int, context_keg_close)
        x_factunit.fact_lower = x_lower
        x_factunit.fact_upper = x_upper


def add_frame_to_planunit(
    x_plan: PlanUnit, x_int: int, required_context_subrope: RopeTerm = None
):
    required_context_subrope = get_empty_str_if_None(required_context_subrope)
    for x_keg in x_plan.get_keg_dict().values():
        for x_reason in x_keg.reasonunits.values():
            if is_sub_rope(x_reason.reason_context, required_context_subrope):
                reason_context_keg = x_plan.get_keg_obj(x_reason.reason_context)
                close = reason_context_keg.close
                denom = reason_context_keg.denom
                morph = reason_context_keg.morph
                add_frame_to_reasonunit(x_reason, x_int, close, denom, morph)
        for x_fact in x_keg.factunits.values():
            if is_sub_rope(x_fact.fact_context, required_context_subrope):
                fact_context_keg = x_plan.get_keg_obj(x_fact.fact_context)
                add_frame_to_factunit(x_fact, x_int, fact_context_keg.close)
