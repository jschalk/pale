from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_False_if_None,
)
from src.ch01_allot.allot import (
    allot_scale,
    default_grain_num_if_None,
    valid_allotment_ratio,
    validate_pool_num,
)
from src.ch02_person.group import AwardUnit, GroupUnit, groupunit_shop, membership_shop
from src.ch02_person.person import (
    PersonUnit,
    personunit_shop,
    personunits_get_from_dict,
)
from src.ch03_labor.labor import LaborUnit
from src.ch04_rope.rope import (
    all_ropes_between,
    create_rope,
    default_knot_if_None,
    get_all_rope_labels,
    get_ancestor_ropes,
    get_default_first_label,
    get_first_label_from_rope,
    get_forefather_ropes,
    get_parent_rope,
    get_tail_label,
    is_string_in_rope,
    is_sub_rope,
    rebuild_rope,
    rope_is_valid_dir_path,
    to_rope,
)
from src.ch05_reason.reason_main import FactUnit, ReasonUnit, RopeTerm, factunit_shop
from src.ch06_keg.healer import HealerUnit
from src.ch06_keg.keg import (
    KegAttrHolder,
    KegUnit,
    get_obj_from_keg_dict,
    kegattrholder_shop,
    kegunit_shop,
)
from src.ch07_plan_logic._ref.ch07_semantic_types import (
    FactNum,
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    ManaGrain,
    MomentRope,
    PersonName,
    PlanName,
    ReasonNum,
    RespectGrain,
    RespectNum,
    RopeTerm,
)
from src.ch07_plan_logic.plan_config import max_tree_traverse_default
from src.ch07_plan_logic.tree_metric import TreeMetrics, treemetrics_shop


class InvalidPlanException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class NewKnotException(Exception):
    pass


class reason_caseException(Exception):
    pass


class PersonUnitsCredorDebtorSumException(Exception):
    pass


class PersonMissingException(Exception):
    pass


class keeps_justException(Exception):
    pass


class _bit_RatioException(Exception):
    pass


class _last_lesson_idException(Exception):
    pass


class healerunit_group_title_Exception(Exception):
    pass


class gogo_calc_stop_calc_Exception(Exception):
    pass


@dataclass
class PlanUnit:
    plan_name: PlanName = None
    moment_rope: MomentRope = None
    knot: KnotTerm = None
    fund_pool: FundNum = None
    fund_grain: FundGrain = None
    respect_grain: RespectGrain = None
    mana_grain: ManaGrain = None
    tally: float = None
    persons: dict[PersonName, PersonUnit] = None
    kegroot: KegUnit = None
    credor_respect: RespectNum = None
    debtor_respect: RespectNum = None
    max_tree_traverse: int = None
    last_lesson_id: int = None
    # fields calculated by cashout
    _keg_dict: dict[RopeTerm, KegUnit] = None
    _keep_dict: dict[RopeTerm, KegUnit] = None
    _healers_dict: dict[HealerName, dict[RopeTerm, KegUnit]] = None
    tree_traverse_count: int = None
    rational: bool = None
    keeps_justified: bool = None
    keeps_buildable: bool = None
    sum_healerunit_kegs_fund_total: float = None
    groupunits: dict[GroupTitle, GroupUnit] = None
    offtrack_kids_star_set: set[RopeTerm] = None
    offtrack_fund: float = None
    reason_contexts: set[RopeTerm] = None
    range_inheritors: dict[RopeTerm, RopeTerm] = None

    def del_last_lesson_id(self):
        self.last_lesson_id = None

    def set_last_lesson_id(self, x_last_lesson_id: int):
        if self.last_lesson_id is not None and x_last_lesson_id < self.last_lesson_id:
            exception_str = f"Cannot set _last_lesson_id to {x_last_lesson_id} because it is less than {self.last_lesson_id}."
            raise _last_lesson_idException(exception_str)
        self.last_lesson_id = x_last_lesson_id

    def set_fund_pool(self, x_fund_pool):
        if valid_allotment_ratio(x_fund_pool, self.fund_grain) is False:
            exception_str = f"Plan '{self.plan_name}' cannot set fund_pool='{x_fund_pool}'. It is not divisible by fund_grain '{self.fund_grain}'"
            raise _bit_RatioException(exception_str)

        self.fund_pool = validate_pool_num(x_fund_pool)

    def set_person_respect(self, x_person_pool: int):
        self.set_credor_respect(x_person_pool)
        self.set_debtor_respect(x_person_pool)
        self.set_fund_pool(x_person_pool)

    def set_credor_respect(self, new_credor_respect: int):
        if valid_allotment_ratio(new_credor_respect, self.respect_grain) is False:
            exception_str = f"Plan '{self.plan_name}' cannot set credor_respect='{new_credor_respect}'. It is not divisible byrespect_grain'{self.respect_grain}'"
            raise _bit_RatioException(exception_str)
        self.credor_respect = new_credor_respect

    def set_debtor_respect(self, new_debtor_respect: int):
        if valid_allotment_ratio(new_debtor_respect, self.respect_grain) is False:
            exception_str = f"Plan '{self.plan_name}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible byrespect_grain'{self.respect_grain}'"
            raise _bit_RatioException(exception_str)
        self.debtor_respect = new_debtor_respect

    def make_rope(
        self,
        parent_rope: RopeTerm = None,
        tail_label: LabelTerm = None,
    ) -> RopeTerm:
        return create_rope(
            parent_rope=parent_rope,
            tail_label=tail_label,
            knot=self.knot,
        )

    def make_l1_rope(self, l1_label: LabelTerm):
        return self.make_rope(self.kegroot.keg_label, l1_label)

    def set_knot(self, new_knot: KnotTerm):
        self.cashout()
        if self.knot != new_knot:
            for x_keg_rope in self._keg_dict.keys():
                if is_string_in_rope(new_knot, x_keg_rope):
                    exception_str = f"Cannot modify knot to '{new_knot}' because it exists an keg keg_label '{x_keg_rope}'"
                    raise NewKnotException(exception_str)

            # modify all rope attrs in kegunits
            self.knot = default_knot_if_None(new_knot)
            for x_keg in self._keg_dict.values():
                x_keg.set_knot(self.knot)

    def set_max_tree_traverse(self, x_int: int):
        if x_int < 2 or not float(x_int).is_integer():
            raise InvalidPlanException(
                f"set_max_tree_traverse: '{x_int}' must be number that is 2 or greater"
            )
        else:
            self.max_tree_traverse = x_int

    def _get_relevant_ropes(self, ropes: dict[RopeTerm,]) -> set[RopeTerm]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for x_rope in ropes:
            to_evaluate_list.append(x_rope)
            to_evaluate_hx_dict[x_rope] = "to_evaluate"
        evaluated_ropes = set()

        # while ropes_to_evaluate != [] and count_x <= tree_metrics.label_count:
        # Why count_x? because count_x might be wrong attr to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            x_rope = to_evaluate_list.pop()
            x_keg = self.get_keg_obj(x_rope)
            for reasonunit_obj in x_keg.reasonunits.values():
                reason_context = reasonunit_obj.reason_context
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_rope=reason_context,
                    rope_type="reasonunit_reason_context",
                )
            forefather_ropes = get_forefather_ropes(x_rope)
            for forefather_rope in forefather_ropes:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_rope=forefather_rope,
                    rope_type="forefather",
                )

            evaluated_ropes.add(x_rope)
        return evaluated_ropes

    def _evaluate_relevancy(
        self,
        to_evaluate_list: list[RopeTerm],
        to_evaluate_hx_dict: dict[RopeTerm, int],
        to_evaluate_rope: RopeTerm,
        rope_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_rope) is None:
            to_evaluate_list.append(to_evaluate_rope)
            to_evaluate_hx_dict[to_evaluate_rope] = rope_type

            if rope_type == "reasonunit_reason_context":
                ru_reason_context_keg = self.get_keg_obj(to_evaluate_rope)
                for (
                    descendant_rope
                ) in ru_reason_context_keg.get_descendant_ropes_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_rope=descendant_rope,
                        rope_type="reasonunit_descendant",
                    )

    def all_kegs_relevant_to_pledge_keg(self, rope: RopeTerm) -> bool:
        pledge_keg_assoc_set = set(self._get_relevant_ropes({rope}))
        all_kegs_set = set(self.get_keg_tree_ordered_rope_list())
        return all_kegs_set == all_kegs_set & (pledge_keg_assoc_set)

    def get_awardunits_metrics(self) -> dict[GroupTitle, AwardUnit]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.awardunits_metrics

    def add_to_groupunit_fund_give_fund_take(
        self,
        group_title: GroupTitle,
        awardheir_fund_give: float,
        awardheir_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_title)
        if x_groupunit is not None:
            x_groupunit.fund_give += awardheir_fund_give
            x_groupunit.fund_take += awardheir_fund_take

    def add_to_groupunit_fund_agenda_give_take(
        self,
        group_title: GroupTitle,
        awardline_fund_give: float,
        awardline_fund_take: float,
    ):
        x_groupunit = self.get_groupunit(group_title)
        if awardline_fund_give is not None and awardline_fund_take is not None:
            x_groupunit.fund_agenda_give += awardline_fund_give
            x_groupunit.fund_agenda_take += awardline_fund_take

    def add_to_personunit_fund_give_take(
        self,
        personunit_person_name: PersonName,
        fund_give,
        fund_take: float,
        fund_agenda_give: float,
        fund_agenda_take: float,
    ):
        x_personunit = self.get_person(personunit_person_name)
        x_personunit.add_person_fund_give_take(
            fund_give=fund_give,
            fund_take=fund_take,
            fund_agenda_give=fund_agenda_give,
            fund_agenda_take=fund_agenda_take,
        )

    def del_personunit(self, person_name: str):
        self.persons.pop(person_name)

    def add_personunit(
        self,
        person_name: PersonName,
        person_cred_lumen: int = None,
        person_debt_lumen: int = None,
    ):
        x_knot = self.knot
        personunit = personunit_shop(
            person_name, person_cred_lumen, person_debt_lumen, x_knot
        )
        self.set_personunit(personunit)

    def set_personunit(
        self, x_personunit: PersonUnit, auto_set_membership: bool = True
    ):
        if x_personunit.groupmark != self.knot:
            x_personunit.groupmark = self.knot
        if x_personunit.respect_grain != self.respect_grain:
            x_personunit.respect_grain = self.respect_grain
        if auto_set_membership and x_personunit.memberships_exist() is False:
            x_personunit.add_membership(x_personunit.person_name)
        self.persons[x_personunit.person_name] = x_personunit

    def person_exists(self, person_name: PersonName) -> bool:
        return self.get_person(person_name) is not None

    def edit_personunit(
        self,
        person_name: PersonName,
        person_cred_lumen: int = None,
        person_debt_lumen: int = None,
    ):
        if self.persons.get(person_name) is None:
            raise PersonMissingException(f"PersonUnit '{person_name}' does not exist.")
        x_personunit = self.get_person(person_name)
        if person_cred_lumen is not None:
            x_personunit.set_person_cred_lumen(person_cred_lumen)
        if person_debt_lumen is not None:
            x_personunit.set_person_debt_lumen(person_debt_lumen)
        self.set_personunit(x_personunit)

    def clear_personunits_memberships(self):
        for x_personunit in self.persons.values():
            x_personunit.clear_memberships()

    def get_person(self, person_name: PersonName) -> PersonUnit:
        return self.persons.get(person_name)

    def get_personunit_group_titles_dict(self) -> dict[GroupTitle, set[PersonName]]:
        x_dict = {}
        for x_personunit in self.persons.values():
            for x_group_title in x_personunit.memberships.keys():
                person_name_set = x_dict.get(x_group_title)
                if person_name_set is None:
                    x_dict[x_group_title] = {x_personunit.person_name}
                else:
                    person_name_set.add(x_personunit.person_name)
                    x_dict[x_group_title] = person_name_set
        return x_dict

    def set_groupunit(self, x_groupunit: GroupUnit):
        x_groupunit.fund_grain = self.fund_grain
        self.groupunits[x_groupunit.group_title] = x_groupunit

    def groupunit_exists(self, group_title: GroupTitle) -> bool:
        return self.groupunits.get(group_title) is not None

    def get_groupunit(self, x_group_title: GroupTitle) -> GroupUnit:
        return self.groupunits.get(x_group_title)

    def create_symmetry_groupunit(self, x_group_title: GroupTitle) -> GroupUnit:
        x_groupunit = groupunit_shop(x_group_title)
        for x_personunit in self.persons.values():
            x_membership = membership_shop(
                group_title=x_group_title,
                group_cred_lumen=x_personunit.person_cred_lumen,
                group_debt_lumen=x_personunit.person_debt_lumen,
                person_name=x_personunit.person_name,
            )
            x_groupunit.set_g_membership(x_membership)
        return x_groupunit

    def get_tree_traverse_generated_groupunits(self) -> set[GroupTitle]:
        x_personunit_group_titles = set(self.get_personunit_group_titles_dict().keys())
        all_group_titles = set(self.groupunits.keys())
        return all_group_titles.difference(x_personunit_group_titles)

    def _is_keg_rangeroot(self, keg_rope: RopeTerm) -> bool:
        parent_rope = get_parent_rope(keg_rope)
        parent_keg = self.get_keg_obj(parent_rope)
        return not parent_keg.has_begin_close()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self.kegroot.factunits.values()
            if fact.fact_lower is not None
            and fact.fact_upper is not None
            and self._is_keg_rangeroot(keg_rope=fact.fact_context)
        ]

    def add_fact(
        self,
        fact_context: RopeTerm,
        fact_state: RopeTerm = None,
        fact_lower: FactNum = None,
        fact_upper: FactNum = None,
        create_missing_kegs: bool = None,
    ):
        """Sets kegroot factunit"""
        fact_state = fact_context if fact_state is None else fact_state
        if create_missing_kegs:
            self._create_kegkid_if_empty(rope=fact_context)
            self._create_kegkid_if_empty(rope=fact_state)

        fact_context_keg = self.get_keg_obj(fact_context)
        x_kegroot = self.kegroot
        x_fact_lower = None
        if fact_upper is not None and fact_lower is None:
            x_fact_lower = x_kegroot.factunits.get(fact_context).fact_lower
        else:
            x_fact_lower = fact_lower
        x_fact_upper = None
        if fact_lower is not None and fact_upper is None:
            x_fact_upper = x_kegroot.factunits.get(fact_context).fact_upper
        else:
            x_fact_upper = fact_upper
        x_factunit = factunit_shop(
            fact_context=fact_context,
            fact_state=fact_state,
            fact_lower=x_fact_lower,
            fact_upper=x_fact_upper,
        )

        if fact_context_keg.has_begin_close() is False:
            x_kegroot.set_factunit(x_factunit)
        # if fact's keg no range or is a "rangeroot" then allow fact to be set
        elif (
            fact_context_keg.has_begin_close()
            and self._is_keg_rangeroot(fact_context) is False
        ):
            raise InvalidPlanException(
                f"Non rangeroot fact:{fact_context} can only be set by rangeroot fact"
            )
        elif fact_context_keg.has_begin_close() and self._is_keg_rangeroot(
            fact_context
        ):
            # WHEN keg is "rangeroot" identify any reason.reason_contexts that are descendants
            # calculate and set those descendant facts
            # example: zietline range (0-, 1.5e9) is rangeroot
            # example: "zietline,wks" (spllt 10080) is range-descendant
            # there exists a reason reason_context "zietline,wks" with case.reason_state = "zietline,wks"
            # and (1,2) reason_divisor=2 (every other wk)
            #
            # should not set "zietline,wks" fact, only "zietline" fact and
            # "zietline,wks" should be set automatica_lly since there exists a reason
            # that has that reason_context.
            x_kegroot.set_factunit(x_factunit)

    def get_fact(self, fact_context: RopeTerm) -> FactUnit:
        return self.kegroot.factunits.get(fact_context)

    def del_fact(self, fact_context: RopeTerm):
        self.kegroot.del_factunit(fact_context)

    def get_keg_dict(self, problem: bool = None) -> dict[RopeTerm, KegUnit]:
        self.cashout()
        if not problem:
            return self._keg_dict
        if self.keeps_justified is False:
            exception_str = f"Cannot return problem set because keeps_justified={self.keeps_justified}."
            raise keeps_justException(exception_str)

        x_kegs = self._keg_dict.values()
        return {x_keg.get_keg_rope(): x_keg for x_keg in x_kegs if x_keg.problem_bool}

    def get_tree_metrics(self) -> TreeMetrics:
        self.cashout()
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_label(
            tree_level=self.kegroot.tree_level,
            reasons=self.kegroot.reasonunits,
            awardunits=self.kegroot.awardunits,
            uid=self.kegroot.uid,
            pledge=self.kegroot.pledge,
            keg_rope=self.kegroot.get_keg_rope(),
        )

        x_keg_list = [self.kegroot]
        while x_keg_list != []:
            parent_keg = x_keg_list.pop()
            for keg_kid in parent_keg.kids.values():
                self._eval_tree_metrics(parent_keg, keg_kid, tree_metrics, x_keg_list)
        return tree_metrics

    def _eval_tree_metrics(self, parent_keg, keg_kid, tree_metrics, x_keg_list):
        keg_kid.tree_level = parent_keg.tree_level + 1
        tree_metrics.evaluate_label(
            tree_level=keg_kid.tree_level,
            reasons=keg_kid.reasonunits,
            awardunits=keg_kid.awardunits,
            uid=keg_kid.uid,
            pledge=keg_kid.pledge,
            keg_rope=keg_kid.get_keg_rope(),
        )
        x_keg_list.append(keg_kid)

    def get_keg_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_keg_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        keg_uid_max = tree_metrics.uid_max
        keg_uid_dict = tree_metrics.uid_dict

        for x_keg in self.get_keg_dict().values():
            if x_keg.uid is None or keg_uid_dict.get(x_keg.uid) > 1:
                new_keg_uid_max = keg_uid_max + 1
                self.edit_keg_attr(keg_rope=x_keg.get_keg_rope(), uid=new_keg_uid_max)
                keg_uid_max = new_keg_uid_max

    def get_reason_contexts(self) -> set[RopeTerm]:
        return set(self.get_tree_metrics().reason_contexts.keys())

    def get_missing_fact_reason_contexts(self) -> dict[RopeTerm, int]:
        tree_metrics = self.get_tree_metrics()
        reason_contexts = tree_metrics.reason_contexts
        missing_reason_contexts = {}
        for reason_context, reason_context_count in reason_contexts.items():
            try:
                self.kegroot.factunits[reason_context]
            except KeyError:
                missing_reason_contexts[reason_context] = reason_context_count
        return missing_reason_contexts

    def add_keg(
        self, keg_rope: RopeTerm, star: float = None, pledge: bool = None
    ) -> KegUnit:
        """default star is 0, pledges will have weight of 0 if star is not passed"""
        x_keg_label = get_tail_label(keg_rope, self.knot)
        x_parent_rope = get_parent_rope(keg_rope, self.knot)
        x_kegunit = kegunit_shop(x_keg_label, star=star)
        if pledge:
            x_kegunit.pledge = True
        self.set_keg_obj(x_kegunit, x_parent_rope)
        return x_kegunit

    def set_l1_keg(
        self,
        keg_kid: KegUnit,
        create_missing_kegs: bool = None,
        get_rid_of_missing_awardunits_awardee_titles: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.set_keg_obj(
            keg_kid=keg_kid,
            parent_rope=self.kegroot.get_keg_rope(),
            create_missing_kegs=create_missing_kegs,
            get_rid_of_missing_awardunits_awardee_titles=get_rid_of_missing_awardunits_awardee_titles,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def set_keg_obj(
        self,
        keg_kid: KegUnit,
        parent_rope: RopeTerm,
        get_rid_of_missing_awardunits_awardee_titles: bool = None,
        create_missing_kegs: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        parent_rope = to_rope(parent_rope, self.knot)
        if LabelTerm(keg_kid.keg_label).is_label(self.knot) is False:
            x_str = f"set_keg failed because '{keg_kid.keg_label}' is not a LabelTerm."
            raise InvalidPlanException(x_str)

        x_first_label = get_first_label_from_rope(parent_rope, self.knot)
        if self.kegroot.keg_label != x_first_label:
            exception_str = f"set_keg failed because parent_rope '{parent_rope}' has an invalid root rope. Should be {self.kegroot.get_keg_rope()}."
            raise InvalidPlanException(exception_str)

        keg_kid.knot = self.knot
        if keg_kid.fund_grain != self.fund_grain:
            keg_kid.fund_grain = self.fund_grain
        if not get_rid_of_missing_awardunits_awardee_titles:
            keg_kid = self._get_filtered_awardunits_keg(keg_kid)
        keg_kid.set_parent_rope(parent_rope=parent_rope)

        # create any missing kegs
        if not create_missing_ancestors and self.keg_exists(parent_rope) is False:
            x_str = f"set_keg failed because '{parent_rope}' keg does not exist."
            raise InvalidPlanException(x_str)
        parent_rope_keg = self.get_keg_obj(parent_rope, create_missing_ancestors)
        parent_rope_keg.add_kid(keg_kid)

        kid_rope = self.make_rope(parent_rope, keg_kid.keg_label)
        if adoptees is not None:
            star_sum = 0
            for adoptee_keg_label in adoptees:
                adoptee_rope = self.make_rope(parent_rope, adoptee_keg_label)
                adoptee_keg = self.get_keg_obj(adoptee_rope)
                star_sum += adoptee_keg.star
                new_adoptee_parent_rope = self.make_rope(kid_rope, adoptee_keg_label)
                self.set_keg_obj(adoptee_keg, new_adoptee_parent_rope)
                self.edit_keg_attr(new_adoptee_parent_rope, star=adoptee_keg.star)
                self.del_keg_obj(adoptee_rope)

            if bundling:
                self.edit_keg_attr(kid_rope, star=star_sum)

        if create_missing_kegs:
            self._create_missing_kegs(rope=kid_rope)

    def _get_filtered_awardunits_keg(self, x_keg: KegUnit) -> KegUnit:
        awardunits_to_delete = [
            awardunit_awardee_title
            for awardunit_awardee_title in x_keg.awardunits.keys()
            if self.get_personunit_group_titles_dict().get(awardunit_awardee_title)
            is None
        ]
        for awardunit_awardee_title in awardunits_to_delete:
            x_keg.awardunits.pop(awardunit_awardee_title)
        if x_keg.laborunit is not None:
            partys_to_delete = [
                _partyunit_party_title
                for _partyunit_party_title in x_keg.laborunit.partys
                if self.get_personunit_group_titles_dict().get(_partyunit_party_title)
                is None
            ]
            for _partyunit_party_title in partys_to_delete:
                x_keg.laborunit.del_partyunit(_partyunit_party_title)
        return x_keg

    def _create_missing_kegs(self, rope):
        self._set_keg_dict()
        posted_keg = self.get_keg_obj(rope)

        for x_reason in posted_keg.reasonunits.values():
            self._create_kegkid_if_empty(rope=x_reason.reason_context)
            for case_x in x_reason.cases.values():
                self._create_kegkid_if_empty(rope=case_x.reason_state)

    def _create_kegkid_if_empty(self, rope: RopeTerm):
        if self.keg_exists(rope) is False:
            self.add_keg(rope)

    def del_keg_obj(self, rope: RopeTerm, del_children: bool = True):
        if rope == self.kegroot.get_keg_rope():
            raise InvalidPlanException("Kegroot cannot be deleted")
        parent_rope = get_parent_rope(rope)
        if self.keg_exists(rope):
            if not del_children:
                self._shift_keg_kids(x_rope=rope)
            parent_keg = self.get_keg_obj(parent_rope)
            parent_keg.del_kid(get_tail_label(rope, self.knot))
        self.cashout()

    def _shift_keg_kids(self, x_rope: RopeTerm):
        parent_rope = get_parent_rope(x_rope)
        d_temp_keg = self.get_keg_obj(x_rope)
        for kid in d_temp_keg.kids.values():
            self.set_keg_obj(kid, parent_rope=parent_rope)

    def set_plan_name(self, new_plan_name):
        self.plan_name = new_plan_name

    def edit_keg_label(self, old_rope: RopeTerm, new_keg_label: LabelTerm):
        if self.knot in new_keg_label:
            exception_str = f"Cannot modify '{old_rope}' because new_keg_label {new_keg_label} contains knot {self.knot}"
            raise InvalidLabelException(exception_str)
        if self.keg_exists(old_rope) is False:
            raise InvalidPlanException(f"Keg {old_rope=} does not exist")

        parent_rope = get_parent_rope(rope=old_rope)
        new_rope = (
            self.make_rope(new_keg_label)
            if parent_rope == ""
            else self.make_rope(parent_rope, new_keg_label)
        )
        if old_rope != new_rope:
            if parent_rope == "":
                self.kegroot.set_keg_label(new_keg_label)
            else:
                self._non_root_keg_label_edit(old_rope, new_keg_label, parent_rope)
            self._kegroot_find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    def _non_root_keg_label_edit(
        self, old_rope: RopeTerm, new_keg_label: LabelTerm, parent_rope: RopeTerm
    ):
        x_keg = self.get_keg_obj(old_rope)
        x_keg.set_keg_label(new_keg_label)
        x_keg.parent_rope = parent_rope
        keg_parent = self.get_keg_obj(get_parent_rope(old_rope))
        keg_parent.kids.pop(get_tail_label(old_rope, self.knot))
        keg_parent.kids[x_keg.keg_label] = x_keg

    def _kegroot_find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.kegroot.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

        keg_iter_list = [self.kegroot]
        while keg_iter_list != []:
            listed_keg = keg_iter_list.pop()
            # add all keg_children in keg list
            if listed_keg.kids is not None:
                for keg_kid in listed_keg.kids.values():
                    keg_iter_list.append(keg_kid)
                    if is_sub_rope(keg_kid.parent_rope, sub_rope=old_rope):
                        keg_kid.parent_rope = rebuild_rope(
                            subj_rope=keg_kid.parent_rope,
                            old_rope=old_rope,
                            new_rope=new_rope,
                        )
                    keg_kid.find_replace_rope(old_rope=old_rope, new_rope=new_rope)

    def _set_kegattrholder_case_ranges(self, x_kegattrholder: KegAttrHolder):
        case_keg = self.get_keg_obj(x_kegattrholder.reason_case)
        x_kegattrholder.set_case_range_influenced_by_case_keg(
            reason_lower=case_keg.begin,
            reason_upper=case_keg.close,
            case_denom=case_keg.denom,
        )

    def edit_reason(
        self,
        keg_rope: RopeTerm,
        reason_context: RopeTerm = None,
        reason_case: RopeTerm = None,
        reason_lower: ReasonNum = None,
        reason_upper: ReasonNum = None,
        reason_divisor: int = None,
    ):
        self.edit_keg_attr(
            keg_rope=keg_rope,
            reason_context=reason_context,
            reason_case=reason_case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
        )

    def edit_keg_attr(
        self,
        keg_rope: RopeTerm,
        star: int = None,
        uid: int = None,
        reason: ReasonUnit = None,
        reason_context: RopeTerm = None,
        reason_case: RopeTerm = None,
        reason_lower: ReasonNum = None,
        reason_upper: ReasonNum = None,
        reason_divisor: int = None,
        reason_del_case_reason_context: RopeTerm = None,
        reason_del_case_reason_state: RopeTerm = None,
        reason_requisite_active: str = None,
        laborunit: LaborUnit = None,
        healerunit: HealerUnit = None,
        begin: float = None,
        close: float = None,
        gogo_want: float = None,
        stop_want: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        morph: bool = None,
        pledge: bool = None,
        factunit: FactUnit = None,
        awardunit: AwardUnit = None,
        awardunit_del: GroupTitle = None,
        is_expanded: bool = None,
        problem_bool: bool = None,
    ):
        if healerunit is not None:
            for x_healer_name in healerunit._healer_names:
                if self.get_personunit_group_titles_dict().get(x_healer_name) is None:
                    exception_str = f"Keg cannot edit healerunit because group_title '{x_healer_name}' does not exist as group in Plan"
                    raise healerunit_group_title_Exception(exception_str)

        if (
            reason_context
            and reason_case
            and not is_sub_rope(reason_case, reason_context)
        ):
            raise reason_caseException(
                f"""Keg cannot edit reason because reason_case is not sub_rope to reason_context 
reason_context: {reason_context}
reason_case:    {reason_case}"""
            )

        x_kegattrholder = kegattrholder_shop(
            star=star,
            uid=uid,
            reason=reason,
            reason_context=reason_context,
            reason_case=reason_case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
            reason_del_case_reason_context=reason_del_case_reason_context,
            reason_del_case_reason_state=reason_del_case_reason_state,
            reason_requisite_active=reason_requisite_active,
            laborunit=laborunit,
            healerunit=healerunit,
            begin=begin,
            close=close,
            gogo_want=gogo_want,
            stop_want=stop_want,
            addin=addin,
            numor=numor,
            denom=denom,
            morph=morph,
            awardunit=awardunit,
            awardunit_del=awardunit_del,
            is_expanded=is_expanded,
            pledge=pledge,
            factunit=factunit,
            problem_bool=problem_bool,
        )
        if reason_case is not None:
            self._set_kegattrholder_case_ranges(x_kegattrholder)
        x_keg = self.get_keg_obj(keg_rope)
        x_keg._set_attrs_to_kegunit(keg_attr=x_kegattrholder)

    def get_agenda_dict(
        self, necessary_reason_context: RopeTerm = None
    ) -> dict[RopeTerm, KegUnit]:
        self.cashout()
        return {
            x_keg.get_keg_rope(): x_keg
            for x_keg in self._keg_dict.values()
            if x_keg.is_agenda_keg(necessary_reason_context)
        }

    def get_all_pledges(self) -> dict[RopeTerm, KegUnit]:
        self.cashout()
        all_kegs = self._keg_dict.values()
        return {x_keg.get_keg_rope(): x_keg for x_keg in all_kegs if x_keg.pledge}

    def set_agenda_task_complete(self, task_rope: RopeTerm, reason_context: RopeTerm):
        pledge_keg = self.get_keg_obj(task_rope)
        pledge_keg.set_factunit_to_complete(self.kegroot.factunits[reason_context])

    def get_credit_ledger_debt_ledger(
        self,
    ) -> tuple[dict[str, float], dict[str, float]]:
        credit_ledger = {}
        debt_ledger = {}
        for x_personunit in self.persons.values():
            credit_ledger[x_personunit.person_name] = x_personunit.person_cred_lumen
            debt_ledger[x_personunit.person_name] = x_personunit.person_debt_lumen
        return credit_ledger, debt_ledger

    def _allot_offtrack_fund(self):
        self._add_to_personunits_fund_give_take(self.offtrack_fund)

    def get_personunits_person_cred_lumen_sum(self) -> float:
        return sum(
            personunit.get_person_cred_lumen() for personunit in self.persons.values()
        )

    def get_personunits_person_debt_lumen_sum(self) -> float:
        return sum(
            personunit.get_person_debt_lumen() for personunit in self.persons.values()
        )

    def _add_to_personunits_fund_give_take(self, keg_keg_fund_total: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(
            credor_ledger, keg_keg_fund_total, self.fund_grain
        )
        fund_take_allot = allot_scale(
            debtor_ledger, keg_keg_fund_total, self.fund_grain
        )
        for x_person_name, person_fund_give in fund_give_allot.items():
            self.get_person(x_person_name).add_fund_give(person_fund_give)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self.reason_contexts:
                self.get_person(x_person_name).add_fund_agenda_give(person_fund_give)
        for x_person_name, person_fund_take in fund_take_allot.items():
            self.get_person(x_person_name).add_fund_take(person_fund_take)
            # if there is no differentiated agenda (what factunits exist do not change agenda)
            if not self.reason_contexts:
                self.get_person(x_person_name).add_fund_agenda_take(person_fund_take)

    def _add_to_personunits_fund_agenda_give_take(self, keg_keg_fund_total: float):
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        fund_give_allot = allot_scale(
            credor_ledger, keg_keg_fund_total, self.fund_grain
        )
        fund_take_allot = allot_scale(
            debtor_ledger, keg_keg_fund_total, self.fund_grain
        )
        for x_person_name, person_fund_give in fund_give_allot.items():
            self.get_person(x_person_name).add_fund_agenda_give(person_fund_give)
        for x_person_name, person_fund_take in fund_take_allot.items():
            self.get_person(x_person_name).add_fund_agenda_take(person_fund_take)

    def _reset_groupunits_fund_give_take(self):
        for groupunit_obj in self.groupunits.values():
            groupunit_obj.clear_group_fund_give_take()

    def _set_groupunits_keg_fund_total(self, awardheirs: dict[GroupTitle, AwardUnit]):
        for awardunit_obj in awardheirs.values():
            x_awardee_title = awardunit_obj.awardee_title
            if not self.groupunit_exists(x_awardee_title):
                self.set_groupunit(self.create_symmetry_groupunit(x_awardee_title))
            self.add_to_groupunit_fund_give_fund_take(
                group_title=awardunit_obj.awardee_title,
                awardheir_fund_give=awardunit_obj.fund_give,
                awardheir_fund_take=awardunit_obj.fund_take,
            )

    def _allot_fund_plan_agenda(self):
        for keg in self._keg_dict.values():
            # If there are no awardlines associated with keg
            # allot keg_fund_total via general personunit
            # cred ratio and debt ratio
            # if keg.is_agenda_keg() and keg.awardlines == {}:
            if keg.is_agenda_keg():
                if keg.awardheir_exists():
                    for x_awardline in keg.awardlines.values():
                        self.add_to_groupunit_fund_agenda_give_take(
                            group_title=x_awardline.awardee_title,
                            awardline_fund_give=x_awardline.fund_give,
                            awardline_fund_take=x_awardline.fund_take,
                        )
                else:
                    self._add_to_personunits_fund_agenda_give_take(
                        keg.get_keg_fund_total()
                    )

    def _allot_groupunits_fund(self):
        for x_groupunit in self.groupunits.values():
            x_groupunit._set_membership_fund_give_fund_take()
            for x_membership in x_groupunit.memberships.values():
                self.add_to_personunit_fund_give_take(
                    personunit_person_name=x_membership.person_name,
                    fund_give=x_membership.fund_give,
                    fund_take=x_membership.fund_take,
                    fund_agenda_give=x_membership.fund_agenda_give,
                    fund_agenda_take=x_membership.fund_agenda_take,
                )

    def _set_personunits_fund_agenda_ratios(self):
        fund_agenda_ratio_give_sum = sum(
            x_personunit.fund_agenda_give for x_personunit in self.persons.values()
        )
        fund_agenda_ratio_take_sum = sum(
            x_personunit.fund_agenda_take for x_personunit in self.persons.values()
        )
        x_personunits_person_cred_lumen_sum = (
            self.get_personunits_person_cred_lumen_sum()
        )
        x_personunits_person_debt_lumen_sum = (
            self.get_personunits_person_debt_lumen_sum()
        )
        for x_personunit in self.persons.values():
            x_personunit.set_fund_agenda_ratio_give_take(
                fund_agenda_ratio_give_sum=fund_agenda_ratio_give_sum,
                fund_agenda_ratio_take_sum=fund_agenda_ratio_take_sum,
                personunits_person_cred_lumen_sum=x_personunits_person_cred_lumen_sum,
                personunits_person_debt_lumen_sum=x_personunits_person_debt_lumen_sum,
            )

    def _reset_personunit_fund_give_take(self):
        for personunit in self.persons.values():
            personunit.clear_fund_give_take()

    def keg_exists(self, rope: RopeTerm) -> bool:
        if rope in {"", None}:
            return False
        root_rope_keg_label = get_first_label_from_rope(rope, self.knot)
        if root_rope_keg_label != self.kegroot.keg_label:
            return False

        labels = get_all_rope_labels(rope, knot=self.knot)
        root_rope_keg_label = labels.pop(0)
        if labels == []:
            return True

        keg_label = labels.pop(0)
        x_keg = self.kegroot.get_kid(keg_label)
        if x_keg is None:
            return False
        while labels != []:
            keg_label = labels.pop(0)
            x_keg = x_keg.get_kid(keg_label)
            if x_keg is None:
                return False
        return True

    def get_keg_obj(self, rope: RopeTerm, if_missing_create: bool = False) -> KegUnit:
        if rope is None:
            raise InvalidPlanException("get_keg_obj received rope=None")
        if self.keg_exists(rope) is False and not if_missing_create:
            raise InvalidPlanException(f"get_keg_obj failed. no keg at '{rope}'")
        labelterms = get_all_rope_labels(rope, knot=self.knot)
        if len(labelterms) == 1:
            return self.kegroot

        labelterms.pop(0)
        keg_label = labelterms.pop(0)
        x_keg = self.kegroot.get_kid(keg_label, if_missing_create)
        while labelterms != []:
            x_keg = x_keg.get_kid(labelterms.pop(0), if_missing_create)

        return x_keg

    def get_keg_ranged_kids(
        self, keg_rope: str, x_gogo_calc: float = None, x_stop_calc: float = None
    ) -> dict[KegUnit]:
        x_keg = self.get_keg_obj(keg_rope)
        return x_keg.get_kids_in_range(x_gogo_calc, x_stop_calc)

    def get_inheritor_keg_list(
        self, range_rope: RopeTerm, inheritor_rope: RopeTerm
    ) -> list[KegUnit]:
        keg_ropes = all_ropes_between(range_rope, inheritor_rope)
        return [self.get_keg_obj(x_keg_rope) for x_keg_rope in keg_ropes]

    def _set_keg_dict(self):
        keg_list = [self.kegroot]
        while keg_list != []:
            x_keg = keg_list.pop()
            x_keg.clear_gogo_calc_stop_calc()
            for keg_kid in x_keg.kids.values():
                keg_kid.set_parent_rope(x_keg.get_keg_rope())
                keg_kid.set_tree_level(x_keg.tree_level)
                keg_list.append(keg_kid)
            self._keg_dict[x_keg.get_keg_rope()] = x_keg
            for x_reason_context in x_keg.reasonunits.keys():
                self.reason_contexts.add(x_reason_context)

    def _raise_gogo_calc_stop_calc_exception(self, keg_rope: RopeTerm):
        exception_str = f"Error has occurred, Keg '{keg_rope}' is having gogo_calc and stop_calc set twice"
        raise gogo_calc_stop_calc_Exception(exception_str)

    def _distribute_range_attrs(self, rangeroot_keg: KegUnit):
        """Populates PlanUnit.range_inheritors, sets KegUnit.gogo_calc, KegUnit.stop_calc"""
        single_rangeroot_keg_list = [rangeroot_keg]
        while single_rangeroot_keg_list != []:
            x_kegunit = single_rangeroot_keg_list.pop()
            x_keg_rope = x_kegunit.get_keg_rope()
            if x_kegunit.range_evaluated:
                self._raise_gogo_calc_stop_calc_exception(x_keg_rope)
            if x_kegunit.has_begin_close():
                x_kegunit.gogo_calc = x_kegunit.begin
                x_kegunit.stop_calc = x_kegunit.close
            else:
                parent_rope = get_parent_rope(x_keg_rope, x_kegunit.knot)
                parent_keg = self.get_keg_obj(parent_rope)
                x_kegunit.gogo_calc = parent_keg.gogo_calc
                x_kegunit.stop_calc = parent_keg.stop_calc
                self.range_inheritors[x_keg_rope] = rangeroot_keg.get_keg_rope()
            x_kegunit._mold_gogo_calc_stop_calc()
            single_rangeroot_keg_list.extend(iter(x_kegunit.kids.values()))

    def _set_kegtree_range_attrs(self):
        for x_keg in self._keg_dict.values():
            if x_keg.has_begin_close():
                self._distribute_range_attrs(x_keg)

            if (
                not x_keg.is_kidless()
                and x_keg.get_kids_star_sum() == 0
                and x_keg.star != 0
            ):
                self.offtrack_kids_star_set.add(x_keg.get_keg_rope())

    def _set_groupunit_personunit_funds(self, keep_exceptions):
        for x_keg in self._keg_dict.values():
            x_keg.set_awardheirs_fund_give_fund_take()
            if x_keg.is_kidless():
                self._set_ancestors_pledge_fund_keep_attrs(
                    x_keg.get_keg_rope(), keep_exceptions
                )
                self._allot_keg_fund_total(x_keg)

    def _set_ancestors_pledge_fund_keep_attrs(
        self, rope: RopeTerm, keep_exceptions: bool = False
    ):
        x_descendant_pledge_count = 0
        child_awardlines = None
        group_everyone = None
        ancestor_ropes = get_ancestor_ropes(rope, self.knot)
        keep_justified_by_problem = True
        healerunit_count = 0

        while ancestor_ropes != []:
            youngest_rope = ancestor_ropes.pop(0)
            x_keg_obj = self.get_keg_obj(youngest_rope)
            x_keg_obj.add_to_descendant_pledge_count(x_descendant_pledge_count)
            if x_keg_obj.is_kidless():
                x_keg_obj.set_kidless_awardlines()
                child_awardlines = x_keg_obj.awardlines
            else:
                x_keg_obj.set_awardlines(child_awardlines)

            if x_keg_obj.task:
                x_descendant_pledge_count += 1

            if (
                group_everyone != False
                and x_keg_obj.all_person_cred != False
                and x_keg_obj.all_person_debt != False
                and x_keg_obj.awardheirs != {}
            ) or (
                group_everyone != False
                and x_keg_obj.all_person_cred is False
                and x_keg_obj.all_person_debt is False
            ):
                group_everyone = False
            elif group_everyone != False:
                group_everyone = True
            x_keg_obj.all_person_cred = group_everyone
            x_keg_obj.all_person_debt = group_everyone

            if x_keg_obj.healerunit.any_healer_name_exists():
                keep_justified_by_problem = False
                healerunit_count += 1
                self.sum_healerunit_kegs_fund_total += x_keg_obj.get_keg_fund_total()
            if x_keg_obj.problem_bool:
                keep_justified_by_problem = True

        if keep_justified_by_problem is False or healerunit_count > 1:
            if keep_exceptions:
                exception_str = f"KegUnit '{rope}' cannot sponsor ancestor keeps."
                raise keeps_justException(exception_str)
            self.keeps_justified = False

    def _clear_kegtree_fund_and_keg_active(self):
        for x_keg in self._keg_dict.values():
            x_keg.clear_awardlines()
            x_keg.clear_descendant_pledge_count()
            x_keg.clear_all_person_cred_debt()

    def _set_kids_keg_active(self, x_keg: KegUnit, parent_keg: KegUnit):
        x_keg.set_reasonheirs(self._keg_dict, parent_keg.reasonheirs)
        x_keg.set_range_inheritors_factheirs(self._keg_dict, self.range_inheritors)
        tt_count = self.tree_traverse_count
        x_keg.set_keg_active(tt_count, self.groupunits, self.plan_name)

    def _allot_keg_fund_total(self, keg: KegUnit):
        if keg.awardheir_exists():
            self._set_groupunits_keg_fund_total(keg.awardheirs)
        elif keg.awardheir_exists() is False:
            self._add_to_personunits_fund_give_take(keg.get_keg_fund_total())

    def _create_groupunits_metrics(self):
        self.groupunits = {}
        for (
            group_title,
            person_name_set,
        ) in self.get_personunit_group_titles_dict().items():
            x_groupunit = groupunit_shop(group_title)
            for x_person_name in person_name_set:
                x_membership = self.get_person(x_person_name).get_membership(
                    group_title
                )
                x_groupunit.set_g_membership(x_membership)
                self.set_groupunit(x_groupunit)

    def _set_personunit_groupunit_respect_ledgers(self):
        self.credor_respect = RespectNum(validate_pool_num(self.credor_respect))
        self.debtor_respect = RespectNum(validate_pool_num(self.debtor_respect))
        credor_ledger, debtor_ledger = self.get_credit_ledger_debt_ledger()
        credor_allot = allot_scale(
            credor_ledger, self.credor_respect, self.respect_grain
        )
        debtor_allot = allot_scale(
            debtor_ledger, self.debtor_respect, self.respect_grain
        )
        for x_person_name, person_credor_pool in credor_allot.items():
            self.get_person(x_person_name).set_credor_pool(person_credor_pool)
        for x_person_name, person_debtor_pool in debtor_allot.items():
            self.get_person(x_person_name).set_debtor_pool(person_debtor_pool)
        self._create_groupunits_metrics()
        self._reset_personunit_fund_give_take()

    def _clear_keg_dict_and_plan_obj_settle_attrs(self):
        self._keg_dict = {self.kegroot.get_keg_rope(): self.kegroot}
        self.rational = False
        self.tree_traverse_count = 0
        self.offtrack_kids_star_set = set()
        self.reason_contexts = set()
        self.range_inheritors = {}
        self.keeps_justified = True
        self.keeps_buildable = False
        self.sum_healerunit_kegs_fund_total = 0
        self._keep_dict = {}
        self._healers_dict = {}

    def _set_kegtree_factheirs_laborheir_awardheirs(self):
        for x_keg in get_sorted_keg_list(self._keg_dict):
            if x_keg == self.kegroot:
                x_keg.set_factheirs(x_keg.factunits)
                x_keg.set_root_keg_reasonheirs()
                x_keg.set_laborheir(None, self.groupunits)
                x_keg.inherit_awardheirs()
            else:
                parent_keg = self.get_keg_obj(x_keg.parent_rope)
                x_keg.set_factheirs(parent_keg.factheirs)
                x_keg.set_laborheir(parent_keg.laborheir, self.groupunits)
                x_keg.inherit_awardheirs(parent_keg.awardheirs)
            x_keg.set_awardheirs_fund_give_fund_take()

    def cashout(self, keep_exceptions: bool = False):
        self._clear_keg_dict_and_plan_obj_settle_attrs()
        self._set_keg_dict()
        self._set_kegtree_range_attrs()
        self._set_personunit_groupunit_respect_ledgers()
        self._clear_personunit_fund_attrs()
        self._clear_kegtree_fund_and_keg_active()
        self._set_kegtree_factheirs_laborheir_awardheirs()

        max_count = self.max_tree_traverse
        while not self.rational and self.tree_traverse_count < max_count:
            self._set_kegtree_keg_active()
            self._set_rational_attr()
            self.tree_traverse_count += 1

        self._set_kegtree_fund_attrs(self.kegroot)
        self._set_groupunit_personunit_funds(keep_exceptions)
        self._set_personunit_fund_related_attrs()
        self._set_plan_keep_attrs()

    def _set_kegtree_keg_active(self):
        """For every kegunit in the KegTree set keg_active to True or False.
        Assumes self.range_inheritors is set with set of ropes for all KegUnits that
        inherit from a ranged KegUnit.
        """

        for x_keg in get_sorted_keg_list(self._keg_dict):
            if x_keg == self.kegroot:
                tt_count = self.tree_traverse_count
                root_keg = self.kegroot
                root_keg.set_keg_active(tt_count, self.groupunits, self.plan_name)
            else:
                parent_keg = self.get_keg_obj(x_keg.parent_rope)
                self._set_kids_keg_active(x_keg, parent_keg)

    def _set_kegtree_fund_attrs(self, root_keg: KegUnit):
        root_keg.set_fund_attr(0, self.fund_pool, self.fund_pool)
        # no function recursion, recursion by iterateing over list that can be added to by iterations
        cache_keg_list = [root_keg]
        while cache_keg_list != []:
            parent_keg = cache_keg_list.pop()
            kids_kegs = parent_keg.kids.items()
            x_ledger = {x_rope: keg_kid.star for x_rope, keg_kid in kids_kegs}
            parent_fund_num = parent_keg.fund_cease - parent_keg.fund_onset
            alloted_fund_num = allot_scale(x_ledger, parent_fund_num, self.fund_grain)

            fund_onset = None
            fund_cease = None
            for x_keg in parent_keg.kids.values():
                if fund_onset is None:
                    fund_onset = parent_keg.fund_onset
                    fund_cease = fund_onset + alloted_fund_num.get(x_keg.keg_label)
                else:
                    fund_onset = fund_cease
                    fund_cease += alloted_fund_num.get(x_keg.keg_label)
                x_keg.set_fund_attr(fund_onset, fund_cease, self.fund_pool)
                cache_keg_list.append(x_keg)

    def _set_rational_attr(self):
        any_keg_active_has_altered = False
        for keg in self._keg_dict.values():
            if keg.keg_active_hx.get(self.tree_traverse_count) is not None:
                any_keg_active_has_altered = True

        if any_keg_active_has_altered is False:
            self.rational = True

    def _set_personunit_fund_related_attrs(self):
        self.set_offtrack_fund()
        self._allot_offtrack_fund()
        self._allot_fund_plan_agenda()
        self._allot_groupunits_fund()
        self._set_personunits_fund_agenda_ratios()

    def _set_plan_keep_attrs(self):
        self._set_keep_dict()
        self._healers_dict = self._get_healers_dict()
        self.keeps_buildable = self._get_buildable_keeps()

    def _set_keep_dict(self):
        if self.keeps_justified is False:
            self.sum_healerunit_kegs_fund_total = 0
        for x_keg in self._keg_dict.values():
            if self.sum_healerunit_kegs_fund_total == 0:
                x_keg.healerunit_ratio = 0
            else:
                x_sum = self.sum_healerunit_kegs_fund_total
                x_keg.healerunit_ratio = x_keg.get_keg_fund_total() / x_sum
            if self.keeps_justified and x_keg.healerunit.any_healer_name_exists():
                self._keep_dict[x_keg.get_keg_rope()] = x_keg

    def _get_healers_dict(self) -> dict[HealerName, dict[RopeTerm, KegUnit]]:
        _healers_dict = {}
        for x_keep_rope, x_keep_keg in self._keep_dict.items():
            for x_healer_name in x_keep_keg.healerunit._healer_names:
                x_groupunit = self.get_groupunit(x_healer_name)
                for x_person_name in x_groupunit.memberships.keys():
                    if _healers_dict.get(x_person_name) is None:
                        _healers_dict[x_person_name] = {x_keep_rope: x_keep_keg}
                    else:
                        healer_dict = _healers_dict.get(x_person_name)
                        healer_dict[x_keep_rope] = x_keep_keg
        return _healers_dict

    def _get_buildable_keeps(self) -> bool:
        return all(
            rope_is_valid_dir_path(keep_rope, self.knot) != False
            for keep_rope in self._keep_dict.keys()
        )

    def _clear_personunit_fund_attrs(self):
        self._reset_groupunits_fund_give_take()
        self._reset_personunit_fund_give_take()

    def get_keg_tree_ordered_rope_list(
        self, no_range_descendants: bool = False
    ) -> list[RopeTerm]:
        keg_list = list(self.get_keg_dict().values())
        label_dict = {
            keg.get_keg_rope().lower(): keg.get_keg_rope() for keg in keg_list
        }
        label_same_capitalization_ordered_list = sorted(list(label_dict))
        label_orginalcapitalization_ordered_list = [
            label_dict[label_l] for label_l in label_same_capitalization_ordered_list
        ]

        list_x = []
        for rope in label_orginalcapitalization_ordered_list:
            if not no_range_descendants:
                list_x.append(rope)
            else:
                anc_list = get_ancestor_ropes(rope=rope)
                if len(anc_list) == 1:
                    list_x.append(rope)
                elif len(anc_list) == 2:
                    if self.kegroot.begin is None and self.kegroot.close is None:
                        list_x.append(rope)
                else:
                    parent_keg = self.get_keg_obj(rope=anc_list[1])
                    if parent_keg.begin is None and parent_keg.close is None:
                        list_x.append(rope)

        return list_x

    def get_kegroot_factunits_dict(self) -> dict[str, str]:
        x_dict = {}
        if self.kegroot.factunits is not None:
            for fact_rope, fact_obj in self.kegroot.factunits.items():
                x_dict[fact_rope] = fact_obj.to_dict()
        return x_dict

    def get_personunits_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {}
        if self.persons is not None:
            for person_name, person_obj in self.persons.items():
                x_dict[person_name] = person_obj.to_dict(all_attrs)
        return x_dict

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "plan_name": self.plan_name,
            "fund_grain": self.fund_grain,
            "fund_pool": self.fund_pool,
            "knot": self.knot,
            "mana_grain": self.mana_grain,
            "max_tree_traverse": self.max_tree_traverse,
            "kegroot": self.kegroot.to_dict(),
            "respect_grain": self.respect_grain,
            "tally": self.tally,
            "persons": self.get_personunits_dict(),
        }
        if self.credor_respect is not None:
            x_dict["credor_respect"] = self.credor_respect
        if self.debtor_respect is not None:
            x_dict["debtor_respect"] = self.debtor_respect
        if self.last_lesson_id is not None:
            x_dict["last_lesson_id"] = self.last_lesson_id

        return x_dict

    def set_dominate_pledge_keg(self, keg_kid: KegUnit):
        keg_kid.pledge = True
        self.set_keg_obj(
            keg_kid=keg_kid,
            parent_rope=self.make_rope(keg_kid.parent_rope),
            get_rid_of_missing_awardunits_awardee_titles=True,
            create_missing_kegs=True,
        )

    def set_offtrack_fund(self) -> float:
        star_set = self.offtrack_kids_star_set
        self.offtrack_fund = sum(
            self.get_keg_obj(rope).get_keg_fund_total() for rope in star_set
        )


def planunit_shop(
    plan_name: PlanName = None,
    moment_rope: RopeTerm = None,
    knot: KnotTerm = None,
    fund_pool: FundNum = None,
    fund_grain: FundGrain = None,
    respect_grain: RespectGrain = None,
    mana_grain: ManaGrain = None,
    tally: float = None,
) -> PlanUnit:
    plan_name = "" if plan_name is None else plan_name
    root_keg_label = get_default_first_label() if moment_rope is None else moment_rope
    x_plan = PlanUnit(
        plan_name=plan_name,
        tally=get_1_if_None(tally),
        moment_rope=root_keg_label,
        persons=get_empty_dict_if_None(),
        groupunits={},
        knot=default_knot_if_None(knot),
        credor_respect=RespectNum(validate_pool_num()),
        debtor_respect=RespectNum(validate_pool_num()),
        fund_pool=validate_pool_num(fund_pool),
        fund_grain=default_grain_num_if_None(fund_grain),
        respect_grain=default_grain_num_if_None(respect_grain),
        mana_grain=default_grain_num_if_None(mana_grain),
        _keg_dict=get_empty_dict_if_None(),
        _keep_dict=get_empty_dict_if_None(),
        _healers_dict=get_empty_dict_if_None(),
        keeps_justified=get_False_if_None(),
        keeps_buildable=get_False_if_None(),
        sum_healerunit_kegs_fund_total=get_0_if_None(),
        offtrack_kids_star_set=set(),
        reason_contexts=set(),
        range_inheritors={},
    )
    x_plan.kegroot = kegunit_shop(
        keg_label=root_keg_label,
        uid=1,
        tree_level=0,
        knot=x_plan.knot,
        fund_grain=x_plan.fund_grain,
        parent_rope="",
    )
    x_plan.set_max_tree_traverse(3)
    x_plan.rational = False
    return x_plan


def get_planunit_from_dict(plan_dict: dict) -> PlanUnit:
    x_plan = planunit_shop()
    x_plan.set_plan_name(obj_from_plan_dict(plan_dict, "plan_name"))
    x_plan.tally = obj_from_plan_dict(plan_dict, "tally")
    x_plan.set_max_tree_traverse(obj_from_plan_dict(plan_dict, "max_tree_traverse"))
    x_plan.moment_rope = plan_dict.get("kegroot").get("keg_label")
    plan_knot = obj_from_plan_dict(plan_dict, "knot")
    x_plan.knot = default_knot_if_None(plan_knot)
    x_plan.fund_pool = validate_pool_num(obj_from_plan_dict(plan_dict, "fund_pool"))
    x_plan.fund_grain = default_grain_num_if_None(
        obj_from_plan_dict(plan_dict, "fund_grain")
    )
    x_plan.respect_grain = default_grain_num_if_None(
        obj_from_plan_dict(plan_dict, "respect_grain")
    )
    x_plan.mana_grain = default_grain_num_if_None(
        obj_from_plan_dict(plan_dict, "mana_grain")
    )
    x_plan.credor_respect = obj_from_plan_dict(plan_dict, "credor_respect")
    x_plan.debtor_respect = obj_from_plan_dict(plan_dict, "debtor_respect")
    x_plan.last_lesson_id = obj_from_plan_dict(plan_dict, "last_lesson_id")
    x_knot = x_plan.knot
    x_persons = obj_from_plan_dict(plan_dict, "persons", x_knot).values()
    for x_personunit in x_persons:
        x_plan.set_personunit(x_personunit)
    create_kegroot_from_plan_dict(x_plan, plan_dict)
    return x_plan


def create_kegroot_from_plan_dict(x_plan: PlanUnit, plan_dict: dict):
    kegroot_dict = plan_dict.get("kegroot")
    x_plan.kegroot = kegunit_shop(
        keg_label=get_obj_from_keg_dict(kegroot_dict, "keg_label"),
        parent_rope="",
        tree_level=0,
        uid=get_obj_from_keg_dict(kegroot_dict, "uid"),
        star=get_obj_from_keg_dict(kegroot_dict, "star"),
        begin=get_obj_from_keg_dict(kegroot_dict, "begin"),
        close=get_obj_from_keg_dict(kegroot_dict, "close"),
        numor=get_obj_from_keg_dict(kegroot_dict, "numor"),
        denom=get_obj_from_keg_dict(kegroot_dict, "denom"),
        morph=get_obj_from_keg_dict(kegroot_dict, "morph"),
        gogo_want=get_obj_from_keg_dict(kegroot_dict, "gogo_want"),
        stop_want=get_obj_from_keg_dict(kegroot_dict, "stop_want"),
        problem_bool=get_obj_from_keg_dict(kegroot_dict, "problem_bool"),
        reasonunits=get_obj_from_keg_dict(kegroot_dict, "reasonunits"),
        laborunit=get_obj_from_keg_dict(kegroot_dict, "laborunit"),
        healerunit=get_obj_from_keg_dict(kegroot_dict, "healerunit"),
        factunits=get_obj_from_keg_dict(kegroot_dict, "factunits"),
        awardunits=get_obj_from_keg_dict(kegroot_dict, "awardunits"),
        is_expanded=get_obj_from_keg_dict(kegroot_dict, "is_expanded"),
        knot=x_plan.knot,
        fund_grain=default_grain_num_if_None(x_plan.fund_grain),
    )
    create_kegroot_kids_from_dict(x_plan, kegroot_dict)


def create_kegroot_kids_from_dict(x_plan: PlanUnit, kegroot_dict: dict):
    to_evaluate_keg_dicts = []
    parent_rope_str = "parent_rope"
    # for every kid dict, set parent_rope in dict, add to to_evaluate_list
    for x_dict in get_obj_from_keg_dict(kegroot_dict, "kids").values():
        x_dict[parent_rope_str] = x_plan.kegroot.get_keg_rope()
        to_evaluate_keg_dicts.append(x_dict)

    while to_evaluate_keg_dicts != []:
        keg_dict = to_evaluate_keg_dicts.pop(0)
        # for every kid dict, set parent_rope in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_keg_dict(keg_dict, "kids").values():
            parent_rope = get_obj_from_keg_dict(keg_dict, parent_rope_str)
            kid_keg_label = get_obj_from_keg_dict(keg_dict, "keg_label")
            kid_dict[parent_rope_str] = x_plan.make_rope(parent_rope, kid_keg_label)
            to_evaluate_keg_dicts.append(kid_dict)
        x_kegkid = kegunit_shop(
            keg_label=get_obj_from_keg_dict(keg_dict, "keg_label"),
            star=get_obj_from_keg_dict(keg_dict, "star"),
            uid=get_obj_from_keg_dict(keg_dict, "uid"),
            begin=get_obj_from_keg_dict(keg_dict, "begin"),
            close=get_obj_from_keg_dict(keg_dict, "close"),
            numor=get_obj_from_keg_dict(keg_dict, "numor"),
            denom=get_obj_from_keg_dict(keg_dict, "denom"),
            morph=get_obj_from_keg_dict(keg_dict, "morph"),
            gogo_want=get_obj_from_keg_dict(keg_dict, "gogo_want"),
            stop_want=get_obj_from_keg_dict(keg_dict, "stop_want"),
            pledge=get_obj_from_keg_dict(keg_dict, "pledge"),
            problem_bool=get_obj_from_keg_dict(keg_dict, "problem_bool"),
            reasonunits=get_obj_from_keg_dict(keg_dict, "reasonunits"),
            laborunit=get_obj_from_keg_dict(keg_dict, "laborunit"),
            healerunit=get_obj_from_keg_dict(keg_dict, "healerunit"),
            awardunits=get_obj_from_keg_dict(keg_dict, "awardunits"),
            factunits=get_obj_from_keg_dict(keg_dict, "factunits"),
            is_expanded=get_obj_from_keg_dict(keg_dict, "is_expanded"),
        )
        x_plan.set_keg_obj(x_kegkid, parent_rope=keg_dict[parent_rope_str])


def obj_from_plan_dict(
    x_dict: dict[str, dict], dict_key: str, _knot: KnotTerm = None
) -> any:
    if dict_key == "persons":
        return personunits_get_from_dict(x_dict[dict_key], _knot)
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) is not None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def get_dict_of_plan_from_dict(x_dict: dict[str, dict]) -> dict[str, PlanUnit]:
    planunits = {}
    for planunit_dict in x_dict.values():
        x_plan = get_planunit_from_dict(plan_dict=planunit_dict)
        planunits[x_plan.plan_name] = x_plan
    return planunits


def get_sorted_keg_list(
    x_dict: dict[RopeTerm, KegUnit], sorting_key: str = None
) -> list[KegUnit]:
    x_list = list(x_dict.values())
    if sorting_key in {"fund_ratio"}:
        x_list.sort(key=lambda x: x.fund_ratio, reverse=True)
    else:
        x_list.sort(key=lambda x: x.get_keg_rope(), reverse=False)
    return x_list
