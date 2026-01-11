# from src.ch06_keg.test._util.ch06_examples import get_range_attrs
# from src.ch07_plan_logic.plan_main import planunit_shop
# from src.ch07_plan_logic.plan_tool import (
#     add_frame_to_planunit,
#     add_frame_to_caseunit,
#     add_frame_to_factunit,
#     add_frame_to_reasonunit,
#     plan_keg_factunit_exists,
#     plan_keg_factunit_get_obj,
#     plan_keg_reason_caseunit_exists,
#     plan_keg_reason_caseunit_get_obj,
#     plan_keg_reasonunit_get_obj,
#     plan_kegunit_get_obj,
# )

# # from src.ch07_plan_logic.test._util.ch07_examples import
# from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


# def test_add_frame_to_caseunit_SetsAttr_Scenario0_NoWrap_jourly():
#     # ESTABLISH
#     bob_plan = planunit_shop()
#     mop_rope = bob_plan.make_l1_rope(exx.mop)
#     bob_plan.add_keg(mop_rope, pledge=True)
#     zeit_rope = bob_plan.make_l1_rope("zeit")
#     jour_rope = bob_plan.make_rope(zeit_rope, "jour")
#     bob_plan.edit_keg_attr(zeit_rope, begin=0, begin=0, close=500400300)
#     bob_plan.edit_keg_attr(jour_rope, denom=1000)
#     mop_jourly_args = {
#         kw.keg_rope: mop_rope,
#         kw.reason_context: zeit_rope,
#         kw.reason_state: zeit_rope,
#         kw.jourly_lower_min: 600,
#         kw.jourly_length_min: 90,
#     }
#     _keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: })
#     set__cases_by_args_dict(bob_plan, mop_jourly_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_jourly_args)
#     jour_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_jourly_args)
#     x__frame_min = 100
#     assert jour_case.reason_lower == 600
#     assert jour_case.reason_upper == 690

#     # WHEN
#     add_frame_to_caseunit(
#         jour_case, x__frame_min, jour_keg.close, jour_keg.denom, jour_keg.morph
#     )

#     # THEN
#     assert jour_case.reason_lower != 600
#     assert jour_case.reason_upper != 690
#     assert jour_case.reason_lower == 600 + 100
#     assert jour_case.reason_upper == 690 + 100


# def test_add_frame_to_caseunit_SetsAttr_Scenario1_Wrap_jourly():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_jourly_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.jour_rope,
#         kw.reason_state: wx.jour_rope,
#         kw._label: wx.two_str,
#         kw.jourly_lower_min: 600,
#         kw.jourly_length_min: 90,
#     }
#     set__cases_by_args_dict(bob_plan, mop_jourly_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_jourly_args)
#     jour_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_jourly_args)
#     jour_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.jour_rope})
#     x__frame_min = 1000
#     assert jour_case.reason_lower == 600
#     assert jour_case.reason_upper == 690

#     # WHEN
#     add_frame_to_caseunit(
#         jour_case, x__frame_min, jour_keg.close, jour_keg.denom, jour_keg.morph
#     )

#     # THEN
#     assert jour_case.reason_lower != 600
#     assert jour_case.reason_upper != 690
#     assert jour_case.reason_lower == (600 + x__frame_min) % jour_case.reason_divisor
#     assert jour_case.reason_upper == (690 + x__frame_min) % jour_case.reason_divisor


# def test_add_frame_to_caseunit_SetsAttr_Scenario3_adds__frame_NoWarp_xjours():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_jours_lower_jour = 3
#     mop_jours_upper_jour = 4
#     mop_every_xjours = 13
#     mop_xjours_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.jours_rope,
#         kw.reason_state: wx.jours_rope,
#         kw._label: wx.two_str,
#         kw.jours_lower_jour: mop_jours_lower_jour,
#         kw.jours_upper_jour: mop_jours_upper_jour,
#         kw.every_xjours: mop_every_xjours,
#     }
#     set__cases_by_args_dict(bob_plan, mop_xjours_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_xjours_args)
#     jours_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.jours_rope})
#     jours_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_xjours_args)
#     x__frame_min = 5000
#     assert jours_case.reason_lower == mop_jours_lower_jour
#     assert jours_case.reason_upper == mop_jours_upper_jour

#     # WHEN
#     add_frame_to_caseunit(
#         jours_case, x__frame_min, jours_keg.close, jours_keg.denom, jours_keg.morph
#     )

#     # THEN
#     assert jours_case.reason_lower != mop_jours_lower_jour
#     assert jours_case.reason_upper != mop_jours_upper_jour
#     assert jours_case.reason_lower == mop_jours_lower_jour + 3
#     assert jours_case.reason_upper == mop_jours_upper_jour + 3


# def test_add_frame_to_caseunit_SetsAttr_Scenario4_adds__frame_Wrap_xjours():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_jours_lower_jour = 3
#     mop_jours_upper_jour = 4
#     mop_every_xjours = 13
#     mop_xjours_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.jours_rope,
#         kw.reason_state: wx.jours_rope,
#         kw._label: wx.two_str,
#         kw.jours_lower_jour: mop_jours_lower_jour,
#         kw.jours_upper_jour: mop_jours_upper_jour,
#         kw.every_xjours: mop_every_xjours,
#     }
#     set__cases_by_args_dict(bob_plan, mop_xjours_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_xjours_args)
#     jours_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_xjours_args)
#     jours_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.jours_rope})
#     x__frame_min = 50000
#     assert jours_case.reason_lower == mop_jours_lower_jour
#     assert jours_case.reason_upper == mop_jours_upper_jour

#     # WHEN
#     add_frame_to_caseunit(
#         jours_case, x__frame_min, jours_keg.close, jours_keg.denom, jours_keg.morph
#     )

#     # THEN
#     assert jours_case.reason_lower != mop_jours_lower_jour
#     assert jours_case.reason_upper != mop_jours_upper_jour
#     print(f"{x__frame_min//1440=}")
#     print(f"{mop_jours_lower_jour + (x__frame_min//1440)=}")
#     ex_lower = (mop_jours_lower_jour + (x__frame_min // 1440)) % mop_every_xjours
#     ex_upper = (mop_jours_upper_jour + (x__frame_min // 1440)) % mop_every_xjours
#     assert jours_case.reason_lower == ex_lower
#     assert jours_case.reason_upper == ex_upper


# def test_add_frame_to_caseunit_SetsAttr_Scenario5_adds__frame_NoWrap_wkly():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_wkly_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.wk_rope,
#         kw.reason_state: wx.wk_rope,
#         kw._label: wx.two_str,
#         kw.wkly_lower_min: 600,
#         kw.wkly_length_min: 90,
#     }
#     set__cases_by_args_dict(bob_plan, mop_wkly_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_wkly_args)
#     wk_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_wkly_args)
#     wk_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.wk_rope})
#     x__frame_min = 100
#     assert wk_case.reason_lower == 600
#     assert wk_case.reason_upper == 690

#     # WHEN
#     add_frame_to_caseunit(
#         wk_case, x__frame_min, wk_keg.close, wk_keg.denom, wk_keg.morph
#     )

#     # THEN
#     assert wk_case.reason_lower != 600
#     assert wk_case.reason_upper != 690
#     assert wk_case.reason_lower == 600 + 100
#     assert wk_case.reason_upper == 690 + 100


# def test_add_frame_to_caseunit_SetsAttr_Scenario6_adds__frame_Wrap_wkly():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_wkly_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.wk_rope,
#         kw.reason_state: wx.wk_rope,
#         kw._label: wx.two_str,
#         kw.wkly_lower_min: 600,
#         kw.wkly_length_min: 90,
#     }
#     set__cases_by_args_dict(bob_plan, mop_wkly_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_wkly_args)
#     wk_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_wkly_args)
#     wk_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.wk_rope})
#     x__frame_min = 10000
#     assert wk_case.reason_lower == 600
#     assert wk_case.reason_upper == 690

#     # WHEN
#     add_frame_to_caseunit(
#         wk_case, x__frame_min, wk_keg.close, wk_keg.denom, wk_keg.morph
#     )

#     # THEN
#     assert wk_case.reason_lower != 600
#     assert wk_case.reason_upper != 690
#     assert (
#         wk_case.reason_lower == (600 + x__frame_min) % wk_case.reason_divisor
#     )
#     assert (
#         wk_case.reason_upper == (690 + x__frame_min) % wk_case.reason_divisor
#     )


# def test_add_frame_to_caseunit_SetsAttr_Scenario7_adds__frame_NoWrap_xwks():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_wks_lower_wk = 3
#     mop_wks_upper_wk = 4
#     mop_every_xwks = 13
#     mop_xwks_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.wks_rope,
#         kw.reason_state: wx.wks_rope,
#         kw._label: wx.two_str,
#         kw.wks_lower_wk: mop_wks_lower_wk,
#         kw.wks_upper_wk: mop_wks_upper_wk,
#         kw.every_xwks: mop_every_xwks,
#     }
#     set__cases_by_args_dict(bob_plan, mop_xwks_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_xwks_args)
#     xwks_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_xwks_args)
#     wks_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.wks_rope})
#     x__frame_min = 24000
#     assert xwks_case.reason_lower == mop_wks_lower_wk
#     assert xwks_case.reason_upper == mop_wks_upper_wk

#     # WHEN
#     add_frame_to_caseunit(
#         xwks_case,
#         x__frame_min,
#         wks_keg.close,
#         wks_keg.denom,
#         wks_keg.morph,
#     )

#     # THEN
#     assert xwks_case.reason_lower != mop_wks_lower_wk
#     assert xwks_case.reason_upper != mop_wks_upper_wk
#     assert xwks_case.reason_lower == mop_wks_lower_wk + 3
#     assert xwks_case.reason_upper == mop_wks_upper_wk + 3


# def test_add_frame_to_caseunit_SetsAttr_Scenario8_adds__frame_Wraps_every_xwks():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     mop_wks_lower_wk = 3
#     mop_wks_upper_wk = 4
#     mop_every_xwks = 13
#     mop_xwks_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.wks_rope,
#         kw.reason_state: wx.wks_rope,
#         kw._label: wx.two_str,
#         kw.wks_lower_wk: mop_wks_lower_wk,
#         kw.wks_upper_wk: mop_wks_upper_wk,
#         kw.every_xwks: mop_every_xwks,
#     }
#     set__cases_by_args_dict(bob_plan, mop_xwks_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_xwks_args)
#     xwks_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_xwks_args)
#     wks_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.wks_rope})
#     x__frame_min = 50000
#     assert xwks_case.reason_lower == mop_wks_lower_wk
#     assert xwks_case.reason_upper == mop_wks_upper_wk

#     # WHEN
#     add_frame_to_caseunit(
#         xwks_case,
#         x__frame_min,
#         wks_keg.close,
#         wks_keg.denom,
#         wks_keg.morph,
#     )

#     # THEN
#     assert xwks_case.reason_lower != mop_wks_lower_wk
#     assert xwks_case.reason_upper != mop_wks_upper_wk
#     print(f"{x__frame_min//7200=}")
#     print(f"{mop_wks_lower_wk + (x__frame_min//7200)=}")
#     ex_lower = (mop_wks_lower_wk + (x__frame_min // 7200)) % mop_every_xwks
#     ex_upper = (mop_wks_upper_wk + (x__frame_min // 7200)) % mop_every_xwks
#     assert xwks_case.reason_lower == ex_lower
#     assert xwks_case.reason_upper == ex_upper


# def test_add_frame_to_caseunit_SetsAttr_Scenario9_adds__frame_NoWrap_mnthjour():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     geo_rope = bob_plan.make_rope(wx.two_yr_rope, wx.Geo)
#     mop_mnthjour_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: geo_rope,
#         kw.reason_state: geo_rope,
#         kw.mnth_label: wx.Geo,
#         kw.yr_mnthjour_lower: 5,
#         kw.yr_mnthjour_length_jours: 3,
#     }
#     set__cases_by_args_dict(bob_plan, mop_mnthjour_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_mnthjour_args)
#     yr_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.two_yr_rope})
#     mnthjour_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_mnthjour_args)

#     print(f"{mnthjour_case.reason_divisor=}")
#     x__frame_min = 500
#     geo_5_Zeit = 43200
#     geo_8_Zeit = 47520
#     assert mnthjour_case.reason_lower == geo_5_Zeit
#     assert mnthjour_case.reason_upper == geo_8_Zeit

#     # WHEN
#     add_frame_to_caseunit(
#         mnthjour_case,
#         x__frame_min,
#         yr_keg.close,
#         yr_keg.denom,
#         yr_keg.morph,
#     )

#     # THEN
#     assert mnthjour_case.reason_lower != geo_5_Zeit
#     assert mnthjour_case.reason_upper != geo_8_Zeit
#     assert mnthjour_case.reason_lower == geo_5_Zeit + x__frame_min
#     assert mnthjour_case.reason_upper == geo_8_Zeit + x__frame_min


# def test_add_frame_to_caseunit_SetsAttr_Scenario10_adds__frame_Wraps_mnthjour():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     geo_rope = bob_plan.make_rope(wx.two_yr_rope, wx.Geo)
#     mop_mnthjour_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: geo_rope,
#         kw.reason_state: geo_rope,
#         kw.mnth_label: wx.Geo,
#         kw.yr_mnthjour_lower: 5,
#         kw.yr_mnthjour_length_jours: 3,
#     }
#     set__cases_by_args_dict(bob_plan, mop_mnthjour_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_mnthjour_args)
#     mnthjour_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_mnthjour_args)
#     yr_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.two_yr_rope})
#     x__frame_min = 5000000
#     geo_5_Zeit = 43200
#     geo_8_Zeit = 47520
#     assert mnthjour_case.reason_lower == geo_5_Zeit
#     assert mnthjour_case.reason_upper == geo_8_Zeit

#     # WHEN
#     add_frame_to_caseunit(
#         mnthjour_case,
#         x__frame_min,
#         yr_keg.close,
#         yr_keg.denom,
#         yr_keg.morph,
#     )

#     # THEN
#     assert mnthjour_case.reason_lower != geo_5_Zeit
#     assert mnthjour_case.reason_upper != geo_8_Zeit
#     print(f"{(geo_5_Zeit + x__frame_min) % 525600=}")
#     print(f"{(geo_8_Zeit + x__frame_min) % 525600=}")
#     assert mnthjour_case.reason_lower == (geo_5_Zeit + x__frame_min) % 525600
#     assert mnthjour_case.reason_upper == (geo_8_Zeit + x__frame_min) % 525600


# def test_add_frame_to_caseunit_SetsAttr_Scenario11_adds__frame_NoWrap_mnthly():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     geo_rope = bob_plan.make_rope(wx.two_yr_rope, wx.Geo)
#     mop_mnthly_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.mnthly_mnthjour_lower: 5,
#         kw.mnthly_length_jours: 3,
#     }
#     set__cases_by_args_dict(bob_plan, mop_mnthly_args)
#     geo_mnth_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_yr_rope,
#         kw.reason_state: geo_rope,
#     }
#     assert plan_keg_reason_caseunit_exists(bob_plan, geo_mnth_args)
#     geo_case = plan_keg_reason_caseunit_get_obj(bob_plan, geo_mnth_args)
#     yr_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.two_yr_rope})

#     print(f"{geo_case.reason_divisor=}")
#     x__frame_min = 500
#     geo_5_Zeit = 43200
#     geo_8_Zeit = 47520
#     assert geo_case.reason_lower == geo_5_Zeit
#     assert geo_case.reason_upper == geo_8_Zeit

#     # WHEN
#     add_frame_to_caseunit(
#         geo_case, x__frame_min, yr_keg.close, yr_keg.denom, yr_keg.morph
#     )

#     # THEN
#     assert geo_case.reason_lower != geo_5_Zeit
#     assert geo_case.reason_upper != geo_8_Zeit
#     assert geo_case.reason_lower == geo_5_Zeit + x__frame_min
#     assert geo_case.reason_upper == geo_8_Zeit + x__frame_min


# def test_add_frame_to_caseunit_SetsAttr_Scenario12_adds__frame_Wraps_mnthly():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     geo_rope = bob_plan.make_rope(wx.two_yr_rope, wx.Geo)
#     mop_mnthly_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.mnthly_mnthjour_lower: 5,
#         kw.mnthly_length_jours: 3,
#     }
#     set__cases_by_args_dict(bob_plan, mop_mnthly_args)
#     geo_mnth_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_yr_rope,
#         kw.reason_state: geo_rope,
#     }
#     assert plan_keg_reason_caseunit_exists(bob_plan, geo_mnth_args)
#     geo_case = plan_keg_reason_caseunit_get_obj(bob_plan, geo_mnth_args)
#     yr_keg = plan_kegunit_get_obj(bob_plan, {kw.keg_rope: wx.two_yr_rope})
#     x__frame_min = 5000000
#     geo_5_Zeit = 43200
#     geo_8_Zeit = 47520
#     assert geo_case.reason_lower == geo_5_Zeit
#     assert geo_case.reason_upper == geo_8_Zeit

#     # WHEN
#     add_frame_to_caseunit(
#         geo_case, x__frame_min, yr_keg.close, yr_keg.denom, yr_keg.morph
#     )

#     # THEN
#     assert geo_case.reason_lower != geo_5_Zeit
#     assert geo_case.reason_upper != geo_8_Zeit
#     print(f"{(geo_5_Zeit + x__frame_min) % 525600=}")
#     print(f"{(geo_8_Zeit + x__frame_min) % 525600=}")
#     assert geo_case.reason_lower == (geo_5_Zeit + x__frame_min) % 525600
#     assert geo_case.reason_upper == (geo_8_Zeit + x__frame_min) % 525600


# def test_add_frame_to_caseunit_SetsAttr_Scenario13_adds__frame_NoWrap_range():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     x_rge_lower_min = 7777
#     x_range_width = 2000
#     mop_range_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_rope,
#         kw.reason_state: wx.two_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     set__cases_by_args_dict(bob_plan, mop_range_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_range_args)
#     _args = {kw.keg_rope: wx.two_rope}
#     _keg = plan_kegunit_get_obj(bob_plan, _args)
#     print(f"{get_range_attrs(_keg)=}")
#     _case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_range_args)

#     x__frame_min = 500
#     x_range_upper_min = x_rge_lower_min + x_range_width
#     assert _case.reason_lower == x_rge_lower_min
#     assert _case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_caseunit(
#         _case,
#         x__frame_min,
#         _keg.close,
#         _keg.denom,
#         _keg.morph,
#     )

#     # THEN
#     assert _case.reason_lower != x_rge_lower_min
#     assert _case.reason_upper != x_range_width
#     assert _case.reason_lower == x_rge_lower_min + x__frame_min
#     assert _case.reason_upper == x_range_upper_min + x__frame_min


# def test_add_frame_to_caseunit_SetsAttr_Scenario14_adds__frame_Wraps_range():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     x_rge_lower_min = 7777
#     x_range_width = 2000
#     mop_range_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_rope,
#         kw.reason_state: wx.two_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     set__cases_by_args_dict(bob_plan, mop_range_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_range_args)
#     _args = {kw.keg_rope: wx.two_rope}
#     _keg = plan_kegunit_get_obj(bob_plan, _args)
#     print(f"{get_range_attrs(_keg)=}")
#     _case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_range_args)

#     x__frame_min = _keg.close + 10005
#     x_range_upper_min = x_rge_lower_min + x_range_width
#     assert _case.reason_lower == x_rge_lower_min
#     assert _case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_caseunit(
#         _case,
#         x__frame_min,
#         _keg.close,
#         _keg.denom,
#         _keg.morph,
#     )

#     # THEN
#     assert _case.reason_lower != x_rge_lower_min
#     assert _case.reason_upper != x_range_width
#     print(
#         f"{x_rge_lower_min + x__frame_min=} vs {_keg.close} (_length)"
#     )
#     expected_lower = (x_rge_lower_min + x__frame_min) % _keg.close
#     expected_upper = (x_range_upper_min + x__frame_min) % _keg.close
#     assert _case.reason_lower == expected_lower
#     assert _case.reason_upper == expected_upper


# def test_add_frame_to_reasonunit_SetsAttr_Scenario0_AllCaseUnitsAre_():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     x_rge_lower_min = 7777
#     x_range_width = 2000
#     mop_range_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_rope,
#         kw.reason_state: wx.two_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     set__cases_by_args_dict(bob_plan, mop_range_args)
#     assert plan_keg_reason_caseunit_exists(bob_plan, mop_range_args)
#     _args = {kw.keg_rope: wx.two_rope}
#     two_reason = plan_keg_reasonunit_get_obj(bob_plan, mop_range_args)
#     _keg = plan_kegunit_get_obj(bob_plan, _args)
#     print(f"{get_range_attrs(_keg)=}")
#     _length = _keg.close
#     _case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_range_args)

#     x__frame_min = _length + 10005
#     x_range_upper_min = x_rge_lower_min + x_range_width
#     assert _case.reason_lower == x_rge_lower_min
#     assert _case.reason_upper == x_range_upper_min

#     # WHEN
#     add_frame_to_reasonunit(
#         two_reason,
#         x__frame_min,
#         _keg.close,
#         _keg.denom,
#         _keg.morph,
#     )

#     # THEN
#     assert _case.reason_lower != x_rge_lower_min
#     assert _case.reason_upper != x_range_width
#     expected_lower = (x_rge_lower_min + x__frame_min) % _length
#     expected_upper = (x_range_upper_min + x__frame_min) % _length
#     assert _case.reason_lower == expected_lower
#     assert _case.reason_upper == expected_upper


# def test_add_frame_to_factunit_SetsAttr__Scenario0_NoWrap():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_plan.add_fact(wx.two_rope, wx.two_rope, x_lower_min, x_upper_min)
#     root_two_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: wx.two_rope,
#     }
#     _args = {kw.keg_rope: wx.mop_rope, kw.keg_rope: wx.two_rope}
#     _keg = plan_kegunit_get_obj(bob_plan, _args)
#     assert plan_keg_factunit_exists(bob_plan, root_two_args)
#     root_two_fact = plan_keg_factunit_get_obj(bob_plan, root_two_args)
#     x__frame_min = 10005
#     assert root_two_fact.fact_lower == x_lower_min
#     assert root_two_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_factunit(root_two_fact, x__frame_min, _keg.close)

#     # THEN
#     assert root_two_fact.fact_lower != x_lower_min
#     assert root_two_fact.fact_upper != x_upper_min
#     expected_lower = (x_lower_min + x__frame_min) % _keg.close
#     expected_upper = (x_upper_min + x__frame_min) % _keg.close
#     assert root_two_fact.fact_lower == expected_lower
#     assert root_two_fact.fact_upper == expected_upper


# def test_add_frame_to_factunit_SetsAttr__Scenario1_Wrap():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_plan.add_fact(wx.two_rope, wx.two_rope, x_lower_min, x_upper_min)
#     root_two_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: wx.two_rope,
#     }
#     _args = {kw.keg_rope: wx.mop_rope, kw.keg_rope: wx.two_rope}
#     _keg = plan_kegunit_get_obj(bob_plan, _args)
#     assert plan_keg_factunit_exists(bob_plan, root_two_args)
#     root_two_fact = plan_keg_factunit_get_obj(bob_plan, root_two_args)
#     x__frame_min = _keg.close + 10010
#     assert root_two_fact.fact_lower == x_lower_min
#     assert root_two_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_factunit(root_two_fact, x__frame_min, _keg.close)

#     # THEN
#     assert root_two_fact.fact_lower != x_lower_min
#     assert root_two_fact.fact_upper != x_upper_min
#     expected_lower = (x_lower_min + x__frame_min) % _keg.close
#     expected_upper = (x_upper_min + x__frame_min) % _keg.close
#     assert root_two_fact.fact_lower == expected_lower
#     assert root_two_fact.fact_upper == expected_upper


# def test_add_frame_to_planunit_SetsAttrs_Scenario0_OnlyFactsAndReasons():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     x_rge_lower_min = 7777
#     x_range_width = 2000
#     mop_range_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_rope,
#         kw.reason_state: wx.two_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     set__cases_by_args_dict(bob_plan, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_plan.add_fact(wx.two_rope, wx.two_rope, x_lower_min, x_upper_min)
#     root_two_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: wx.two_rope,
#     }
#     _args = {kw.keg_rope: wx.mop_rope, kw.keg_rope: wx.two_rope}
#     _keg = plan_kegunit_get_obj(bob_plan, _args)
#     assert plan_keg_factunit_exists(bob_plan, root_two_args)
#     root_two_fact = plan_keg_factunit_get_obj(bob_plan, root_two_args)

#     two_reason = plan_keg_reasonunit_get_obj(bob_plan, mop_range_args)
#     _length = _keg.close
#     _case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_range_args)

#     x__frame_min = _length + 10005
#     x_range_upper_min = x_rge_lower_min + x_range_width
#     assert _case.reason_lower == x_rge_lower_min
#     assert _case.reason_upper == x_range_upper_min
#     assert root_two_fact.fact_lower == x_lower_min
#     assert root_two_fact.fact_upper == x_upper_min

#     # WHEN
#     add_frame_to_planunit(bob_plan, x__frame_min)

#     # THEN
#     assert _case.reason_lower != x_rge_lower_min
#     assert _case.reason_upper != x_range_upper_min
#     assert root_two_fact.fact_lower != x_lower_min
#     assert root_two_fact.fact_upper != x_upper_min


# def test_add_frame_to_planunit_SetsAttrs_Scenario1_FilterFactsAndReasonsEdited():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     add__kegunit(bob_plan, get_lizzy9_config())
#     lizzy9_str = get_lizzy9_config().get(kw._label)
#     zeit_rope = bob_plan.make_l1_rope("zeit")
#     lizzy9_rope = bob_plan.make_rope(zeit_rope, lizzy9_str)
#     x_rge_lower_min = 7777
#     x_range_width = 2000
#     mop_two_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_rope,
#         kw.reason_state: wx.two_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     mop_lizzy9_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: lizzy9_str,
#         kw.reason_context: lizzy9_rope,
#         kw.reason_state: lizzy9_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     set__cases_by_args_dict(bob_plan, mop_two_args)
#     set__cases_by_args_dict(bob_plan, mop_lizzy9_args)
#     x_lower_min = 7777
#     x_upper_min = 8000
#     bob_plan.add_fact(wx.two_rope, wx.two_rope, x_lower_min, x_upper_min)
#     bob_plan.add_fact(lizzy9_rope, lizzy9_rope, x_lower_min, x_upper_min)
#     root_two_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: wx.two_rope,
#     }
#     root_lizzy9_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: lizzy9_rope,
#     }
#     root_two_fact = plan_keg_factunit_get_obj(bob_plan, root_two_args)
#     root_lizzy9_fact = plan_keg_factunit_get_obj(bob_plan, root_lizzy9_args)
#     two_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_two_args)
#     lizzy9_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_lizzy9_args)

#     x__frame_min = 10005
#     assert two_case.reason_lower == x_rge_lower_min
#     assert lizzy9_case.reason_lower == x_rge_lower_min
#     assert root_two_fact.fact_lower == x_lower_min
#     assert root_lizzy9_fact.fact_lower == x_lower_min

#     # WHEN
#     add_frame_to_planunit(
#         bob_plan, x__frame_min, required_context_subrope=wx.two_rope
#     )

#     # THEN
#     assert lizzy9_case.reason_lower == x_rge_lower_min
#     assert root_lizzy9_fact.fact_lower == x_lower_min
#     assert two_case.reason_lower != x_rge_lower_min
#     assert root_two_fact.fact_lower != x_lower_min


# def test_add_frame_to_planunit_SetsAttrs_Scenario2_IgnoreNonRangeReasonsFacts():
#     # ESTABLISH
#     bob_plan = get_bob_two_plan()
#     bob_plan.add_keg(wx.clean_rope)
#     bob_plan.edit_keg_attr(
#         wx.mop_rope, reason_context=wx.clean_rope, reason_case=wx.clean_rope
#     )
#     x_rge_lower_min = 7777
#     x_range_width = 2000
#     mop_range_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw._label: wx.two_str,
#         kw.reason_context: wx.two_rope,
#         kw.reason_state: wx.two_rope,
#         kw.rge_lower_min: x_rge_lower_min,
#         kw.range_width: x_range_width,
#     }
#     mop_clean_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.reason_context: wx.clean_rope,
#         kw.reason_state: wx.clean_rope,
#     }
#     set__cases_by_args_dict(bob_plan, mop_range_args)
#     x_lower_min = 5555
#     x_upper_min = 8000
#     bob_plan.add_fact(wx.two_rope, wx.two_rope, x_lower_min, x_upper_min)
#     bob_plan.add_fact(wx.clean_rope, wx.clean_rope)
#     root_two_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: wx.two_rope,
#     }
#     root_clean_args = {
#         kw.keg_rope: wx.mop_rope,
#         kw.keg_rope: bob_plan.kegroot.get_keg_rope(),
#         kw.fact_context: wx.clean_rope,
#     }
#     assert plan_keg_factunit_exists(bob_plan, root_two_args)
#     assert plan_keg_factunit_exists(bob_plan, root_clean_args)
#     root_two_fact = plan_keg_factunit_get_obj(bob_plan, root_two_args)
#     root_clean_fact = plan_keg_factunit_get_obj(bob_plan, root_clean_args)
#     two_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_range_args)
#     clean_case = plan_keg_reason_caseunit_get_obj(bob_plan, mop_clean_args)

#     x__frame_min = 10005
#     x_range_upper_min = x_rge_lower_min + x_range_width
#     assert two_case.reason_lower == x_rge_lower_min
#     assert two_case.reason_upper == x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_two_fact.fact_lower == x_lower_min
#     assert root_two_fact.fact_upper == x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None

#     # WHEN
#     add_frame_to_planunit(bob_plan, x__frame_min)

#     # THEN
#     assert two_case.reason_lower != x_rge_lower_min
#     assert two_case.reason_upper != x_range_upper_min
#     assert clean_case.reason_lower is None
#     assert clean_case.reason_upper is None
#     assert root_two_fact.fact_lower != x_lower_min
#     assert root_two_fact.fact_upper != x_upper_min
#     assert root_clean_fact.fact_lower is None
#     assert root_clean_fact.fact_upper is None
