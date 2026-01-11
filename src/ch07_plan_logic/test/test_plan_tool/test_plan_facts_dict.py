from copy import deepcopy as copy_deepcopy
from src.ch04_rope.rope import create_rope
from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_tool import (
    clear_factunits_from_plan,
    get_plan_root_facts_dict,
    set_factunits_to_plan,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_get_plan_root_facts_dict_ReturnsObj_Scenario0_No_factunits():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    # WHEN / THEN
    assert get_plan_root_facts_dict(sue_plan) == {}
    assert get_plan_root_facts_dict(sue_plan) == sue_plan.get_kegroot_factunits_dict()


def test_get_plan_root_facts_dict_ReturnsObj_Scenario1_factunits_Exist():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_l1_rope("clean")
    dirty_rope = sue_plan.make_l1_rope("dirty")
    sue_plan.add_fact(casa_rope, dirty_rope, create_missing_kegs=True)

    # WHEN
    sue_fact_dict = get_plan_root_facts_dict(sue_plan)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get(kw.fact_context) == casa_rope
    assert casa_fact_dict.get(kw.fact_state) == dirty_rope
    expected_sue_fact_dict = {
        casa_rope: {kw.fact_context: casa_rope, kw.fact_state: dirty_rope}
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_get_plan_root_facts_dict_ReturnsObj_Scenario2_factunits_Exist():
    # ESTABLISH
    sue_plan = planunit_shop(exx.sue)
    casa_rope = sue_plan.make_l1_rope("casa")
    clean_rope = sue_plan.make_l1_rope("clean")
    dirty_rope = sue_plan.make_l1_rope("dirty")
    dirty_reason_lower = 10
    dirty_reason_upper = 13
    sue_plan.add_fact(
        casa_rope, dirty_rope, dirty_reason_lower, dirty_reason_upper, True
    )

    # WHEN
    sue_fact_dict = get_plan_root_facts_dict(sue_plan)

    # THEN
    assert sue_fact_dict.get(casa_rope) != None
    casa_fact_dict = sue_fact_dict.get(casa_rope)
    assert casa_fact_dict.get(kw.fact_context) == casa_rope
    assert casa_fact_dict.get(kw.fact_state) == dirty_rope
    assert casa_fact_dict.get("fact_lower") == dirty_reason_lower
    assert casa_fact_dict.get("fact_upper") == dirty_reason_upper
    expected_sue_fact_dict = {
        casa_rope: {
            kw.fact_context: casa_rope,
            kw.fact_state: dirty_rope,
            "fact_lower": dirty_reason_lower,
            "fact_upper": dirty_reason_upper,
        }
    }
    print(f"{sue_fact_dict=}")
    print(f"{expected_sue_fact_dict=}")
    assert sue_fact_dict == expected_sue_fact_dict


def test_set_factunits_to_plan_ReturnsObj_Scenario0_PlanEmptyNoFacts():
    # ESTABLISH
    yao_plan = planunit_shop("Yao", exx.a23)
    before_yao_plan = copy_deepcopy(yao_plan)
    facts_dict = {}
    assert yao_plan.to_dict() == before_yao_plan.to_dict()

    # WHEN
    set_factunits_to_plan(yao_plan, facts_dict)

    # THEN
    assert yao_plan.to_dict() == before_yao_plan.to_dict()


def test_set_factunits_to_plan_ReturnsObj_Scenario1_Plan1FactsChanged():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, exx.mop)
    bob_plan.add_keg(floor_rope)
    bob_plan.add_keg(clean_rope)
    bob_plan.add_keg(dirty_rope)
    bob_plan.add_keg(mop_rope, pledge=True)
    bob_plan.edit_keg_attr(mop_rope, reason_context=floor_rope, reason_case=dirty_rope)
    dirty_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: dirty_rope}
    }
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_kegroot_factunits_dict() != dirty_facts_dict
    assert bob_plan.get_kegroot_factunits_dict() == {}
    assert bob_plan.to_dict() == before_bob_plan.to_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, dirty_facts_dict)

    # THEN
    assert bob_plan.to_dict() != before_bob_plan.to_dict()
    assert bob_plan.get_kegroot_factunits_dict() == dirty_facts_dict


def test_set_factunits_to_plan_ReturnsObj_Scenario2_FactUnit_reason_context_DoesNotExistInPlan():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, exx.mop)
    bob_plan.add_keg(floor_rope)
    # bob_plan.add_keg(clean_rope)
    bob_plan.add_keg(dirty_rope)
    bob_plan.add_keg(mop_rope, pledge=True)
    bob_plan.edit_keg_attr(mop_rope, reason_context=floor_rope, reason_case=dirty_rope)
    clean_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: clean_rope}
    }
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_kegroot_factunits_dict() != clean_facts_dict
    assert bob_plan.get_kegroot_factunits_dict() == {}
    assert bob_plan.to_dict() == before_bob_plan.to_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, clean_facts_dict)

    # THEN
    assert bob_plan.to_dict() != before_bob_plan.to_dict()
    assert bob_plan.get_kegroot_factunits_dict() == clean_facts_dict
    assert bob_plan.get_keg_obj(clean_rope)


def test_set_factunits_to_plan_ReturnsObj_Scenario3_FactUnit_reason_context_Withoutreason_contextNotAddedToPlan():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, exx.mop)
    bob_plan.add_keg(floor_rope)
    # bob_plan.add_keg(clean_rope)
    bob_plan.add_keg(dirty_rope)
    bob_plan.add_keg(mop_rope, pledge=True)
    bob_plan.edit_keg_attr(mop_rope, reason_context=floor_rope, reason_case=dirty_rope)

    weather_str = "weather"
    raining_str = "raining"
    weather_rope = bob_plan.make_l1_rope(weather_str)
    rain_rope = bob_plan.make_rope(weather_rope, raining_str)

    two_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: clean_rope},
        weather_rope: {kw.fact_context: weather_rope, kw.fact_state: rain_rope},
    }
    before_bob_plan = copy_deepcopy(bob_plan)
    assert bob_plan.get_kegroot_factunits_dict() != two_facts_dict
    assert bob_plan.get_kegroot_factunits_dict() == {}
    assert bob_plan.to_dict() == before_bob_plan.to_dict()

    # WHEN
    set_factunits_to_plan(bob_plan, two_facts_dict)

    # THEN
    assert floor_rope in set(bob_plan.get_kegroot_factunits_dict().keys())
    assert weather_rope not in set(bob_plan.get_kegroot_factunits_dict().keys())
    assert bob_plan.to_dict() != before_bob_plan.to_dict()


def test_clear_factunits_from_plan_ReturnsObj_Scenario1_FactUnit_Exist():
    # ESTABLISH
    bob_plan = planunit_shop("Bob", exx.a23)
    floor_str = "floor situation"
    dirty_str = "dirty"
    casa_rope = bob_plan.make_l1_rope(exx.casa)
    floor_rope = bob_plan.make_rope(casa_rope, floor_str)
    clean_rope = bob_plan.make_rope(floor_rope, exx.clean)
    dirty_rope = bob_plan.make_rope(floor_rope, dirty_str)
    mop_rope = bob_plan.make_rope(casa_rope, exx.mop)
    bob_plan.add_keg(floor_rope)
    # bob_plan.add_keg(clean_rope)
    bob_plan.add_keg(dirty_rope)
    bob_plan.add_keg(mop_rope, pledge=True)
    bob_plan.edit_keg_attr(mop_rope, reason_context=floor_rope, reason_case=dirty_rope)
    bob_plan.add_fact(floor_rope, dirty_rope)
    floor_facts_dict = {
        floor_rope: {kw.fact_context: floor_rope, kw.fact_state: dirty_rope}
    }
    assert bob_plan.get_kegroot_factunits_dict() == floor_facts_dict
    assert bob_plan.get_kegroot_factunits_dict() != {}

    # WHEN
    clear_factunits_from_plan(bob_plan)

    # THEN
    assert bob_plan.get_kegroot_factunits_dict() != floor_facts_dict
    assert bob_plan.get_kegroot_factunits_dict() == {}
