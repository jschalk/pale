from src.ch01_allot.allot import default_pool_num
from src.ch04_rope.rope import to_rope
from src.ch05_reason.reason_main import caseunit_shop, reasonheir_shop, reasonunit_shop
from src.ch06_keg.healer import healerunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_graphic import display_kegtree
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.test._util.ch07_examples import (
    from_list_get_active,
    get_planunit_with7am_clean_table_reason,
    get_planunit_with_4_levels_and_2reasons,
    planunit_v001,
)
from src.ref.keywords import ExampleStrs as exx


def test_PlanUnit_cashout_Sets_active_WhenFactSaysNo():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_planunit.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_planunit.make_rope(wk_rope, sun_str)

    # for keg in sue_planunit._keg_dict.values():
    #     print(f"{casa_rope=} {keg.get_keg_rope()=}")
    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    assert sue_planunit.get_keg_obj(casa_rope).keg_active is None

    # WHEN
    sue_planunit.add_fact(fact_context=wk_rope, fact_state=sun_rope)
    sue_planunit.cashout()

    # THEN
    assert sue_planunit._keg_dict != {}
    assert len(sue_planunit._keg_dict) == 17
    # for keg in sue_planunit._keg_dict.values():
    #     print(f"{casa_rope=} {keg.get_keg_rope()=}")
    assert sue_planunit.get_keg_obj(casa_rope).keg_active is False


def test_PlanUnit_cashout_Sets_active_WhenFactModifies():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_planunit.make_l1_rope(wk_str)
    sun_str = "Wed"
    sun_rope = sue_planunit.make_rope(wk_rope, sun_str)
    casa_rope = sue_planunit.make_l1_rope(exx.casa)

    # WHEN
    sue_planunit.add_fact(fact_context=wk_rope, fact_state=sun_rope)

    # THEN
    sue_planunit.cashout()
    assert sue_planunit._keg_dict
    assert len(sue_planunit._keg_dict) == 17
    assert sue_planunit._keg_dict.get(casa_rope).keg_active is False

    # WHEN
    nation_str = "nation"
    nation_rope = sue_planunit.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_planunit.make_rope(nation_rope, usa_str)
    sue_planunit.add_fact(fact_context=nation_rope, fact_state=usa_rope)

    # THEN
    sue_planunit.cashout()
    assert sue_planunit._keg_dict
    assert len(sue_planunit._keg_dict) == 17
    assert sue_planunit._keg_dict.get(casa_rope).keg_active

    # WHEN
    france_str = "France"
    france_rope = sue_planunit.make_rope(nation_rope, france_str)
    sue_planunit.add_fact(fact_context=nation_rope, fact_state=france_rope)

    # THEN
    sue_planunit.cashout()
    assert sue_planunit._keg_dict
    assert len(sue_planunit._keg_dict) == 17
    assert sue_planunit._keg_dict.get(casa_rope).keg_active is False


def test_PlanUnit_cashout_Sets_keg_dict():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_planunit.make_l1_rope(wk_str)
    wed_rope = sue_planunit.make_rope(wk_rope, exx.wed)
    nation_str = "nation"
    nation_rope = sue_planunit.make_l1_rope(nation_str)
    france_str = "France"
    france_rope = sue_planunit.make_rope(nation_rope, france_str)
    sue_planunit.add_fact(fact_context=wk_rope, fact_state=wed_rope)
    sue_planunit.add_fact(fact_context=nation_rope, fact_state=france_rope)

    casa_rope = sue_planunit.make_l1_rope(exx.casa)
    casa_keg = sue_planunit.get_keg_obj(casa_rope)
    print(f"{sue_planunit.plan_name=} {len(casa_keg.reasonunits)=}")
    # print(f"{casa_keg.reasonunits=}")
    print(f"{sue_planunit.plan_name=} {len(sue_planunit.kegroot.factunits)=}")
    # print(f"{sue_planunit.kegroot.factunits=}")

    sue_planunit.cashout()
    assert sue_planunit._keg_dict
    assert len(sue_planunit._keg_dict) == 17

    usa_str = "USA"
    usa_rope = sue_planunit.make_rope(nation_rope, usa_str)
    oregon_str = "Oregon"
    oregon_rope = sue_planunit.make_rope(usa_rope, oregon_str)

    wed = caseunit_shop(reason_state=wed_rope)
    wed.case_active = True
    wed.task = False
    usa = caseunit_shop(reason_state=usa_rope)
    usa.case_active = True
    usa.task = False

    wed_lu = reasonunit_shop(wk_rope, cases={wed.reason_state: wed})
    sta_lu = reasonunit_shop(nation_rope, cases={usa.reason_state: usa})
    wed_lh = reasonheir_shop(
        reason_context=wk_rope,
        cases={wed.reason_state: wed},
        reason_active=True,
        task=False,
        parent_heir_active=True,
    )
    sta_lh = reasonheir_shop(
        reason_context=nation_rope,
        cases={usa.reason_state: usa},
        reason_active=True,
        task=False,
        parent_heir_active=True,
    )

    x1_reasonunits = {
        wed_lu.reason_context: wed_lu,
        sta_lu.reason_context: sta_lu,
    }
    x1_reasonheirs = {
        wed_lh.reason_context: wed_lh,
        sta_lh.reason_context: sta_lh,
    }

    # WHEN
    sue_planunit.add_fact(fact_context=nation_rope, fact_state=oregon_rope)
    sue_planunit.cashout()

    # THEN
    casa_keg = sue_planunit._keg_dict.get(casa_rope)
    print(f"\nlook at {casa_keg.get_keg_rope()=}")
    assert casa_keg.parent_rope == sue_planunit.kegroot.get_keg_rope()
    assert casa_keg.kids == {}
    assert casa_keg.star == 30
    assert casa_keg.keg_label == exx.casa
    assert casa_keg.tree_level == 1
    assert casa_keg.keg_active
    assert casa_keg.pledge
    # print(f"{casa_keg.reasonheirs=}")
    nation_reasonheir = casa_keg.reasonheirs[nation_rope]
    print(f"  {nation_reasonheir=}")
    print(f"  {nation_reasonheir.reason_active=}\n")
    # assert casa_keg.reasonheirs == x1_reasonheirs

    assert len(casa_keg.reasonheirs) == len(x1_reasonheirs)
    wk_reasonheir = casa_keg.reasonheirs.get(wk_rope)
    # usa_case = wk_reasonheir.cases.get(usa_rope)
    print(f"    {casa_keg.keg_label=}")
    # print(f"    {usa_case.reason_context=}")
    # print(f"    {usa_case.task=}")
    # print(f"    {usa_case.task=}")
    assert wk_reasonheir.task is False
    # print(f"      cases: {w=}")
    # w_state = usa_case.cases[wed_rope].reason_state
    # print(f"      {w_state=}")
    # assert usa_case.task == w_state.task
    # assert usa_case.case_active == w_state.reason_active
    # assert wk_reasonheir.cases == wk_reasonheir.cases

    # assert casa_keg.reasonunits == x1_reasonunits

    # print("iterate through every keg...")
    # for x_keg in keg_dict:
    #     if str(type(x_keg)).find(".keg.KegUnit'>") > 0:
    #         assert x_keg.keg_active is not None

    #     # print("")
    #     # print(f"{x_keg.keg_label=}")
    #     # print(f"{len(x_keg.reasonunits)=}")
    #     print(
    #         f"  {x_keg.keg_label} iterate through every reasonheir... {len(x_keg.reasonheirs)=} {x_keg.keg_label=}"
    #     )
    #     # print(f"{x_keg.reasonheirs=}")
    #     for reason in x_keg.reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.reason_context=}")
    #         assert reason.reason_active is not None
    #         for case_x in reason.cases.values():
    #             assert case_x.reason_active is not None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.cases, type_str="src.s2_planunit.reason.CaseUnit"
    #         )


# def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
#     bool_x = True
#     for x_value in x_dict.values():
#         if type_str not in str(type(x_value)):
#             bool_x = False
#         print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
#     return bool_x


def test_PlanUnit_cashout_CalculatesRangeAttributes():
    # ESTABLISH
    sue_planunit = get_planunit_with7am_clean_table_reason()
    sue_planunit.cashout()
    house_str = "houseadministration"
    house_rope = sue_planunit.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_planunit.make_rope(house_rope, clean_str)
    assert sue_planunit._keg_dict.get(clean_rope).keg_active is False

    # set facts as midevening to 8am
    ziet_str = "ziettech"
    ziet_rope = sue_planunit.make_l1_rope(ziet_str)
    x24hr_str = "24hr"
    x24hr_rope = sue_planunit.make_rope(ziet_rope, x24hr_str)
    x24hr_reason_context = x24hr_rope
    x24hr_fact_state = x24hr_rope
    x24hr_reason_lower = 0.0
    x24hr_reason_upper = 8.0

    # WHEN
    sue_planunit.add_fact(
        x24hr_reason_context,
        fact_state=x24hr_fact_state,
        fact_lower=x24hr_reason_lower,
        fact_upper=x24hr_reason_upper,
    )

    # THEN
    sue_planunit.cashout()
    assert sue_planunit._keg_dict.get(clean_rope).keg_active

    # WHEN
    # set facts as 8am to 10am
    x24hr_reason_lower = 8.0
    x24hr_reason_upper = 10.0
    print(sue_planunit.kegroot.factunits[x24hr_rope])
    sue_planunit.add_fact(
        x24hr_reason_context,
        fact_state=x24hr_fact_state,
        fact_lower=x24hr_reason_lower,
        fact_upper=x24hr_reason_upper,
    )
    print(sue_planunit.kegroot.factunits[x24hr_rope])
    print(sue_planunit.kegroot.kids[house_str].kids[clean_str].reasonunits)
    # sue_planunit.kegroot.kids["houseadministration"].kids[clean_str].keg_active = None

    # THEN
    sue_planunit.cashout()
    assert sue_planunit._keg_dict.get(clean_rope).keg_active is False


def test_PlanUnit_get_agenda_dict_ReturnsObj_WithSinglePledge():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()

    # WHEN
    pledge_kegs = sue_planunit.get_agenda_dict()

    # THEN
    assert pledge_kegs is not None
    assert len(pledge_kegs) > 0
    assert len(pledge_kegs) == 1


def test_PlanUnit_cashout_SetsData_planunit_v001():
    # ESTABLISH
    yao_planunit = planunit_v001()
    print(f"{yao_planunit.get_reason_contexts()=}")
    jour_min_str = "jour_minute"
    jour_min_rope = yao_planunit.make_l1_rope(jour_min_str)
    yao_planunit.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=1439,
    )

    mood_str = "Moods"
    mood_rope = yao_planunit.make_l1_rope(mood_str)
    yao_planunit.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    print(f"{yao_planunit.get_reason_contexts()=}")

    yr_mon_str = "yr_month"
    yr_mon_rope = yao_planunit.make_l1_rope(yr_mon_str)
    yao_planunit.add_fact(fact_context=yr_mon_rope, fact_state=yr_mon_rope)
    websites_str = "Websites"
    web_rope = yao_planunit.make_l1_rope(websites_str)
    yao_planunit.add_fact(fact_context=web_rope, fact_state=web_rope)
    assert yao_planunit is not None
    # print(f"{yao_planunit.plan_name=}")
    # print(f"{len(yao_planunit.kegroot.kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_rope = yao_planunit.make_l1_rope(ulty_str)

    # if yao_planunit.kegroot.kids["Ultimate Frisbee"].keg_label == "Ultimate Frisbee":
    assert yao_planunit.kegroot.kids[ulty_str].reasonunits is not None
    assert yao_planunit.plan_name is not None

    # for fact in yao_planunit.kegroot.factunits.values():
    #     print(f"{fact=}")

    # WHEN
    yao_planunit.cashout()

    # THEN
    # print(f"{str(type(keg))=}")
    # print(f"{len(keg_dict)=}")
    laundry_str = "laundry mon"
    casa_rope = yao_planunit.make_l1_rope("casa")
    cleaning_rope = yao_planunit.make_rope(casa_rope, "cleaning")
    laundry_rope = yao_planunit.make_rope(cleaning_rope, laundry_str)

    # for keg in keg_dict:
    #     assert (
    #         str(type(keg)).find(".keg.KegUnit'>") > 0
    #         or str(type(keg)).find(".keg.KegUnit'>") > 0
    #     )
    #     # print(f"{keg.keg_label=}")
    #     if keg.keg_label == laundry_str:
    #         for reason in keg.reasonunits.values():
    #             print(f"{keg.keg_label=} {reason.reason_context=}")  # {reason.cases=}")
    # assert keg.keg_active is False
    assert yao_planunit._keg_dict.get(laundry_rope).keg_active is False

    # WHEN
    wk_str = "sem_jours"
    wk_rope = yao_planunit.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = yao_planunit.make_rope(wk_rope, mon_str)
    yao_planunit.add_fact(fact_context=wk_rope, fact_state=mon_rope)
    yao_planunit.cashout()

    # THEN
    assert yao_planunit._keg_dict.get(laundry_rope).keg_active is False


def test_PlanUnit_cashout_OptionWeekJoursReturnsObj_planunit_v001():
    # ESTABLISH
    yao_planunit = planunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_planunit.make_l1_rope(hr_number_str)
    yao_planunit.add_fact(
        fact_context=hr_number_rope,
        fact_state=hr_number_rope,
        fact_lower=0,
        fact_upper=23,
    )
    jour_min_str = "jour_minute"
    jour_min_rope = yao_planunit.make_l1_rope(jour_min_str)
    yao_planunit.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=59,
    )
    mon_wk_str = "month_wk"
    mon_wk_rope = yao_planunit.make_l1_rope(mon_wk_str)
    yao_planunit.add_fact(fact_context=mon_wk_rope, fact_state=mon_wk_rope)
    nation_str = "Nation-States"
    nation_rope = yao_planunit.make_l1_rope(nation_str)
    yao_planunit.add_fact(fact_context=nation_rope, fact_state=nation_rope)
    mood_str = "Moods"
    mood_rope = yao_planunit.make_l1_rope(mood_str)
    yao_planunit.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_planunit.make_l1_rope(aaron_str)
    yao_planunit.add_fact(fact_context=aaron_rope, fact_state=aaron_rope)
    websites_str = "Websites"
    web_rope = yao_planunit.make_l1_rope(websites_str)
    yao_planunit.add_fact(fact_context=web_rope, fact_state=web_rope)
    yr_mon_str = "yr_month"
    yr_mon_rope = yao_planunit.make_l1_rope(yr_mon_str)
    yao_planunit.add_fact(
        fact_context=yr_mon_rope, fact_state=yr_mon_rope, fact_lower=0, fact_upper=1000
    )

    yao_planunit.cashout()
    missing_facts = yao_planunit.get_missing_fact_reason_contexts()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    wk_str = "sem_jours"
    wk_rope = yao_planunit.make_l1_rope(wk_str)
    mon_str = "Mon"
    mon_rope = yao_planunit.make_rope(wk_rope, mon_str)
    tue_str = "Tue"
    tue_rope = yao_planunit.make_rope(wk_rope, tue_str)
    mon_case_x = caseunit_shop(reason_state=mon_rope)
    mon_case_x.case_active = False
    mon_case_x.task = False
    tue_case_x = caseunit_shop(reason_state=tue_rope)
    tue_case_x.case_active = False
    tue_case_x.task = False
    mt_cases = {
        mon_case_x.reason_state: mon_case_x,
        tue_case_x.reason_state: tue_case_x,
    }
    mt_reasonunit = reasonunit_shop(wk_rope, cases=mt_cases)
    mt_reasonheir = reasonheir_shop(wk_rope, cases=mt_cases, reason_active=False)
    x_kegroot = yao_planunit.kegroot
    x_kegroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_planunit.reasonunits[wk_rope].reason_context=}")
    # print(f"{yao_planunit.reasonunits[wk_rope].cases[mon_rope].reason_state=}")
    # print(f"{yao_planunit.reasonunits[wk_rope].cases[tue_rope].reason_state=}")
    wk_reasonunit = x_kegroot.reasonunits[wk_rope]
    print(f"{wk_reasonunit.cases=}")
    case_mon = wk_reasonunit.cases.get(mon_rope)
    case_tue = wk_reasonunit.cases.get(tue_rope)
    assert case_mon
    assert case_mon == mt_reasonunit.cases[case_mon.reason_state]
    assert case_tue
    assert case_tue == mt_reasonunit.cases[case_tue.reason_state]
    assert wk_reasonunit == mt_reasonunit

    # WHEN
    keg_dict = yao_planunit.get_keg_dict()

    # THEN
    gen_wk_reasonheir = x_kegroot.get_reasonheir(wk_rope)
    gen_mon_case = gen_wk_reasonheir.cases.get(mon_rope)
    assert gen_mon_case.case_active == mt_reasonheir.cases.get(mon_rope).case_active
    assert gen_mon_case == mt_reasonheir.cases.get(mon_rope)
    assert gen_wk_reasonheir.cases == mt_reasonheir.cases
    assert gen_wk_reasonheir == mt_reasonheir

    casa_rope = yao_planunit.make_l1_rope(exx.casa)
    bird_str = "say hi to birds"
    bird_rope = yao_planunit.make_rope(casa_rope, bird_str)
    assert from_list_get_active(bird_rope, keg_dict) is False


def test_PlanUnit_cashout_SetsKegUnitsActiveWithEvery6WeeksReason_planunit_v001():
    # ESTABLISH
    yao_planunit = planunit_v001()
    hr_num_str = "hr_number"
    hr_num_rope = yao_planunit.make_l1_rope(hr_num_str)
    min_str = "jour_minute"
    min_rope = yao_planunit.make_l1_rope(min_str)

    # WHEN
    yao_planunit.add_fact(
        fact_context=hr_num_rope, fact_state=hr_num_rope, fact_lower=0, fact_upper=23
    )
    yao_planunit.add_fact(
        fact_context=min_rope, fact_state=min_rope, fact_lower=0, fact_upper=59
    )
    yao_planunit.cashout()

    # THEN
    ced_wk_reason_context = yao_planunit.make_l1_rope("ced_wk")

    reason_divisor = None
    reason_lower = None
    reason_upper = None
    print(f"{len(yao_planunit._keg_dict)=}")

    casa_rope = yao_planunit.make_l1_rope("casa")
    cleaning_rope = yao_planunit.make_rope(casa_rope, "cleaning")
    clean_couch_rope = yao_planunit.make_rope(
        cleaning_rope, "clean sheets couch blankets"
    )
    clean_sheet_keg = yao_planunit.get_keg_obj(clean_couch_rope)
    # print(f"{clean_sheet_keg.reasonunits.values()=}")
    ced_wk_reason = clean_sheet_keg.reasonunits.get(ced_wk_reason_context)
    ced_wk_case = ced_wk_reason.cases.get(ced_wk_reason_context)
    print(
        f"{clean_sheet_keg.keg_label=} {ced_wk_reason.reason_context=} {ced_wk_case.reason_state=}"
    )
    # print(f"{clean_sheet_keg.keg_label=} {ced_wk_reason.reason_context=} {case_x=}")
    reason_divisor = ced_wk_case.reason_divisor
    reason_lower = ced_wk_case.reason_lower
    reason_upper = ced_wk_case.reason_upper
    # print(f"{keg.reasonunits=}")
    assert clean_sheet_keg.keg_active is False

    # for keg in keg_dict:
    #     # print(f"{keg.parent_rope=}")
    #     if keg.keg_label == "clean sheets couch blankets":
    #         print(f"{keg.get_keg_rope()=}")

    assert reason_divisor == 6
    assert reason_lower == 1
    print(
        f"There exists a keg with a reason_context {ced_wk_reason_context} that also has lemmet div =6 and reason_lower/reason_upper =1"
    )
    # print(f"{len(keg_dict)=}")
    ced_wk_reason_lower = 6001

    # WHEN
    yao_planunit.add_fact(
        ced_wk_reason_context,
        fact_state=ced_wk_reason_context,
        fact_lower=ced_wk_reason_lower,
        fact_upper=ced_wk_reason_lower,
    )
    nation_str = "Nation-States"
    nation_rope = yao_planunit.make_l1_rope(nation_str)
    yao_planunit.add_fact(fact_context=nation_rope, fact_state=nation_rope)
    print(
        f"Nation set and also fact set: {ced_wk_reason_context=} with {ced_wk_reason_lower=} and {ced_wk_reason_lower=}"
    )
    print(f"{yao_planunit.kegroot.factunits=}")
    yao_planunit.cashout()

    # THEN
    wk_str = "ced_wk"
    wk_rope = yao_planunit.make_l1_rope(wk_str)
    casa_rope = yao_planunit.make_l1_rope("casa")
    cleaning_rope = yao_planunit.make_rope(casa_rope, "cleaning")
    clean_couch_str = "clean sheets couch blankets"
    clean_couch_rope = yao_planunit.make_rope(cleaning_rope, clean_couch_str)
    clean_couch_keg = yao_planunit.get_keg_obj(rope=clean_couch_rope)
    wk_reason = clean_couch_keg.reasonunits.get(wk_rope)
    wk_case = wk_reason.cases.get(wk_rope)
    print(f"{clean_couch_keg.keg_label=} {wk_reason.reason_context=} {wk_case=}")
    assert wk_case.reason_divisor == 6 and wk_case.reason_lower == 1


def test_PlanUnit_cashout_SetsAttr_KegUnits_active_planunit_v001():
    # ESTABLISH
    yao_planunit = planunit_v001()

    # WHEN
    yao_planunit.cashout()

    # THEN
    print(f"{len(yao_planunit._keg_dict)=}")
    # first_keg_kid_count = 0
    # first_keg_kid_none_count = 0
    # first_keg_kid_true_count = 0
    # first_keg_kid_false_count = 0
    # for keg in keg_list:
    #     if str(type(keg)).find(".keg.KegUnit'>") > 0:
    #         first_keg_kid_count += 1
    #         if keg.keg_active is None:
    #             first_keg_kid_none_count += 1
    #         elif keg.keg_active:
    #             first_keg_kid_true_count += 1
    #         elif keg.keg_active is False:
    #             first_keg_kid_false_count += 1

    # print(f"{first_keg_kid_count=}")
    # print(f"{first_keg_kid_none_count=}")
    # print(f"{first_keg_kid_true_count=}")
    # print(f"{first_keg_kid_false_count=}")

    # keg_kid_count = 0
    # for keg in keg_list_without_kegroot:
    #     keg_kid_count += 1
    #     print(f"{keg.keg_label=} {keg_kid_count=}")
    #     assert keg.keg_active is not None
    #     assert keg.keg_active in (True, False)
    # assert keg_kid_count == len(keg_list_without_kegroot)

    assert len(yao_planunit._keg_dict) == sum(
        keg.keg_active is not None for keg in yao_planunit._keg_dict.values()
    )


def test_PlanUnit_cashout_EveryTwoMonthReturnsObj_planunit_v001():
    # ESTABLISH
    yao_planunit = planunit_v001()
    minute_str = "jour_minute"
    minute_rope = yao_planunit.make_l1_rope(minute_str)
    yao_planunit.add_fact(
        fact_context=minute_rope, fact_state=minute_rope, fact_lower=0, fact_upper=1399
    )
    month_str = "month_wk"
    month_rope = yao_planunit.make_l1_rope(month_str)
    yao_planunit.add_fact(fact_context=month_rope, fact_state=month_rope)
    nations_str = "Nation-States"
    nations_rope = yao_planunit.make_l1_rope(nations_str)
    yao_planunit.add_fact(fact_context=nations_rope, fact_state=nations_rope)
    mood_str = "Moods"
    mood_rope = yao_planunit.make_l1_rope(mood_str)
    yao_planunit.add_fact(fact_context=mood_rope, fact_state=mood_rope)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_planunit.make_l1_rope(aaron_str)
    yao_planunit.add_fact(fact_context=aaron_rope, fact_state=aaron_rope)
    websites_str = "Websites"
    websites_rope = yao_planunit.make_l1_rope(websites_str)
    yao_planunit.add_fact(fact_context=websites_rope, fact_state=websites_rope)
    sem_jours_str = "sem_jours"
    sem_jours_rope = yao_planunit.make_l1_rope(sem_jours_str)
    yao_planunit.add_fact(fact_context=sem_jours_rope, fact_state=sem_jours_rope)
    keg_dict = yao_planunit.get_keg_dict()
    print(f"{len(keg_dict)=}")

    casa_rope = yao_planunit.make_l1_rope(exx.casa)
    clean_str = "cleaning"
    clean_rope = yao_planunit.make_rope(casa_rope, clean_str)
    mat_keg_label = "deep clean play mat"
    mat_rope = yao_planunit.make_rope(clean_rope, mat_keg_label)
    assert from_list_get_active(mat_rope, keg_dict) is False

    yr_month_reason_context = yao_planunit.make_l1_rope("yr_month")
    print(f"{yr_month_reason_context=}, {yr_month_reason_context=}")

    # WHEN
    yao_planunit.add_fact(
        yr_month_reason_context,
        fact_state=yr_month_reason_context,
        fact_lower=0,
        fact_upper=8,
    )
    ced_wk = yao_planunit.make_l1_rope("ced_wk")
    yao_planunit.add_fact(
        fact_context=ced_wk, fact_state=ced_wk, fact_lower=0, fact_upper=4
    )
    yao_planunit.cashout()

    # THEN
    print(f"{len(keg_dict)=}")
    print(f"{len(yao_planunit.kegroot.factunits)=}")
    assert from_list_get_active(mat_rope, yao_planunit._keg_dict)


def test_PlanUnit_cashout_SetsEmpty_sum_healerunit_kegs_fund_total():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    assert sue_planunit.sum_healerunit_kegs_fund_total == 0
    assert sue_planunit._keep_dict == {}

    # WHEN
    sue_planunit.cashout()

    # THEN
    assert sue_planunit.sum_healerunit_kegs_fund_total == 0
    assert sue_planunit._keep_dict == {}


def test_PlanUnit_cashout_Sets_sum_healerunit_kegs_fund_total(graphics_bool):
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    sue_planunit.add_personunit("Sue")
    sue_planunit.cashout()
    nation_rope = sue_planunit.make_l1_rope("nation")
    usa_rope = sue_planunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_planunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({"Sue"})
    sue_planunit.edit_keg_attr(
        oregon_rope, problem_bool=True, healerunit=sue_healerunit
    )
    oregon_keg = sue_planunit.get_keg_obj(oregon_rope)
    print(f"{oregon_keg.fund_ratio=}")
    assert sue_planunit.sum_healerunit_kegs_fund_total == 0
    assert oregon_keg.healerunit_ratio == 0

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert (
        sue_planunit.sum_healerunit_kegs_fund_total == 0.038461539 * default_pool_num()
    )
    assert oregon_keg.healerunit_ratio == 1

    # WHEN
    wk_rope = sue_planunit.make_l1_rope("sem_jours")
    sue_planunit.edit_keg_attr(wk_rope, problem_bool=True)
    mon_rope = sue_planunit.make_rope(wk_rope, "Mon")
    sue_planunit.edit_keg_attr(mon_rope, healerunit=sue_healerunit)
    mon_keg = sue_planunit.get_keg_obj(mon_rope)
    # print(f"{mon_keg.problem_bool=} {mon_keg.fund_ratio=}")
    sue_planunit.cashout()
    # THEN
    assert (
        sue_planunit.sum_healerunit_kegs_fund_total != 0.038461539 * default_pool_num()
    )
    assert (
        sue_planunit.sum_healerunit_kegs_fund_total == 0.06923077 * default_pool_num()
    )
    assert oregon_keg.healerunit_ratio == 0.5555555571604938
    assert mon_keg.healerunit_ratio == 0.4444444428395062

    # WHEN
    tue_rope = sue_planunit.make_rope(wk_rope, "Tue")
    sue_planunit.edit_keg_attr(tue_rope, healerunit=sue_healerunit)
    tue_keg = sue_planunit.get_keg_obj(tue_rope)
    # print(f"{tue_keg.problem_bool=} {tue_keg.fund_ratio=}")
    # sat_rope = sue_planunit.make_rope(wk_rope, "Sat")
    # sat_keg = sue_planunit.get_keg_obj(sat_rope)
    # print(f"{sat_keg.problem_bool=} {sat_keg.fund_ratio=}")
    sue_planunit.cashout()

    # THEN
    assert (
        sue_planunit.sum_healerunit_kegs_fund_total
        != 0.06923076923076923 * default_pool_num()
    )
    assert (
        sue_planunit.sum_healerunit_kegs_fund_total == 0.100000001 * default_pool_num()
    )
    assert oregon_keg.healerunit_ratio == 0.38461538615384616
    assert mon_keg.healerunit_ratio == 0.3076923069230769
    assert tue_keg.healerunit_ratio == 0.3076923069230769

    # WHEN
    sue_planunit.edit_keg_attr(wk_rope, healerunit=sue_healerunit)
    wk_keg = sue_planunit.get_keg_obj(wk_rope)
    print(f"{wk_keg.keg_label=} {wk_keg.problem_bool=} {wk_keg.fund_ratio=}")
    sue_planunit.cashout()
    # THEN
    display_kegtree(sue_planunit, "Keep", graphics_bool)
    assert sue_planunit.sum_healerunit_kegs_fund_total == 0
    assert oregon_keg.healerunit_ratio == 0
    assert mon_keg.healerunit_ratio == 0
    assert tue_keg.healerunit_ratio == 0


def test_PlanUnit_cashout_Sets_keep_dict_v1(graphics_bool):
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    sue_planunit.add_personunit("Sue")
    sue_planunit.cashout()
    nation_rope = sue_planunit.make_l1_rope("nation")
    usa_rope = sue_planunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_planunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({"Sue"})
    sue_planunit.edit_keg_attr(
        oregon_rope, problem_bool=True, healerunit=sue_healerunit
    )
    assert len(sue_planunit._keep_dict) == 0
    assert sue_planunit._keep_dict.get(oregon_rope) is None

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert len(sue_planunit._keep_dict) == 1
    assert sue_planunit._keep_dict.get(oregon_rope) is not None

    # WHEN
    wk_rope = sue_planunit.make_l1_rope("sem_jours")
    sue_planunit.edit_keg_attr(wk_rope, problem_bool=True)
    mon_rope = sue_planunit.make_rope(wk_rope, "Mon")
    sue_planunit.edit_keg_attr(mon_rope, healerunit=sue_healerunit)
    # mon_keg = sue_planunit.get_keg_obj(mon_rope)
    # print(f"{mon_keg.problem_bool=} {mon_keg.fund_ratio=}")
    sue_planunit.cashout()
    # THEN
    assert len(sue_planunit._keep_dict) == 2
    assert sue_planunit._keep_dict.get(oregon_rope) is not None
    assert sue_planunit._keep_dict.get(mon_rope) is not None

    # WHEN
    tue_rope = sue_planunit.make_rope(wk_rope, "Tue")
    sue_planunit.edit_keg_attr(tue_rope, healerunit=sue_healerunit)
    # tue_keg = sue_planunit.get_keg_obj(tue_rope)
    # print(f"{tue_keg.problem_bool=} {tue_keg.fund_ratio=}")
    # sat_rope = sue_planunit.make_rope(wk_rope, "Sat")
    # sat_keg = sue_planunit.get_keg_obj(sat_rope)
    # print(f"{sat_keg.problem_bool=} {sat_keg.fund_ratio=}")
    sue_planunit.cashout()

    # THEN
    assert len(sue_planunit._keep_dict) == 3
    assert sue_planunit._keep_dict.get(oregon_rope) is not None
    assert sue_planunit._keep_dict.get(mon_rope) is not None
    assert sue_planunit._keep_dict.get(tue_rope) is not None

    # WHEN
    sue_planunit.edit_keg_attr(wk_rope, healerunit=sue_healerunit)
    wk_keg = sue_planunit.get_keg_obj(wk_rope)
    print(f"{wk_keg.keg_label=} {wk_keg.problem_bool=} {wk_keg.fund_ratio=}")
    sue_planunit.cashout()
    # THEN
    display_kegtree(sue_planunit, "Keep", graphics_bool)
    assert len(sue_planunit._keep_dict) == 0
    assert sue_planunit._keep_dict == {}


def test_PlanUnit_cashout_Sets_healers_dict():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    sue_planunit.add_personunit(exx.sue)
    sue_planunit.add_personunit(exx.bob)
    assert sue_planunit._healers_dict == {}

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert sue_planunit._healers_dict == {}

    # ESTABLISH
    nation_rope = sue_planunit.make_l1_rope("nation")
    usa_rope = sue_planunit.make_rope(nation_rope, "USA")
    oregon_keep_rope = sue_planunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({exx.sue})
    sue_planunit.edit_keg_attr(
        oregon_keep_rope, problem_bool=True, healerunit=sue_healerunit
    )

    wk_rope = sue_planunit.make_l1_rope("sem_jours")
    bob_healerunit = healerunit_shop({exx.bob})
    sue_planunit.edit_keg_attr(wk_rope, problem_bool=True, healerunit=bob_healerunit)
    assert sue_planunit._healers_dict == {}

    # WHEN
    sue_planunit.cashout()

    # THEN
    assert len(sue_planunit._healers_dict) == 2
    wk_keg = sue_planunit.get_keg_obj(wk_rope)
    assert sue_planunit._healers_dict.get(exx.bob) == {wk_rope: wk_keg}
    oregon_keg = sue_planunit.get_keg_obj(oregon_keep_rope)
    assert sue_planunit._healers_dict.get(exx.sue) == {oregon_keep_rope: oregon_keg}


def test_PlanUnit_cashout_Sets_keeps_buildable_True():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    sue_planunit.add_personunit(exx.sue)
    sue_planunit.add_personunit(exx.bob)
    assert sue_planunit.keeps_buildable is False

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert sue_planunit.keeps_buildable

    # ESTABLISH
    nation_rope = sue_planunit.make_l1_rope("nation")
    usa_rope = sue_planunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_planunit.make_rope(usa_rope, "Oregon")
    sue_healerunit = healerunit_shop({exx.sue})
    sue_planunit.edit_keg_attr(
        oregon_rope, problem_bool=True, healerunit=sue_healerunit
    )

    wk_rope = sue_planunit.make_l1_rope("sem_jours")
    bob_healerunit = healerunit_shop({exx.bob})
    sue_planunit.edit_keg_attr(wk_rope, problem_bool=True, healerunit=bob_healerunit)

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert sue_planunit.keeps_buildable


def test_PlanUnit_cashout_Sets_keeps_buildable_False():
    # ESTABLISH
    sue_planunit = get_planunit_with_4_levels_and_2reasons()
    sue_planunit.add_personunit(exx.sue)
    sue_planunit.add_personunit(exx.bob)
    assert sue_planunit.keeps_buildable is False

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert sue_planunit.keeps_buildable

    # ESTABLISH
    nation_rope = sue_planunit.make_l1_rope("nation")
    usa_rope = sue_planunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_planunit.make_rope(usa_rope, "Oregon")
    bend_str = "Be/nd"
    bend_rope = sue_planunit.make_rope(oregon_rope, bend_str)
    sue_planunit.set_keg_obj(kegunit_shop(bend_str), oregon_rope)
    sue_healerunit = healerunit_shop({exx.sue})
    sue_planunit.edit_keg_attr(bend_rope, problem_bool=True, healerunit=sue_healerunit)
    assert sue_planunit.keeps_buildable

    # WHEN
    sue_planunit.cashout()
    # THEN
    assert sue_planunit.keeps_buildable is False
