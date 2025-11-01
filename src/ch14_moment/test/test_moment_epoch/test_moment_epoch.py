from src.ch13_epoch.epoch_main import epochunit_shop
from src.ch13_epoch.test._util.ch13_examples import get_creg_config
from src.ch14_moment.moment_epoch import get_moment_epochholder
from src.ch14_moment.moment_main import momentunit_shop
from src.ch14_moment.test._util.ch14_env import get_temp_dir
from src.ref.keywords import ExampleStrs as exx


def test_get_moment_epochholder_ReturnsObj_Scenario0_Empty_offi_time():
    # ESTABLISH
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir())
    assert sue_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not sue_momentunit.offi_time_max

    # WHEN
    sue_epochholder = get_moment_epochholder(sue_momentunit)

    # THEN
    assert sue_momentunit.offi_time_max == 0
    assert sue_epochholder.x_min == 0
    # assert sue_epochholder.x_min == sue_offi_time_max
    assert sue_epochholder
    assert sue_epochholder._month == "March"
    assert sue_epochholder._hour == "12am"
    assert sue_epochholder._minute == 0
    assert sue_epochholder._monthday == 1
    assert sue_epochholder._c400_number == 0
    assert sue_epochholder._year_num == 0


def test_get_moment_epochholder_ReturnsObj_Scenario1_MomentUnit_NonDefaultAttrs():
    # ESTABLISH
    sue_fund_grain = 5
    sue_respect_grain = 4
    sue_mana_grain = 7
    sue_momentunit = momentunit_shop(
        exx.sue,
        get_temp_dir(),
        knot=exx.slash,
        fund_grain=sue_fund_grain,
        respect_grain=sue_respect_grain,
        mana_grain=sue_mana_grain,
    )
    assert sue_momentunit.epoch == epochunit_shop(get_creg_config())
    assert not sue_momentunit.offi_time_max

    # WHEN
    sue_epochholder = get_moment_epochholder(sue_momentunit)

    # THEN
    assert sue_momentunit.offi_time_max == 0
    assert sue_epochholder.x_min == 0

    assert sue_epochholder
    # assert sue_epochholder.x_min == sue_offi_time_max
    sue_beliefunit = sue_epochholder.x_beliefunit
    assert sue_beliefunit.belief_name == "for_EpochHolder_calculation"
    assert sue_beliefunit.moment_label == sue_momentunit.moment_label
    assert sue_beliefunit.knot == sue_momentunit.knot
    assert sue_beliefunit.fund_grain == sue_momentunit.fund_grain
    assert sue_beliefunit.respect_grain == sue_momentunit.respect_grain
    assert sue_beliefunit.mana_grain == sue_momentunit.mana_grain
    assert sue_epochholder._month == "March"
    assert sue_epochholder._hour == "12am"
    assert sue_epochholder._minute == 0
    assert sue_epochholder._monthday == 1
    assert sue_epochholder._c400_number == 0
    assert sue_epochholder._year_num == 0
    #  beliefunit_shop()
    #  epochholder_shop()


# def test_add_frame_to_momentunit_obj_SetsAttr_Scenario0_tran_time():
#     pass


# def test_add_frame_to_momentunit_obj_SetsAttr_Scenario1_bud_time():
#     pass


# def test_add_frame_to_momentunit_obj_SetsAttr_Scenario2_offi_time():
#     pass
