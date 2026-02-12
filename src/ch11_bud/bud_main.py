from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    create_csv,
    del_in_nested_dict,
    exists_in_nested_dict,
    get_0_if_None,
    get_empty_dict_if_None,
    get_empty_set_if_None,
    get_from_nested_dict,
    set_in_nested_dict,
)
from src.ch01_allot.allot import default_pool_num
from src.ch11_bud._ref.ch11_semantic_types import (
    FundNum,
    MomentRope,
    PartnerName,
    PlanName,
    TimeNum,
)


class calc_magnitudeException(Exception):
    pass


class tran_time_Exception(Exception):
    pass


DEFAULT_CELLDEPTH = 2


@dataclass
class TranUnit:
    src: PlanName = None
    dst: PartnerName = None
    tran_time: TimeNum = None
    amount: FundNum = None


def tranunit_shop(
    src: PlanName, dst: PartnerName, tran_time: TimeNum, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, tran_time=tran_time, amount=amount)


@dataclass
class TranBook:
    moment_rope: MomentRope = None
    tranunits: dict[PlanName, dict[PartnerName, dict[TimeNum, FundNum]]] = None
    _partners_net: dict[PlanName, dict[PartnerName, FundNum]] = None

    def set_tranunit(
        self,
        tranunit: TranUnit,
        blocked_tran_times: set[TimeNum] = None,
        offi_time_max: TimeNum = None,
    ):
        self.add_tranunit(
            plan_name=tranunit.src,
            partner_name=tranunit.dst,
            tran_time=tranunit.tran_time,
            amount=tranunit.amount,
            blocked_tran_times=blocked_tran_times,
            offi_time_max=offi_time_max,
        )

    def add_tranunit(
        self,
        plan_name: PlanName,
        partner_name: PartnerName,
        tran_time: TimeNum,
        amount: FundNum,
        blocked_tran_times: set[TimeNum] = None,
        offi_time_max: TimeNum = None,
    ):
        if tran_time in get_empty_set_if_None(blocked_tran_times):
            exception_str = (
                f"Cannot set tranunit for tran_time={tran_time}, TimeNum is blocked"
            )
            raise tran_time_Exception(exception_str)
        if offi_time_max != None and tran_time >= offi_time_max:
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, TimeNum is greater than current time={offi_time_max}"
            raise tran_time_Exception(exception_str)
        x_keylist = [plan_name, partner_name, tran_time]
        set_in_nested_dict(self.tranunits, x_keylist, amount)

    def tranunit_exists(
        self, src: PlanName, dst: PartnerName, tran_time: TimeNum
    ) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True) != None

    def get_tranunit(
        self, src: PlanName, dst: PartnerName, tran_time: TimeNum
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)
        if x_amount != None:
            return tranunit_shop(src, dst, tran_time, x_amount)

    def get_amount(
        self, src: PlanName, dst: PartnerName, tran_time: TimeNum
    ) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)

    def del_tranunit(
        self, src: PlanName, dst: PartnerName, tran_time: TimeNum
    ) -> TranUnit:
        x_keylist = [src, dst, tran_time]
        if exists_in_nested_dict(self.tranunits, x_keylist):
            del_in_nested_dict(self.tranunits, x_keylist)

    def get_tran_times(self) -> set[TimeNum]:
        x_set = set()
        for dst_dict in self.tranunits.values():
            for tran_time_dict in dst_dict.values():
                x_set.update(set(tran_time_dict.keys()))
        return x_set

    def get_plans_partners_net(
        self,
    ) -> dict[PlanName, dict[PartnerName, FundNum]]:
        plans_partners_net_dict = {}
        for plan_name, plan_dict in self.tranunits.items():
            for partner_name, partner_dict in plan_dict.items():
                if plans_partners_net_dict.get(plan_name) is None:
                    plans_partners_net_dict[plan_name] = {}
                plan_net_dict = plans_partners_net_dict.get(plan_name)
                plan_net_dict[partner_name] = sum(partner_dict.values())
        return plans_partners_net_dict

    def get_partners_net_dict(self) -> dict[PartnerName, FundNum]:
        partners_net_dict = {}
        for plan_dict in self.tranunits.values():
            for partner_name, partner_dict in sorted(plan_dict.items()):
                if partners_net_dict.get(partner_name) is None:
                    partners_net_dict[partner_name] = sum(partner_dict.values())
                else:
                    partners_net_dict[partner_name] += sum(partner_dict.values())
        return partners_net_dict

    def _get_partners_headers(self) -> list:
        return ["partner_name", "net_amount"]

    def _get_partners_net_array(self) -> list[list]:
        x_kegs = self.get_partners_net_dict().items()
        return [[partner_name, net_amount] for partner_name, net_amount in x_kegs]

    def get_partners_net_csv(self) -> str:
        return create_csv(self._get_partners_headers(), self._get_partners_net_array())

    def join(self, x_tranbook):
        sorted_tranunits = sorted(
            x_tranbook.tranunits.items(),
            key=lambda x: next(iter(next(iter(x[1].values())).keys())),
        )
        for src_partner_name, dst_dict in sorted_tranunits:
            for dst_partner_name, tran_time_dict in dst_dict.items():
                for x_tran_time, x_amount in tran_time_dict.items():
                    self.add_tranunit(
                        src_partner_name, dst_partner_name, x_tran_time, x_amount
                    )

    def to_dict(
        self,
    ) -> dict[MomentRope, dict[PlanName, dict[PartnerName, dict[TimeNum, FundNum]]]]:
        """Returns dict that is serializable to JSON."""

        return {"moment_rope": self.moment_rope, "tranunits": self.tranunits}


def tranbook_shop(
    x_moment_rope: MomentRope,
    x_tranunits: dict[PlanName, dict[PartnerName, dict[TimeNum, FundNum]]] = None,
):
    return TranBook(
        moment_rope=x_moment_rope,
        tranunits=get_empty_dict_if_None(x_tranunits),
        _partners_net={},
    )


def get_tranbook_from_dict(x_dict: dict) -> TranBook:
    x_tranunits = x_dict.get("tranunits")
    new_tranunits = {}
    for x_plan_name, x_partner_dict in x_tranunits.items():
        for x_partner_name, x_tran_time_dict in x_partner_dict.items():
            for x_tran_time, x_amount in x_tran_time_dict.items():
                x_key_list = [x_plan_name, x_partner_name, int(x_tran_time)]
                set_in_nested_dict(new_tranunits, x_key_list, x_amount)
    return tranbook_shop(x_dict.get("moment_rope"), new_tranunits)


@dataclass
class BudUnit:
    bud_time: TimeNum = None
    quota: FundNum = None
    celldepth: int = None  # non-negative
    _magnitude: FundNum = None  # how much of the actual quota is distributed
    _bud_partner_nets: dict[PartnerName, FundNum] = None  # ledger of bud outcome

    def set_bud_partner_net(
        self, x_partner_name: PartnerName, bud_partner_net: FundNum
    ):
        self._bud_partner_nets[x_partner_name] = bud_partner_net

    def bud_partner_net_exists(self, x_partner_name: PartnerName) -> bool:
        return self._bud_partner_nets.get(x_partner_name) != None

    def get_bud_partner_net(self, x_partner_name: PartnerName) -> FundNum:
        return self._bud_partner_nets.get(x_partner_name)

    def del_bud_partner_net(self, x_partner_name: PartnerName):
        self._bud_partner_nets.pop(x_partner_name)

    def calc_magnitude(self):
        bud_partner_nets = self._bud_partner_nets.values()
        x_cred_sum = sum(da_net for da_net in bud_partner_nets if da_net > 0)
        x_debt_sum = sum(da_net for da_net in bud_partner_nets if da_net < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_bud_partner_net={x_debt_sum}, cred_bud_partner_net={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def to_dict(self) -> dict[str,]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"bud_time": self.bud_time, "quota": self.quota}
        if self._bud_partner_nets:
            x_dict["bud_partner_nets"] = self._bud_partner_nets
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        if self.celldepth != DEFAULT_CELLDEPTH:
            x_dict["celldepth"] = self.celldepth
        return x_dict


def budunit_shop(
    bud_time: TimeNum,
    quota: FundNum = None,
    bud_partner_nets: dict[PartnerName, FundNum] = None,
    magnitude: FundNum = None,
    celldepth: int = None,
) -> BudUnit:
    if quota is None:
        quota = default_pool_num()
    if celldepth is None:
        celldepth = DEFAULT_CELLDEPTH

    return BudUnit(
        bud_time=bud_time,
        quota=quota,
        celldepth=celldepth,
        _bud_partner_nets=get_empty_dict_if_None(bud_partner_nets),
        _magnitude=get_0_if_None(magnitude),
    )


@dataclass
class PlanBudHistory:
    plan_name: PlanName = None
    buds: dict[TimeNum, BudUnit] = None
    # calculated fields
    _sum_budunit_quota: FundNum = None
    _sum_partner_bud_nets: int = None
    _bud_time_min: TimeNum = None
    _bud_time_max: TimeNum = None

    def set_bud(self, x_bud: BudUnit):
        self.buds[x_bud.bud_time] = x_bud

    def add_bud(self, x_bud_time: TimeNum, x_quota: FundNum, celldepth: int = None):
        budunit = budunit_shop(bud_time=x_bud_time, quota=x_quota, celldepth=celldepth)
        self.set_bud(budunit)

    def bud_time_exists(self, x_bud_time: TimeNum) -> bool:
        return self.buds.get(x_bud_time) != None

    def get_bud(self, x_bud_time: TimeNum) -> BudUnit:
        return self.buds.get(x_bud_time)

    def del_bud(self, x_bud_time: TimeNum):
        self.buds.pop(x_bud_time)

    def get_2d_array(self) -> list[list]:
        return [
            [self.plan_name, x_bud.bud_time, x_bud.quota]
            for x_bud in self.buds.values()
        ]

    def get_headers(self) -> list:
        return ["plan_name", "bud_time", "quota"]

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        return {"plan_name": self.plan_name, "buds": self._get_buds_dict()}

    def _get_buds_dict(self) -> dict:
        return {x_bud.bud_time: x_bud.to_dict() for x_bud in self.buds.values()}

    def get_bud_times(self) -> set[TimeNum]:
        return set(self.buds.keys())

    def get_tranbook(self, moment_rope: MomentRope) -> TranBook:
        x_tranbook = tranbook_shop(moment_rope)
        for x_bud_time, x_bud in self.buds.items():
            for dst_partner_name, x_quota in x_bud._bud_partner_nets.items():
                x_tranbook.add_tranunit(
                    plan_name=self.plan_name,
                    partner_name=dst_partner_name,
                    tran_time=x_bud_time,
                    amount=x_quota,
                )
        return x_tranbook


def planbudhistory_shop(plan_name: PlanName) -> PlanBudHistory:
    return PlanBudHistory(plan_name=plan_name, buds={}, _sum_partner_bud_nets={})


def get_budunit_from_dict(x_dict: dict) -> BudUnit:
    x_bud_time = x_dict.get("bud_time")
    x_quota = x_dict.get("quota")
    x_bud_net = x_dict.get("bud_partner_nets")
    x_magnitude = x_dict.get("magnitude")
    x_celldepth = x_dict.get("celldepth")
    return budunit_shop(
        x_bud_time, x_quota, x_bud_net, x_magnitude, celldepth=x_celldepth
    )


def get_planbudhistory_from_dict(x_dict: dict) -> PlanBudHistory:
    x_plan_name = x_dict.get("plan_name")
    x_planbudhistory = planbudhistory_shop(x_plan_name)
    x_planbudhistory.buds = get_buds_from_dict(x_dict.get("buds"))
    return x_planbudhistory


def get_buds_from_dict(buds_dict: dict) -> dict[TimeNum, BudUnit]:
    x_dict = {}
    for x_bud_dict in buds_dict.values():
        x_budunit = get_budunit_from_dict(x_bud_dict)
        x_dict[x_budunit.bud_time] = x_budunit
    return x_dict
