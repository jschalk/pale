from copy import deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_False_if_None,
    get_positive_int,
)
from src.ch01_allot.allot import allot_scale, default_grain_num_if_None
from src.ch02_person.group import (
    AwardHeir,
    AwardLine,
    AwardUnit,
    GroupUnit,
    awardheir_shop,
    awardline_shop,
    get_awardunits_from_dict,
)
from src.ch03_labor.labor import (
    LaborHeir,
    LaborUnit,
    get_laborunit_from_dict,
    laborheir_shop,
    laborunit_shop,
)
from src.ch04_rope.rope import (
    all_ropes_between,
    create_rope,
    find_replace_rope_key_dict,
    is_sub_rope,
    rebuild_rope,
    replace_knot,
)
from src.ch05_reason.reason_main import (
    FactCore,
    FactHeir,
    FactUnit,
    ReasonCore,
    ReasonHeir,
    ReasonUnit,
    RopeTerm,
    factheir_shop,
    factunit_shop,
    get_dict_from_factunits,
    get_factunits_from_dict,
    get_reasonunits_from_dict,
    reasonheir_shop,
    reasonunit_shop,
)
from src.ch06_keg._ref.ch06_semantic_types import (
    FundGrain,
    FundNum,
    GroupTitle,
    KnotTerm,
    LabelTerm,
    PersonName,
    ReasonNum,
    RopeTerm,
    default_knot_if_None,
)
from src.ch06_keg.healer import HealerUnit, get_healerunit_from_dict, healerunit_shop
from src.ch06_keg.range_toolbox import RangeUnit, get_morphed_rangeunit


class InvalidKegException(Exception):
    pass


class KegGetDescendantsException(Exception):
    pass


class keg_label_NotEmptyException(Exception):
    pass


class ranged_fact_keg_Exception(Exception):
    pass


@dataclass
class KegAttrHolder:
    star: int = None
    uid: int = None
    reason: ReasonUnit = None
    reason_context: RopeTerm = None
    reason_case: RopeTerm = None
    reason_lower: ReasonNum = None
    reason_upper: ReasonNum = None
    reason_divisor: int = None
    reason_del_case_reason_context: RopeTerm = None
    reason_del_case_reason_state: RopeTerm = None
    reason_requisite_active: str = None
    laborunit: LaborUnit = None
    healerunit: HealerUnit = None
    begin: float = None
    close: float = None
    gogo_want: float = None
    stop_want: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    morph: bool = None
    pledge: bool = None
    factunit: FactUnit = None
    awardunit: AwardUnit = None
    awardunit_del: GroupTitle = None
    is_expanded: bool = None
    problem_bool: bool = None

    def set_case_range_influenced_by_case_keg(
        self,
        reason_lower,
        reason_upper,
        case_denom,
    ):
        if self.reason_case is not None:
            if self.reason_lower is None:
                self.reason_lower = reason_lower
            if self.reason_upper is None:
                self.reason_upper = reason_upper
            if self.reason_divisor is None:
                self.reason_divisor = case_denom


def kegattrholder_shop(
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
) -> KegAttrHolder:
    return KegAttrHolder(
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
        pledge=pledge,
        factunit=factunit,
        awardunit=awardunit,
        awardunit_del=awardunit_del,
        is_expanded=is_expanded,
        problem_bool=problem_bool,
    )


@dataclass
class KegUnit:
    """
    Represents a kegual unit within pale. Can represent a pledge, a task, a different keg's
    reason or fact, a parent keg of other kegs.
    Funds: Funds come from the parent keg and go to the child kegs.
    Awards: Desribes whom the funding comes from and whome it goes to.
    Pledges: A keg can declare itself a pledge. It can be active or not active.
      Pledge Reason: A keg can require that all reasons be active to be active. (No reasons=active)
      Pledge Fact: Each reason checks facts to determine if it is active.


    funding, and hierarchical relationships.

    Attributes
    ----------
    keg_label : LabelTerm of keg.
    parent_rope : RopeTerm that this keg stems from. Empty string for root kegs.
    knot : str Identifier or label for bridging kegs.
    optional:
    star : int weight that is arbitrary used by parent keg to calculated relative importance.
    kids : dict[RopeTerm], mapping of child kegs by their LabelTerm
    uid : int Unique identifier, forgot how I use this.
    awardunits : dict[GroupTitle, AwardUnit] that describe who funds and who is funded
    reasonunits : dict[RopeTerm, ReasonUnit] that stores all reasons
    laborunit : LaborUnit that describes whom this pledge is for
    factunits : dict[RopeTerm, FactUnit] that stores all facts
    healerunit : HealerUnit, if a ancestor keg is a problem, this can donote a healing keg.
    begin : float that describes the begin of a numberical range if it exists
    close : float that describes the close of a numberical range if it exists
    addin : float that describes addition to parent range calculations
    denom : int that describes denominator to parent range calculations
    numor : int that describes numerator to parent range calculations
    morph : bool that describes how to change parent range in calculations.
    gogo_want : float
    stop_want : float
    pledge : bool that describes if the keg is a pledge.
    problem_bool : bool that describes if the keg is a problem.
    is_expanded : bool flag for whether the keg is expanded.

    active : bool that describes if the keg pledge is keg_active, calculated by PlanUnit.
    active_hx : dict[int, bool] Historical record of active state, used to calcualte if changes have occured
    all_person_cred : bool Flag indicating there are not explicitley defined awardunits
    all_person_debt : bool Flag indicating there are not explicitley defined awardunits
    awardheirs : dict[GroupTitle, AwardHeir] parent keg provided awards.
    awardlines : dict[GroupTitle, AwardLine] child keg provided awards.
    descendant_pledge_count : int Count of descendant kegs marked as pledges.
    factheirs : dict[RopeTerm, FactHeir] parent keg provided facts.
    fund_ratio : float
    fund_grain : FundGrain Smallest indivisible funding component.
    fund_onset : FundNum number at which funding onsets inside PlanUnit funding range
    fund_cease : FundNum number at which funding ceases inside PlanUnit funding range
    healerunit_ratio : float
    tree_level : int that describes Depth tree_level in keg hierarchy.
    range_evaluated : bool Flag indicating whether range has been evaluated.
    reasonheirs : dict[RopeTerm, ReasonHeir] parent keg provided reasoning branches.
    task : bool describes if a unit can be changed to inactive with fact range change.
    laborheir : LaborHeir parent keg provided labor relationships
    gogo_calc : float
    stop_calc : float
    """

    keg_label: LabelTerm = None
    parent_rope: RopeTerm = None
    knot: KnotTerm = None
    kids: dict[LabelTerm,] = None
    star: int = None
    uid: int = None  # Calculated field?
    awardunits: dict[GroupTitle, AwardUnit] = None
    reasonunits: dict[RopeTerm, ReasonUnit] = None
    laborunit: LaborUnit = None
    factunits: dict[RopeTerm, FactUnit] = None
    healerunit: HealerUnit = None
    begin: float = None
    close: float = None
    addin: float = None
    denom: int = None
    numor: int = None
    morph: bool = None
    gogo_want: float = None
    stop_want: float = None
    pledge: bool = None
    problem_bool: bool = None
    is_expanded: bool = None
    # Calculated fields
    keg_active: bool = None
    keg_active_hx: dict[int, bool] = None
    all_person_cred: bool = None
    all_person_debt: bool = None
    awardheirs: dict[GroupTitle, AwardHeir] = None
    awardlines: dict[GroupTitle, AwardLine] = None
    descendant_pledge_count: int = None
    factheirs: dict[RopeTerm, FactHeir] = None
    fund_ratio: float = None
    fund_grain: FundGrain = None
    fund_onset: FundNum = None
    fund_cease: FundNum = None
    healerunit_ratio: float = None
    tree_level: int = None
    range_evaluated: bool = None
    reasonheirs: dict[RopeTerm, ReasonHeir] = None
    task: bool = None
    laborheir: LaborHeir = None
    gogo_calc: float = None
    stop_calc: float = None

    def is_agenda_keg(self, necessary_reason_context: RopeTerm = None) -> bool:
        reason_context_reasonunit_exists = self.reason_context_reasonunit_exists(
            necessary_reason_context
        )
        return self.pledge and self.keg_active and reason_context_reasonunit_exists

    def reason_context_reasonunit_exists(
        self, necessary_reason_context: RopeTerm = None
    ) -> bool:
        x_reasons = self.reasonunits.values()
        x_reason_context = necessary_reason_context
        return x_reason_context is None or any(
            reason.reason_context == x_reason_context for reason in x_reasons
        )

    def record_keg_active_hx(
        self, tree_traverse_count: int, prev_keg_active: bool, now_keg_active: bool
    ):
        if tree_traverse_count == 0:
            self.keg_active_hx = {0: now_keg_active}
        elif prev_keg_active != now_keg_active:
            self.keg_active_hx[tree_traverse_count] = now_keg_active

    def set_factheirs(self, facts: dict[RopeTerm, FactCore]):
        facts_dict = get_empty_dict_if_None(facts)
        self.factheirs = {}
        for x_factcore in facts_dict.values():
            self._set_factheir(x_factcore)

    def _set_factheir(self, x_fact: FactCore):
        if (
            x_fact.fact_context == self.get_keg_rope()
            and self.gogo_calc is not None
            and self.stop_calc is not None
            and self.begin is None
            and self.close is None
        ):
            raise ranged_fact_keg_Exception(
                f"Cannot have fact for range inheritor '{self.get_keg_rope()}'. A ranged fact keg must have _begin, _close"
            )
        x_factheir = factheir_shop(
            x_fact.fact_context, x_fact.fact_state, x_fact.fact_lower, x_fact.fact_upper
        )
        self.delete_factunit_if_past(x_factheir)
        x_factheir = self.apply_factunit_moldations(x_factheir)
        self.factheirs[x_factheir.fact_context] = x_factheir

    def apply_factunit_moldations(self, factheir: FactHeir) -> FactHeir:
        for factunit in self.factunits.values():
            if factunit.fact_context == factheir.fact_context:
                factheir.mold(factunit)
        return factheir

    def delete_factunit_if_past(self, factheir: FactHeir):
        delete_factunit = False
        for factunit in self.factunits.values():
            if (
                factunit.fact_context == factheir.fact_context
                and factunit.fact_upper is not None
                and factheir.fact_lower is not None
            ) and factunit.fact_upper < factheir.fact_lower:
                delete_factunit = True

        if delete_factunit:
            del self.factunits[factunit.fact_context]

    def set_factunit(self, factunit: FactUnit):
        self.factunits[factunit.fact_context] = factunit

    def factunit_exists(self, x_fact_context: RopeTerm) -> bool:
        return self.factunits.get(x_fact_context) != None

    def get_factunits_dict(self) -> dict[RopeTerm, str]:
        return get_dict_from_factunits(self.factunits)

    def set_factunit_to_complete(self, fact_contextunit: FactUnit):
        # if a keg is considered a task then a factheir.fact_lower attribute can be increased to
        # a number <= factheir.fact_upper so the keg no longer is a task. This method finds
        # the minimal factheir.fact_lower to modify keg.task is False. keg_core.factheir cannot be straight up manipulated
        # so it is mandatory that keg.factunit is different.
        # self.set_factunits(reason_context=fact, fact=reason_context, reason_lower=reason_upper, reason_upper=fact_upper)
        self.factunits[fact_contextunit.fact_context] = factunit_shop(
            fact_context=fact_contextunit.fact_context,
            fact_state=fact_contextunit.fact_context,
            fact_lower=fact_contextunit.fact_upper,
            fact_upper=fact_contextunit.fact_upper,
        )

    def del_factunit(self, fact_context: RopeTerm):
        self.factunits.pop(fact_context)

    def set_fund_attr(
        self,
        x_fund_onset: FundNum,
        x_fund_cease: FundNum,
        fund_pool: FundNum,
    ):
        self.fund_onset = x_fund_onset
        self.fund_cease = x_fund_cease
        self.fund_ratio = self.get_keg_fund_total() / fund_pool
        self.set_awardheirs_fund_give_fund_take()

    def get_keg_fund_total(self) -> float:
        """Return keg fund keg total. Equal to difference of fund_cease and fund_onset"""
        if self.fund_onset is None or self.fund_cease is None:
            return 0
        else:
            return self.fund_cease - self.fund_onset

    def get_kids_in_range(
        self, x_gogo: float = None, x_stop: float = None
    ) -> dict[LabelTerm,]:
        if x_gogo is None and x_stop is None:
            x_gogo = self.gogo_want
            x_gogo = self.stop_want
        elif x_gogo is not None and x_stop is None:
            x_stop = x_gogo

        if x_gogo is None and x_stop is None:
            return self.kids.values()

        x_dict = {}
        for x_keg in self.kids.values():
            x_gogo_in_range = x_gogo >= x_keg.gogo_calc and x_gogo < x_keg.stop_calc
            x_stop_in_range = x_stop > x_keg.gogo_calc and x_stop < x_keg.stop_calc
            both_in_range = x_gogo <= x_keg.gogo_calc and x_stop >= x_keg.stop_calc

            if x_gogo_in_range or x_stop_in_range or both_in_range:
                x_dict[x_keg.keg_label] = x_keg
        return x_dict

    def get_obj_key(self) -> LabelTerm:
        return self.keg_label

    def get_keg_rope(self) -> RopeTerm:
        if self.parent_rope in (None, ""):
            return create_rope(self.keg_label, knot=self.knot)
        else:
            return create_rope(self.parent_rope, self.keg_label, knot=self.knot)

    def clear_descendant_pledge_count(self):
        self.descendant_pledge_count = None

    def set_descendant_pledge_count_zero_if_None(self):
        if self.descendant_pledge_count is None:
            self.descendant_pledge_count = 0

    def add_to_descendant_pledge_count(self, x_int: int):
        self.set_descendant_pledge_count_zero_if_None()
        self.descendant_pledge_count += x_int

    def get_descendant_ropes_from_kids(self) -> dict[RopeTerm, int]:
        descendant_ropes = {}
        to_evaluate_kegs = list(self.kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_kegs != [] and count_x < max_count:
            x_keg = to_evaluate_kegs.pop()
            descendant_ropes[x_keg.get_keg_rope()] = -1
            to_evaluate_kegs.extend(x_keg.kids.values())
            count_x += 1

        if count_x == max_count:
            raise KegGetDescendantsException(
                f"Keg '{self.get_keg_rope()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_ropes

    def clear_all_person_cred_debt(self):
        self.all_person_cred = None
        self.all_person_debt = None

    def set_tree_level(self, parent_tree_level):
        self.tree_level = parent_tree_level + 1

    def set_parent_rope(self, parent_rope):
        self.parent_rope = parent_rope

    def inherit_awardheirs(self, parent_awardheirs: dict[GroupTitle, AwardHeir] = None):
        parent_awardheirs = {} if parent_awardheirs is None else parent_awardheirs
        self.awardheirs = {}
        for ib in parent_awardheirs.values():
            awardheir = awardheir_shop(
                awardee_title=ib.awardee_title,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self.awardheirs[awardheir.awardee_title] = awardheir

        for ib in self.awardunits.values():
            awardheir = awardheir_shop(
                awardee_title=ib.awardee_title,
                give_force=ib.give_force,
                take_force=ib.take_force,
            )
            self.awardheirs[awardheir.awardee_title] = awardheir

    def set_kidless_awardlines(self):
        # get awardlines from self
        for bh in self.awardheirs.values():
            x_awardline = awardline_shop(
                awardee_title=bh.awardee_title,
                fund_give=bh.fund_give,
                fund_take=bh.fund_take,
            )
            self.awardlines[x_awardline.awardee_title] = x_awardline

    def set_awardlines(self, child_awardlines: dict[GroupTitle, AwardLine] = None):
        if child_awardlines is None:
            child_awardlines = {}

        # get awardlines from child
        for bl in child_awardlines.values():
            if self.awardlines.get(bl.awardee_title) is None:
                self.awardlines[bl.awardee_title] = awardline_shop(
                    awardee_title=bl.awardee_title,
                    fund_give=0,
                    fund_take=0,
                )

            self.awardlines[bl.awardee_title].add_fund_give_take(
                fund_give=bl.fund_give, fund_take=bl.fund_take
            )

    def set_awardheirs_fund_give_fund_take(self):
        give_ledger = {}
        take_ledger = {}
        for x_awardee_title, x_awardheir in self.awardheirs.items():
            give_ledger[x_awardee_title] = x_awardheir.give_force
            take_ledger[x_awardee_title] = x_awardheir.take_force
        x_keg_fund_total = self.get_keg_fund_total()
        give_allot = allot_scale(give_ledger, x_keg_fund_total, self.fund_grain)
        take_allot = allot_scale(take_ledger, x_keg_fund_total, self.fund_grain)
        for x_awardee_title, x_awardheir in self.awardheirs.items():
            x_awardheir.fund_give = give_allot.get(x_awardee_title)
            x_awardheir.fund_take = take_allot.get(x_awardee_title)

    def clear_awardlines(self):
        self.awardlines = {}

    def set_keg_label(self, keg_label: str):
        if keg_label in {None, ""}:
            exception_str = "Cannot set Keg's Label empty or None"
            raise keg_label_NotEmptyException(exception_str)
        else:
            self.keg_label = keg_label

    def set_knot(self, new_knot: KnotTerm):
        old_knot = deepcopy(self.knot)
        if old_knot is None:
            old_knot = default_knot_if_None()
        self.knot = default_knot_if_None(new_knot)
        if old_knot != self.knot:
            self._find_replace_knot(old_knot)

    def _find_replace_knot(self, old_knot):
        self.parent_rope = replace_knot(self.parent_rope, old_knot, self.knot)

        new_reasonunits = {}
        for reasonunit_rope, reasonunit_obj in self.reasonunits.items():
            new_reasonunit_rope = replace_knot(
                rope=reasonunit_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            reasonunit_obj.set_knot(self.knot)
            new_reasonunits[new_reasonunit_rope] = reasonunit_obj
        self.reasonunits = new_reasonunits

        new_factunits = {}
        for factunit_rope, x_factunit in self.factunits.items():
            new_reason_context_rope = replace_knot(
                rope=factunit_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            x_factunit.fact_context = new_reason_context_rope
            new_fact_state_rope = replace_knot(
                rope=x_factunit.fact_state,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            x_factunit.set_attr(fact_state=new_fact_state_rope)
            new_factunits[new_reason_context_rope] = x_factunit
        self.factunits = new_factunits

    def _set_attrs_to_kegunit(self, keg_attr: KegAttrHolder):
        if keg_attr.star is not None:
            self.star = keg_attr.star
        if keg_attr.uid is not None:
            self.uid = keg_attr.uid
        if keg_attr.reason is not None:
            self.set_reasonunit(reason=keg_attr.reason)
        if keg_attr.reason_context is not None and keg_attr.reason_case is not None:
            self.set_reason_case(
                reason_context=keg_attr.reason_context,
                case=keg_attr.reason_case,
                reason_lower=keg_attr.reason_lower,
                reason_upper=keg_attr.reason_upper,
                reason_divisor=keg_attr.reason_divisor,
            )
        if (
            keg_attr.reason_context is not None
            and keg_attr.reason_requisite_active is not None
        ):
            self.set_reason_requisite_active(
                reason_context=keg_attr.reason_context,
                active_requisite=keg_attr.reason_requisite_active,
            )
        if keg_attr.laborunit is not None:
            self.laborunit = keg_attr.laborunit
        if keg_attr.healerunit is not None:
            self.healerunit = keg_attr.healerunit
        if keg_attr.begin is not None:
            self.begin = keg_attr.begin
        if keg_attr.close is not None:
            self.close = keg_attr.close
        if keg_attr.gogo_want is not None:
            self.gogo_want = keg_attr.gogo_want
        if keg_attr.stop_want is not None:
            self.stop_want = keg_attr.stop_want
        if keg_attr.addin is not None:
            self.addin = keg_attr.addin
        if keg_attr.numor is not None:
            self.numor = keg_attr.numor
        if keg_attr.denom is not None:
            self.denom = keg_attr.denom
        if keg_attr.morph is not None:
            self.morph = keg_attr.morph
        if keg_attr.awardunit is not None:
            self.set_awardunit(awardunit=keg_attr.awardunit)
        if keg_attr.awardunit_del is not None:
            self.del_awardunit(awardee_title=keg_attr.awardunit_del)
        if keg_attr.is_expanded is not None:
            self.is_expanded = keg_attr.is_expanded
        if keg_attr.pledge is not None:
            self.pledge = keg_attr.pledge
        if keg_attr.factunit is not None:
            self.set_factunit(keg_attr.factunit)
        if keg_attr.problem_bool is not None:
            self.problem_bool = keg_attr.problem_bool

        self._del_reasonunit_all_cases(
            reason_context=keg_attr.reason_del_case_reason_context,
            case=keg_attr.reason_del_case_reason_state,
        )
        self._set_addin_to_zero_if_any_moldations_exist()

    def _set_addin_to_zero_if_any_moldations_exist(self):
        if (
            self.begin is not None
            and self.close is not None
            and (self.numor is not None or self.denom is not None)
            and self.addin is None
        ):
            self.addin = 0

    def clear_gogo_calc_stop_calc(self):
        self.range_evaluated = False
        self.gogo_calc = None
        self.stop_calc = None

    def _mold_gogo_calc_stop_calc(self):
        r_keg_numor = get_1_if_None(self.numor)
        r_keg_denom = get_1_if_None(self.denom)
        r_keg_addin = get_0_if_None(self.addin)

        if self.gogo_calc is None or self.stop_calc is None:
            pass
        elif self.gogo_want != None and self.stop_want != None:
            stop_want_less_than_gogo_calc = self.stop_want < self.gogo_calc
            gogo_want_greater_than_stop_calc = self.gogo_want > self.stop_calc
            if stop_want_less_than_gogo_calc or gogo_want_greater_than_stop_calc:
                self.gogo_calc = None
                self.stop_calc = None
            else:
                self.gogo_calc = max(self.gogo_calc, self.gogo_want)
                self.stop_calc = min(self.stop_calc, self.stop_want)
        elif get_False_if_None(self.morph):
            x_gogo = self.gogo_calc
            x_stop = self.stop_calc
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, self.denom)
            self.gogo_calc = x_rangeunit.gogo
            self.stop_calc = x_rangeunit.stop
        else:
            self.gogo_calc = self.gogo_calc + r_keg_addin
            self.stop_calc = self.stop_calc + r_keg_addin
            self.gogo_calc = (self.gogo_calc * r_keg_numor) / r_keg_denom
            self.stop_calc = (self.stop_calc * r_keg_numor) / r_keg_denom
        self.range_evaluated = True

    def _del_reasonunit_all_cases(self, reason_context: RopeTerm, case: RopeTerm):
        if reason_context is not None and case is not None:
            self.del_reasonunit_case(reason_context=reason_context, case=case)
            if len(self.reasonunits[reason_context].cases) == 0:
                self.del_reasonunit_reason_context(reason_context=reason_context)

    def set_reason_requisite_active(
        self, reason_context: RopeTerm, active_requisite: str
    ):
        x_reasonunit = self._get_or_create_reasonunit(reason_context=reason_context)
        if active_requisite is False:
            x_reasonunit.active_requisite = False
        elif active_requisite == "Set to Ignore":
            x_reasonunit.active_requisite = None
        elif active_requisite:
            x_reasonunit.active_requisite = True

    def _get_or_create_reasonunit(self, reason_context: RopeTerm) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self.reasonunits[reason_context]
        except Exception:
            x_reasonunit = reasonunit_shop(reason_context, knot=self.knot)
            self.reasonunits[reason_context] = x_reasonunit
        return x_reasonunit

    def set_reason_case(
        self,
        reason_context: RopeTerm,
        case: RopeTerm,
        reason_lower: ReasonNum,
        reason_upper: ReasonNum,
        reason_divisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(reason_context=reason_context)
        x_reasonunit.set_case(
            case=case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
        )

    def del_reasonunit_reason_context(self, reason_context: RopeTerm):
        try:
            self.reasonunits.pop(reason_context)
        except KeyError as e:
            raise InvalidKegException(f"No ReasonUnit at '{reason_context}'") from e

    def del_reasonunit_case(self, reason_context: RopeTerm, case: RopeTerm):
        reason_unit = self.reasonunits[reason_context]
        reason_unit.del_case(case=case)

    def add_kid(self, keg_kid):
        self.kids[keg_kid.keg_label] = keg_kid
        self.kids = dict(sorted(self.kids.items()))

    def get_kid(self, keg_kid_keg_label: LabelTerm, if_missing_create=False):
        if if_missing_create is False:
            return self.kids.get(keg_kid_keg_label)
        try:
            return self.kids[keg_kid_keg_label]
        except Exception:
            KeyError
            self.add_kid(kegunit_shop(keg_kid_keg_label))
            return_keg = self.kids.get(keg_kid_keg_label)
        return return_keg

    def del_kid(self, keg_kid_keg_label: LabelTerm):
        self.kids.pop(keg_kid_keg_label)

    def clear_kids(self):
        self.kids = {}

    def get_kids_star_sum(self) -> float:
        return sum(x_kid.star for x_kid in self.kids.values())

    def set_awardunit(self, awardunit: AwardUnit):
        self.awardunits[awardunit.awardee_title] = awardunit

    def get_awardunit(self, awardee_title: GroupTitle) -> AwardUnit:
        return self.awardunits.get(awardee_title)

    def del_awardunit(self, awardee_title: GroupTitle):
        try:
            self.awardunits.pop(awardee_title)
        except KeyError as e:
            raise (f"Cannot delete awardunit '{awardee_title}'.") from e

    def awardunit_exists(self, x_awardee_title: GroupTitle) -> bool:
        return self.awardunits.get(x_awardee_title) != None

    def set_reasonunit(self, reason: ReasonUnit):
        reason.knot = self.knot
        self.reasonunits[reason.reason_context] = reason

    def reasonunit_exists(self, x_reason_context: RopeTerm) -> bool:
        return self.reasonunits.get(x_reason_context) != None

    def get_reasonunit(self, reason_context: RopeTerm) -> ReasonUnit:
        return self.reasonunits.get(reason_context)

    def set_reasonheirs_reason_active(self):
        self.clear_reasonheirs_reason_active()
        for x_reasonheir in self.reasonheirs.values():
            x_reasonheir.set_reason_active(factheirs=self.factheirs)

    def set_keg_active(
        self,
        tree_traverse_count: int,
        groupunits: dict[GroupTitle, GroupUnit] = None,
        plan_name: PersonName = None,
    ):
        prev_to_now_active = deepcopy(self.keg_active)
        self.keg_active = self._create_active_bool(groupunits, plan_name)
        self._set_keg_task()
        self.record_keg_active_hx(
            tree_traverse_count, prev_to_now_active, self.keg_active
        )

    def _set_keg_task(self):
        self.task = False
        if self.pledge and self.keg_active and self.reasonheirs_satisfied():
            self.task = True

    def reasonheirs_satisfied(self) -> bool:
        return self.reasonheirs == {} or self._any_reasonheir_task_true()

    def _any_reasonheir_task_true(self) -> bool:
        return any(x_reasonheir.task for x_reasonheir in self.reasonheirs.values())

    def _create_active_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        plan_name: PersonName,
    ) -> bool:
        self.set_reasonheirs_reason_active()
        active_bool = self.all_reasonheirs_are_active()
        if active_bool and groupunits != {} and plan_name is not None:
            self.laborheir.set_plan_name_is_labor(groupunits, plan_name)
            if self.laborheir.plan_name_is_labor is False:
                active_bool = False
        return active_bool

    def set_range_inheritors_factheirs(
        self,
        plan_keg_dict: dict[RopeTerm,],
        range_inheritors: dict[RopeTerm, RopeTerm],
    ):
        for reason_context in self.reasonheirs.keys():
            if rangeroot_rope := range_inheritors.get(reason_context):
                all_kegs = all_kegs_between(
                    plan_keg_dict=plan_keg_dict,
                    src_rope=rangeroot_rope,
                    dst_reason_context=reason_context,
                    knot=self.knot,
                )
                self._set_range_inheritor_factheir(
                    all_kegs=all_kegs,
                    rangeroot_rope=rangeroot_rope,
                    fact_context=reason_context,
                )

    def _set_range_inheritor_factheir(
        self, all_kegs: list, rangeroot_rope: RopeTerm, fact_context: RopeTerm
    ):
        if rangeroot_factheir := self.factheirs.get(rangeroot_rope):
            new_factheir_obj = create_range_inheritor_factheir(
                rangeroot_factheir=rangeroot_factheir,
                all_kegs=all_kegs,
                fact_context=fact_context,
            )
            self._set_factheir(new_factheir_obj)

    def all_reasonheirs_are_active(self) -> bool:
        x_reasonheirs = self.reasonheirs.values()
        return all(
            x_reasonheir.reason_active != False for x_reasonheir in x_reasonheirs
        )

    def clear_reasonheirs_reason_active(self):
        for reason in self.reasonheirs.values():
            reason.clear_reason_active()

    def _coalesce_with_reasonunits(
        self, reasonheirs: dict[RopeTerm, ReasonHeir]
    ) -> dict[RopeTerm, ReasonHeir]:
        new_reasonheirs = deepcopy(reasonheirs)
        new_reasonheirs |= self.reasonunits
        return new_reasonheirs

    def set_reasonheirs(
        self,
        plan_keg_dict: dict[RopeTerm,],
        reasonheirs: dict[RopeTerm, ReasonCore],
    ):
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)
        self.reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            old_reason_context = old_reasonheir.reason_context
            old_active_requisite = old_reasonheir.active_requisite
            new_reasonheir = reasonheir_shop(
                old_reason_context, None, old_active_requisite
            )
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            if reason_context_keg := plan_keg_dict.get(old_reasonheir.reason_context):
                new_reasonheir.set_heir_active(reason_context_keg.keg_active)
            self.reasonheirs[new_reasonheir.reason_context] = new_reasonheir

    def set_root_keg_reasonheirs(self):
        self.reasonheirs = {}
        for x_reasonunit in self.reasonunits.values():
            new_reasonheir = reasonheir_shop(x_reasonunit.reason_context)
            new_reasonheir.inherit_from_reasonheir(x_reasonunit)
            self.reasonheirs[new_reasonheir.reason_context] = new_reasonheir

    def get_reasonheir(self, reason_context: RopeTerm) -> ReasonHeir:
        return self.reasonheirs.get(reason_context)

    def get_reasonunits_dict(self):
        return {
            reason_context: reason.to_dict()
            for reason_context, reason in self.reasonunits.items()
        }

    def get_kids_dict(self) -> dict[RopeTerm,]:
        return {c_rope: kid.to_dict() for c_rope, kid in self.kids.items()}

    def get_awardunits_dict(self) -> dict[GroupTitle, dict]:
        x_awardunits = self.awardunits.items()
        return {
            x_awardee_title: awardunit.to_dict()
            for x_awardee_title, awardunit in x_awardunits
        }

    def is_kidless(self) -> bool:
        return self.kids == {}

    def has_begin_close(self) -> bool:
        return self.begin is not None and self.close is not None

    def awardheir_exists(self) -> bool:
        return self.awardheirs != {}

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"star": self.star}

        if self.keg_label is not None:
            x_dict["keg_label"] = self.keg_label
        if self.uid is not None:
            x_dict["uid"] = self.uid
        if self.kids not in [{}, None]:
            x_dict["kids"] = self.get_kids_dict()
        if self.reasonunits not in [{}, None]:
            x_dict["reasonunits"] = self.get_reasonunits_dict()
        if self.laborunit not in [None, laborunit_shop()]:
            x_dict["laborunit"] = self.get_laborunit_dict()
        if self.healerunit not in [None, healerunit_shop()]:
            x_dict["healerunit"] = self.healerunit.to_dict()
        if self.awardunits not in [{}, None]:
            x_dict["awardunits"] = self.get_awardunits_dict()
        if self.begin is not None:
            x_dict["begin"] = self.begin
        if self.close is not None:
            x_dict["close"] = self.close
        if self.addin is not None:
            x_dict["addin"] = self.addin
        if self.numor is not None:
            x_dict["numor"] = self.numor
        if self.denom is not None:
            x_dict["denom"] = self.denom
        if self.morph is not None:
            x_dict["morph"] = self.morph
        if self.gogo_want is not None:
            x_dict["gogo_want"] = self.gogo_want
        if self.stop_want is not None:
            x_dict["stop_want"] = self.stop_want
        if self.pledge:
            x_dict["pledge"] = self.pledge
        if self.problem_bool:
            x_dict["problem_bool"] = self.problem_bool
        if self.factunits not in [{}, None]:
            x_dict["factunits"] = self.get_factunits_dict()
        if self.is_expanded is False:
            x_dict["is_expanded"] = self.is_expanded

        return x_dict

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        if is_sub_rope(ref_rope=self.parent_rope, sub_rope=old_rope):
            self.parent_rope = rebuild_rope(self.parent_rope, old_rope, new_rope)

        self.reasonunits == find_replace_rope_key_dict(
            dict_x=self.reasonunits, old_rope=old_rope, new_rope=new_rope
        )

        self.factunits == find_replace_rope_key_dict(
            dict_x=self.factunits, old_rope=old_rope, new_rope=new_rope
        )

    def set_laborunit_empty_if_None(self):
        if self.laborunit is None:
            self.laborunit = laborunit_shop()

    def set_laborheir(
        self,
        parent_laborheir: LaborHeir,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        self.laborheir = laborheir_shop()
        self.laborheir.set_partys(
            parent_laborheir=parent_laborheir,
            laborunit=self.laborunit,
            groupunits=groupunits,
        )

    def get_laborunit_dict(self) -> dict:
        return self.laborunit.to_dict()


def kegunit_shop(
    keg_label: LabelTerm,
    uid: int = None,  # Calculated field?
    parent_rope: RopeTerm = None,
    kids: dict = None,
    star: int = 1,
    awardunits: dict[GroupTitle, AwardUnit] = None,
    awardheirs: dict[GroupTitle, AwardHeir] = None,  # Calculated field
    awardlines: dict[GroupTitle, AwardUnit] = None,  # Calculated field
    reasonunits: dict[RopeTerm, ReasonUnit] = None,
    reasonheirs: dict[RopeTerm, ReasonHeir] = None,  # Calculated field
    laborunit: LaborUnit = None,
    laborheir: LaborHeir = None,  # Calculated field
    factunits: dict[FactUnit] = None,
    factheirs: dict[FactHeir] = None,  # Calculated field
    healerunit: HealerUnit = None,
    begin: float = None,
    close: float = None,
    gogo_want: float = None,
    stop_want: float = None,
    addin: float = None,
    denom: int = None,
    numor: int = None,
    morph: bool = None,
    pledge: bool = None,
    problem_bool: bool = None,
    # Calculated fields
    tree_level: int = None,
    fund_ratio: float = None,
    fund_grain: FundGrain = None,
    fund_onset: FundNum = None,
    fund_cease: FundNum = None,
    task: bool = None,
    keg_active: bool = None,
    descendant_pledge_count: int = None,
    all_person_cred: bool = None,
    all_person_debt: bool = None,
    is_expanded: bool = True,
    keg_active_hx: dict[int, bool] = None,
    knot: KnotTerm = None,
    healerunit_ratio: float = None,
) -> KegUnit:
    x_healerunit = healerunit_shop() if healerunit is None else healerunit

    x_kegkid = KegUnit(
        keg_label=None,
        uid=uid,
        parent_rope=parent_rope,
        kids=get_empty_dict_if_None(kids),
        star=get_positive_int(star),
        awardunits=get_empty_dict_if_None(awardunits),
        awardheirs=get_empty_dict_if_None(awardheirs),
        awardlines=get_empty_dict_if_None(awardlines),
        reasonunits=get_empty_dict_if_None(reasonunits),
        reasonheirs=get_empty_dict_if_None(reasonheirs),
        laborunit=laborunit,
        laborheir=laborheir,
        factunits=get_empty_dict_if_None(factunits),
        factheirs=get_empty_dict_if_None(factheirs),
        healerunit=x_healerunit,
        begin=begin,
        close=close,
        gogo_want=gogo_want,
        stop_want=stop_want,
        addin=addin,
        denom=denom,
        numor=numor,
        morph=morph,
        pledge=get_False_if_None(pledge),
        problem_bool=get_False_if_None(problem_bool),
        # Calculated fields
        tree_level=tree_level,
        fund_ratio=fund_ratio,
        fund_grain=default_grain_num_if_None(fund_grain),
        fund_onset=fund_onset,
        fund_cease=fund_cease,
        task=task,
        keg_active=keg_active,
        descendant_pledge_count=descendant_pledge_count,
        all_person_cred=all_person_cred,
        all_person_debt=all_person_debt,
        is_expanded=is_expanded,
        keg_active_hx=get_empty_dict_if_None(keg_active_hx),
        knot=default_knot_if_None(knot),
        healerunit_ratio=get_0_if_None(healerunit_ratio),
    )
    x_kegkid.set_keg_label(keg_label=keg_label)
    x_kegkid.set_laborunit_empty_if_None()
    return x_kegkid


def get_obj_from_keg_dict(x_dict: dict[str, dict], dict_key: str) -> any:
    if dict_key == "reasonunits":
        return (
            get_reasonunits_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else None
        )
    elif dict_key == "laborunit":
        return (
            get_laborunit_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else laborunit_shop()
        )
    elif dict_key == "healerunit":
        return (
            get_healerunit_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else healerunit_shop()
        )
    elif dict_key == "factunits":
        facts_dict = get_empty_dict_if_None(x_dict.get(dict_key))
        return get_factunits_from_dict(facts_dict)
    elif dict_key == "awardunits":
        return (
            get_awardunits_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) is not None
            else get_awardunits_from_dict({})
        )
    elif dict_key in {"kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else {}
    elif dict_key in {"pledge", "problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else False
    elif dict_key in {"is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else True
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) is not None else None


def all_kegs_between(
    plan_keg_dict: dict[RopeTerm, KegUnit],
    src_rope: RopeTerm,
    dst_reason_context: RopeTerm,
    knot: KnotTerm,
) -> list[KegUnit]:
    all_ropes = all_ropes_between(src_rope, dst_reason_context, knot)
    return [plan_keg_dict.get(x_rope) for x_rope in all_ropes]


def get_rangeunit_from_lineage_of_kegs(
    keg_list: list[KegUnit], x_gogo: float, x_stop: float
) -> RangeUnit:
    for x_keg in keg_list:
        if x_keg.addin:
            x_gogo += get_0_if_None(x_keg.addin)
            x_stop += get_0_if_None(x_keg.addin)
        if (x_keg.numor or x_keg.denom) and not x_keg.morph:
            x_gogo *= get_1_if_None(x_keg.numor) / get_1_if_None(x_keg.denom)
            x_stop *= get_1_if_None(x_keg.numor) / get_1_if_None(x_keg.denom)
        if x_keg.denom and x_keg.morph:
            x_rangeunit = get_morphed_rangeunit(x_gogo, x_stop, x_keg.denom)
            x_gogo = x_rangeunit.gogo
            x_stop = x_rangeunit.stop
    return RangeUnit(x_gogo, x_stop)


def create_range_inheritor_factheir(
    rangeroot_factheir: FactHeir, all_kegs: list[KegUnit], fact_context: RopeTerm
) -> FactHeir:
    x_rangeunit = get_rangeunit_from_lineage_of_kegs(
        keg_list=all_kegs,
        x_gogo=rangeroot_factheir.fact_lower,
        x_stop=rangeroot_factheir.fact_upper,
    )
    return factheir_shop(
        fact_context=fact_context,
        fact_state=fact_context,
        fact_lower=x_rangeunit.gogo,
        fact_upper=x_rangeunit.stop,
    )
