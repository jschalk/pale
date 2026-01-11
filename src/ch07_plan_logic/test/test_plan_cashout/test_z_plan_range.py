from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_get_keg_ranged_kids_ReturnsAllChildren():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    ziet_rope = yao_planunit.make_l1_rope("ziet")
    tech_rope = yao_planunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_planunit.make_rope(tech_rope, exx.wk)
    wk_keg = kegunit_shop(exx.wk, begin=0, close=10800)
    yao_planunit.set_keg_obj(wk_keg, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_keg = kegunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_keg = kegunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_keg = kegunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_keg = kegunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_keg = kegunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_keg = kegunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_keg = kegunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_planunit.set_keg_obj(mon_keg, wk_rope)
    yao_planunit.set_keg_obj(tue_keg, wk_rope)
    yao_planunit.set_keg_obj(wed_keg, wk_rope)
    yao_planunit.set_keg_obj(thu_keg, wk_rope)
    yao_planunit.set_keg_obj(fri_keg, wk_rope)
    yao_planunit.set_keg_obj(sat_keg, wk_rope)
    yao_planunit.set_keg_obj(sun_keg, wk_rope)
    yao_planunit.cashout()

    # WHEN
    ranged_kegs = yao_planunit.get_keg_ranged_kids(keg_rope=wk_rope)

    # # THEN
    assert len(ranged_kegs) == 7


def test_PlanUnit_get_keg_ranged_kids_ReturnsSomeChildrenScenario1():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    ziet_rope = yao_planunit.make_l1_rope("ziet")
    tech_rope = yao_planunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_planunit.make_rope(tech_rope, exx.wk)
    wk_keg = kegunit_shop(exx.wk, begin=0, close=10800)
    yao_planunit.set_keg_obj(wk_keg, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_keg = kegunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_keg = kegunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_keg = kegunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_keg = kegunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_keg = kegunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_keg = kegunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_keg = kegunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_planunit.set_keg_obj(mon_keg, wk_rope)
    yao_planunit.set_keg_obj(tue_keg, wk_rope)
    yao_planunit.set_keg_obj(wed_keg, wk_rope)
    yao_planunit.set_keg_obj(thu_keg, wk_rope)
    yao_planunit.set_keg_obj(fri_keg, wk_rope)
    yao_planunit.set_keg_obj(sat_keg, wk_rope)
    yao_planunit.set_keg_obj(sun_keg, wk_rope)
    yao_planunit.cashout()

    # WHEN
    x_begin = 1440
    x_close = 4 * 1440
    print(f"{x_begin=} {x_close=}")
    ranged_kegs = yao_planunit.get_keg_ranged_kids(wk_rope, x_begin, x_close)

    # THEN
    # for keg_x in wk_keg.kids.values():
    #     print(f"{keg_x.keg_label=} {keg_x.gogo_calc=} {keg_x.stop_calc=} ")
    # print("")
    # for keg_x in ranged_kegs.values():
    #     print(f"{keg_x.keg_label=} {keg_x.gogo_calc=} {keg_x.stop_calc=} ")
    assert len(ranged_kegs) == 3


def test_PlanUnit_get_keg_ranged_kids_ReturnsSomeChildrenScenario2():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    ziet_rope = yao_planunit.make_l1_rope("ziet")
    tech_rope = yao_planunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_planunit.make_rope(tech_rope, exx.wk)
    wk_keg = kegunit_shop(exx.wk, begin=0, close=10800)
    yao_planunit.set_keg_obj(wk_keg, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_keg = kegunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_keg = kegunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_keg = kegunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_keg = kegunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_keg = kegunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_keg = kegunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_keg = kegunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_planunit.set_keg_obj(mon_keg, wk_rope)
    yao_planunit.set_keg_obj(tue_keg, wk_rope)
    yao_planunit.set_keg_obj(wed_keg, wk_rope)
    yao_planunit.set_keg_obj(thu_keg, wk_rope)
    yao_planunit.set_keg_obj(fri_keg, wk_rope)
    yao_planunit.set_keg_obj(sat_keg, wk_rope)
    yao_planunit.set_keg_obj(sun_keg, wk_rope)
    yao_planunit.cashout()

    # WHEN / THEN
    assert len(yao_planunit.get_keg_ranged_kids(wk_rope, 0, 1440)) == 1
    assert len(yao_planunit.get_keg_ranged_kids(wk_rope, 0, 2000)) == 2
    assert len(yao_planunit.get_keg_ranged_kids(wk_rope, 0, 3000)) == 3


def test_PlanUnit_get_keg_ranged_kids_ReturnsSomeChildrenScenario3():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    ziet_rope = yao_planunit.make_l1_rope("ziet")
    tech_rope = yao_planunit.make_rope(ziet_rope, "tech")
    wk_rope = yao_planunit.make_rope(tech_rope, exx.wk)
    wk_keg = kegunit_shop(exx.wk, begin=0, close=10800)
    yao_planunit.set_keg_obj(wk_keg, tech_rope)
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sun_str = "Sun"
    mon_keg = kegunit_shop(mon_str, gogo_want=1440 * 0, stop_want=1440 * 1)
    tue_keg = kegunit_shop(tue_str, gogo_want=1440 * 1, stop_want=1440 * 2)
    wed_keg = kegunit_shop(exx.wed, gogo_want=1440 * 2, stop_want=1440 * 3)
    thu_keg = kegunit_shop(thu_str, gogo_want=1440 * 3, stop_want=1440 * 4)
    fri_keg = kegunit_shop(fri_str, gogo_want=1440 * 4, stop_want=1440 * 5)
    sat_keg = kegunit_shop(sat_str, gogo_want=1440 * 5, stop_want=1440 * 6)
    sun_keg = kegunit_shop(sun_str, gogo_want=1440 * 6, stop_want=1440 * 7)
    yao_planunit.set_keg_obj(mon_keg, wk_rope)
    yao_planunit.set_keg_obj(tue_keg, wk_rope)
    yao_planunit.set_keg_obj(wed_keg, wk_rope)
    yao_planunit.set_keg_obj(thu_keg, wk_rope)
    yao_planunit.set_keg_obj(fri_keg, wk_rope)
    yao_planunit.set_keg_obj(sat_keg, wk_rope)
    yao_planunit.set_keg_obj(sun_keg, wk_rope)
    yao_planunit.cashout()

    # WHEN / THEN
    assert len(yao_planunit.get_keg_ranged_kids(wk_rope, 0)) == 1
    assert len(yao_planunit.get_keg_ranged_kids(wk_rope, 1440)) == 1

    # ESTABLISH
    wks_keg = kegunit_shop(exx.wk, gogo_want=0, stop_want=1440 * 5)
    yao_planunit.set_keg_obj(wks_keg, wk_rope)

    # WHEN
    yao_planunit.cashout()

    # THEN
    assert len(yao_planunit.get_keg_ranged_kids(wk_rope, 1440)) == 2
