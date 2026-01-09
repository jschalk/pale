from src.ch01_py.file_toolbox import open_json, save_json
from src.ch11_bud.bud_main import planbudhistory_shop
from src.ch13_epoch.epoch_main import (
    DEFAULT_EPOCH_LENGTH,
    epochunit_shop,
    get_epoch_length,
)
from src.ch13_epoch.test._util.ch13_examples import get_creg_config
from src.ch14_moment.moment_frame import (
    add_epoch_frame_to_momentunit,
    get_moment_epochholder,
)
from src.ch14_moment.moment_main import momentunit_shop
from src.ch14_moment.test._util.ch14_env import get_temp_dir, temp_dir_setup
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
    sue_planunit = sue_epochholder.x_planunit
    assert sue_planunit.plan_name == "for_EpochHolder_calculation"
    assert sue_planunit.moment_label == sue_momentunit.moment_label
    assert sue_planunit.knot == sue_momentunit.knot
    assert sue_planunit.fund_grain == sue_momentunit.fund_grain
    assert sue_planunit.respect_grain == sue_momentunit.respect_grain
    assert sue_planunit.mana_grain == sue_momentunit.mana_grain
    assert sue_epochholder._month == "March"
    assert sue_epochholder._hour == "12am"
    assert sue_epochholder._minute == 0
    assert sue_epochholder._monthday == 1
    assert sue_epochholder._c400_number == 0
    assert sue_epochholder._year_num == 0
    #  planunit_shop()
    #  epochholder_shop()


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario0_tran_time():
    # ESTABLISH
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir())
    t55 = 55
    sue_momentunit.paybook.add_tranunit(exx.sue, exx.yao, t55, 3)
    epoch_frame_min = 6
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, epoch_frame_min)

    # THEN
    assert not sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)
    expected_time = t55 + epoch_frame_min
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, expected_time)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario1_tran_time_ModularAddition():
    # ESTABLISH
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir())
    t55 = 55
    sue_momentunit.paybook.add_tranunit(exx.sue, exx.yao, t55, 3)
    frame_min = DEFAULT_EPOCH_LENGTH + 300
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, frame_min)

    # THEN
    assert not sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)
    expected_time = (t55 + frame_min) % DEFAULT_EPOCH_LENGTH
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, expected_time)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario2_tran_time_DifferentEpochUnit():
    # ESTABLISH
    creg_epochunit = epochunit_shop(get_creg_config())
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir(), creg_epochunit)
    t55 = 55
    sue_momentunit.paybook.add_tranunit(exx.sue, exx.yao, t55, 3)
    epoch_length = get_epoch_length(get_creg_config())
    frame_min = epoch_length + 300
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, frame_min)

    # THEN
    assert not sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)
    expected_time = (t55 + frame_min) % epoch_length
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, expected_time)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario3_tran_time_NoErrorWhenUsingSameTIme():
    # ESTABLISH
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir())
    t55 = 55
    t65 = 65
    t75 = 75
    sue_momentunit.paybook.add_tranunit(exx.sue, exx.yao, t55, 3)
    sue_momentunit.paybook.add_tranunit(exx.sue, exx.yao, t65, 3)
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t65)
    assert not sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t75)

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, 10)

    # THEN
    assert not sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t55)
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t65)
    assert sue_momentunit.paybook.tranunit_exists(exx.sue, exx.yao, t75)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario4_bud_time():
    # ESTABLISH
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir())
    t55_quota = 4
    t55_time = 55
    epoch_frame_min = 10
    t65_time = t55_time + epoch_frame_min
    sue_bud_hx = planbudhistory_shop(exx.sue)
    sue_bud_hx.add_bud(x_bud_time=t55_time, x_quota=t55_quota)
    sue_momentunit.set_planbudhistory(sue_bud_hx)
    assert sue_momentunit.bud_quota_exists(exx.sue, t55_time, t55_quota)
    assert not sue_momentunit.bud_quota_exists(exx.sue, t65_time, t55_quota)

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, epoch_frame_min)

    # THEN
    assert not sue_momentunit.bud_quota_exists(exx.sue, t55_time, t55_quota)
    assert sue_momentunit.bud_quota_exists(exx.sue, t65_time, t55_quota)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario5_bud_time_ModularAddition():
    # ESTABLISH
    creg_epochunit = epochunit_shop(get_creg_config())
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir(), creg_epochunit)
    t55_quota = 4
    t55_time = 55
    epoch_frame_min = 10
    epoch_length = get_epoch_length(get_creg_config())
    t0x_time = t55_time + epoch_frame_min + epoch_length
    sue_bud_hx = planbudhistory_shop(exx.sue)
    sue_bud_hx.add_bud(x_bud_time=t55_time, x_quota=t55_quota)
    sue_momentunit.set_planbudhistory(sue_bud_hx)
    assert sue_momentunit.bud_quota_exists(exx.sue, t55_time, t55_quota)
    assert not sue_momentunit.bud_quota_exists(exx.sue, t0x_time, t55_quota)

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, epoch_frame_min)

    # THEN
    assert not sue_momentunit.bud_quota_exists(exx.sue, t55_time, t55_quota)
    expected_time = t0x_time % epoch_length
    assert t0x_time != expected_time
    assert sue_momentunit.bud_quota_exists(exx.sue, expected_time, t55_quota)


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario6_offi_time():
    # ESTABLISH
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir())
    epoch_frame_min = 10
    t55_offi_time = 55
    t65_offi_time = t55_offi_time + epoch_frame_min
    sue_momentunit.offi_times.add(t55_offi_time)
    assert t55_offi_time in sue_momentunit.offi_times
    assert t65_offi_time not in sue_momentunit.offi_times

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, epoch_frame_min)

    # THEN
    assert t55_offi_time not in sue_momentunit.offi_times
    assert t65_offi_time in sue_momentunit.offi_times


def test_add_epoch_frame_to_momentunit_SetsAttr_Scenario7_offi_time_Set():
    # ESTABLISH
    creg_epochunit = epochunit_shop(get_creg_config())
    sue_momentunit = momentunit_shop(exx.sue, get_temp_dir(), creg_epochunit)
    epoch_length = get_epoch_length(get_creg_config())
    epoch_frame_min = 10 + epoch_length
    t55_offi_time = 55
    epected_offi_time = t55_offi_time + epoch_frame_min % epoch_length
    sue_momentunit.offi_times.add(t55_offi_time)
    assert t55_offi_time in sue_momentunit.offi_times
    assert epected_offi_time not in sue_momentunit.offi_times

    # WHEN
    add_epoch_frame_to_momentunit(sue_momentunit, epoch_frame_min)

    # THEN
    assert t55_offi_time not in sue_momentunit.offi_times
    assert epected_offi_time in sue_momentunit.offi_times
