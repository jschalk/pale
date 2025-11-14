from sqlite3 import connect as sqlite3_connect
from src.ch06_plan.test._util.ch06_examples import get_range_attrs
from src.ch07_belief_logic.belief_tool import (
    belief_plan_factunit_exists,
    belief_plan_factunit_get_obj,
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reasonunit_get_obj,
    belief_planunit_get_obj,
)
from src.ch13_epoch.epoch_main import (
    DEFAULT_EPOCH_LENGTH,
    add_epoch_planunit,
    get_c400_constants,
)
from src.ch13_epoch.epoch_reason import set_epoch_cases_by_args_dict
from src.ch13_epoch.test._util.ch13_examples import (
    Ch13ExampleStrs as wx,
    get_bob_five_belief,
    get_lizzy9_config,
)
from src.ch15_nabu.nabu_config import get_nabu_config_dict
from src.ch17_idea.idea_config import get_dimens_with_idea_element
from src.ch18_world_etl.etl_cotonum import (
    add_epoch_frame_to_db_beliefunit,
    add_frame_to_db_beliefunit,
    add_frame_to_db_caseunit,
    add_frame_to_db_factunit,
    add_frame_to_db_reasonunit,
)
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    get_update_heard_agg_epochtime_sqlstr,
    get_update_heard_agg_epochtime_sqlstrs,
    update_heard_agg_epochtime_columns,
)
from src.ch18_world_etl.obj2db_belief import insert_h_agg_obj
from src.ch18_world_etl.test._util.ch18_examples import (
    insert_blfcase_special_h_agg as insert_blfcase,
    insert_mmtoffi_special_offi_time_otx as insert_offi_time_otx,
    insert_mmtunit_special_c400_number as insert_c400_number,
    insert_nabepoc_h_agg_otx_inx_time as insert_otx_inx_time,
    select_blfcase_special_h_agg as select_blfcase,
    select_mmtoffi_special_offi_time_inx as select_offi_time_inx,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

# TODO create function that updates all nabuable otx fields.
# identify the change
# update semantic_type: CotoNum belief_plan_reason_caseunit_h_agg_put reason_lower, reason_upper
# update semantic_type: CotoNum belief_plan_factunit_h_agg_put fact_lower, fact_upper


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario0_NoWrap_dayly():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     spark7 = 7
#     bob_belief = get_bob_five_belief()
#     print(f"{bob_belief.moment_label=}")
#     mop_dayly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.day_rope,
#         kw.reason_state: wx.day_rope,
#         kw.epoch_label: wx.five_str,
#         kw.dayly_lower_min: 600,
#         kw.dayly_duration_min: 90,
#     }
#     day_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.day_rope})
#     set_epoch_cases_by_args_dict(bob_belief, mop_dayly_args)
#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_heard_tables(cursor)
#         insert_h_agg_obj(cursor, bob_belief, spark7, exx.yao)
#         blfcase_objs = select_blfcase(
#             cursor, spark7, "YY", exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
#         )
#         print(f"{blfcase_objs=}")
#         assert blfcase_objs
#         x_epoch_frame_min = 100
#         blfcase_obj0 = blfcase_objs[0]
#         assert blfcase_obj0.reason_lower_otx == 600
#         assert not blfcase_obj0.reason_lower_inx
#         assert blfcase_obj0.reason_upper_otx == 690
#         assert not blfcase_obj0.reason_upper_inx

#         # WHEN
#         add_frame_to_db_caseunit(
#             cursor,
#             blfcase_obj0,
#             x_epoch_frame_min,
#             day_plan.close,
#             day_plan.denom,
#             day_plan.morph,
#         )

#         # THEN
#         after_blfcase_obj0 = select_blfcase(
#             cursor, spark7, "YY", exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
#         )[0]
#         assert after_blfcase_obj0.reason_lower_otx == 600
#         assert after_blfcase_obj0.reason_lower_inx == 600 + 100
#         assert after_blfcase_obj0.reason_upper_otx == 690
#         assert after_blfcase_obj0.reason_upper_inx == 690 + 100
#     assert 1 == 2


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario1_Wrap_dayly():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_dayly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.day_rope,
#         kw.reason_state: wx.day_rope,
#         kw.epoch_label: wx.five_str,
#         kw.dayly_lower_min: 600,
#         kw.dayly_duration_min: 90,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_dayly_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
#     day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
#     day_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.day_rope})
#     x_epoch_frame_min = 1000
#     assert day_case.reason_lower == 600
#     assert day_case.reason_upper == 690

#     # WHEN
#     add_frame_to_db_caseunit(
#         day_case, x_epoch_frame_min, day_plan.close, day_plan.denom, day_plan.morph
#     )

#     # THEN
#     assert day_case.reason_lower != 600
#     assert day_case.reason_upper != 690
#     assert day_case.reason_lower == (600 + x_epoch_frame_min) % day_case.reason_divisor
#     assert day_case.reason_upper == (690 + x_epoch_frame_min) % day_case.reason_divisor


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario3_adds_epoch_frame_NoWarp_xdays():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_days_lower_day = 3
#     mop_days_upper_day = 4
#     mop_every_xdays = 13
#     mop_xdays_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.days_rope,
#         kw.reason_state: wx.days_rope,
#         kw.epoch_label: wx.five_str,
#         kw.days_lower_day: mop_days_lower_day,
#         kw.days_upper_day: mop_days_upper_day,
#         kw.every_xdays: mop_every_xdays,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_xdays_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
#     days_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.days_rope})
#     days_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xdays_args)
#     x_epoch_frame_min = 5000
#     assert days_case.reason_lower == mop_days_lower_day
#     assert days_case.reason_upper == mop_days_upper_day

#     # WHEN
#     add_frame_to_db_caseunit(
#         days_case, x_epoch_frame_min, days_plan.close, days_plan.denom, days_plan.morph
#     )

#     # THEN
#     assert days_case.reason_lower != mop_days_lower_day
#     assert days_case.reason_upper != mop_days_upper_day
#     assert days_case.reason_lower == mop_days_lower_day + 3
#     assert days_case.reason_upper == mop_days_upper_day + 3


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario4_adds_epoch_frame_Wrap_xdays():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_days_lower_day = 3
#     mop_days_upper_day = 4
#     mop_every_xdays = 13
#     mop_xdays_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.days_rope,
#         kw.reason_state: wx.days_rope,
#         kw.epoch_label: wx.five_str,
#         kw.days_lower_day: mop_days_lower_day,
#         kw.days_upper_day: mop_days_upper_day,
#         kw.every_xdays: mop_every_xdays,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_xdays_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
#     days_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xdays_args)
#     days_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.days_rope})
#     x_epoch_frame_min = 50000
#     assert days_case.reason_lower == mop_days_lower_day
#     assert days_case.reason_upper == mop_days_upper_day

#     # WHEN
#     add_frame_to_db_caseunit(
#         days_case, x_epoch_frame_min, days_plan.close, days_plan.denom, days_plan.morph
#     )

#     # THEN
#     assert days_case.reason_lower != mop_days_lower_day
#     assert days_case.reason_upper != mop_days_upper_day
#     print(f"{x_epoch_frame_min//1440=}")
#     print(f"{mop_days_lower_day + (x_epoch_frame_min//1440)=}")
#     ex_lower = (mop_days_lower_day + (x_epoch_frame_min // 1440)) % mop_every_xdays
#     ex_upper = (mop_days_upper_day + (x_epoch_frame_min // 1440)) % mop_every_xdays
#     assert days_case.reason_lower == ex_lower
#     assert days_case.reason_upper == ex_upper


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario5_adds_epoch_frame_NoWrap_weekly():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_weekly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.week_rope,
#         kw.reason_state: wx.week_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weekly_lower_min: 600,
#         kw.weekly_duration_min: 90,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_weekly_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
#     week_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
#     week_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.week_rope})
#     x_epoch_frame_min = 100
#     assert week_case.reason_lower == 600
#     assert week_case.reason_upper == 690

#     # WHEN
#     add_frame_to_db_caseunit(
#         week_case, x_epoch_frame_min, week_plan.close, week_plan.denom, week_plan.morph
#     )

#     # THEN
#     assert week_case.reason_lower != 600
#     assert week_case.reason_upper != 690
#     assert week_case.reason_lower == 600 + 100
#     assert week_case.reason_upper == 690 + 100


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario6_adds_epoch_frame_Wrap_weekly():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_weekly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.week_rope,
#         kw.reason_state: wx.week_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weekly_lower_min: 600,
#         kw.weekly_duration_min: 90,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_weekly_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
#     week_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
#     week_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.week_rope})
#     x_epoch_frame_min = 10000
#     assert week_case.reason_lower == 600
#     assert week_case.reason_upper == 690

#     # WHEN
#     add_frame_to_db_caseunit(
#         week_case, x_epoch_frame_min, week_plan.close, week_plan.denom, week_plan.morph
#     )

#     # THEN
#     assert week_case.reason_lower != 600
#     assert week_case.reason_upper != 690
#     assert (
#         week_case.reason_lower == (600 + x_epoch_frame_min) % week_case.reason_divisor
#     )
#     assert (
#         week_case.reason_upper == (690 + x_epoch_frame_min) % week_case.reason_divisor
#     )


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario7_adds_epoch_frame_NoWrap_xweeks():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_weeks_lower_week = 3
#     mop_weeks_upper_week = 4
#     mop_every_xweeks = 13
#     mop_xweeks_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.weeks_rope,
#         kw.reason_state: wx.weeks_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weeks_lower_week: mop_weeks_lower_week,
#         kw.weeks_upper_week: mop_weeks_upper_week,
#         kw.every_xweeks: mop_every_xweeks,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_xweeks_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)
#     xweeks_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xweeks_args)
#     weeks_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.weeks_rope})
#     x_epoch_frame_min = 24000
#     assert xweeks_case.reason_lower == mop_weeks_lower_week
#     assert xweeks_case.reason_upper == mop_weeks_upper_week

#     # WHEN
#     add_frame_to_db_caseunit(
#         xweeks_case,
#         x_epoch_frame_min,
#         weeks_plan.close,
#         weeks_plan.denom,
#         weeks_plan.morph,
#     )

#     # THEN
#     assert xweeks_case.reason_lower != mop_weeks_lower_week
#     assert xweeks_case.reason_upper != mop_weeks_upper_week
#     assert xweeks_case.reason_lower == mop_weeks_lower_week + 3
#     assert xweeks_case.reason_upper == mop_weeks_upper_week + 3


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario8_adds_epoch_frame_Wraps_every_xweeks():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     mop_weeks_lower_week = 3
#     mop_weeks_upper_week = 4
#     mop_every_xweeks = 13
#     mop_xweeks_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.weeks_rope,
#         kw.reason_state: wx.weeks_rope,
#         kw.epoch_label: wx.five_str,
#         kw.weeks_lower_week: mop_weeks_lower_week,
#         kw.weeks_upper_week: mop_weeks_upper_week,
#         kw.every_xweeks: mop_every_xweeks,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_xweeks_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)
#     xweeks_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xweeks_args)
#     weeks_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.weeks_rope})
#     x_epoch_frame_min = 50000
#     assert xweeks_case.reason_lower == mop_weeks_lower_week
#     assert xweeks_case.reason_upper == mop_weeks_upper_week

#     # WHEN
#     add_frame_to_db_caseunit(
#         xweeks_case,
#         x_epoch_frame_min,
#         weeks_plan.close,
#         weeks_plan.denom,
#         weeks_plan.morph,
#     )

#     # THEN
#     assert xweeks_case.reason_lower != mop_weeks_lower_week
#     assert xweeks_case.reason_upper != mop_weeks_upper_week
#     print(f"{x_epoch_frame_min//7200=}")
#     print(f"{mop_weeks_lower_week + (x_epoch_frame_min//7200)=}")
#     ex_lower = (mop_weeks_lower_week + (x_epoch_frame_min // 7200)) % mop_every_xweeks
#     ex_upper = (mop_weeks_upper_week + (x_epoch_frame_min // 7200)) % mop_every_xweeks
#     assert xweeks_case.reason_lower == ex_lower
#     assert xweeks_case.reason_upper == ex_upper


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario9_adds_epoch_frame_NoWrap_monthday():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthday_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: geo_rope,
#         kw.reason_state: geo_rope,
#         kw.month_label: wx.Geo,
#         kw.year_monthday_lower: 5,
#         kw.year_monthday_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_monthday_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)
#     year_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.five_year_rope})
#     monthday_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_monthday_args)

#     print(f"{monthday_case.reason_divisor=}")
#     x_epoch_frame_min = 500
#     geo_5_EpochTime = 43200
#     geo_8_EpochTime = 47520
#     assert monthday_case.reason_lower == geo_5_EpochTime
#     assert monthday_case.reason_upper == geo_8_EpochTime

#     # WHEN
#     add_frame_to_db_caseunit(
#         monthday_case,
#         x_epoch_frame_min,
#         year_plan.close,
#         year_plan.denom,
#         year_plan.morph,
#     )

#     # THEN
#     assert monthday_case.reason_lower != geo_5_EpochTime
#     assert monthday_case.reason_upper != geo_8_EpochTime
#     assert monthday_case.reason_lower == geo_5_EpochTime + x_epoch_frame_min
#     assert monthday_case.reason_upper == geo_8_EpochTime + x_epoch_frame_min


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario10_adds_epoch_frame_Wraps_monthday():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthday_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: geo_rope,
#         kw.reason_state: geo_rope,
#         kw.month_label: wx.Geo,
#         kw.year_monthday_lower: 5,
#         kw.year_monthday_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_monthday_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)
#     monthday_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_monthday_args)
#     year_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.five_year_rope})
#     x_epoch_frame_min = 5000000
#     geo_5_EpochTime = 43200
#     geo_8_EpochTime = 47520
#     assert monthday_case.reason_lower == geo_5_EpochTime
#     assert monthday_case.reason_upper == geo_8_EpochTime

#     # WHEN
#     add_frame_to_db_caseunit(
#         monthday_case,
#         x_epoch_frame_min,
#         year_plan.close,
#         year_plan.denom,
#         year_plan.morph,
#     )

#     # THEN
#     assert monthday_case.reason_lower != geo_5_EpochTime
#     assert monthday_case.reason_upper != geo_8_EpochTime
#     print(f"{(geo_5_EpochTime + x_epoch_frame_min) % 525600=}")
#     print(f"{(geo_8_EpochTime + x_epoch_frame_min) % 525600=}")
#     assert monthday_case.reason_lower == (geo_5_EpochTime + x_epoch_frame_min) % 525600
#     assert monthday_case.reason_upper == (geo_8_EpochTime + x_epoch_frame_min) % 525600


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario11_adds_epoch_frame_NoWrap_monthly():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.monthly_monthday_lower: 5,
#         kw.monthly_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_monthly_args)
#     geo_month_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_year_rope,
#         kw.reason_state: geo_rope,
#     }
#     assert belief_plan_reason_caseunit_exists(bob_belief, geo_month_args)
#     geo_case = belief_plan_reason_caseunit_get_obj(bob_belief, geo_month_args)
#     year_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.five_year_rope})

#     print(f"{geo_case.reason_divisor=}")
#     x_epoch_frame_min = 500
#     geo_5_EpochTime = 43200
#     geo_8_EpochTime = 47520
#     assert geo_case.reason_lower == geo_5_EpochTime
#     assert geo_case.reason_upper == geo_8_EpochTime

#     # WHEN
#     add_frame_to_db_caseunit(
#         geo_case, x_epoch_frame_min, year_plan.close, year_plan.denom, year_plan.morph
#     )

#     # THEN
#     assert geo_case.reason_lower != geo_5_EpochTime
#     assert geo_case.reason_upper != geo_8_EpochTime
#     assert geo_case.reason_lower == geo_5_EpochTime + x_epoch_frame_min
#     assert geo_case.reason_upper == geo_8_EpochTime + x_epoch_frame_min


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario12_adds_epoch_frame_Wraps_monthly():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
#     mop_monthly_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.monthly_monthday_lower: 5,
#         kw.monthly_duration_days: 3,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_monthly_args)
#     geo_month_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_year_rope,
#         kw.reason_state: geo_rope,
#     }
#     assert belief_plan_reason_caseunit_exists(bob_belief, geo_month_args)
#     geo_case = belief_plan_reason_caseunit_get_obj(bob_belief, geo_month_args)
#     year_plan = belief_planunit_get_obj(bob_belief, {kw.plan_rope: wx.five_year_rope})
#     x_epoch_frame_min = 5000000
#     geo_5_EpochTime = 43200
#     geo_8_EpochTime = 47520
#     assert geo_case.reason_lower == geo_5_EpochTime
#     assert geo_case.reason_upper == geo_8_EpochTime

#     # WHEN
#     add_frame_to_db_caseunit(
#         geo_case, x_epoch_frame_min, year_plan.close, year_plan.denom, year_plan.morph
#     )

#     # THEN
#     assert geo_case.reason_lower != geo_5_EpochTime
#     assert geo_case.reason_upper != geo_8_EpochTime
#     print(f"{(geo_5_EpochTime + x_epoch_frame_min) % 525600=}")
#     print(f"{(geo_8_EpochTime + x_epoch_frame_min) % 525600=}")
#     assert geo_case.reason_lower == (geo_5_EpochTime + x_epoch_frame_min) % 525600
#     assert geo_case.reason_upper == (geo_8_EpochTime + x_epoch_frame_min) % 525600


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario13_adds_epoch_frame_NoWrap_range():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_range_args)
#     epoch_args = {kw.plan_rope: wx.five_rope}
#     epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
#     print(f"{get_range_attrs(epoch_plan)=}")
#     epoch_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)

#     x_epoch_frame_min = 500
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_db_caseunit(
#         epoch_case,
#         x_epoch_frame_min,
#         epoch_plan.close,
#         epoch_plan.denom,
#         epoch_plan.morph,
#     )

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min + x_epoch_frame_min
#     assert epoch_case.reason_upper == x_range_upper_min + x_epoch_frame_min


# def test_add_frame_to_db_caseunit_SetsAttr_Scenario14_adds_epoch_frame_Wraps_range():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_range_args)
#     epoch_args = {kw.plan_rope: wx.five_rope}
#     epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
#     print(f"{get_range_attrs(epoch_plan)=}")
#     epoch_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)

#     x_epoch_frame_min = epoch_plan.close + 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_db_caseunit(
#         epoch_case,
#         x_epoch_frame_min,
#         epoch_plan.close,
#         epoch_plan.denom,
#         epoch_plan.morph,
#     )

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_duration
#     print(
#         f"{x_range_lower_min + x_epoch_frame_min=} vs {epoch_plan.close} (epoch_length)"
#     )
#     expected_lower = (x_range_lower_min + x_epoch_frame_min) % epoch_plan.close
#     expected_upper = (x_range_upper_min + x_epoch_frame_min) % epoch_plan.close
#     assert epoch_case.reason_lower == expected_lower
#     assert epoch_case.reason_upper == expected_upper


# def test_add_frame_to_db_reasonunit_SetsAttr_Scenario0_AllCaseUnitsAre_epoch():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_range_args)
#     epoch_args = {kw.plan_rope: wx.five_rope}
#     five_reason = belief_plan_reasonunit_get_obj(bob_belief, mop_range_args)
#     epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
#     print(f"{get_range_attrs(epoch_plan)=}")
#     epoch_length = epoch_plan.close
#     epoch_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)

#     x_epoch_frame_min = epoch_length + 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_db_reasonunit(
#         five_reason,
#         x_epoch_frame_min,
#         epoch_plan.close,
#         epoch_plan.denom,
#         epoch_plan.morph,
#     )

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_duration
#     expected_lower = (x_range_lower_min + x_epoch_frame_min) % epoch_length
#     expected_upper = (x_range_upper_min + x_epoch_frame_min) % epoch_length
#     assert epoch_case.reason_lower == expected_lower
#     assert epoch_case.reason_upper == expected_upper


# def test_add_frame_to_db_factunit_SetsAttr_epoch_Scenario0_NoWrap():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_belief.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     epoch_args = {kw.plan_rope: wx.mop_rope, kw.plan_rope: wx.five_rope}
#     epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
#     assert belief_plan_factunit_exists(bob_belief, root_five_args)
#     root_five_fact = belief_plan_factunit_get_obj(bob_belief, root_five_args)
#     x_epoch_frame_min = 10005
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_db_factunit(root_five_fact, x_epoch_frame_min, epoch_plan.close)

#     # THEN
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     expected_lower = (x_lower_min + x_epoch_frame_min) % epoch_plan.close
#     expected_upper = (x_upper_min + x_epoch_frame_min) % epoch_plan.close
#     assert root_five_fact.fact_lower == expected_lower
#     assert root_five_fact.fact_upper == expected_upper


# def test_add_frame_to_db_factunit_SetsAttr_epoch_Scenario1_Wrap():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_belief.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     epoch_args = {kw.plan_rope: wx.mop_rope, kw.plan_rope: wx.five_rope}
#     epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
#     assert belief_plan_factunit_exists(bob_belief, root_five_args)
#     root_five_fact = belief_plan_factunit_get_obj(bob_belief, root_five_args)
#     x_epoch_frame_min = epoch_plan.close + 10010
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_db_factunit(root_five_fact, x_epoch_frame_min, epoch_plan.close)

#     # THEN
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     expected_lower = (x_lower_min + x_epoch_frame_min) % epoch_plan.close
#     expected_upper = (x_upper_min + x_epoch_frame_min) % epoch_plan.close
#     assert root_five_fact.fact_lower == expected_lower
#     assert root_five_fact.fact_upper == expected_upper


# def test_add_frame_to_db_beliefunit_SetsAttrs_Scenario0_OnlyEpochFactsAndReasons():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_belief.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     epoch_args = {kw.plan_rope: wx.mop_rope, kw.plan_rope: wx.five_rope}
#     epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
#     assert belief_plan_factunit_exists(bob_belief, root_five_args)
#     root_five_fact = belief_plan_factunit_get_obj(bob_belief, root_five_args)

#     five_reason = belief_plan_reasonunit_get_obj(bob_belief, mop_range_args)
#     epoch_length = epoch_plan.close
#     epoch_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)

#     x_epoch_frame_min = epoch_length + 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert epoch_case.reason_lower == x_range_lower_min
#     assert epoch_case.reason_upper == x_range_upper_min
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_db_beliefunit(bob_belief, x_epoch_frame_min)

#     # THEN
#     assert epoch_case.reason_lower != x_range_lower_min
#     assert epoch_case.reason_upper != x_range_upper_min
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min


# def test_add_frame_to_db_beliefunit_SetsAttrs_Scenario1_FilterFactsAndReasonsEdited():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     add_epoch_planunit(bob_belief, get_lizzy9_config())
#     lizzy9_str = get_lizzy9_config().get(kw.epoch_label)
#     time_rope = bob_belief.make_l1_rope("time")
#     lizzy9_rope = bob_belief.make_rope(time_rope, lizzy9_str)
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     mop_lizzy9_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: lizzy9_str,
#         kw.reason_context: lizzy9_rope,
#         kw.reason_state: lizzy9_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_five_args)
#     set_epoch_cases_by_args_dict(bob_belief, mop_lizzy9_args)
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_belief.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     bob_belief.add_fact(lizzy9_rope, lizzy9_rope, x_lower_min, x_upper_min)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     root_lizzy9_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: lizzy9_rope,
#     }
#     root_five_fact = belief_plan_factunit_get_obj(bob_belief, root_five_args)
#     root_lizzy9_fact = belief_plan_factunit_get_obj(bob_belief, root_lizzy9_args)
#     five_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_five_args)
#     lizzy9_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_lizzy9_args)

#     x_epoch_frame_min = 10005
#     assert five_case.reason_lower == x_range_lower_min
#     assert lizzy9_case.reason_lower == x_range_lower_min
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_lizzy9_fact.fact_lower == x_lower_min

#     # WHEN
#     add_frame_to_db_beliefunit(
#         bob_belief, x_epoch_frame_min, required_context_subrope=wx.five_rope
#     )

#     # THEN
#     assert lizzy9_case.reason_lower == x_range_lower_min
#     assert root_lizzy9_fact.fact_lower == x_lower_min
#     assert five_case.reason_lower != x_range_lower_min
#     assert root_five_fact.fact_lower != x_lower_min


# def test_add_frame_to_db_beliefunit_SetsAttrs_Scenario2_IgnoreNonRangeReasonsFacts():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     bob_belief.add_plan(wx.clean_rope)
#     bob_belief.edit_plan_attr(
#         wx.mop_rope, reason_context=wx.clean_rope, reason_case=wx.clean_rope
#     )
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     mop_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.clean_rope,
#         kw.reason_state: wx.clean_rope,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_belief.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     bob_belief.add_fact(wx.clean_rope, wx.clean_rope)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     root_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.clean_rope,
#     }
#     assert belief_plan_factunit_exists(bob_belief, root_five_args)
#     assert belief_plan_factunit_exists(bob_belief, root_clean_args)
#     root_five_fact = belief_plan_factunit_get_obj(bob_belief, root_five_args)
#     root_clean_fact = belief_plan_factunit_get_obj(bob_belief, root_clean_args)
#     five_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)
#     clean_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_clean_args)

#     x_epoch_frame_min = 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert five_case.reason_lower == x_range_lower_min
#     assert five_case.reason_upper == x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None

#     # WHEN
#     add_frame_to_db_beliefunit(bob_belief, x_epoch_frame_min)

#     # THEN
#     assert five_case.reason_lower != x_range_lower_min
#     assert five_case.reason_upper != x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None


# def test_add_epoch_frame_to_db_beliefunit_SetsAttrs_Scenario0_IgnoreNonRangeReasonsFacts():
#     # ESTABLISH
#     bob_belief = get_bob_five_belief()
#     bob_belief.add_plan(wx.clean_rope)
#     bob_belief.edit_plan_attr(
#         wx.mop_rope, reason_context=wx.clean_rope, reason_case=wx.clean_rope
#     )
#     x_range_lower_min = 7777
#     x_range_duration = 2000
#     mop_range_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.epoch_label: wx.five_str,
#         kw.reason_context: wx.five_rope,
#         kw.reason_state: wx.five_rope,
#         kw.range_lower_min: x_range_lower_min,
#         kw.range_duration: x_range_duration,
#     }
#     mop_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.reason_context: wx.clean_rope,
#         kw.reason_state: wx.clean_rope,
#     }
#     set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_belief.add_fact(wx.five_rope, wx.five_rope, x_lower_min, x_upper_min)
#     bob_belief.add_fact(wx.clean_rope, wx.clean_rope)
#     root_five_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.five_rope,
#     }
#     root_clean_args = {
#         kw.plan_rope: wx.mop_rope,
#         kw.plan_rope: bob_belief.planroot.get_plan_rope(),
#         kw.fact_context: wx.clean_rope,
#     }
#     assert belief_plan_factunit_exists(bob_belief, root_five_args)
#     assert belief_plan_factunit_exists(bob_belief, root_clean_args)
#     root_five_fact = belief_plan_factunit_get_obj(bob_belief, root_five_args)
#     root_clean_fact = belief_plan_factunit_get_obj(bob_belief, root_clean_args)
#     five_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)
#     clean_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_clean_args)

#     x_epoch_frame_min = 10005
#     x_range_upper_min = x_range_lower_min + x_range_duration
#     assert five_case.reason_lower == x_range_lower_min
#     assert five_case.reason_upper == x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower == x_lower_min
#     assert root_five_fact.fact_upper == x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None

#     # WHEN
#     add_epoch_frame_to_db_beliefunit(
#         x_belief=bob_belief, epoch_label=wx.five_str, epoch_frame_min=x_epoch_frame_min
#     )

#     # THEN
#     assert five_case.reason_lower != x_range_lower_min
#     assert five_case.reason_upper != x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_five_fact.fact_lower != x_lower_min
#     assert root_five_fact.fact_upper != x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None
