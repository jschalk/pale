from dataclasses import dataclass
from src.ch01_py.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.ch02_allot.allot import (
    allot_scale,
    default_grain_num_if_None,
    validate_pool_num,
)
from src.ch07_plan_logic.plan_main import PlanUnit
from src.ch12_keep._ref.ch12_semantic_types import (
    ManaGrain,
    ManaNum,
    MomentLabel,
    PersonName,
    PlanName,
    RespectNum,
    RopeTerm,
)


def get_patientledger(x_plan: PlanUnit) -> dict[PersonName, RespectNum]:
    return {
        personunit.person_name: personunit.person_cred_lumen
        for personunit in x_plan.persons.values()
        if personunit.person_cred_lumen > 0
    }


def get_doctorledger(x_plan: PlanUnit) -> dict[PersonName, RespectNum]:
    return {
        personunit.person_name: personunit.person_debt_lumen
        for personunit in x_plan.persons.values()
        if personunit.person_debt_lumen > 0
    }


@dataclass
class RiverBook:
    plan_name: PlanName = None
    rivercares: dict[PersonName, float] = None
    mana_grain: ManaGrain = None


def riverbook_shop(plan_name: PlanName, mana_grain: ManaGrain = None):
    x_riverbook = RiverBook(plan_name)
    x_riverbook.rivercares = {}
    x_riverbook.mana_grain = default_grain_num_if_None(mana_grain)
    return x_riverbook


def create_riverbook(
    plan_name: PlanName,
    keep_patientledger: dict,
    book_point_amount: int,
    mana_grain: ManaGrain = None,
) -> RiverBook:
    x_riverbook = riverbook_shop(plan_name, mana_grain)
    x_riverbook.rivercares = allot_scale(
        ledger=keep_patientledger,
        scale_number=book_point_amount,
        grain_unit=x_riverbook.mana_grain,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    healer_name: PlanName = None
    number: int = None
    keep_patientledgers: dict[PlanName : dict[PersonName, float]] = None
    riverbooks: dict[PersonName, RiverBook] = None
    mana_grain: ManaGrain = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.plan_name] = x_riverbook

    def set_riverbook(
        self,
        book_person_name: PersonName,
        book_point_amount: float,
    ):
        plan_patientledger = self.keep_patientledgers.get(book_person_name)
        if plan_patientledger is not None:
            x_riverbook = create_riverbook(
                plan_name=book_person_name,
                keep_patientledger=plan_patientledger,
                book_point_amount=book_point_amount,
                mana_grain=default_grain_num_if_None(self.mana_grain),
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[PersonName, float]:
        x_dict = {}
        for x_riverbook in self.riverbooks.values():
            for caree, charge_amount in x_riverbook.rivercares.items():
                if x_dict.get(caree) is None:
                    x_dict[caree] = charge_amount
                else:
                    x_dict[caree] = x_dict[caree] + charge_amount
        return x_dict


def rivercycle_shop(
    healer_name: PlanName,
    number: int,
    keep_patientledgers: dict[PlanName : dict[PersonName, float]] = None,
    mana_grain: ManaGrain = None,
):
    return RiverCycle(
        healer_name=healer_name,
        number=number,
        keep_patientledgers=get_empty_dict_if_None(keep_patientledgers),
        riverbooks=get_empty_dict_if_None(),
        mana_grain=default_grain_num_if_None(mana_grain),
    )


def create_init_rivercycle(
    healer_name: PlanName,
    keep_patientledgers: dict[PlanName : dict[PersonName, float]],
    keep_point_magnitude: ManaNum = None,
    mana_grain: ManaGrain = None,
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(
        healer_name, 0, keep_patientledgers, mana_grain=mana_grain
    )
    x_rivercycle.set_riverbook(healer_name, validate_pool_num(keep_point_magnitude))
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle,
    prev_cycle_cycleledger_post_need: dict[PersonName, float],
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        healer_name=prev_rivercycle.healer_name,
        number=prev_rivercycle.number + 1,
        keep_patientledgers=prev_rivercycle.keep_patientledgers,
        mana_grain=prev_rivercycle.mana_grain,
    )
    for carer_id, chargeing_amount in prev_cycle_cycleledger_post_need.items():
        next_rivercycle.set_riverbook(carer_id, chargeing_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    moment_label: MomentLabel = None
    plan_name: PlanName = None
    keep_rope: RopeTerm = None
    person_name: PersonName = None
    number: int = None
    need_bill_amount: float = None
    care_amount: float = None
    doctor_rank_num: float = None
    patient_rank_num: float = None
    need_paid_amount: float = None
    need_paid_bool: float = None
    need_paid_rank_num: float = None
    need_paid_rank_percent: float = None
    doctor_count: float = None
    patient_count: float = None
    doctor_rank_percent: float = None
    patient_rank_percent: float = None
    rewards_count: float = None
    rewards_magnitude: float = None

    def set_need_bill_amount(self, x_need_bill_amount: float):
        self.need_bill_amount = x_need_bill_amount
        self.set_need_paid_bool()

    def set_need_paid_amount(self, x_need_paid_amount: float):
        self.need_paid_amount = x_need_paid_amount
        self.set_need_paid_bool()

    def set_need_paid_bool(self):
        self.need_paid_bool = (
            self.need_bill_amount is not None
            and self.need_bill_amount == self.need_paid_amount
        )

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        return {
            "moment_label": self.moment_label,
            "healer_name": self.plan_name,
            "keep_rope": self.keep_rope,
            "need_bill_amount": self.need_bill_amount,
            "care_amount": self.care_amount,
            "doctor_rank_num": self.doctor_rank_num,
            "patient_rank_num": self.patient_rank_num,
            "need_paid_amount": self.need_paid_amount,
            "need_paid_bool": self.need_paid_bool,
            "need_paid_rank_num": self.need_paid_rank_num,
            "need_paid_rank_percent": self.need_paid_rank_percent,
            "doctor_count": self.doctor_count,
            "patient_count": self.patient_count,
            "doctor_rank_percent": self.doctor_rank_percent,
            "patient_rank_percent": self.patient_rank_percent,
            "rewards_count": self.rewards_count,
            "rewards_magnitude": self.rewards_magnitude,
        }


def rivergrade_shop(
    moment_label: MomentLabel,
    plan_name: PlanName,
    keep_rope: RopeTerm,
    person_name: PersonName,
    number: float = None,
    doctor_count: int = None,
    patient_count: int = None,
):
    return RiverGrade(
        moment_label=moment_label,
        plan_name=plan_name,
        keep_rope=keep_rope,
        person_name=person_name,
        number=get_0_if_None(number),
        doctor_count=doctor_count,
        patient_count=patient_count,
    )
