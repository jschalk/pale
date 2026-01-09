from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch11_bud.bud_main import beliefbudhistory_shop, tranbook_shop
from src.ch13_epoch.epoch_main import (
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
    # create empty beliefunit
    x_beliefunit = beliefunit_shop(
        belief_name="for_EpochHolder_calculation",
        moment_label=momentunit.moment_label,
        knot=momentunit.knot,
        fund_grain=momentunit.fund_grain,
        respect_grain=momentunit.respect_grain,
        mana_grain=momentunit.mana_grain,
    )
    moment_epoch_label = momentunit.epoch.epoch_label
    moment_epoch_config = momentunit.epoch.to_dict()
    # create epoch keg from momentunit.epoch_config
    add_epoch_kegunit(x_beliefunit, moment_epoch_config)
    x_epochholder = epochholder_shop(x_beliefunit, moment_epoch_label, 0)
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
    new_beliefbudhistorys = {}
    for belief_name, beliefhistory in momentunit.beliefbudhistorys.items():
        new_beliefbudhistory = beliefbudhistory_shop(belief_name)
        for bud_time, budunit in beliefhistory.buds.items():
            new_bud_time = bud_time + epoch_frame_min % epoch_length
            new_beliefbudhistory.add_bud(
                x_bud_time=new_bud_time,
                x_quota=budunit.quota,
                celldepth=budunit.celldepth,
            )
        new_beliefbudhistorys[belief_name] = new_beliefbudhistory
    momentunit.beliefbudhistorys = new_beliefbudhistorys


def add_epoch_frame_to_paybook_tran_time(momentunit: MomentUnit, epoch_frame_min: int):
    epoch_length = get_epoch_length(momentunit.get_epoch_config())
    new_paybook = tranbook_shop(momentunit.moment_label)
    for belief_name, voice_values in momentunit.paybook.tranunits.items():
        for voice_name, trans_values in voice_values.items():
            for tran_time, amount in trans_values.items():
                new_tran_time = tran_time + epoch_frame_min % epoch_length
                new_paybook.add_tranunit(belief_name, voice_name, new_tran_time, amount)
    momentunit.paybook = new_paybook
