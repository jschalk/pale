from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch11_bud.bud_main import planbudhistory_shop, tranbook_shop
from src.ch13_time.epoch_main import (
    EpochHolder,
    add_epoch_kegunit,
    epochholder_shop,
    get_epoch_length,
    get_epoch_rope,
)
from src.ch14_moment.moment_main import MomentUnit


def get_moment_epochholder(momentunit: MomentUnit) -> EpochHolder:
    """Returns EpochHolder from MomentUnit attrs."""
    momentunit.set_offi_time_max(0)
    # create empty planunit
    x_planunit = planunit_shop(
        plan_name="for_EpochHolder_calculation",
        moment_rope=momentunit.moment_rope,
        knot=momentunit.knot,
        fund_grain=momentunit.fund_grain,
        respect_grain=momentunit.respect_grain,
        mana_grain=momentunit.mana_grain,
    )
    moment_epoch_label = momentunit.epoch.epoch_label
    moment_epoch_config = momentunit.epoch.to_dict()
    # create epoch keg from momentunit.epoch_config
    add_epoch_kegunit(x_planunit, moment_epoch_config)
    x_epochholder = epochholder_shop(x_planunit, moment_epoch_label, 0)
    x_epochholder.calc_epoch()
    return x_epochholder


def add_epoch_frame_to_momentunit(momentunit: MomentUnit, epoch_frame_min: int):
    add_epoch_frame_to_paybook_tran_time(momentunit, epoch_frame_min)
    add_epoch_frame_to_budhistory_bud_time(momentunit, epoch_frame_min)
    add_epoch_frame_to_budhistory_offi_time(momentunit, epoch_frame_min)


def add_epoch_frame_to_budhistory_offi_time(
    momentunit: MomentUnit, epoch_frame_min: int
):
    epoch_length = get_epoch_length(momentunit.get_epoch_config())
    new_offi_times = {
        (offi_time + epoch_frame_min) % epoch_length
        for offi_time in momentunit.offi_times
    }
    momentunit.offi_times = new_offi_times


def add_epoch_frame_to_budhistory_bud_time(
    momentunit: MomentUnit, epoch_frame_min: int
):
    epoch_length = get_epoch_length(momentunit.get_epoch_config())
    new_planbudhistorys = {}
    for plan_name, planhistory in momentunit.planbudhistorys.items():
        new_planbudhistory = planbudhistory_shop(plan_name)
        for bud_time, budunit in planhistory.buds.items():
            new_bud_time = bud_time + epoch_frame_min % epoch_length
            new_planbudhistory.add_bud(
                x_bud_time=new_bud_time,
                x_quota=budunit.quota,
                celldepth=budunit.celldepth,
            )
        new_planbudhistorys[plan_name] = new_planbudhistory
    momentunit.planbudhistorys = new_planbudhistorys


def add_epoch_frame_to_paybook_tran_time(momentunit: MomentUnit, epoch_frame_min: int):
    epoch_length = get_epoch_length(momentunit.get_epoch_config())
    new_paybook = tranbook_shop(momentunit.moment_rope)
    for plan_name, person_values in momentunit.paybook.tranunits.items():
        for person_name, trans_values in person_values.items():
            for tran_time, amount in trans_values.items():
                new_tran_time = tran_time + epoch_frame_min % epoch_length
                new_paybook.add_tranunit(plan_name, person_name, new_tran_time, amount)
    momentunit.paybook = new_paybook
