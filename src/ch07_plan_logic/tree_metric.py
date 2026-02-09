from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.ch02_person.group import AwardUnit
from src.ch05_reason.reason_main import ReasonUnit, RopeTerm
from src.ch07_plan_logic._ref.ch07_semantic_types import GroupTitle


@dataclass
class TreeMetrics:
    label_count: int = None
    tree_level_count: dict[int, int] = None
    reason_contexts: dict[RopeTerm, int] = None
    awardunits_metrics: dict[GroupTitle, AwardUnit] = None
    keg_uid_max: int = None
    keg_uid_dict: dict[int, int] = None
    all_keg_keg_uids_are_unique: bool = None
    last_evaluated_pledge_keg_rope: RopeTerm = None

    def evaluate_label(
        self,
        tree_level: int,
        reasons: dict[RopeTerm, ReasonUnit],
        awardunits: dict[GroupTitle, AwardUnit],
        keg_uid: int,
        pledge: bool,
        keg_rope: RopeTerm,
    ):
        self.label_count += 1
        self.evaluate_pledge(pledge=pledge, keg_rope=keg_rope)
        self.evaluate_level(tree_level=tree_level)
        self.evaluate_reasonunits(reasons=reasons)
        self.evaluate_awardunits(awardunits=awardunits)
        self.evaluate_keg_uid_max(keg_uid=keg_uid)

    def evaluate_pledge(self, pledge: bool, keg_rope: RopeTerm):
        if pledge:
            self.last_evaluated_pledge_keg_rope = keg_rope

    def evaluate_level(self, tree_level):
        if self.tree_level_count.get(tree_level) is None:
            self.tree_level_count[tree_level] = 1
        else:
            self.tree_level_count[tree_level] += 1

    def evaluate_reasonunits(self, reasons: dict[RopeTerm, ReasonUnit]):
        reasons = {} if reasons is None else reasons
        for reason in reasons.values():
            if self.reason_contexts.get(reason.reason_context) is None:
                self.reason_contexts[reason.reason_context] = 1
            else:
                self.reason_contexts[reason.reason_context] = (
                    self.reason_contexts[reason.reason_context] + 1
                )

    def evaluate_awardunits(self, awardunits: dict[GroupTitle, AwardUnit]):
        if awardunits is not None:
            for awardunit in awardunits.values():
                self.awardunits_metrics[awardunit.awardee_title] = awardunit

    def evaluate_keg_uid_max(self, keg_uid):
        if keg_uid is not None and self.keg_uid_max < keg_uid:
            self.keg_uid_max = keg_uid

        if self.keg_uid_dict.get(keg_uid) is None:
            self.keg_uid_dict[keg_uid] = 1
        else:
            self.keg_uid_dict[keg_uid] += 1
            self.all_keg_keg_uids_are_unique = False


def treemetrics_shop(
    label_count: int = None,
    level_count: dict[int, int] = None,
    reason_contexts: dict[RopeTerm, int] = None,
    awardunits_metrics: dict[GroupTitle, AwardUnit] = None,
    keg_uid_max: int = None,
    keg_uid_dict: dict[int, int] = None,
) -> TreeMetrics:
    x_treemetrics = TreeMetrics(
        label_count=get_0_if_None(label_count),
        tree_level_count=get_empty_dict_if_None(level_count),
        reason_contexts=get_empty_dict_if_None(reason_contexts),
        awardunits_metrics=get_empty_dict_if_None(awardunits_metrics),
        keg_uid_dict=get_empty_dict_if_None(keg_uid_dict),
        keg_uid_max=get_0_if_None(keg_uid_max),
    )
    if x_treemetrics.all_keg_keg_uids_are_unique is None:
        x_treemetrics.all_keg_keg_uids_are_unique = True
    return x_treemetrics
