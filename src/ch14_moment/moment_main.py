from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_0_if_None, get_empty_set_if_None
from src.ch00_py.file_toolbox import create_path, get_dir_file_strs, open_json, set_dir
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch07_plan_logic.plan_main import PlanUnit, planunit_shop
from src.ch09_plan_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_plan_lesson.lesson_filehandler import (
    gut_file_exists,
    open_gut_file,
    save_gut_file,
)
from src.ch10_plan_listen.basis_plan import create_listen_basis
from src.ch10_plan_listen.keep_tool import (
    create_treasury_db_file,
    open_job_file,
    save_duty_plan,
    save_job_file,
)
from src.ch10_plan_listen.listen_main import (
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
)
from src.ch11_bud._ref.ch11_path import create_cell_dir_path
from src.ch11_bud.bud_filehandler import cellunit_save_to_dir
from src.ch11_bud.bud_main import (
    BudUnit,
    PlanBudHistory,
    TranBook,
    TranUnit,
    get_planbudhistory_from_dict,
    get_tranbook_from_dict,
    planbudhistory_shop,
    tranbook_shop,
)
from src.ch11_bud.cell_main import cellunit_shop
from src.ch13_time.epoch_main import (
    EpochUnit,
    TimeNum,
    add_epoch_kegunit,
    epochunit_shop,
)
from src.ch14_moment._ref.ch14_semantic_types import (
    FundGrain,
    FundNum,
    KnotTerm,
    ManaGrain,
    MomentRope,
    PersonName,
    PlanName,
    RespectGrain,
    SparkInt,
    default_knot_if_None,
)


def get_default_job_listen_count() -> int:
    return 3


class budunit_Exception(Exception):
    pass


class set_paypurchase_Exception(Exception):
    pass


class set_offi_time_max_Exception(Exception):
    pass


@dataclass
class MomentUnit:
    """Data pipelines:
    pipeline1: lessons->gut
    pipeline2: gut->dutys
    pipeline3: duty->vision
    pipeline4: vision->job
    pipeline5: gut->job (direct)
    pipeline6: gut->vision->job (through visions)
    pipeline7: lessons->job (could be 5 of 6)
    """

    # TODO extraction pipelines into standalone functions
    moment_rope: MomentRope = None
    moment_mstr_dir: str = None
    epoch: EpochUnit = None
    planbudhistorys: dict[PlanName, PlanBudHistory] = None
    paybook: TranBook = None
    offi_times: set[TimeNum] = None
    knot: KnotTerm = None
    fund_grain: FundGrain = None
    respect_grain: RespectGrain = None
    mana_grain: ManaGrain = None
    job_listen_rotations: int = None
    # calculated fields
    offi_time_max: TimeNum = None
    moment_dir: str = None
    plans_dir: str = None
    lessons_dir: str = None
    all_tranbook: TranBook = None

    # directory setup
    def _set_moment_dirs(self):
        moments_dir = create_path(self.moment_mstr_dir, "moments")
        self.moment_dir = create_path(moments_dir, self.moment_rope)
        self.plans_dir = create_path(self.moment_dir, "plans")
        self.lessons_dir = create_path(self.moment_dir, "lessons")
        set_dir(x_path=self.moment_dir)
        set_dir(x_path=self.plans_dir)
        set_dir(x_path=self.lessons_dir)

    def _get_plan_dir(self, plan_name) -> str:
        return create_path(self.plans_dir, plan_name)

    def _get_plan_dir_names(self) -> set:
        plans = get_dir_file_strs(
            self.plans_dir, include_dirs=True, include_files=False
        )
        return sorted(list(plans.keys()))

    # plan administration
    def _set_all_healer_dutys(self, plan_name: PlanName):
        x_gut = open_gut_file(self.moment_mstr_dir, self.moment_rope, plan_name)
        x_gut.cashout()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            for keep_rope in healer_dict.keys():
                create_treasury_db_file(
                    self.moment_mstr_dir,
                    plan_name=plan_name,
                    moment_rope=self.moment_rope,
                    keep_rope=keep_rope,
                    knot=self.knot,
                )
                save_duty_plan(
                    moment_mstr_dir=self.moment_mstr_dir,
                    plan_name=healer_name,
                    moment_rope=self.moment_rope,
                    keep_rope=keep_rope,
                    knot=None,
                    duty_plan=x_gut,
                )

    # job plan administration
    def create_empty_plan_from_moment(self, plan_name: PlanName) -> PlanUnit:
        return planunit_shop(
            plan_name,
            self.moment_rope,
            knot=self.knot,
            fund_grain=self.fund_grain,
            respect_grain=self.respect_grain,
            mana_grain=self.mana_grain,
        )

    def create_gut_file_if_none(self, plan_name: PlanName) -> None:
        if not gut_file_exists(self.moment_mstr_dir, self.moment_rope, plan_name):
            empty_plan = self.create_empty_plan_from_moment(plan_name)
            save_gut_file(self.moment_mstr_dir, empty_plan)

    def create_init_job_from_guts(self, plan_name: PlanName) -> None:
        self.create_gut_file_if_none(plan_name)
        x_gut = open_gut_file(self.moment_mstr_dir, self.moment_rope, plan_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.moment_mstr_dir, x_job)
        save_job_file(self.moment_mstr_dir, x_job)

    def rotate_job(self, plan_name: PlanName) -> PlanUnit:
        x_job = open_job_file(self.moment_mstr_dir, self.moment_rope, plan_name)
        x_job.cashout()
        # # if planunit has healers create job from healers.
        # create planunit from debtors roll
        return listen_to_debtors_roll_jobs_into_job(
            self.moment_mstr_dir, self.moment_rope, plan_name
        )

    def generate_all_jobs(self) -> None:
        plan_names = self._get_plan_dir_names()
        for plan_name in plan_names:
            self.create_init_job_from_guts(plan_name)

        for _ in range(self.job_listen_rotations):
            for plan_name in plan_names:
                save_job_file(self.moment_mstr_dir, self.rotate_job(plan_name))

    def get_job_file_plan(self, plan_name: PlanName) -> PlanUnit:
        return open_job_file(self.moment_mstr_dir, self.moment_rope, plan_name)

    # planbudhistorys
    def set_planbudhistory(self, x_planbudhistory: PlanBudHistory) -> None:
        self.planbudhistorys[x_planbudhistory.plan_name] = x_planbudhistory

    def planbudhistory_exists(self, x_plan_name: PlanName) -> bool:
        return self.planbudhistorys.get(x_plan_name) != None

    def get_planbudhistory(self, x_plan_name: PlanName) -> PlanBudHistory:
        return self.planbudhistorys.get(x_plan_name)

    def del_planbudhistory(self, x_plan_name: PlanName) -> None:
        self.planbudhistorys.pop(x_plan_name)

    def add_budunit(
        self,
        plan_name: PlanName,
        bud_time: TimeNum,
        quota: int,
        allow_prev_to_offi_time_max_entry: bool = False,
        celldepth: int = None,
    ):
        self.offi_time_max = get_0_if_None(self.offi_time_max)
        if bud_time < self.offi_time_max and not allow_prev_to_offi_time_max_entry:
            exception_str = f"Cannot set budunit because bud_time {bud_time} is less than MomentUnit.offi_time_max {self.offi_time_max}."
            raise budunit_Exception(exception_str)
        if self.planbudhistory_exists(plan_name) is False:
            self.set_planbudhistory(planbudhistory_shop(plan_name))
        x_planbudhistory = self.get_planbudhistory(plan_name)
        x_planbudhistory.add_bud(bud_time, quota, celldepth)

    def bud_quota_exists(
        self,
        plan_name: PlanName,
        bud_time: TimeNum,
        quota: int,
    ) -> bool:
        planbudhistory = self.get_planbudhistory(plan_name)
        if not planbudhistory:
            return False
        budunit = planbudhistory.get_bud(bud_time)
        return budunit.quota == quota if budunit else False

    def get_budunit(self, plan_name: PlanName, bud_time: TimeNum) -> BudUnit:
        if not self.get_planbudhistory(plan_name):
            return None
        x_planbudhistory = self.get_planbudhistory(plan_name)
        return x_planbudhistory.get_bud(bud_time)

    def to_dict(self, include_paybook: bool = True) -> dict:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "moment_rope": self.moment_rope,
            "moment_mstr_dir": self.moment_mstr_dir,
            "knot": self.knot,
            "fund_grain": self.fund_grain,
            "mana_grain": self.mana_grain,
            "planbudhistorys": self._get_planbudhistorys_dict(),
            "respect_grain": self.respect_grain,
            "epoch": self.epoch.to_dict(),
            "offi_times": list(self.offi_times),
        }
        if include_paybook:
            x_dict["paybook"] = self.paybook.to_dict()
        return x_dict

    def _get_planbudhistorys_dict(self) -> dict[PlanName, dict]:
        return {
            x_bud.plan_name: x_bud.to_dict() for x_bud in self.planbudhistorys.values()
        }

    def get_planbudhistorys_bud_times(self) -> set[TimeNum]:
        all_budunit_bud_times = set()
        for x_planbudhistory in self.planbudhistorys.values():
            all_budunit_bud_times.update(x_planbudhistory.get_bud_times())
        return all_budunit_bud_times

    def set_paypurchase(self, x_paypurchase: TranUnit):
        self.paybook.set_tranunit(
            tranunit=x_paypurchase,
            blocked_tran_times=self.get_planbudhistorys_bud_times(),
            offi_time_max=self.offi_time_max,
        )

    def add_paypurchase(
        self,
        plan_name: PlanName,
        person_name: PersonName,
        tran_time: TimeNum,
        amount: FundNum,
        blocked_tran_times: set[TimeNum] = None,
        offi_time_max: TimeNum = None,
    ) -> None:
        self.paybook.add_tranunit(
            plan_name=plan_name,
            person_name=person_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            offi_time_max=offi_time_max,
        )

    def paypurchase_exists(
        self, src: PlanName, dst: PersonName, x_tran_time: TimeNum
    ) -> bool:
        return self.paybook.tranunit_exists(src, dst, x_tran_time)

    def get_paypurchase(
        self, src: PlanName, dst: PersonName, x_tran_time: TimeNum
    ) -> TranUnit:
        return self.paybook.get_tranunit(src, dst, x_tran_time)

    def del_paypurchase(
        self, src: PlanName, dst: PersonName, x_tran_time: TimeNum
    ) -> TranUnit:
        return self.paybook.del_tranunit(src, dst, x_tran_time)

    def clear_paypurchases(self):
        self.paybook = tranbook_shop(self.moment_rope)

    # def set_offi_time(self, offi_time: TimeNum):
    #     self.offi_time = offi_time
    #     if self.offi_time_max < self.offi_time:
    #         self.offi_time_max = self.offi_time

    def set_offi_time_max(self, x_offi_time_max: TimeNum):
        x_tran_times = self.paybook.get_tran_times()
        if x_tran_times != set() and max(x_tran_times) >= x_offi_time_max:
            exception_str = f"Cannot set offi_time_max {x_offi_time_max}, paypurchase with greater tran_time exists"
            raise set_offi_time_max_Exception(exception_str)
        # if self.offi_time > x_offi_time_max:
        #     exception_str = f"Cannot set offi_time_max={x_offi_time_max} because it is less than offi_time={self.offi_time}"
        #     raise set_offi_time_max_Exception(exception_str)
        self.offi_time_max = x_offi_time_max

    # def set_offi_time(
    #     self, offi_time: TimeNum, offi_time_max: TimeNum
    # ):
    #     self.set_offi_time(offi_time)
    #     self.set_offi_time_max(_offi_time_max)

    def set_all_tranbook(self) -> None:
        x_tranunits = copy_deepcopy(self.paybook.tranunits)
        x_tranbook = tranbook_shop(self.moment_rope, x_tranunits)
        for plan_name, x_planbudhistory in self.planbudhistorys.items():
            for x_bud_time, x_budunit in x_planbudhistory.buds.items():
                for person_name, x_amount in x_budunit._bud_person_nets.items():
                    x_tranbook.add_tranunit(
                        plan_name, person_name, x_bud_time, x_amount
                    )
        self.all_tranbook = x_tranbook

    def create_buds_root_cells(
        self,
        ote1_dict: dict[PlanName, dict[TimeNum, SparkInt]],
    ) -> None:
        for plan_name, planbudhistory in self.planbudhistorys.items():
            for bud_time in planbudhistory.buds.keys():
                self._create_bud_root_cell(plan_name, ote1_dict, bud_time)

    def _create_bud_root_cell(
        self,
        plan_name: PlanName,
        ote1_dict: dict[PlanName, dict[TimeNum, SparkInt]],
        bud_time: TimeNum,
    ) -> None:
        past_spark_num = _get_ote1_max_past_spark_num(plan_name, ote1_dict, bud_time)
        budunit = self.get_budunit(plan_name, bud_time)
        cellunit = cellunit_shop(
            bud_plan_name=plan_name,
            ancestors=[],
            spark_num=past_spark_num,
            celldepth=budunit.celldepth,
            quota=budunit.quota,
            mana_grain=self.mana_grain,
        )
        root_cell_dir = create_cell_dir_path(
            self.moment_mstr_dir, self.moment_rope, plan_name, bud_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)

    def get_epoch_config(self) -> dict:
        return self.epoch.to_dict()

    def add_epoch_to_gut(self, plan_name: PlanName) -> None:
        """Adds the epoch to the gut file for the given plan."""
        x_gut = open_gut_file(self.moment_mstr_dir, self.moment_rope, plan_name)
        add_epoch_kegunit(x_gut, self.get_epoch_config())
        save_gut_file(self.moment_mstr_dir, x_gut)

    def add_epoch_to_guts(self) -> None:
        """Adds the epoch to all gut files."""
        plan_names = self._get_plan_dir_names()
        for plan_name in plan_names:
            self.add_epoch_to_gut(plan_name)


def _get_ote1_max_past_spark_num(
    plan_name: str, ote1_dict: dict[str, dict[str, int]], bud_time: int
) -> SparkInt:
    """Using the grab most recent ote1 spark int before a given bud_time"""
    ote1_plan_dict = ote1_dict.get(plan_name)
    if not ote1_plan_dict:
        return None
    spark_timenums = set(ote1_plan_dict.keys())
    if past_timenums := {tp for tp in spark_timenums if int(tp) <= bud_time}:
        max_past_timenum = max(past_timenums)
        return ote1_plan_dict.get(max_past_timenum)


def momentunit_shop(
    moment_rope: MomentRope,
    moment_mstr_dir: str,
    epoch: EpochUnit = None,
    offi_times: set[TimeNum] = None,
    knot: KnotTerm = None,
    fund_grain: float = None,
    respect_grain: float = None,
    mana_grain: float = None,
    job_listen_rotations: int = None,
) -> MomentUnit:
    if epoch is None:
        epoch = epochunit_shop()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_momentunit = MomentUnit(
        moment_rope=moment_rope,
        moment_mstr_dir=moment_mstr_dir,
        epoch=epoch,
        planbudhistorys={},
        paybook=tranbook_shop(moment_rope),
        offi_times=get_empty_set_if_None(offi_times),
        knot=default_knot_if_None(knot),
        fund_grain=default_grain_num_if_None(fund_grain),
        respect_grain=default_grain_num_if_None(respect_grain),
        mana_grain=default_grain_num_if_None(mana_grain),
        all_tranbook=tranbook_shop(moment_rope),
        job_listen_rotations=job_listen_rotations,
    )
    if x_momentunit.moment_mstr_dir:
        x_momentunit._set_moment_dirs()
    return x_momentunit


def _get_planbudhistorys_from_dict(
    planbudhistorys_dict: dict,
) -> dict[PlanName, PlanBudHistory]:
    return {
        x_plan_name: get_planbudhistory_from_dict(planbudhistory_dict)
        for x_plan_name, planbudhistory_dict in planbudhistorys_dict.items()
    }


def get_momentunit_from_dict(moment_dict: dict) -> MomentUnit:
    x_moment_rope = moment_dict.get("moment_rope")
    x_moment = momentunit_shop(
        moment_rope=x_moment_rope,
        moment_mstr_dir=moment_dict.get("moment_mstr_dir"),
        offi_times=set(moment_dict.get("offi_times")),
        knot=moment_dict.get("knot"),
        fund_grain=moment_dict.get("fund_grain"),
        respect_grain=moment_dict.get("respect_grain"),
        mana_grain=moment_dict.get("mana_grain"),
    )
    moment_dict_epoch_value = moment_dict.get("epoch")
    if moment_dict_epoch_value:
        x_moment.epoch = epochunit_shop(moment_dict_epoch_value)
    else:
        x_moment.epoch = epochunit_shop(None)
    x_moment.planbudhistorys = _get_planbudhistorys_from_dict(
        moment_dict.get("planbudhistorys")
    )
    x_moment.paybook = get_tranbook_from_dict(moment_dict.get("paybook"))
    return x_moment


def get_default_path_momentunit(
    moment_mstr_dir: str, moment_rope: MomentRope
) -> MomentUnit:
    moment_json_path = create_moment_json_path(moment_mstr_dir, moment_rope)
    x_momentunit = get_momentunit_from_dict(open_json(moment_json_path))
    x_momentunit.moment_mstr_dir = moment_mstr_dir
    x_momentunit._set_moment_dirs()
    return x_momentunit
