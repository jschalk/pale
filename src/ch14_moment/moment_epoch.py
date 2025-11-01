from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_epoch.epoch_main import (
    EpochHolder,
    add_epoch_planunit,
    epochholder_shop,
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
    # create epoch plan from momentunit.epoch_config
    add_epoch_planunit(x_beliefunit, moment_epoch_config)
    x_epochholder = epochholder_shop(x_beliefunit, moment_epoch_label, 0)
    x_epochholder.calc_epoch()
    return x_epochholder
