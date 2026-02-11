from datetime import datetime
from src.ch00_py.plotly_toolbox import conditional_fig_show
from src.ch02_person.group import awardunit_shop
from src.ch05_reason.reason_main import reasonunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch13_time.epoch_main import (
    add_epoch_kegunit,
    get_c400_constants,
    get_epoch_min_difference,
    get_epoch_min_from_dt,
    get_year_rope,
)
from src.ch13_time.test._util.ch13_examples import (
    add_time_creg_kegunit,
    add_time_five_kegunit,
    creg_hour_int_label,
    creg_weekday_kegunits,
    cregtime_kegunit,
    display_current_creg_five_min,
    get_creg_config,
    get_creg_min_from_dt,
    get_five_config,
    get_five_min_from_dt,
    get_fri,
    get_mon,
    get_sat,
    get_sun,
    get_thu,
    get_tue,
    get_wed,
)
from src.ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_get_creg_config_ReturnsObj():
    # ESTABLISH
    creg_config = get_creg_config()
    five_config = get_five_config()

    # WHEN
    creg_offset = creg_config.get(kw.yr1_jan1_offset)
    five_offset = five_config.get(kw.yr1_jan1_offset)

    # THEN
    assert creg_offset == 440640
    assert five_offset == 1683478080
    c400_len = get_c400_constants().c400_leap_length
    assert five_offset == (c400_len * 8) + 440640
    assert creg_config.get(kw.monthday_index) == 1
    assert five_config.get(kw.monthday_index) == 0


def test_cregtime_kegunit_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert cregtime_kegunit().begin == 0
    assert cregtime_kegunit().close == 1472657760
    assert cregtime_kegunit().close == get_c400_constants().c400_leap_length * 7


def test_creg_weekday_kegunits_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert creg_weekday_kegunits().get(get_wed()).gogo_want == 0
    assert creg_weekday_kegunits().get(get_thu()).gogo_want == 1440
    assert creg_weekday_kegunits().get(get_fri()).gogo_want == 2880
    assert creg_weekday_kegunits().get(get_sat()).gogo_want == 4320
    assert creg_weekday_kegunits().get(get_sun()).gogo_want == 5760
    assert creg_weekday_kegunits().get(get_mon()).gogo_want == 7200
    assert creg_weekday_kegunits().get(get_tue()).gogo_want == 8640
    assert creg_weekday_kegunits().get(get_wed()).stop_want == 1440
    assert creg_weekday_kegunits().get(get_thu()).stop_want == 2880
    assert creg_weekday_kegunits().get(get_fri()).stop_want == 4320
    assert creg_weekday_kegunits().get(get_sat()).stop_want == 5760
    assert creg_weekday_kegunits().get(get_sun()).stop_want == 7200
    assert creg_weekday_kegunits().get(get_mon()).stop_want == 8640
    assert creg_weekday_kegunits().get(get_tue()).stop_want == 10080


def test_add_time_creg_kegunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(kw.time)
    creg_rope = sue_planunit.make_rope(time_rope, kw.creg)
    day_rope = sue_planunit.make_rope(creg_rope, kw.day)
    days_rope = sue_planunit.make_rope(creg_rope, kw.days)
    print(f"{time_rope=}")
    print(f"{creg_rope=}")
    print(f"{day_rope=}")
    assert not sue_planunit.keg_exists(time_rope)
    assert not sue_planunit.keg_exists(creg_rope)
    assert not sue_planunit.keg_exists(day_rope)
    assert not sue_planunit.keg_exists(days_rope)

    # WHEN
    sue_planunit = add_time_creg_kegunit(sue_planunit)

    # THEN
    assert sue_planunit.keg_exists(time_rope)
    assert sue_planunit.keg_exists(creg_rope)
    assert sue_planunit.keg_exists(day_rope)
    assert sue_planunit.keg_exists(days_rope)
    assert sue_planunit.get_keg_obj(creg_rope).begin == 0
    assert sue_planunit.get_keg_obj(creg_rope).close == 1472657760
    assert sue_planunit.get_keg_obj(day_rope).denom == 1440
    assert sue_planunit.get_keg_obj(day_rope).morph
    assert sue_planunit.get_keg_obj(days_rope).denom == 1440
    assert sue_planunit.get_keg_obj(days_rope).morph is None


def test_add_time_creg_kegunit_ReturnsObjWith_weeks():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(kw.time)
    creg_rope = sue_planunit.make_rope(time_rope, kw.creg)
    week_rope = sue_planunit.make_rope(creg_rope, kw.week)
    sun_rope = sue_planunit.make_rope(week_rope, get_sun())
    mon_rope = sue_planunit.make_rope(week_rope, get_mon())
    tue_rope = sue_planunit.make_rope(week_rope, get_tue())
    wed_rope = sue_planunit.make_rope(week_rope, get_wed())
    thu_rope = sue_planunit.make_rope(week_rope, get_thu())
    fri_rope = sue_planunit.make_rope(week_rope, get_fri())
    sat_rope = sue_planunit.make_rope(week_rope, get_sat())
    weeks_rope = sue_planunit.make_rope(creg_rope, kw.weeks)

    assert not sue_planunit.keg_exists(week_rope)
    assert not sue_planunit.keg_exists(sun_rope)
    assert not sue_planunit.keg_exists(mon_rope)
    assert not sue_planunit.keg_exists(tue_rope)
    assert not sue_planunit.keg_exists(wed_rope)
    assert not sue_planunit.keg_exists(thu_rope)
    assert not sue_planunit.keg_exists(fri_rope)
    assert not sue_planunit.keg_exists(sat_rope)
    assert not sue_planunit.keg_exists(weeks_rope)

    # WHEN
    sue_planunit = add_time_creg_kegunit(sue_planunit)

    # THEN
    assert sue_planunit.keg_exists(week_rope)
    assert sue_planunit.get_keg_obj(week_rope).gogo_want is None
    assert sue_planunit.get_keg_obj(week_rope).stop_want is None
    assert sue_planunit.get_keg_obj(week_rope).denom == 10080
    assert sue_planunit.get_keg_obj(week_rope).morph
    assert sue_planunit.keg_exists(sun_rope)
    assert sue_planunit.keg_exists(mon_rope)
    assert sue_planunit.keg_exists(tue_rope)
    assert sue_planunit.keg_exists(wed_rope)
    assert sue_planunit.keg_exists(thu_rope)
    assert sue_planunit.keg_exists(fri_rope)
    assert sue_planunit.keg_exists(sat_rope)
    assert sue_planunit.keg_exists(weeks_rope)
    assert sue_planunit.get_keg_obj(weeks_rope).denom == 10080
    assert sue_planunit.get_keg_obj(weeks_rope).morph is None


def test_add_time_creg_kegunit_ReturnsObjWith_c400_leap_rope():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(kw.time)
    creg_rope = sue_planunit.make_rope(time_rope, kw.creg)
    c400_leap_rope = sue_planunit.make_rope(creg_rope, kw.c400_leap)
    c400_core_rope = sue_planunit.make_rope(c400_leap_rope, kw.c400_core)
    c100_rope = sue_planunit.make_rope(c400_core_rope, kw.c100)
    yr4_leap_rope = sue_planunit.make_rope(c100_rope, kw.yr4_leap)
    yr4_core_rope = sue_planunit.make_rope(yr4_leap_rope, kw.yr4_core)
    year_rope = sue_planunit.make_rope(yr4_core_rope, kw.year)

    assert not sue_planunit.keg_exists(c400_leap_rope)

    # WHEN
    sue_planunit = add_time_creg_kegunit(sue_planunit)

    # THEN
    assert sue_planunit.keg_exists(c400_leap_rope)
    c400_leap_keg = sue_planunit.get_keg_obj(c400_leap_rope)
    assert not c400_leap_keg.gogo_want
    assert not c400_leap_keg.stop_want
    assert c400_leap_keg.denom == 210379680
    assert c400_leap_keg.morph

    assert sue_planunit.keg_exists(c400_core_rope)
    c400_core_keg = sue_planunit.get_keg_obj(c400_core_rope)
    assert not c400_core_keg.gogo_want
    assert not c400_core_keg.stop_want
    assert c400_core_keg.denom == 210378240
    assert c400_core_keg.morph

    assert sue_planunit.keg_exists(c100_rope)
    c100_keg = sue_planunit.get_keg_obj(c100_rope)
    assert not c100_keg.gogo_want
    assert not c100_keg.stop_want
    assert c100_keg.denom == 52594560
    assert c100_keg.morph

    assert sue_planunit.keg_exists(yr4_leap_rope)
    yr4_leap_keg = sue_planunit.get_keg_obj(yr4_leap_rope)
    assert not yr4_leap_keg.gogo_want
    assert not yr4_leap_keg.stop_want
    assert yr4_leap_keg.denom == 2103840
    assert yr4_leap_keg.morph

    assert sue_planunit.keg_exists(yr4_core_rope)
    yr4_core_keg = sue_planunit.get_keg_obj(yr4_core_rope)
    assert not yr4_core_keg.gogo_want
    assert not yr4_core_keg.stop_want
    assert yr4_core_keg.denom == 2102400
    assert yr4_core_keg.morph

    assert sue_planunit.keg_exists(year_rope)
    year_keg = sue_planunit.get_keg_obj(year_rope)
    assert not year_keg.gogo_want
    assert not year_keg.stop_want
    assert year_keg.denom == 525600
    assert year_keg.morph


def test_add_time_creg_kegunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(kw.time)
    creg_rope = sue_planunit.make_rope(time_rope, kw.creg)
    year_rope = get_year_rope(sue_planunit, kw.creg)

    assert not sue_planunit.keg_exists(creg_rope)
    assert not sue_planunit.keg_exists(year_rope)

    jan_rope = sue_planunit.make_rope(year_rope, exx.January)
    feb_rope = sue_planunit.make_rope(year_rope, exx.February)
    mar_rope = sue_planunit.make_rope(year_rope, exx.March)
    apr_rope = sue_planunit.make_rope(year_rope, exx.April)
    may_rope = sue_planunit.make_rope(year_rope, exx.May)
    jun_rope = sue_planunit.make_rope(year_rope, exx.June)
    jul_rope = sue_planunit.make_rope(year_rope, exx.July)
    aug_rope = sue_planunit.make_rope(year_rope, exx.August)
    sep_rope = sue_planunit.make_rope(year_rope, exx.September)
    oct_rope = sue_planunit.make_rope(year_rope, exx.October)
    nov_rope = sue_planunit.make_rope(year_rope, exx.November)
    dec_rope = sue_planunit.make_rope(year_rope, exx.December)
    assert not sue_planunit.keg_exists(jan_rope)
    assert not sue_planunit.keg_exists(feb_rope)
    assert not sue_planunit.keg_exists(mar_rope)
    assert not sue_planunit.keg_exists(apr_rope)
    assert not sue_planunit.keg_exists(may_rope)
    assert not sue_planunit.keg_exists(jun_rope)
    assert not sue_planunit.keg_exists(jul_rope)
    assert not sue_planunit.keg_exists(aug_rope)
    assert not sue_planunit.keg_exists(sep_rope)
    assert not sue_planunit.keg_exists(oct_rope)
    assert not sue_planunit.keg_exists(nov_rope)
    assert not sue_planunit.keg_exists(dec_rope)
    assert not sue_planunit.keg_exists(year_rope)

    # WHEN
    sue_planunit = add_time_creg_kegunit(sue_planunit)

    # THEN
    assert sue_planunit.keg_exists(creg_rope)
    assert sue_planunit.keg_exists(year_rope)

    year_keg = sue_planunit.get_keg_obj(year_rope)
    # assert year_keg.morph
    assert sue_planunit.keg_exists(jan_rope)
    assert sue_planunit.keg_exists(feb_rope)
    assert sue_planunit.keg_exists(mar_rope)
    assert sue_planunit.keg_exists(apr_rope)
    assert sue_planunit.keg_exists(may_rope)
    assert sue_planunit.keg_exists(jun_rope)
    assert sue_planunit.keg_exists(jul_rope)
    assert sue_planunit.keg_exists(aug_rope)
    assert sue_planunit.keg_exists(sep_rope)
    assert sue_planunit.keg_exists(oct_rope)
    assert sue_planunit.keg_exists(nov_rope)
    assert sue_planunit.keg_exists(dec_rope)
    assert sue_planunit.get_keg_obj(jan_rope).addin == 1440
    assert sue_planunit.get_keg_obj(feb_rope).addin == 1440
    assert sue_planunit.get_keg_obj(mar_rope).addin == 1440
    assert sue_planunit.get_keg_obj(apr_rope).addin == 1440
    assert sue_planunit.get_keg_obj(may_rope).addin == 1440
    assert sue_planunit.get_keg_obj(jun_rope).addin == 1440
    assert sue_planunit.get_keg_obj(jul_rope).addin == 1440
    assert sue_planunit.get_keg_obj(aug_rope).addin == 1440
    assert sue_planunit.get_keg_obj(sep_rope).addin == 1440
    assert sue_planunit.get_keg_obj(oct_rope).addin == 1440
    assert sue_planunit.get_keg_obj(nov_rope).addin == 1440
    assert sue_planunit.get_keg_obj(dec_rope).addin == 1440

    assert sue_planunit.get_keg_obj(jan_rope).gogo_want == 440640
    assert sue_planunit.get_keg_obj(feb_rope).gogo_want == 485280
    assert sue_planunit.get_keg_obj(mar_rope).gogo_want == 0
    assert sue_planunit.get_keg_obj(apr_rope).gogo_want == 44640
    assert sue_planunit.get_keg_obj(may_rope).gogo_want == 87840
    assert sue_planunit.get_keg_obj(jun_rope).gogo_want == 132480
    assert sue_planunit.get_keg_obj(jul_rope).gogo_want == 175680
    assert sue_planunit.get_keg_obj(aug_rope).gogo_want == 220320
    assert sue_planunit.get_keg_obj(sep_rope).gogo_want == 264960
    assert sue_planunit.get_keg_obj(oct_rope).gogo_want == 308160
    assert sue_planunit.get_keg_obj(nov_rope).gogo_want == 352800
    assert sue_planunit.get_keg_obj(dec_rope).gogo_want == 396000

    assert sue_planunit.get_keg_obj(jan_rope).stop_want == 485280
    assert sue_planunit.get_keg_obj(feb_rope).stop_want == 525600
    assert sue_planunit.get_keg_obj(mar_rope).stop_want == 44640
    assert sue_planunit.get_keg_obj(apr_rope).stop_want == 87840
    assert sue_planunit.get_keg_obj(may_rope).stop_want == 132480
    assert sue_planunit.get_keg_obj(jun_rope).stop_want == 175680
    assert sue_planunit.get_keg_obj(jul_rope).stop_want == 220320
    assert sue_planunit.get_keg_obj(aug_rope).stop_want == 264960
    assert sue_planunit.get_keg_obj(sep_rope).stop_want == 308160
    assert sue_planunit.get_keg_obj(oct_rope).stop_want == 352800
    assert sue_planunit.get_keg_obj(nov_rope).stop_want == 396000
    assert sue_planunit.get_keg_obj(dec_rope).stop_want == 440640


def test_add_time_creg_kegunit_ReturnsObjWith_c400_leap():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(kw.time)
    creg_rope = sue_planunit.make_rope(time_rope, kw.creg)
    day_rope = sue_planunit.make_rope(creg_rope, kw.day)
    days_rope = sue_planunit.make_rope(creg_rope, kw.days)
    print(f"{time_rope=}")
    print(f"{creg_rope=}")
    print(f"{day_rope=}")
    assert not sue_planunit.keg_exists(time_rope)
    assert not sue_planunit.keg_exists(creg_rope)
    assert not sue_planunit.keg_exists(day_rope)
    assert not sue_planunit.keg_exists(days_rope)

    # WHEN
    sue_planunit = add_time_creg_kegunit(sue_planunit)

    # THEN
    assert sue_planunit.keg_exists(time_rope)
    assert sue_planunit.keg_exists(creg_rope)
    creg_keg = sue_planunit.get_keg_obj(creg_rope)
    assert creg_keg.begin == 0
    assert creg_keg.close == 1472657760
    assert sue_planunit.keg_exists(day_rope)
    day_keg = sue_planunit.get_keg_obj(day_rope)
    assert day_keg.denom == 1440
    assert day_keg.morph
    assert sue_planunit.keg_exists(days_rope)
    days_keg = sue_planunit.get_keg_obj(days_rope)
    assert days_keg.denom == 1440
    assert not days_keg.morph


def test_add_time_creg_kegunit_ReturnsObjWith_hours():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_rope = sue_planunit.make_l1_rope(kw.time)
    creg_rope = sue_planunit.make_rope(time_rope, kw.creg)
    day_rope = sue_planunit.make_rope(creg_rope, kw.day)
    hour_rope = sue_planunit.make_rope(day_rope, kw.hour)
    hr_00_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(0))
    hr_01_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(1))
    hr_02_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(2))
    hr_03_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(3))
    hr_04_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(4))
    hr_05_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(5))
    hr_06_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(6))
    hr_07_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(7))
    hr_08_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(8))
    hr_09_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(9))
    hr_10_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(10))
    hr_11_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(11))
    hr_12_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(12))
    hr_13_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(13))
    hr_14_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(14))
    hr_15_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(15))
    hr_16_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(16))
    hr_17_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(17))
    hr_18_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(18))
    hr_19_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(19))
    hr_20_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(20))
    hr_21_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(21))
    hr_22_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(22))
    hr_23_rope = sue_planunit.make_rope(day_rope, creg_hour_int_label(23))

    print(f"{day_rope=}")
    print(f"{hr_00_rope=}")
    assert not sue_planunit.keg_exists(time_rope)
    assert not sue_planunit.keg_exists(creg_rope)
    assert not sue_planunit.keg_exists(day_rope)
    assert not sue_planunit.keg_exists(hr_00_rope)
    assert not sue_planunit.keg_exists(hr_01_rope)
    assert not sue_planunit.keg_exists(hr_02_rope)
    assert not sue_planunit.keg_exists(hr_03_rope)
    assert not sue_planunit.keg_exists(hr_04_rope)
    assert not sue_planunit.keg_exists(hr_05_rope)
    assert not sue_planunit.keg_exists(hr_06_rope)
    assert not sue_planunit.keg_exists(hr_07_rope)
    assert not sue_planunit.keg_exists(hr_08_rope)
    assert not sue_planunit.keg_exists(hr_09_rope)
    assert not sue_planunit.keg_exists(hr_10_rope)
    assert not sue_planunit.keg_exists(hr_11_rope)
    assert not sue_planunit.keg_exists(hr_12_rope)
    assert not sue_planunit.keg_exists(hr_13_rope)
    assert not sue_planunit.keg_exists(hr_14_rope)
    assert not sue_planunit.keg_exists(hr_15_rope)
    assert not sue_planunit.keg_exists(hr_16_rope)
    assert not sue_planunit.keg_exists(hr_17_rope)
    assert not sue_planunit.keg_exists(hr_18_rope)
    assert not sue_planunit.keg_exists(hr_19_rope)
    assert not sue_planunit.keg_exists(hr_20_rope)
    assert not sue_planunit.keg_exists(hr_21_rope)
    assert not sue_planunit.keg_exists(hr_22_rope)
    assert not sue_planunit.keg_exists(hr_23_rope)

    # WHEN
    sue_planunit = add_time_creg_kegunit(sue_planunit)

    # THEN
    day_keg = sue_planunit.get_keg_obj(day_rope)
    print(f"{day_keg.kids.keys()=}")
    assert sue_planunit.keg_exists(time_rope)
    assert sue_planunit.keg_exists(creg_rope)
    assert sue_planunit.keg_exists(day_rope)
    # assert sue_planunit.get_keg_obj(hour_rope).denom == 60
    # assert sue_planunit.get_keg_obj(hour_rope).morph
    # assert not sue_planunit.get_keg_obj(hour_rope).gogo_want
    # assert not sue_planunit.get_keg_obj(hour_rope).stop_want
    assert sue_planunit.keg_exists(hr_00_rope)
    assert sue_planunit.keg_exists(hr_01_rope)
    assert sue_planunit.keg_exists(hr_02_rope)
    assert sue_planunit.keg_exists(hr_03_rope)
    assert sue_planunit.keg_exists(hr_04_rope)
    assert sue_planunit.keg_exists(hr_05_rope)
    assert sue_planunit.keg_exists(hr_06_rope)
    assert sue_planunit.keg_exists(hr_07_rope)
    assert sue_planunit.keg_exists(hr_08_rope)
    assert sue_planunit.keg_exists(hr_09_rope)
    assert sue_planunit.keg_exists(hr_10_rope)
    assert sue_planunit.keg_exists(hr_11_rope)
    assert sue_planunit.keg_exists(hr_12_rope)
    assert sue_planunit.keg_exists(hr_13_rope)
    assert sue_planunit.keg_exists(hr_14_rope)
    assert sue_planunit.keg_exists(hr_15_rope)
    assert sue_planunit.keg_exists(hr_16_rope)
    assert sue_planunit.keg_exists(hr_17_rope)
    assert sue_planunit.keg_exists(hr_18_rope)
    assert sue_planunit.keg_exists(hr_19_rope)
    assert sue_planunit.keg_exists(hr_20_rope)
    assert sue_planunit.keg_exists(hr_21_rope)
    assert sue_planunit.keg_exists(hr_22_rope)
    assert sue_planunit.keg_exists(hr_23_rope)
    assert sue_planunit.get_keg_obj(hr_00_rope).gogo_want == 0
    assert sue_planunit.get_keg_obj(hr_01_rope).gogo_want == 60
    assert sue_planunit.get_keg_obj(hr_02_rope).gogo_want == 120
    assert sue_planunit.get_keg_obj(hr_03_rope).gogo_want == 180
    assert sue_planunit.get_keg_obj(hr_04_rope).gogo_want == 240
    assert sue_planunit.get_keg_obj(hr_05_rope).gogo_want == 300
    assert sue_planunit.get_keg_obj(hr_06_rope).gogo_want == 360
    assert sue_planunit.get_keg_obj(hr_07_rope).gogo_want == 420
    assert sue_planunit.get_keg_obj(hr_08_rope).gogo_want == 480
    assert sue_planunit.get_keg_obj(hr_09_rope).gogo_want == 540
    assert sue_planunit.get_keg_obj(hr_10_rope).gogo_want == 600
    assert sue_planunit.get_keg_obj(hr_11_rope).gogo_want == 660
    assert sue_planunit.get_keg_obj(hr_12_rope).gogo_want == 720
    assert sue_planunit.get_keg_obj(hr_13_rope).gogo_want == 780
    assert sue_planunit.get_keg_obj(hr_14_rope).gogo_want == 840
    assert sue_planunit.get_keg_obj(hr_15_rope).gogo_want == 900
    assert sue_planunit.get_keg_obj(hr_16_rope).gogo_want == 960
    assert sue_planunit.get_keg_obj(hr_17_rope).gogo_want == 1020
    assert sue_planunit.get_keg_obj(hr_18_rope).gogo_want == 1080
    assert sue_planunit.get_keg_obj(hr_19_rope).gogo_want == 1140
    assert sue_planunit.get_keg_obj(hr_20_rope).gogo_want == 1200
    assert sue_planunit.get_keg_obj(hr_21_rope).gogo_want == 1260
    assert sue_planunit.get_keg_obj(hr_22_rope).gogo_want == 1320
    assert sue_planunit.get_keg_obj(hr_23_rope).gogo_want == 1380
    assert sue_planunit.get_keg_obj(hr_00_rope).stop_want == 60
    assert sue_planunit.get_keg_obj(hr_01_rope).stop_want == 120
    assert sue_planunit.get_keg_obj(hr_02_rope).stop_want == 180
    assert sue_planunit.get_keg_obj(hr_03_rope).stop_want == 240
    assert sue_planunit.get_keg_obj(hr_04_rope).stop_want == 300
    assert sue_planunit.get_keg_obj(hr_05_rope).stop_want == 360
    assert sue_planunit.get_keg_obj(hr_06_rope).stop_want == 420
    assert sue_planunit.get_keg_obj(hr_07_rope).stop_want == 480
    assert sue_planunit.get_keg_obj(hr_08_rope).stop_want == 540
    assert sue_planunit.get_keg_obj(hr_09_rope).stop_want == 600
    assert sue_planunit.get_keg_obj(hr_10_rope).stop_want == 660
    assert sue_planunit.get_keg_obj(hr_11_rope).stop_want == 720
    assert sue_planunit.get_keg_obj(hr_12_rope).stop_want == 780
    assert sue_planunit.get_keg_obj(hr_13_rope).stop_want == 840
    assert sue_planunit.get_keg_obj(hr_14_rope).stop_want == 900
    assert sue_planunit.get_keg_obj(hr_15_rope).stop_want == 960
    assert sue_planunit.get_keg_obj(hr_16_rope).stop_want == 1020
    assert sue_planunit.get_keg_obj(hr_17_rope).stop_want == 1080
    assert sue_planunit.get_keg_obj(hr_18_rope).stop_want == 1140
    assert sue_planunit.get_keg_obj(hr_19_rope).stop_want == 1200
    assert sue_planunit.get_keg_obj(hr_20_rope).stop_want == 1260
    assert sue_planunit.get_keg_obj(hr_21_rope).stop_want == 1320
    assert sue_planunit.get_keg_obj(hr_22_rope).stop_want == 1380
    assert sue_planunit.get_keg_obj(hr_23_rope).stop_want == 1440


def test_add_time_creg_kegunit_ReturnsObjWith_offset_KegUnits():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_kegunit(sue_plan)
    sue_plan.cashout()
    time_rope = sue_plan.make_l1_rope(kw.time)
    creg_rope = sue_plan.make_rope(time_rope, kw.creg)
    five_rope = sue_plan.make_rope(time_rope, kw.five)
    creg_yr1_jan1_offset_rope = sue_plan.make_rope(creg_rope, kw.yr1_jan1_offset)
    five_yr1_jan1_offset_rope = sue_plan.make_rope(five_rope, kw.yr1_jan1_offset)

    assert sue_plan.keg_exists(creg_yr1_jan1_offset_rope)
    creg_yr1_offset_keg = sue_plan.get_keg_obj(creg_yr1_jan1_offset_rope)
    assert creg_yr1_offset_keg.addin == get_creg_config().get(kw.yr1_jan1_offset)
    assert not sue_plan.keg_exists(five_yr1_jan1_offset_rope)

    # WHEN
    sue_plan = add_time_five_kegunit(sue_plan)

    # THEN
    assert sue_plan.keg_exists(creg_yr1_jan1_offset_rope)
    assert sue_plan.keg_exists(five_yr1_jan1_offset_rope)
    five_yr1_offset_keg = sue_plan.get_keg_obj(five_yr1_jan1_offset_rope)
    assert five_yr1_offset_keg.addin == get_five_config().get(kw.yr1_jan1_offset)


def test_add_epoch_kegunit_SetsAttr_Scenario0():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.cashout()
    time_rope = sue_plan.make_l1_rope(kw.time)
    creg_rope = sue_plan.make_rope(time_rope, kw.creg)
    creg_yr1_jan1_offset_rope = sue_plan.make_rope(creg_rope, kw.yr1_jan1_offset)
    creg_year_rope = get_year_rope(sue_plan, kw.creg)
    print(f"{creg_year_rope=}")
    # print(f"{sue_plan._keg_dict.keys()=}")
    creg_config = get_creg_config()

    assert not sue_plan.keg_exists(creg_year_rope)
    assert not sue_plan.keg_exists(creg_yr1_jan1_offset_rope)

    # WHEN
    add_epoch_kegunit(sue_plan, creg_config)

    # THEN
    assert sue_plan.keg_exists(creg_year_rope)
    assert sue_plan.keg_exists(creg_yr1_jan1_offset_rope)
    creg_offset_keg = sue_plan.get_keg_obj(creg_yr1_jan1_offset_rope)
    assert creg_offset_keg.addin == creg_config.get(kw.yr1_jan1_offset)


# def test_PlanUnit_get_keg_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_planunit = planunit_shop("Sue")
#     sue_planunit.set_time_creg_kegs(c400_number=7)

#     # WHEN THEN
#     time_rope = sue_planunit.make_l1_rope("time")
#     tech_rope = sue_planunit.make_rope(time_rope, "tech")
#     week_rope = sue_planunit.make_rope(tech_rope, "week")
#     assert len(sue_planunit.get_keg_ranged_kids(week_rope, begin=0, close=1440)) == 1
#     assert len(sue_planunit.get_keg_ranged_kids(week_rope, begin=0, close=2000)) == 2
#     assert len(sue_planunit.get_keg_ranged_kids(week_rope, begin=0, close=3000)) == 3


# def test_PlanUnit_get_keg_ranged_kids_ReturnsSomeChildrenScenario3():
#     # ESTABLISH
#     sue_planunit = planunit_shop("Sue")
#     sue_planunit.set_time_creg_kegs(c400_number=7)

#     # WHEN THEN
#     time_rope = sue_planunit.make_l1_rope("time")
#     tech_rope = sue_planunit.make_rope(time_rope, "tech")
#     week_rope = sue_planunit.make_rope(tech_rope, "week")
#     assert len(sue_planunit.get_keg_ranged_kids(keg_rope=week_rope, begin=0)) == 1
#     assert len(sue_planunit.get_keg_ranged_kids(keg_rope=week_rope, begin=1440)) == 1


def test_PlanUnit_get_agenda_dict_DoesNotReturnPledgeKegsOutsideRange():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_plan = add_time_creg_kegunit(planunit_shop(exx.sue))
    clean_rope = sue_plan.make_l1_rope(exx.clean)
    sue_plan.set_l1_keg(kegunit_shop(exx.clean, pledge=True))
    time_rope = sue_plan.make_l1_rope("time")
    cregtime_rope = sue_plan.make_rope(time_rope, kw.creg)
    day_rope = sue_plan.make_rope(cregtime_rope, "day")

    sue_plan.edit_keg_attr(
        clean_rope,
        reason_context=day_rope,
        reason_case=day_rope,
        reason_lower=320,
        reason_upper=480,
    )

    # WHEN
    x_fact_lower1 = 2063971110
    x_fact_upper1 = 2063971110
    sue_plan.add_fact(
        cregtime_rope,
        fact_state=cregtime_rope,
        fact_lower=x_fact_lower1,
        fact_upper=x_fact_upper1,
    )

    # THEN
    agenda_dict = sue_plan.get_agenda_dict()
    clean_keg = agenda_dict.get(clean_rope)
    day_factheir = clean_keg.factheirs.get(day_rope)
    day_reasonheir = clean_keg.reasonheirs.get(day_rope)
    day_heir_case = day_reasonheir.cases.get(day_rope)
    print(
        f"{day_factheir.fact_context=} {day_factheir.fact_lower} {day_factheir.fact_upper}"
    )
    print(f"{day_heir_case=}")
    assert len(agenda_dict) == 1
    assert clean_rope in agenda_dict.keys()

    # WHEN
    x_fact_lower2 = 500
    x_fact_upper2 = 500
    sue_plan.add_fact(
        cregtime_rope,
        fact_state=cregtime_rope,
        fact_lower=x_fact_lower2,
        fact_upper=x_fact_upper2,
    )
    # print(f"{sue_plan.kegroot.factunits=}")

    # THEN
    clean_keg = sue_plan.get_keg_obj(clean_rope)
    day_factheir = clean_keg.factheirs.get(day_rope)
    day_reasonheir = clean_keg.reasonheirs.get(day_rope)
    day_heir_case = day_reasonheir.cases.get(day_rope)
    print(
        f"{day_factheir.fact_context=} {day_factheir.fact_lower} {day_factheir.fact_upper}"
    )
    print(f"{day_heir_case=}")
    agenda2_dict = sue_plan.get_agenda_dict()
    assert len(agenda2_dict) == 0


def test_PlanUnit_create_agenda_keg_CreatesAllPlanAttributes():
    # WHEN "I am cleaning the cuisine since I'm in the flat and its 8am and its dirty and its for my family"

    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    assert len(sue_plan.persons) == 0
    assert len(sue_plan.get_personunit_group_titles_dict()) == 0

    clean_str = "cleanings"
    clean_rope = sue_plan.make_l1_rope(clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_plan.make_rope(clean_rope, sweep_str)
    sweep_keg = kegunit_shop(sweep_str, parent_rope=clean_rope)
    print(f"{sweep_keg.get_keg_rope()=}")
    house_str = "house"
    house_rope = sue_plan.make_l1_rope(house_str)
    cuisine_room_str = "cuisine room"
    cuisine_room_rope = sue_plan.make_rope(house_rope, cuisine_room_str)
    cuisine_dirty_str = "dirty"
    cuisine_dirty_rope = sue_plan.make_rope(cuisine_room_rope, cuisine_dirty_str)

    # create gregorian epoch
    add_time_creg_kegunit(sue_plan)
    time_rope = sue_plan.make_l1_rope("time")
    cregtime_rope = sue_plan.make_rope(time_rope, kw.creg)
    creg_keg = sue_plan.get_keg_obj(cregtime_rope)
    print(f"{creg_keg.kids.keys()=}")
    daytime_rope = sue_plan.make_rope(cregtime_rope, "day")
    reason_lower_8am = 480
    reason_upper_8am = 480

    dirty_cuisine_reason = reasonunit_shop(cuisine_room_rope)
    dirty_cuisine_reason.set_case(case=cuisine_dirty_rope)
    sweep_keg.set_reasonunit(reason=dirty_cuisine_reason)

    daytime_reason = reasonunit_shop(daytime_rope)
    daytime_reason.set_case(
        case=daytime_rope, reason_lower=reason_lower_8am, reason_upper=reason_upper_8am
    )
    sweep_keg.set_reasonunit(reason=daytime_reason)

    family_str = ",family"
    awardunit_z = awardunit_shop(awardee_title=family_str)
    sweep_keg.set_awardunit(awardunit_z)

    assert len(sue_plan.persons) == 0
    assert len(sue_plan.get_personunit_group_titles_dict()) == 0
    assert len(sue_plan.kegroot.kids) == 1
    assert sue_plan.get_keg_obj(daytime_rope).denom == 1440
    assert sue_plan.get_keg_obj(daytime_rope).morph
    print(f"{sweep_keg.get_keg_rope()=}")

    # ESTABLISH
    sue_plan.set_dominate_pledge_keg(keg_kid=sweep_keg)

    # THEN
    # for keg_kid in sue_plan.kegroot.kids.keys():
    #     print(f"  {keg_kid=}")

    print(f"{sweep_keg.get_keg_rope()=}")
    assert sue_plan.get_keg_obj(sweep_rope) is not None
    assert sue_plan.get_keg_obj(sweep_rope).keg_label == sweep_str
    assert sue_plan.get_keg_obj(sweep_rope).pledge
    assert len(sue_plan.get_keg_obj(sweep_rope).reasonunits) == 2
    assert sue_plan.get_keg_obj(clean_rope) is not None
    assert sue_plan.get_keg_obj(cuisine_room_rope) is not None
    assert sue_plan.get_keg_obj(cuisine_dirty_rope) is not None
    assert len(sue_plan.get_personunit_group_titles_dict()) == 0
    assert sue_plan.get_personunit_group_titles_dict().get(family_str) is None

    assert len(sue_plan.kegroot.kids) == 3


def test_KegCore_get_agenda_dict_ReturnsObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/pale/issues/69
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    add_time_creg_kegunit(sue_plan)

    casa_rope = sue_plan.make_l1_rope(exx.casa)
    laundry_str = "do_laundry"
    laundry_rope = sue_plan.make_rope(casa_rope, laundry_str)
    sue_plan.set_l1_keg(kegunit_shop(exx.casa))
    sue_plan.set_keg_obj(kegunit_shop(laundry_str, pledge=True), casa_rope)
    time_rope = sue_plan.make_l1_rope("time")
    cregtime_rope = sue_plan.make_rope(time_rope, kw.creg)
    sue_plan.edit_keg_attr(
        laundry_rope,
        reason_context=cregtime_rope,
        reason_case=cregtime_rope,
        reason_lower=3420.0,
        reason_upper=3420.0,
        reason_divisor=10080.0,
    )
    print("set first fact")

    sue_plan.add_fact(cregtime_rope, cregtime_rope, 1064131200, fact_upper=1064135133)
    print("get 1st agenda dictionary")
    sue_agenda_dict = sue_plan.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")
    assert sue_agenda_dict == {}

    laundry_keg = sue_plan.get_keg_obj(laundry_rope)
    laundry_reasonheir = laundry_keg.get_reasonheir(cregtime_rope)
    laundry_case = laundry_reasonheir.get_case(cregtime_rope)
    laundry_factheir = laundry_keg.factheirs.get(cregtime_rope)
    # print(
    #     f"{laundry_keg.keg_active=} {laundry_case.reason_lower=} {laundry_factheir.fact_lower % 10080=}"
    # )
    # print(
    #     f"{laundry_keg.keg_active=} {laundry_case.reason_upper=} {laundry_factheir.fact_upper % 10080=}"
    # )
    # print(f"{laundry_reasonheir.reason_context=} {laundry_case=}")
    # for x_kegunit in sue_plan._keg_dict.values():
    #     if x_kegunit.keg_label in [laundry_str]:
    #         print(f"{x_kegunit.keg_label=} {x_kegunit.begin=} {x_kegunit.close=}")
    #         print(f"{x_kegunit.kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_plan.add_fact(cregtime_rope, cregtime_rope, 1064131200, fact_upper=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_plan.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_keg = sue_plan.get_keg_obj(laundry_rope)
    laundry_reasonheir = laundry_keg.get_reasonheir(cregtime_rope)
    laundry_case = laundry_reasonheir.get_case(cregtime_rope)
    laundry_factheir = laundry_keg.factheirs.get(cregtime_rope)
    # print(
    #     f"{laundry_keg.keg_active=} {laundry_case.reason_lower=} {laundry_factheir.fact_lower % 10080=}"
    # )
    # print(
    #     f"{laundry_keg.keg_active=} {laundry_case.reason_upper=} {laundry_factheir.fact_upper % 10080=}"
    # )
    # for x_kegunit in sue_plan._keg_dict.values():
    #     if x_kegunit.keg_label in [laundry_str]:
    #         print(f"{x_kegunit.keg_label=} {x_kegunit.begin=} {x_kegunit.close=}")
    #         print(f"{x_kegunit.kids.keys()=}")
    #         creg_factheir = x_kegunit.factheirs.get(cregtime_rope)
    #         print(f"{creg_factheir.fact_lower % 10080=}")
    #         print(f"{creg_factheir.fact_upper % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


def test_add_time_five_kegunit_SetsAttr_Scenario0_AddsMultiple_epochs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_kegunit(sue_plan)
    sue_plan.cashout()
    time_rope = sue_plan.make_l1_rope(kw.time)
    creg_rope = sue_plan.make_rope(time_rope, kw.creg)
    five_rope = sue_plan.make_rope(time_rope, kw.five)
    creg_yr1_jan1_offset_rope = sue_plan.make_rope(creg_rope, kw.yr1_jan1_offset)
    five_yr1_jan1_offset_rope = sue_plan.make_rope(five_rope, kw.yr1_jan1_offset)
    creg_year_rope = get_year_rope(sue_plan, kw.creg)
    five_year_rope = get_year_rope(sue_plan, kw.five)
    print(f"{creg_year_rope=}")
    print(f"{five_year_rope=}")
    # print(f"{sue_plan._keg_dict.keys()=}")

    assert not sue_plan.keg_exists(five_year_rope)
    assert sue_plan.keg_exists(creg_year_rope)
    assert sue_plan.keg_exists(creg_yr1_jan1_offset_rope)
    creg_offset_keg = sue_plan.get_keg_obj(creg_yr1_jan1_offset_rope)
    assert creg_offset_keg.addin == get_creg_config().get(kw.yr1_jan1_offset)
    assert not sue_plan.keg_exists(five_yr1_jan1_offset_rope)

    # WHEN
    sue_plan = add_time_five_kegunit(sue_plan)

    # THEN
    assert sue_plan.keg_exists(five_year_rope)
    assert sue_plan.keg_exists(creg_year_rope)
    assert sue_plan.keg_exists(creg_yr1_jan1_offset_rope)
    assert sue_plan.keg_exists(five_yr1_jan1_offset_rope)
    five_offset_keg = sue_plan.get_keg_obj(five_yr1_jan1_offset_rope)
    assert five_offset_keg.addin == get_five_config().get(kw.yr1_jan1_offset)


def test_get_creg_min_from_dt_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_creg_min_from_dt(datetime(1938, 11, 10))
    assert get_creg_min_from_dt(datetime(1, 1, 1)) == 440640
    assert get_creg_min_from_dt(datetime(1, 1, 2)) == 440640 + 1440
    assert get_creg_min_from_dt(datetime(1938, 11, 10)) == 1019653920
    # assert g_lw.get_time_dt_from_min(
    #     min=g_lw.get_creg_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    # ) == datetime(2000, 1, 1, 0, 0)
    assert get_creg_min_from_dt(datetime(800, 1, 1, 0, 0)) == 420672960
    assert get_creg_min_from_dt(datetime(1200, 1, 1, 0, 0)) == 631052640
    assert get_creg_min_from_dt(datetime(1201, 3, 1, 0, 0)) == 631664640
    assert get_creg_min_from_dt(datetime(1201, 3, 1, 0, 20)) == 631664660

    x_minutes = 1063817280
    assert get_creg_min_from_dt(datetime(2022, 10, 29, 0, 0)) == x_minutes
    x_next_day = x_minutes + 1440
    assert get_creg_min_from_dt(datetime(2022, 10, 30, 0, 0)) == x_next_day


def test_get_epoch_min_from_dt_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_kegunit(sue_plan)
    sue_plan.cashout()
    x_datetime = datetime(2022, 10, 30, 0, 0)
    time_rope = sue_plan.make_l1_rope(kw.time)
    creg_rope = sue_plan.make_rope(time_rope, kw.creg)

    # WHEN
    creg_min = get_epoch_min_from_dt(sue_plan, creg_rope, x_datetime)

    # THEN
    print(f"                        {creg_min=}")
    print(f"{get_creg_min_from_dt(x_datetime)=}")
    assert creg_min == get_creg_min_from_dt(x_datetime)


def test_get_epoch_min_difference_ReturnsObj():
    # ESTABLISH
    creg_config = get_creg_config()
    five_config = get_five_config()

    # WHEN
    five_creg_diff = get_epoch_min_difference(five_config, creg_config)
    creg_five_diff = get_epoch_min_difference(creg_config, five_config)

    # THEN
    c400_len = get_c400_constants().c400_leap_length
    c400_8x = c400_len * 8
    assert creg_five_diff == -c400_8x
    assert five_creg_diff == c400_8x


def test_get_creg_min_from_dt_ReturnsObj_get_five_min_from_dt_ReturnsObj(
    graphics_bool,
):
    # ESTABLISH
    mar1_2000_datetime = datetime(2000, 3, 1)

    # WHEN
    creg_mar1_2000_len = get_creg_min_from_dt(mar1_2000_datetime)
    five_mar1_2000_len = get_five_min_from_dt(mar1_2000_datetime)

    # THEN
    creg_config = get_creg_config()
    five_config = get_five_config()
    five_creg_diff = get_epoch_min_difference(five_config, creg_config)
    c400_len = get_c400_constants().c400_leap_length
    assert creg_mar1_2000_len == c400_len * 5
    assert five_mar1_2000_len == c400_len * 13
    assert five_mar1_2000_len - creg_mar1_2000_len == c400_len * 8
    assert five_mar1_2000_len - creg_mar1_2000_len == five_creg_diff

    display_current_creg_five_min(graphics_bool)
