from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import reasonunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import (
    get_mop_with_reason_planunit_example1,
    get_planunit_with_4_levels,
)
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_get_relevant_ropes_EmptyRopeTermReturnsEmpty():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()

    # WHEN
    relevant_ropes = sue_plan._get_relevant_ropes({})

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 0
    assert relevant_ropes == set()


def test_PlanUnit_get_relevant_ropes_RootRopeTermReturnsOnlyItself():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_rope = sue_plan.kegroot.get_keg_rope()

    # WHEN
    root_dict = {root_rope: -1}
    relevant_ropes = sue_plan._get_relevant_ropes(root_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 1
    assert relevant_ropes == {root_rope}


def test_PlanUnit_get_relevant_ropes_SimpleReturnsOnlyAncestors():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_rope = sue_plan.kegroot.get_keg_rope()

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_plan.make_rope(wk_rope, sun_str)
    sun_dict = {sun_rope}
    relevant_ropes = sue_plan._get_relevant_ropes(sun_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert relevant_ropes == {root_rope, sun_rope, wk_rope}


def test_PlanUnit_get_relevant_ropes_ReturnsSimpleReasonUnitreason_context():
    # ESTABLISH
    sue_plan = planunit_shop(plan_name="Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_plan.make_rope(casa_rope, floor_str)
    floor_keg = kegunit_shop(floor_str)
    sue_plan.set_keg_obj(floor_keg, parent_rope=casa_rope)

    unim_str = "unimportant"
    unim_rope = sue_plan.make_l1_rope(unim_str)
    unim_keg = kegunit_shop(unim_str)
    sue_plan.set_keg_obj(unim_keg, parent_rope=sue_plan.kegroot.get_keg_rope())

    situation_str = "cleaniness situation"
    situation_rope = sue_plan.make_rope(casa_rope, situation_str)
    situation_keg = kegunit_shop(situation_str)
    sue_plan.set_keg_obj(situation_keg, parent_rope=casa_rope)
    floor_reason = reasonunit_shop(reason_context=situation_rope)
    floor_reason.set_case(case=situation_rope)
    sue_plan.edit_keg_attr(floor_rope, reason=floor_reason)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = sue_plan._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 4
    root_rope = sue_plan.kegroot.get_keg_rope()
    assert relevant_ropes == {root_rope, casa_rope, situation_rope, floor_rope}
    assert unim_rope not in relevant_ropes


def test_PlanUnit_get_relevant_ropes_ReturnsReasonUnitreason_contextAndDescendents():
    # ESTABLISH
    x_plan = get_mop_with_reason_planunit_example1()
    root_rope = x_plan.kegroot.get_keg_rope()
    casa_rope = x_plan.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = x_plan.make_rope(casa_rope, floor_str)

    unim_str = "unimportant"
    unim_rope = x_plan.make_l1_rope(unim_str)

    situation_str = "cleaniness situation"
    situation_rope = x_plan.make_rope(casa_rope, situation_str)

    clean_rope = x_plan.make_rope(situation_rope, exx.clean)

    very_much_str = "very_much"
    very_much_rope = x_plan.make_rope(clean_rope, very_much_str)

    moderately_str = "moderately"
    moderately_rope = x_plan.make_rope(clean_rope, moderately_str)

    dirty_str = "dirty"
    dirty_rope = x_plan.make_rope(situation_rope, dirty_str)

    # WHEN
    floor_dict = {floor_rope}
    relevant_ropes = x_plan._get_relevant_ropes(floor_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 8
    assert clean_rope in relevant_ropes
    assert dirty_rope in relevant_ropes
    assert moderately_rope in relevant_ropes
    assert very_much_rope in relevant_ropes
    assert relevant_ropes == {
        root_rope,
        casa_rope,
        situation_rope,
        floor_rope,
        clean_rope,
        dirty_rope,
        very_much_rope,
        moderately_rope,
    }
    assert unim_rope not in relevant_ropes


def test_PlanUnit_get_relevant_ropes_ReturnSimple():
    # ESTABLISH
    yao_plan = planunit_shop(plan_name=exx.yao)
    root_rope = yao_plan.kegroot.get_keg_rope()
    min_range_x_str = "a_minute_range"
    min_range_x_rope = yao_plan.make_l1_rope(min_range_x_str)
    min_range_keg = kegunit_shop(min_range_x_str, begin=0, close=2880)
    yao_plan.set_l1_keg(min_range_keg)

    jour_length_str = "jour_1ce"
    jour_length_rope = yao_plan.make_l1_rope(jour_length_str)
    jour_length_keg = kegunit_shop(jour_length_str, begin=0, close=1440)
    yao_plan.set_l1_keg(jour_length_keg)

    hr_length_str = "hr_length"
    hr_length_rope = yao_plan.make_l1_rope(hr_length_str)
    hr_length_keg = kegunit_shop(hr_length_str)
    yao_plan.set_l1_keg(hr_length_keg)

    min_jours_str = "jours in minute_range"
    min_jours_rope = yao_plan.make_rope(min_range_x_rope, min_jours_str)
    min_jours_keg = kegunit_shop(min_jours_str)
    yao_plan.set_keg_obj(min_jours_keg, parent_rope=min_range_x_rope)

    # WHEN
    print(f"{yao_plan._keg_dict.keys()}")
    ropes_dict = {min_jours_rope}
    relevant_ropes = yao_plan._get_relevant_ropes(ropes_dict)

    # THEN
    print(f"{relevant_ropes=}")
    assert len(relevant_ropes) == 3
    assert min_range_x_rope in relevant_ropes
    assert jour_length_rope not in relevant_ropes
    assert hr_length_rope not in relevant_ropes
    assert min_jours_rope in relevant_ropes
    assert root_rope in relevant_ropes
    # min_jours_keg = yao_plan.get_keg_obj(min_jours_rope)


def test_PlanUnit_get_inheritor_keg_list_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_planunit = planunit_shop("Yao")
    tech_rope = yao_planunit.make_l1_rope("tech")
    wk_rope = yao_planunit.make_rope(tech_rope, exx.wk)
    yao_planunit.set_keg_obj(kegunit_shop(exx.wk, begin=0, close=10800), tech_rope)
    mon_str = "Mon"
    mon_rope = yao_planunit.make_rope(wk_rope, mon_str)
    yao_planunit.set_keg_obj(kegunit_shop(mon_str), wk_rope)
    yao_planunit.cashout()

    # WHEN
    x_inheritor_keg_list = yao_planunit.get_inheritor_keg_list(wk_rope, mon_rope)

    # # THEN
    assert len(x_inheritor_keg_list) == 2
    wk_keg = yao_planunit.get_keg_obj(wk_rope)
    mon_keg = yao_planunit.get_keg_obj(mon_rope)
    assert x_inheritor_keg_list == [wk_keg, mon_keg]
