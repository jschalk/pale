from dataclasses import dataclass
from src.ch01_py.dict_toolbox import get_0_if_None, get_1_if_None
from src.ch02_allot.allot import allot_scale, default_grain_num_if_None
from src.ch03_person._ref.ch03_semantic_types import (
    FundNum,
    GroupMark,
    NameTerm,
    PersonName,
    RespectGrain,
    RespectNum,
    default_groupmark_if_None,
)
from src.ch03_person.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)


def is_nameterm(x_nameterm: NameTerm, groupmark: GroupMark):
    x_nameterm = NameTerm(x_nameterm)
    return x_nameterm.is_name(groupmark=groupmark)


class ValidateNameTermException(Exception):
    pass


def validate_nameterm(
    x_nameterm: NameTerm, x_groupmark: str, not_nameterm_required: bool = False
) -> NameTerm:
    if is_nameterm(x_nameterm, x_groupmark) and not_nameterm_required:
        raise ValidateNameTermException(
            f"'{x_nameterm}' must not be a NameTerm. Must contain GroupMark: '{x_groupmark}'"
        )
    elif is_nameterm(x_nameterm, x_groupmark) is False and not not_nameterm_required:
        raise ValidateNameTermException(
            f"'{x_nameterm}' must be a NameTerm. Cannot contain GroupMark: '{x_groupmark}'"
        )
    return x_nameterm


class Bad_person_nameMemberShipException(Exception):
    pass


@dataclass
class PersonUnit:
    """This represents the plan_name's opinion of the PersonUnit.person_name
    PersonUnit.person_cred_lumen represents how much person_cred_lumen the _plan_name projects to the person_name
    PersonUnit.person_debt_lumen represents how much person_debt_lumen the _plan_name projects to the person_name
    """

    person_name: PersonName = None
    groupmark: str = None
    respect_grain: RespectGrain = None
    person_cred_lumen: int = None
    person_debt_lumen: int = None
    # special attribute: static in plan json, in memory it is deleted after loading and recalculated during saving.
    memberships: dict[PersonName, MemberShip] = None
    # calculated fields
    credor_pool: RespectNum = None
    debtor_pool: RespectNum = None
    irrational_person_debt_lumen: int = None  # set by listening process
    inallocable_person_debt_lumen: int = None  # set by listening process
    # set by Plan.cashout()
    fund_give: FundNum = None
    fund_take: FundNum = None
    fund_agenda_give: FundNum = None
    fund_agenda_take: FundNum = None
    fund_agenda_ratio_give: FundNum = None
    fund_agenda_ratio_take: FundNum = None

    def set_name(self, x_person_name: PersonName):
        self.person_name = validate_nameterm(x_person_name, self.groupmark)

    def set_respect_grain(self, x_respect_grain: float):
        self.respect_grain = x_respect_grain

    def set_credor_person_debt_lumen(
        self,
        person_cred_lumen: float = None,
        person_debt_lumen: float = None,
    ):
        if person_cred_lumen is not None:
            self.set_person_cred_lumen(person_cred_lumen)
        if person_debt_lumen is not None:
            self.set_person_debt_lumen(person_debt_lumen)

    def set_person_cred_lumen(self, person_cred_lumen: int):
        self.person_cred_lumen = person_cred_lumen

    def set_person_debt_lumen(self, person_debt_lumen: int):
        self.person_debt_lumen = person_debt_lumen

    def get_person_cred_lumen(self):
        return get_1_if_None(self.person_cred_lumen)

    def get_person_debt_lumen(self):
        return get_1_if_None(self.person_debt_lumen)

    def clear_fund_give_take(self):
        self.fund_give = 0
        self.fund_take = 0
        self.fund_agenda_give = 0
        self.fund_agenda_take = 0
        self.fund_agenda_ratio_give = 0
        self.fund_agenda_ratio_take = 0

    def add_irrational_person_debt_lumen(self, x_irrational_person_debt_lumen: float):
        self.irrational_person_debt_lumen += x_irrational_person_debt_lumen

    def add_inallocable_person_debt_lumen(self, x_inallocable_person_debt_lumen: float):
        self.inallocable_person_debt_lumen += x_inallocable_person_debt_lumen

    def reset_listen_calculated_attrs(self):
        self.irrational_person_debt_lumen = 0
        self.inallocable_person_debt_lumen = 0

    def add_fund_give(self, fund_give: float):
        self.fund_give += fund_give

    def add_fund_take(self, fund_take: float):
        self.fund_take += fund_take

    def add_fund_agenda_give(self, fund_agenda_give: float):
        self.fund_agenda_give += fund_agenda_give

    def add_fund_agenda_take(self, fund_agenda_take: float):
        self.fund_agenda_take += fund_agenda_take

    def add_person_fund_give_take(
        self,
        fund_give: float,
        fund_take,
        fund_agenda_give: float,
        fund_agenda_take,
    ):
        self.add_fund_give(fund_give)
        self.add_fund_take(fund_take)
        self.add_fund_agenda_give(fund_agenda_give)
        self.add_fund_agenda_take(fund_agenda_take)

    def set_fund_agenda_ratio_give_take(
        self,
        fund_agenda_ratio_give_sum: float,
        fund_agenda_ratio_take_sum: float,
        personunits_person_cred_lumen_sum: float,
        personunits_person_debt_lumen_sum: float,
    ):
        total_person_cred_lumen = personunits_person_cred_lumen_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self.fund_agenda_ratio_give = (
            self.get_person_cred_lumen() / total_person_cred_lumen
            if fund_agenda_ratio_give_sum == 0
            else self.fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_person_debt_lumen = personunits_person_debt_lumen_sum
            self.fund_agenda_ratio_take = (
                self.get_person_debt_lumen() / total_person_debt_lumen
            )
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self.fund_agenda_ratio_take = self.fund_agenda_take / ratio_take_sum

    def add_membership(
        self,
        group_title: GroupTitle,
        group_cred_lumen: float = None,
        group_debt_lumen: float = None,
    ):
        x_membership = membership_shop(group_title, group_cred_lumen, group_debt_lumen)
        self.set_membership(x_membership)

    def set_membership(self, x_membership: MemberShip):
        x_group_title = x_membership.group_title
        group_title_is_person_name = is_nameterm(x_group_title, self.groupmark)
        if group_title_is_person_name and self.person_name != x_group_title:
            exception_str = f"PersonUnit with person_name='{self.person_name}' cannot have link to '{x_group_title}'."
            raise Bad_person_nameMemberShipException(exception_str)

        x_membership.person_name = self.person_name
        self.memberships[x_membership.group_title] = x_membership

    def get_membership(self, group_title: GroupTitle) -> MemberShip:
        return self.memberships.get(group_title)

    def membership_exists(self, group_title: GroupTitle) -> bool:
        return self.memberships.get(group_title) is not None

    def delete_membership(self, group_title: GroupTitle):
        return self.memberships.pop(group_title)

    def memberships_exist(self):
        return len(self.memberships) != 0

    def clear_memberships(self):
        self.memberships = {}

    def set_credor_pool(self, credor_pool: RespectNum):
        self.credor_pool = credor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_cred_lumen
            for x_membership in self.memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.credor_pool, self.respect_grain)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).credor_pool = alloted_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self.debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_debt_lumen
            for x_membership in self.memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.debtor_pool, self.respect_grain)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).debtor_pool = alloted_pool

    def get_memberships_dict(self) -> dict:
        return {
            x_membership.group_title: x_membership.to_dict()
            for x_membership in self.memberships.values()
        }

    def to_dict(self, all_attrs: bool = False) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "person_name": self.person_name,
            "person_cred_lumen": self.person_cred_lumen,
            "person_debt_lumen": self.person_debt_lumen,
            "memberships": self.get_memberships_dict(),
        }
        if self.irrational_person_debt_lumen not in [None, 0]:
            x_dict["irrational_person_debt_lumen"] = self.irrational_person_debt_lumen
        if self.inallocable_person_debt_lumen not in [None, 0]:
            x_dict["inallocable_person_debt_lumen"] = self.inallocable_person_debt_lumen

        if all_attrs:
            self.all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def all_attrs_necessary_in_dict(self, x_dict):
        x_dict["fund_give"] = self.fund_give
        x_dict["fund_take"] = self.fund_take
        x_dict["fund_agenda_give"] = self.fund_agenda_give
        x_dict["fund_agenda_take"] = self.fund_agenda_take
        x_dict["fund_agenda_ratio_give"] = self.fund_agenda_ratio_give
        x_dict["fund_agenda_ratio_take"] = self.fund_agenda_ratio_take


def personunits_get_from_dict(
    x_dict: dict, groupmark: str = None
) -> dict[str, PersonUnit]:
    personunits = {}
    for personunit_dict in x_dict.values():
        x_personunit = personunit_get_from_dict(personunit_dict, groupmark)
        personunits[x_personunit.person_name] = x_personunit
    return personunits


def personunit_get_from_dict(personunit_dict: dict, groupmark: str) -> PersonUnit:
    x_person_name = personunit_dict["person_name"]
    x_person_cred_lumen = personunit_dict["person_cred_lumen"]
    x_person_debt_lumen = personunit_dict["person_debt_lumen"]
    x_memberships_dict = personunit_dict["memberships"]
    x_personunit = personunit_shop(
        x_person_name, x_person_cred_lumen, x_person_debt_lumen, groupmark
    )
    x_personunit.memberships = memberships_get_from_dict(
        x_memberships_dict, x_person_name
    )
    irrational_person_debt_lumen = personunit_dict.get(
        "irrational_person_debt_lumen", 0
    )
    inallocable_person_debt_lumen = personunit_dict.get(
        "inallocable_person_debt_lumen", 0
    )
    x_personunit.add_irrational_person_debt_lumen(
        get_0_if_None(irrational_person_debt_lumen)
    )
    x_personunit.add_inallocable_person_debt_lumen(
        get_0_if_None(inallocable_person_debt_lumen)
    )

    return x_personunit


def personunit_shop(
    person_name: PersonName,
    person_cred_lumen: int = None,
    person_debt_lumen: int = None,
    groupmark: str = None,
    respect_grain: float = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        person_cred_lumen=get_1_if_None(person_cred_lumen),
        person_debt_lumen=get_1_if_None(person_debt_lumen),
        memberships={},
        credor_pool=0,
        debtor_pool=0,
        irrational_person_debt_lumen=0,
        inallocable_person_debt_lumen=0,
        fund_give=0,
        fund_take=0,
        fund_agenda_give=0,
        fund_agenda_take=0,
        fund_agenda_ratio_give=0,
        fund_agenda_ratio_take=0,
        groupmark=default_groupmark_if_None(groupmark),
        respect_grain=default_grain_num_if_None(respect_grain),
    )
    x_personunit.set_name(x_person_name=person_name)
    return x_personunit


class calc_give_take_net_Exception(Exception):
    pass


def calc_give_take_net(x_give: float, x_take: float) -> float:
    x_give = get_0_if_None(x_give)
    x_take = get_0_if_None(x_take)
    if x_give < 0 or x_take < 0:
        if x_give < 0 and x_take >= 0:
            parameters_str = f"calc_give_take_net x_give={x_give}."
        elif x_give >= 0:
            parameters_str = f"calc_give_take_net x_take={x_take}."
        else:
            parameters_str = f"calc_give_take_net x_give={x_give} and x_take={x_take}."
        exception_str = f"{parameters_str} Only non-negative numbers allowed."
        raise calc_give_take_net_Exception(exception_str)
    return x_give - x_take
