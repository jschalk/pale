from src.ch00_py.dict_toolbox import get_from_nested_dict
from src.ch07_plan_logic.plan_main import PlanUnit
from src.ch08_plan_atom.atom_main import PlanAtom
from src.ch09_plan_lesson.delta import PlanDelta


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_from_nested_dict(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: PlanDelta, x_plan: PlanUnit) -> list[str]:
    atoms_dict = x_delta.planatoms
    planunit_atom = get_leg_obj(atoms_dict, ["UPDATE", "planunit"])

    personunit_insert_dict = get_leg_obj(atoms_dict, ["INSERT", "plan_personunit"])
    personunit_update_dict = get_leg_obj(atoms_dict, ["UPDATE", "plan_personunit"])
    personunit_delete_dict = get_leg_obj(atoms_dict, ["DELETE", "plan_personunit"])

    x_list = ["INSERT", "plan_person_membership"]
    person_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "plan_person_membership"]
    person_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_person_membership"]
    person_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_kegunit"]
    plan_kegunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "plan_kegunit"]
    plan_kegunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_kegunit"]
    plan_kegunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_keg_awardunit"]
    plan_keg_awardunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "plan_keg_awardunit"]
    plan_keg_awardunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_keg_awardunit"]
    plan_keg_awardunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_keg_reasonunit"]
    plan_keg_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "plan_keg_reasonunit"]
    plan_keg_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_keg_reasonunit"]
    plan_keg_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_keg_reason_caseunit"]
    plan_keg_reason_caseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "plan_keg_reason_caseunit"]
    plan_keg_reason_caseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_keg_reason_caseunit"]
    plan_keg_reason_caseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_keg_partyunit"]
    plan_keg_partyunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_keg_partyunit"]
    plan_keg_partyunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_keg_healerunit"]
    plan_keg_healerunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_keg_healerunit"]
    plan_keg_healerunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "plan_keg_factunit"]
    plan_keg_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "plan_keg_factunit"]
    plan_keg_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "plan_keg_factunit"]
    plan_keg_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if planunit_atom is not None:
        add_planunit_legible_list(leg_list, planunit_atom, x_plan)
    if personunit_insert_dict is not None:
        add_plan_personunit_insert_to_legible_list(
            leg_list, personunit_insert_dict, x_plan
        )
    if personunit_update_dict is not None:
        add_plan_personunit_update_to_legible_list(
            leg_list, personunit_update_dict, x_plan
        )
    if personunit_delete_dict is not None:
        add_plan_personunit_delete_to_legible_list(
            leg_list, personunit_delete_dict, x_plan
        )

    if person_membership_insert_dict is not None:
        add_plan_person_membership_insert_to_legible_list(
            leg_list, person_membership_insert_dict, x_plan
        )
    if person_membership_update_dict is not None:
        add_plan_person_membership_update_to_legible_list(
            leg_list, person_membership_update_dict, x_plan
        )
    if person_membership_delete_dict is not None:
        add_plan_person_membership_delete_to_legible_list(
            leg_list, person_membership_delete_dict, x_plan
        )

    if plan_kegunit_insert_dict is not None:
        add_plan_kegunit_insert_to_legible_list(
            leg_list, plan_kegunit_insert_dict, x_plan
        )
    if plan_kegunit_update_dict is not None:
        add_plan_kegunit_update_to_legible_list(
            leg_list, plan_kegunit_update_dict, x_plan
        )
    if plan_kegunit_delete_dict is not None:
        add_plan_kegunit_delete_to_legible_list(
            leg_list, plan_kegunit_delete_dict, x_plan
        )

    if plan_keg_awardunit_insert_dict is not None:
        add_plan_keg_awardunit_insert_to_legible_list(
            leg_list, plan_keg_awardunit_insert_dict, x_plan
        )
    if plan_keg_awardunit_update_dict is not None:
        add_plan_keg_awardunit_update_to_legible_list(
            leg_list, plan_keg_awardunit_update_dict, x_plan
        )
    if plan_keg_awardunit_delete_dict is not None:
        add_plan_keg_awardunit_delete_to_legible_list(
            leg_list, plan_keg_awardunit_delete_dict, x_plan
        )

    if plan_keg_reasonunit_insert_dict is not None:
        add_plan_keg_reasonunit_insert_to_legible_list(
            leg_list, plan_keg_reasonunit_insert_dict, x_plan
        )
    if plan_keg_reasonunit_update_dict is not None:
        add_plan_keg_reasonunit_update_to_legible_list(
            leg_list, plan_keg_reasonunit_update_dict, x_plan
        )
    if plan_keg_reasonunit_delete_dict is not None:
        add_plan_keg_reasonunit_delete_to_legible_list(
            leg_list, plan_keg_reasonunit_delete_dict, x_plan
        )

    if plan_keg_reason_caseunit_insert_dict is not None:
        add_plan_reason_caseunit_insert_to_legible_list(
            leg_list, plan_keg_reason_caseunit_insert_dict, x_plan
        )
    if plan_keg_reason_caseunit_update_dict is not None:
        add_plan_reason_caseunit_update_to_legible_list(
            leg_list, plan_keg_reason_caseunit_update_dict, x_plan
        )
    if plan_keg_reason_caseunit_delete_dict is not None:
        add_plan_reason_caseunit_delete_to_legible_list(
            leg_list, plan_keg_reason_caseunit_delete_dict, x_plan
        )

    if plan_keg_partyunit_insert_dict is not None:
        add_plan_keg_partyunit_insert_to_legible_list(
            leg_list, plan_keg_partyunit_insert_dict, x_plan
        )
    if plan_keg_partyunit_delete_dict is not None:
        add_plan_keg_partyunit_delete_to_legible_list(
            leg_list, plan_keg_partyunit_delete_dict, x_plan
        )

    if plan_keg_healerunit_insert_dict is not None:
        add_plan_keg_healerunit_insert_to_legible_list(
            leg_list, plan_keg_healerunit_insert_dict, x_plan
        )
    if plan_keg_healerunit_delete_dict is not None:
        add_plan_keg_healerunit_delete_to_legible_list(
            leg_list, plan_keg_healerunit_delete_dict, x_plan
        )

    if plan_keg_factunit_insert_dict is not None:
        add_plan_keg_factunit_insert_to_legible_list(
            leg_list, plan_keg_factunit_insert_dict, x_plan
        )
    if plan_keg_factunit_update_dict is not None:
        add_plan_keg_factunit_update_to_legible_list(
            leg_list, plan_keg_factunit_update_dict, x_plan
        )
    if plan_keg_factunit_delete_dict is not None:
        add_plan_keg_factunit_delete_to_legible_list(
            leg_list, plan_keg_factunit_delete_dict, x_plan
        )

    return leg_list


def add_planunit_legible_list(
    legible_list: list[str], x_atom: PlanAtom, x_plan: PlanUnit
):
    jvalues = x_atom.jvalues
    _tally_str = "tally"
    _max_tree_traverse_str = "max_tree_traverse"
    _max_tree_traverse_value = jvalues.get(_max_tree_traverse_str)
    credor_respect_value = jvalues.get("credor_respect")
    debtor_respect_value = jvalues.get("debtor_respect")
    _tally_value = jvalues.get(_tally_str)

    if _max_tree_traverse_value is not None:
        x_str = f"{x_plan.plan_name}'s maximum number of Plan evaluations set to {_max_tree_traverse_value}"
        legible_list.append(x_str)
    if (
        credor_respect_value is not None
        and debtor_respect_value is not None
        and credor_respect_value == debtor_respect_value
    ):
        x_str = f"{x_plan.plan_name}'s total pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif credor_respect_value is not None:
        x_str = f"{x_plan.plan_name}'s credor pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif debtor_respect_value is not None:
        x_str = f"{x_plan.plan_name}'s debtor pool is now {debtor_respect_value}"
        legible_list.append(x_str)
    if _tally_value is not None:
        x_str = f"{x_plan.plan_name}'s plan tally set to {_tally_value}"
        legible_list.append(x_str)


def add_plan_personunit_insert_to_legible_list(
    legible_list: list[str], personunit_dict: PlanAtom, x_plan: PlanUnit
):
    for personunit_atom in personunit_dict.values():
        person_name = personunit_atom.get_value("person_name")
        person_cred_lumen_value = personunit_atom.get_value("person_cred_lumen")
        person_debt_lumen_value = personunit_atom.get_value("person_debt_lumen")
        x_str = f"{person_name} was added with {person_cred_lumen_value} score credit and {person_debt_lumen_value} score debt"
        legible_list.append(x_str)


def add_plan_personunit_update_to_legible_list(
    legible_list: list[str], personunit_dict: PlanAtom, x_plan: PlanUnit
):
    for personunit_atom in personunit_dict.values():
        person_name = personunit_atom.get_value("person_name")
        person_cred_lumen_value = personunit_atom.get_value("person_cred_lumen")
        person_debt_lumen_value = personunit_atom.get_value("person_debt_lumen")
        if person_cred_lumen_value is not None and person_debt_lumen_value is not None:
            x_str = f"{person_name} now has {person_cred_lumen_value} score credit and {person_debt_lumen_value} score debt."
        elif person_cred_lumen_value is not None:
            x_str = f"{person_name} now has {person_cred_lumen_value} score credit."
        elif person_debt_lumen_value is not None:
            x_str = f"{person_name} now has {person_debt_lumen_value} score debt."
        legible_list.append(x_str)


def add_plan_personunit_delete_to_legible_list(
    legible_list: list[str], personunit_dict: PlanAtom, x_plan: PlanUnit
):
    for personunit_atom in personunit_dict.values():
        person_name = personunit_atom.get_value("person_name")
        x_str = f"{person_name} was removed from score persons."
        legible_list.append(x_str)


def add_plan_person_membership_insert_to_legible_list(
    legible_list: list[str],
    person_membership_insert_dict: dict,
    x_plan: PlanUnit,
):
    for person_membership_dict in person_membership_insert_dict.values():
        for person_membership_atom in person_membership_dict.values():
            group_title = person_membership_atom.get_value("group_title")
            person_name = person_membership_atom.get_value("person_name")
            group_cred_lumen_value = person_membership_atom.get_value(
                "group_cred_lumen"
            )
            group_debt_lumen_value = person_membership_atom.get_value(
                "group_debt_lumen"
            )
            x_str = f"Group '{group_title}' has new membership {person_name} with group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
            legible_list.append(x_str)


def add_plan_person_membership_update_to_legible_list(
    legible_list: list[str],
    person_membership_update_dict: dict,
    x_plan: PlanUnit,
):
    for person_membership_dict in person_membership_update_dict.values():
        for person_membership_atom in person_membership_dict.values():
            group_title = person_membership_atom.get_value("group_title")
            person_name = person_membership_atom.get_value("person_name")
            group_cred_lumen_value = person_membership_atom.get_value(
                "group_cred_lumen"
            )
            group_debt_lumen_value = person_membership_atom.get_value(
                "group_debt_lumen"
            )
            if (
                group_cred_lumen_value is not None
                and group_debt_lumen_value is not None
            ):
                x_str = f"Group '{group_title}' membership {person_name} has new group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
            elif group_cred_lumen_value is not None:
                x_str = f"Group '{group_title}' membership {person_name} has new group_cred_lumen_value{group_cred_lumen_value}."
            elif group_debt_lumen_value is not None:
                x_str = f"Group '{group_title}' membership {person_name} has new group_debt_lumen_value={group_debt_lumen_value}."
            legible_list.append(x_str)


def add_plan_person_membership_delete_to_legible_list(
    legible_list: list[str],
    person_membership_delete_dict: dict,
    x_plan: PlanUnit,
):
    for person_membership_dict in person_membership_delete_dict.values():
        for person_membership_atom in person_membership_dict.values():
            group_title = person_membership_atom.get_value("group_title")
            person_name = person_membership_atom.get_value("person_name")
            x_str = f"Group '{group_title}' no longer has membership {person_name}."
            legible_list.append(x_str)


def add_plan_kegunit_insert_to_legible_list(
    legible_list: list[str], kegunit_insert_dict: dict, x_plan: PlanUnit
):
    _problem_bool_str = "problem_bool"
    for kegunit_atom in kegunit_insert_dict.values():
        rope_value = kegunit_atom.get_value("keg_rope")
        _addin_value = kegunit_atom.get_value("addin")
        _begin_value = kegunit_atom.get_value("begin")
        _close_value = kegunit_atom.get_value("close")
        _denom_value = kegunit_atom.get_value("denom")
        _numor_value = kegunit_atom.get_value("numor")
        _problem_bool_value = kegunit_atom.get_value(_problem_bool_str)
        _morph_value = kegunit_atom.get_value("morph")
        _star_value = kegunit_atom.get_value("star")
        pledge_value = kegunit_atom.get_value("pledge")
        x_str = f"Created Keg '{rope_value}'. "
        if _addin_value is not None:
            x_str += f"addin={_addin_value}."
        if _begin_value is not None:
            x_str += f"begin={_begin_value}."
        if _close_value is not None:
            x_str += f"close={_close_value}."
        if _denom_value is not None:
            x_str += f"denom={_denom_value}."
        if _numor_value is not None:
            x_str += f"numor={_numor_value}."
        if _problem_bool_value is not None:
            x_str += f"problem_bool={_problem_bool_value}."
        if _morph_value is not None:
            x_str += f"morph={_morph_value}."
        if _star_value is not None:
            x_str += f"star={_star_value}."
        if pledge_value is not None:
            x_str += f"pledge={pledge_value}."

        legible_list.append(x_str)


def add_plan_kegunit_update_to_legible_list(
    legible_list: list[str], kegunit_update_dict: dict, x_plan: PlanUnit
):
    _problem_bool_str = "problem_bool"
    for kegunit_atom in kegunit_update_dict.values():
        rope_value = kegunit_atom.get_value("keg_rope")
        addin_value = kegunit_atom.get_value("addin")
        begin_value = kegunit_atom.get_value("begin")
        close_value = kegunit_atom.get_value("close")
        denom_value = kegunit_atom.get_value("denom")
        numor_value = kegunit_atom.get_value("numor")
        problem_bool_value = kegunit_atom.get_value(_problem_bool_str)
        morph_value = kegunit_atom.get_value("morph")
        star_value = kegunit_atom.get_value("star")
        pledge_value = kegunit_atom.get_value("pledge")
        x_str = f"Keg '{rope_value}' set these attrs: "
        if addin_value is not None:
            x_str += f"addin={addin_value}."
        if begin_value is not None:
            x_str += f"begin={begin_value}."
        if close_value is not None:
            x_str += f"close={close_value}."
        if denom_value is not None:
            x_str += f"denom={denom_value}."
        if numor_value is not None:
            x_str += f"numor={numor_value}."
        if problem_bool_value is not None:
            x_str += f"problem_bool={problem_bool_value}."
        if morph_value is not None:
            x_str += f"morph={morph_value}."
        if star_value is not None:
            x_str += f"star={star_value}."
        if pledge_value is not None:
            x_str += f"pledge={pledge_value}."

        legible_list.append(x_str)


def add_plan_kegunit_delete_to_legible_list(
    legible_list: list[str], kegunit_delete_dict: dict, x_plan: PlanUnit
):
    for kegunit_atom in kegunit_delete_dict.values():
        rope_value = kegunit_atom.get_value("keg_rope")
        x_str = f"Keg '{rope_value}' was deleted."
        legible_list.append(x_str)


def add_plan_keg_awardunit_insert_to_legible_list(
    legible_list: list[str], keg_awardunit_insert_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_awardunit_insert_dict.values():
        for keg_awardunit_atom in rope_dict.values():
            awardee_title_value = keg_awardunit_atom.get_value("awardee_title")
            rope_value = keg_awardunit_atom.get_value("keg_rope")
            give_force_value = keg_awardunit_atom.get_value("give_force")
            take_force_value = keg_awardunit_atom.get_value("take_force")
            x_str = f"AwardUnit created for group {awardee_title_value} for keg '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_plan_keg_awardunit_update_to_legible_list(
    legible_list: list[str], keg_awardunit_update_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_awardunit_update_dict.values():
        for keg_awardunit_atom in rope_dict.values():
            awardee_title_value = keg_awardunit_atom.get_value("awardee_title")
            rope_value = keg_awardunit_atom.get_value("keg_rope")
            give_force_value = keg_awardunit_atom.get_value("give_force")
            take_force_value = keg_awardunit_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for keg '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for keg '{rope_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for keg '{rope_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_plan_keg_awardunit_delete_to_legible_list(
    legible_list: list[str], keg_awardunit_delete_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_awardunit_delete_dict.values():
        for keg_awardunit_atom in rope_dict.values():
            awardee_title_value = keg_awardunit_atom.get_value("awardee_title")
            rope_value = keg_awardunit_atom.get_value("keg_rope")
            x_str = f"AwardUnit for group {awardee_title_value}, keg '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_plan_keg_reasonunit_insert_to_legible_list(
    legible_list: list[str], keg_reasonunit_insert_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_reasonunit_insert_dict.values():
        for keg_reasonunit_atom in rope_dict.values():
            rope_value = keg_reasonunit_atom.get_value("keg_rope")
            reason_context_value = keg_reasonunit_atom.get_value("reason_context")
            active_requisite_value = keg_reasonunit_atom.get_value("active_requisite")
            x_str = f"ReasonUnit created for keg '{rope_value}' with reason_context '{reason_context_value}'."
            if active_requisite_value is not None:
                x_str += f" active_requisite={active_requisite_value}."
            legible_list.append(x_str)


def add_plan_keg_reasonunit_update_to_legible_list(
    legible_list: list[str], keg_reasonunit_update_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_reasonunit_update_dict.values():
        for keg_reasonunit_atom in rope_dict.values():
            rope_value = keg_reasonunit_atom.get_value("keg_rope")
            reason_context_value = keg_reasonunit_atom.get_value("reason_context")
            active_requisite_value = keg_reasonunit_atom.get_value("active_requisite")
            if active_requisite_value is not None:
                x_str = f"ReasonUnit reason_context='{reason_context_value}' for keg '{rope_value}' set with active_requisite={active_requisite_value}."
            else:
                x_str = f"ReasonUnit reason_context='{reason_context_value}' for keg '{rope_value}' and no longer checks reason_context active mode."
            legible_list.append(x_str)


def add_plan_keg_reasonunit_delete_to_legible_list(
    legible_list: list[str], keg_reasonunit_delete_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_reasonunit_delete_dict.values():
        for keg_reasonunit_atom in rope_dict.values():
            rope_value = keg_reasonunit_atom.get_value("keg_rope")
            reason_context_value = keg_reasonunit_atom.get_value("reason_context")
            x_str = f"ReasonUnit reason_context='{reason_context_value}' for keg '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_plan_reason_caseunit_insert_to_legible_list(
    legible_list: list[str],
    keg_reason_caseunit_insert_dict: dict,
    x_plan: PlanUnit,
):
    for rope_dict in keg_reason_caseunit_insert_dict.values():
        for reason_context_dict in rope_dict.values():
            for keg_reason_caseunit_atom in reason_context_dict.values():
                rope_value = keg_reason_caseunit_atom.get_value("keg_rope")
                reason_context_value = keg_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = keg_reason_caseunit_atom.get_value("reason_state")
                reason_divisor_value = keg_reason_caseunit_atom.get_value(
                    "reason_divisor"
                )
                reason_upper_value = keg_reason_caseunit_atom.get_value("reason_upper")
                reason_lower_value = keg_reason_caseunit_atom.get_value("reason_lower")
                x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for keg '{rope_value}'."
                if reason_lower_value is not None:
                    x_str += f" reason_lower={reason_lower_value}."
                if reason_upper_value is not None:
                    x_str += f" reason_upper={reason_upper_value}."
                if reason_divisor_value is not None:
                    x_str += f" reason_divisor={reason_divisor_value}."
                legible_list.append(x_str)


def add_plan_reason_caseunit_update_to_legible_list(
    legible_list: list[str],
    keg_reason_caseunit_update_dict: dict,
    x_plan: PlanUnit,
):
    for rope_dict in keg_reason_caseunit_update_dict.values():
        for reason_context_dict in rope_dict.values():
            for keg_reason_caseunit_atom in reason_context_dict.values():
                rope_value = keg_reason_caseunit_atom.get_value("keg_rope")
                reason_context_value = keg_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = keg_reason_caseunit_atom.get_value("reason_state")
                reason_divisor_value = keg_reason_caseunit_atom.get_value(
                    "reason_divisor"
                )
                reason_upper_value = keg_reason_caseunit_atom.get_value("reason_upper")
                reason_lower_value = keg_reason_caseunit_atom.get_value("reason_lower")
                x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for keg '{rope_value}'."
                if reason_lower_value is not None:
                    x_str += f" reason_lower={reason_lower_value}."
                if reason_upper_value is not None:
                    x_str += f" reason_upper={reason_upper_value}."
                if reason_divisor_value is not None:
                    x_str += f" reason_divisor={reason_divisor_value}."
                legible_list.append(x_str)


def add_plan_reason_caseunit_delete_to_legible_list(
    legible_list: list[str],
    keg_reason_caseunit_delete_dict: dict,
    x_plan: PlanUnit,
):
    for rope_dict in keg_reason_caseunit_delete_dict.values():
        for reason_context_dict in rope_dict.values():
            for keg_reason_caseunit_atom in reason_context_dict.values():
                rope_value = keg_reason_caseunit_atom.get_value("keg_rope")
                reason_context_value = keg_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = keg_reason_caseunit_atom.get_value("reason_state")
                x_str = f"CaseUnit '{reason_state_value}' deleted from reason '{reason_context_value}' for keg '{rope_value}'."
                legible_list.append(x_str)


def add_plan_keg_partyunit_insert_to_legible_list(
    legible_list: list[str], keg_partyunit_insert_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_partyunit_insert_dict.values():
        for keg_partyunit_atom in rope_dict.values():
            party_title_value = keg_partyunit_atom.get_value("party_title")
            rope_value = keg_partyunit_atom.get_value("keg_rope")
            x_str = f"partyunit '{party_title_value}' created for keg '{rope_value}'."
            legible_list.append(x_str)


def add_plan_keg_partyunit_delete_to_legible_list(
    legible_list: list[str], keg_partyunit_delete_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_partyunit_delete_dict.values():
        for keg_partyunit_atom in rope_dict.values():
            party_title_value = keg_partyunit_atom.get_value("party_title")
            rope_value = keg_partyunit_atom.get_value("keg_rope")
            x_str = f"partyunit '{party_title_value}' deleted for keg '{rope_value}'."
            legible_list.append(x_str)


def add_plan_keg_healerunit_insert_to_legible_list(
    legible_list: list[str], keg_healerunit_insert_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_healerunit_insert_dict.values():
        for keg_healerunit_atom in rope_dict.values():
            healer_name_value = keg_healerunit_atom.get_value("healer_name")
            rope_value = keg_healerunit_atom.get_value("keg_rope")
            x_str = f"HealerUnit '{healer_name_value}' created for keg '{rope_value}'."
            legible_list.append(x_str)


def add_plan_keg_healerunit_delete_to_legible_list(
    legible_list: list[str], keg_healerunit_delete_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_healerunit_delete_dict.values():
        for keg_healerunit_atom in rope_dict.values():
            healer_name_value = keg_healerunit_atom.get_value("healer_name")
            rope_value = keg_healerunit_atom.get_value("keg_rope")
            x_str = f"HealerUnit '{healer_name_value}' deleted for keg '{rope_value}'."
            legible_list.append(x_str)


def add_plan_keg_factunit_insert_to_legible_list(
    legible_list: list[str], keg_factunit_insert_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_factunit_insert_dict.values():
        for keg_factunit_atom in rope_dict.values():
            rope_value = keg_factunit_atom.get_value("keg_rope")
            fact_context_value = keg_factunit_atom.get_value("fact_context")
            fact_state_value = keg_factunit_atom.get_value("fact_state")
            fact_upper_value = keg_factunit_atom.get_value("fact_upper")
            fact_lower_value = keg_factunit_atom.get_value("fact_lower")
            x_str = f"FactUnit '{fact_state_value}' created for reason_context '{fact_context_value}' for keg '{rope_value}'."
            if fact_lower_value is not None:
                x_str += f" fact_lower={fact_lower_value}."
            if fact_upper_value is not None:
                x_str += f" fact_upper={fact_upper_value}."
            legible_list.append(x_str)


def add_plan_keg_factunit_update_to_legible_list(
    legible_list: list[str], keg_factunit_update_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_factunit_update_dict.values():
        for keg_factunit_atom in rope_dict.values():
            rope_value = keg_factunit_atom.get_value("keg_rope")
            fact_context_value = keg_factunit_atom.get_value("fact_context")
            fact_state_value = keg_factunit_atom.get_value("fact_state")
            fact_upper_value = keg_factunit_atom.get_value("fact_upper")
            fact_lower_value = keg_factunit_atom.get_value("fact_lower")
            x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{fact_context_value}' for keg '{rope_value}'."
            if fact_lower_value is not None:
                x_str += f" fact_lower={fact_lower_value}."
            if fact_upper_value is not None:
                x_str += f" fact_upper={fact_upper_value}."
            legible_list.append(x_str)


def add_plan_keg_factunit_delete_to_legible_list(
    legible_list: list[str], keg_factunit_delete_dict: dict, x_plan: PlanUnit
):
    for rope_dict in keg_factunit_delete_dict.values():
        for keg_factunit_atom in rope_dict.values():
            rope_value = keg_factunit_atom.get_value("keg_rope")
            fact_context_value = keg_factunit_atom.get_value("fact_context")
            fact_state_value = keg_factunit_atom.get_value("fact_state")
            x_str = f"FactUnit reason_context '{fact_context_value}' deleted for keg '{rope_value}'."
            legible_list.append(x_str)
