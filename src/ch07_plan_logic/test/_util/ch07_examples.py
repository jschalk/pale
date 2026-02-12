from enum import Enum
from src.ch00_py.file_toolbox import open_json
from src.ch03_labor.labor import laborunit_shop
from src.ch04_rope.rope import RopeTerm, create_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch06_keg.keg import kegunit_shop
from src.ch07_plan_logic.plan_main import (
    PlanUnit,
    get_planunit_from_dict,
    planunit_shop,
)
from src.ref.keywords import ExampleStrs as exx

# from src.ch00_py.file_toolbox import save_file
# from src.ch07_plan_logic.test._util.ch07_env import get_plan_examples_dir as env_dir
# from src.ch07_plan_logic.test._util.example_plans import planunit_v001, planunit_v002

# save_json(env_dir(), "example_plan3.json", planunit_v001().to_dict())
# save_json(env_dir(), "example_plan4.json", planunit_v002().to_dict())


def planunit_v001() -> PlanUnit:
    plan1_path = "src/ch07_plan_logic/test/_util/example_plan1.json"
    return get_planunit_from_dict(open_json(plan1_path))


def planunit_v001_with_large_agenda() -> PlanUnit:
    yao_plan = planunit_v001()
    jour_minute_rope = yao_plan.make_l1_rope("jour_minute")
    month_wk_rope = yao_plan.make_l1_rope("month_wk")
    nations_rope = yao_plan.make_l1_rope("Nation-States")
    mood_rope = yao_plan.make_l1_rope("Moods")
    aaron_rope = yao_plan.make_l1_rope("Aaron Donald objects effected by him")
    yr_month_rope = yao_plan.make_l1_rope("yr_month")
    season_rope = yao_plan.make_l1_rope("Seasons")
    ced_wk_rope = yao_plan.make_l1_rope("ced_wk")
    sem_jours_rope = yao_plan.make_l1_rope("sem_jours")

    yao_plan.add_fact(aaron_rope, aaron_rope)
    yao_plan.add_fact(ced_wk_rope, ced_wk_rope, fact_lower=0, fact_upper=53)
    yao_plan.add_fact(jour_minute_rope, jour_minute_rope, 0, 1399)
    # yao_plan.add_fact(websites, websites)
    yao_plan.add_fact(month_wk_rope, month_wk_rope, fact_lower=0, fact_upper=5)
    yao_plan.add_fact(mood_rope, mood_rope)
    # yao_plan.add_fact(movie, movie)
    yao_plan.add_fact(nations_rope, nations_rope)
    yao_plan.add_fact(season_rope, season_rope)
    yao_plan.add_fact(yr_month_rope, yr_month_rope, fact_lower=0, fact_upper=12)
    # yao_plan.add_fact(water, water)
    yao_plan.add_fact(sem_jours_rope, sem_jours_rope)
    return yao_plan


def planunit_v002() -> PlanUnit:
    plan2_path = "src/ch07_plan_logic/test/_util/example_plan2.json"
    return get_planunit_from_dict(open_json(plan2_path))


def get_planunit_with_4_levels() -> PlanUnit:
    # sourcery skip: extract-duplicate-method
    sue_plan = planunit_shop("Sue", exx.a23)
    sue_plan.set_l1_keg(kegunit_shop(exx.casa, star=30, pledge=True))
    cat_str = "cat have dinner"
    sue_plan.set_l1_keg(kegunit_shop(cat_str, star=30, pledge=True))

    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    keg_kid_sem_jours = kegunit_shop(wk_str, star=40)
    sue_plan.set_l1_keg(keg_kid_sem_jours)
    sun_str = "Sun"
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sue_plan.set_keg_obj(kegunit_shop(sun_str, star=20), wk_rope)
    sue_plan.set_keg_obj(kegunit_shop(mon_str, star=20), wk_rope)
    sue_plan.set_keg_obj(kegunit_shop(tue_str, star=20), wk_rope)
    sue_plan.set_keg_obj(kegunit_shop(exx.wed, star=20), wk_rope)
    sue_plan.set_keg_obj(kegunit_shop(thu_str, star=30), wk_rope)
    sue_plan.set_keg_obj(kegunit_shop(fri_str, star=40), wk_rope)
    sue_plan.set_keg_obj(kegunit_shop(sat_str, star=50), wk_rope)

    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    keg_kid_nation = kegunit_shop(nation_str, star=30)
    sue_plan.set_l1_keg(keg_kid_nation)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    keg_grandkid_usa = kegunit_shop(usa_str, star=50)
    keg_grandkid_france = kegunit_shop(france_str, star=50)
    keg_grandkid_brazil = kegunit_shop(brazil_str, star=50)
    sue_plan.set_keg_obj(keg_grandkid_france, nation_rope)
    sue_plan.set_keg_obj(keg_grandkid_brazil, nation_rope)
    sue_plan.set_keg_obj(keg_grandkid_usa, nation_rope)
    texas_str = "Texas"
    oregon_str = "Oregon"
    keg_grandgrandkid_usa_texas = kegunit_shop(texas_str, star=50)
    keg_grandgrandkid_usa_oregon = kegunit_shop(oregon_str, star=50)
    sue_plan.set_keg_obj(keg_grandgrandkid_usa_texas, usa_rope)
    sue_plan.set_keg_obj(keg_grandgrandkid_usa_oregon, usa_rope)
    return sue_plan


def get_planunit_with_4_levels_and_2reasons() -> PlanUnit:
    # sourcery skip: extract-duplicate-method
    sue_plan = get_planunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wed_rope = sue_plan.make_rope(wk_rope, exx.wed)
    wk_reason = reasonunit_shop(wk_rope)
    wk_reason.set_case(wed_rope)

    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    nation_reason = reasonunit_shop(nation_rope)
    nation_reason.set_case(usa_rope)

    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sue_plan.edit_keg_attr(casa_rope, reason=wk_reason)
    sue_plan.edit_keg_attr(casa_rope, reason=nation_reason)
    return sue_plan


def get_planunit_with_4_levels_and_2reasons_2facts() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wed_rope = sue_plan.make_rope(wk_rope, exx.wed)
    nation_str = "nation"
    nation_rope = sue_plan.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_plan.make_rope(nation_rope, usa_str)
    sue_plan.add_fact(fact_context=wk_rope, fact_state=wed_rope)
    sue_plan.add_fact(fact_context=nation_rope, fact_state=usa_rope)
    return sue_plan


def get_planunit_with7am_clean_table_reason() -> PlanUnit:
    sue_plan = get_planunit_with_4_levels_and_2reasons_2facts()

    ziet_str = "ziettech"
    ziet_rope = sue_plan.make_l1_rope(ziet_str)
    ziet_keg = kegunit_shop(ziet_str)

    x24hr_str = "24hr"
    x24hr_rope = sue_plan.make_rope(ziet_rope, x24hr_str)
    x24hr_keg = kegunit_shop(x24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_rope = sue_plan.make_rope(x24hr_rope, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_keg = kegunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_keg = kegunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_keg = kegunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_keg = kegunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_keg = kegunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_plan.set_l1_keg(ziet_keg)
    sue_plan.set_keg_obj(x24hr_keg, ziet_rope)
    sue_plan.set_keg_obj(am_keg, x24hr_rope)
    sue_plan.set_keg_obj(pm_keg, x24hr_rope)
    sue_plan.set_keg_obj(n1_keg, am_rope)  # keg_am
    sue_plan.set_keg_obj(n2_keg, am_rope)  # keg_am
    sue_plan.set_keg_obj(n3_keg, am_rope)  # keg_am

    house_str = "houseadministration"
    house_rope = sue_plan.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_plan.make_rope(house_rope, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_rope = sue_plan.make_rope(clean_rope, soap_str)
    grab_str = "grab soap"
    grab_rope = sue_plan.make_rope(soap_rope, grab_str)
    house_keg = kegunit_shop(house_str)
    clean_keg = kegunit_shop(clean_str, pledge=True)
    dish_keg = kegunit_shop(dish_str, pledge=True)
    soap_keg = kegunit_shop(soap_str, pledge=True)
    grab_keg = kegunit_shop(grab_str, pledge=True)

    sue_plan.set_l1_keg(house_keg)
    sue_plan.set_keg_obj(clean_keg, house_rope)
    sue_plan.set_keg_obj(dish_keg, clean_rope)
    sue_plan.set_keg_obj(soap_keg, clean_rope)
    sue_plan.set_keg_obj(grab_keg, soap_rope)

    clean_table_7am_reason_context = x24hr_rope
    clean_table_7am_case_rope = x24hr_rope
    clean_table_7am_reason_lower = 7.0
    clean_table_7am_reason_upper = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_reason_context)
    clean_table_7am_reason.set_case(
        case=clean_table_7am_case_rope,
        reason_lower=clean_table_7am_reason_lower,
        reason_upper=clean_table_7am_reason_upper,
    )
    sue_plan.edit_keg_attr(clean_rope, reason=clean_table_7am_reason)
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    sue_plan.edit_keg_attr(casa_rope, reason=clean_table_7am_reason)
    return sue_plan


def get_planunit_1task_1ceo_minutes_reason_1fact() -> PlanUnit:
    yao_plan = planunit_shop("Yao")
    hr_min_str = "hr"
    hr_min_keg = kegunit_shop(hr_min_str)
    hr_rope = yao_plan.make_l1_rope(hr_min_str)
    hr_reasonunit = reasonunit_shop(hr_rope)
    hr_reasonunit.set_case(hr_rope, reason_lower=80, reason_upper=90)
    yao_plan.set_l1_keg(hr_min_keg)
    yao_plan.add_fact(hr_rope, hr_rope, 85, 95)
    mail_str = "obtain mail"
    mail_rope = yao_plan.make_l1_rope(mail_str)
    mail_keg = kegunit_shop(mail_str, pledge=True)
    yao_plan.set_l1_keg(mail_keg)
    yao_plan.edit_keg_attr(mail_rope, reason=hr_reasonunit)
    return yao_plan


def get_planunit_x1_3levels_1reason_1facts() -> PlanUnit:
    tiger_rope = create_rope("tiger")
    zia_plan = planunit_shop("Zia", tiger_rope)
    shave_str = "shave"
    shave_rope = zia_plan.make_l1_rope(shave_str)
    keg_kid_shave = kegunit_shop(shave_str, star=30, pledge=True)
    zia_plan.set_l1_keg(keg_kid_shave)
    wk_str = "sem_jours"
    wk_rope = zia_plan.make_l1_rope(wk_str)
    wk_keg = kegunit_shop(wk_str, star=40)
    zia_plan.set_l1_keg(wk_keg)

    sun_str = "Sun"
    sun_rope = zia_plan.make_rope(wk_rope, sun_str)
    church_str = "Church"
    church_rope = zia_plan.make_rope(sun_rope, church_str)
    mon_str = "Mon"
    mon_rope = zia_plan.make_rope(wk_rope, mon_str)
    keg_grandkidU = kegunit_shop(sun_str, star=20)
    keg_grandkidM = kegunit_shop(mon_str, star=20)
    zia_plan.set_keg_obj(keg_grandkidU, wk_rope)
    zia_plan.set_keg_obj(keg_grandkidM, wk_rope)

    shave_reason = reasonunit_shop(wk_rope)
    shave_reason.set_case(mon_rope)

    zia_plan.edit_keg_attr(shave_rope, reason=shave_reason)
    zia_plan.add_fact(fact_context=wk_rope, fact_state=sun_rope)
    x_factunit = factunit_shop(fact_context=wk_rope, fact_state=church_rope)
    zia_plan.edit_keg_attr(shave_rope, factunit=x_factunit)
    return zia_plan


def get_planunit_reason_context_ziet_example() -> PlanUnit:
    sue_plan = planunit_shop("Sue")
    sue_plan.set_l1_keg(kegunit_shop("casa"))
    return sue_plan


def get_planunit_irrational_example() -> PlanUnit:
    # sourcery skip: extract-duplicate-method
    # this plan has no definitive agenda because 2 pledge kegs are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken.keg_active is True, egg.keg_active is set to False
    # Step 1: if egg.keg_active is False, chicken.keg_active is set to False
    # Step 2: if chicken.keg_active is False, egg.keg_active is set to True
    # Step 3: if egg.keg_active is True, chicken.keg_active is set to True
    # Step 4: back to step 0.
    # after hatter_plan.cashout these should be true:
    # 1. hatter_plan._irrational is True
    # 2. hatter_plan.tree_traverse_count = hatter_plan.max_tree_traverse

    hatter_plan = planunit_shop("Mad Hatter")
    hatter_plan.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_plan.make_l1_rope(egg_str)
    hatter_plan.set_l1_keg(kegunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_plan.make_l1_rope(chicken_str)
    hatter_plan.set_l1_keg(kegunit_shop(chicken_str))

    # set egg pledge is True when chicken first is False
    hatter_plan.edit_keg_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )

    # set chick pledge is True when egg first is False
    hatter_plan.edit_keg_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )

    return hatter_plan


def get_mop_with_reason_planunit_example1():
    sue_plan = planunit_shop("Sue")
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_plan.make_rope(casa_rope, floor_str)
    floor_keg = kegunit_shop(floor_str, pledge=True)
    sue_plan.set_keg_obj(floor_keg, casa_rope)
    sue_plan.set_l1_keg(kegunit_shop("unimportant"))

    situation_str = "cleaniness situation"
    situation_rope = sue_plan.make_rope(casa_rope, situation_str)
    sue_plan.set_keg_obj(kegunit_shop(situation_str), casa_rope)

    clean_rope = sue_plan.make_rope(situation_rope, exx.clean)
    sue_plan.set_keg_obj(kegunit_shop(exx.clean), situation_rope)
    sue_plan.set_keg_obj(kegunit_shop("very_much"), clean_rope)
    sue_plan.set_keg_obj(kegunit_shop("moderately"), clean_rope)
    sue_plan.set_keg_obj(kegunit_shop("dirty"), situation_rope)

    floor_reason = reasonunit_shop(situation_rope)
    floor_reason.set_case(case=situation_rope)
    sue_plan.edit_keg_attr(floor_rope, reason=floor_reason)
    return sue_plan


def get_planunit_laundry_example1() -> PlanUnit:
    yao_plan = planunit_shop(exx.yao)
    cali_str = "Cali"
    yao_plan.add_partnerunit(exx.yao)
    yao_plan.add_partnerunit(cali_str)

    basket_str = "laundry basket situation"
    b_full_str = "full"
    b_smel_str = "smelly"
    b_bare_str = "bare"
    b_fine_str = "fine"
    b_half_str = "half full"
    do_laundry_str = "do_laundry"
    casa_rope = yao_plan.make_l1_rope(exx.casa)
    basket_rope = yao_plan.make_rope(casa_rope, basket_str)
    b_full_rope = yao_plan.make_rope(basket_rope, b_full_str)
    b_smel_rope = yao_plan.make_rope(basket_rope, b_smel_str)
    laundry_task_rope = yao_plan.make_rope(casa_rope, do_laundry_str)
    yao_plan.set_l1_keg(kegunit_shop(exx.casa))
    yao_plan.set_keg_obj(kegunit_shop(basket_str), casa_rope)
    yao_plan.set_keg_obj(kegunit_shop(b_full_str), basket_rope)
    yao_plan.set_keg_obj(kegunit_shop(b_smel_str), basket_rope)
    yao_plan.set_keg_obj(kegunit_shop(b_bare_str), basket_rope)
    yao_plan.set_keg_obj(kegunit_shop(b_fine_str), basket_rope)
    yao_plan.set_keg_obj(kegunit_shop(b_half_str), basket_rope)
    yao_plan.set_keg_obj(kegunit_shop(do_laundry_str, pledge=True), casa_rope)

    # laundry requirement
    yao_plan.edit_keg_attr(
        laundry_task_rope, reason_context=basket_rope, reason_case=b_full_rope
    )
    # laundry requirement
    yao_plan.edit_keg_attr(
        laundry_task_rope, reason_context=basket_rope, reason_case=b_smel_rope
    )
    cali_laborunit = laborunit_shop()
    cali_laborunit.add_party(cali_str)
    yao_plan.edit_keg_attr(laundry_task_rope, laborunit=cali_laborunit)
    yao_plan.add_fact(fact_context=basket_rope, fact_state=b_full_rope)

    return yao_plan


def from_list_get_active(
    rope: RopeTerm, keg_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_keg = None

    active_true_count = 0
    active_false_count = 0
    for keg in keg_dict.values():
        if keg.get_keg_rope() == rope:
            temp_keg = keg
            print(f"s for KegUnit {temp_keg.get_keg_rope()}  {temp_keg.keg_active=}")

        if keg.keg_active:
            active_true_count += 1
        elif keg.keg_active is False:
            active_false_count += 1

    active = temp_keg.keg_active
    print(
        f"Set active: {keg.keg_label=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
