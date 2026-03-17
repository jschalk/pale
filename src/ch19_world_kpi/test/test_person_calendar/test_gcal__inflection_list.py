from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import PersonUnit, get_sorted_plan_list
from src.ch13_time.epoch_main import (
    get_day_rope,
    get_default_epoch_config_dict,
    get_epoch_min_from_dt,
    get_epoch_rope,
)
from src.ch13_time.epoch_reason import set_epoch_fact
from src.ch19_world_kpi._ref.ch19_semantic_types import LabelTerm, RopeTerm
from src.ch19_world_kpi.gcalendar import DayEvent, get_inflection_points
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_no_events_returns_empty():
    # ESTABLISH / WHEN / THEN
    assert get_inflection_points([]) == []


def test_get_inflection_points_ReturnsObj_Scenario0_single_event():
    # ESTABLISH
    x1_plan = planunit_shop(exx.mop, fund_ratio=0.1)
    dayevent = DayEvent(x1_plan, 1, "100%", 0, day_min_upper=60)

    # WHEN
    points = get_inflection_points([dayevent])

    # THEN
    assert points == [(0, dayevent), (60, None)]


def test_get_inflection_points_ReturnsObj_Scenario1_two_sequential_events_no_overlap():
    # ESTABLISH
    x1_plan = planunit_shop(exx.mop, fund_ratio=0.1)
    y2_dayevent = DayEvent(x1_plan, 1, "100%", 0, day_min_upper=30)
    y3_dayevent = DayEvent(x1_plan, 1, "100%", 60, day_min_upper=90)

    # WHEN
    points = get_inflection_points([y2_dayevent, y3_dayevent])

    # THEN
    assert points == [(0, y2_dayevent), (30, None), (60, y3_dayevent), (90, None)]


# TODO add more tests
# def test_higher_importance_event_interrupts():
#     low = CalendarEvent(importance_weight=1.0, start_time=0, end_time=60)
#     high = CalendarEvent(importance_weight=3.0, start_time=30, end_time=90)
#     points = get_inflection_points([low, high], timeline_end=90)
#     assert points == [(0, low), (30, high), (90, None)]


# def test_lower_importance_event_does_not_interrupt():
#     high = CalendarEvent(importance_weight=3.0, start_time=0, end_time=60)
#     low = CalendarEvent(importance_weight=1.0, start_time=30, end_time=90)
#     points = get_inflection_points([high, low], timeline_end=90)
#     assert points == [(0, high), (60, low), (90, None)]


# def test_gap_between_events_produces_none_inflection():
#     e1 = CalendarEvent(importance_weight=1.0, start_time=0, end_time=30)
#     e2 = CalendarEvent(importance_weight=1.0, start_time=60, end_time=90)
#     points = get_inflection_points([e1, e2], timeline_end=90)
#     gap_point = next(t for t, e in points if e is None and t == 30)
#     assert gap_point == 30


# def test_overlapping_same_importance_no_extra_inflection():
#     e1 = CalendarEvent(importance_weight=2.0, start_time=0, end_time=60)
#     e2 = CalendarEvent(importance_weight=2.0, start_time=30, end_time=90)
#     points = get_inflection_points([e1, e2], timeline_end=90)
#     times = [t for t, _ in points]
#     # should not produce an inflection at t=30 since importance didn't change
#     assert 30 not in times
