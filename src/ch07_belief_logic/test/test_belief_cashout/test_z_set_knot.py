from pytest import raises as pytest_raises
from src.ch04_rope.rope import create_rope
from src.ch05_reason.reason import factunit_shop, reasonunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ref.keywords import ExampleStrs as exx


def test_BeliefUnit_set_plan_SetsAttrs_Scenario0_fund_grain():
    # ESTABLISH'
    x_fund_grain = 500
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.fund_grain = x_fund_grain
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, "cleaning")
    cuisine_plan = planunit_shop("cuisine to use")
    assert cuisine_plan.fund_grain != x_fund_grain

    # WHEN
    sue_belief.set_plan_obj(cuisine_plan, clean_rope)

    # THEN
    assert cuisine_plan.fund_grain == x_fund_grain


def test_belief_set_knot_RaisesErrorIfNew_knot_IsAnPlan_label():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    print(f"{zia_belief.max_tree_traverse=}")
    casa_rope = zia_belief.make_l1_rope(exx.casa)
    zia_belief.set_l1_plan(planunit_shop(exx.casa))
    casa_str = f"casa cuisine{exx.slash}clean"
    zia_belief.set_plan_obj(planunit_shop(casa_str), parent_rope=casa_rope)

    # WHEN / THEN
    casa_rope = zia_belief.make_rope(casa_rope, casa_str)
    print(f"{casa_rope=}")
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_knot(exx.slash)
    assert (
        str(excinfo.value)
        == f"Cannot modify knot to '{exx.slash}' because it exists an plan plan_label '{casa_rope}'"
    )


def test_belief_set_knot_Modifies_parent_rope():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    zia_belief.set_l1_plan(planunit_shop(exx.casa))
    semicolon_casa_rope = zia_belief.make_l1_rope(exx.casa)
    zia_belief.set_plan_obj(planunit_shop(exx.cuisine), semicolon_casa_rope)
    semicolon_cuisine_rope = zia_belief.make_rope(semicolon_casa_rope, exx.cuisine)
    cuisine_plan = zia_belief.get_plan_obj(semicolon_cuisine_rope)
    semicolon_str = ";"
    assert zia_belief.knot == semicolon_str
    semicolon_cuisine_rope = zia_belief.make_rope(semicolon_casa_rope, exx.cuisine)
    # print(f"{cuisine_plan.parent_rope=} {cuisine_plan.plan_label=}")
    # semicolon_casa_plan = zia_belief.get_plan_obj(semicolon_casa_rope)
    # print(f"{semicolon_casa_plan.parent_rope=} {semicolon_casa_plan.plan_label=}")
    assert cuisine_plan.get_plan_rope() == semicolon_cuisine_rope

    # WHEN
    zia_belief.set_knot(exx.slash)

    # THEN
    assert cuisine_plan.get_plan_rope() != semicolon_cuisine_rope
    zia_moment_label = zia_belief.planroot.plan_label
    slash_casa_rope = create_rope(zia_moment_label, exx.casa, knot=exx.slash)
    slash_cuisine_rope = create_rope(slash_casa_rope, exx.cuisine, knot=exx.slash)
    assert cuisine_plan.get_plan_rope() == slash_cuisine_rope


def test_belief_set_knot_ModifiesReasonUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    zia_belief.set_l1_plan(planunit_shop(exx.casa))
    ziet_str = "ziet"
    semicolon_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_belief.make_rope(semicolon_ziet_rope, _8am_str)

    semicolon_ziet_reasonunit = reasonunit_shop(reason_context=semicolon_ziet_rope)
    semicolon_ziet_reasonunit.set_case(semicolon_8am_rope)

    semicolon_casa_rope = zia_belief.make_l1_rope(exx.casa)
    zia_belief.edit_plan_attr(semicolon_casa_rope, reason=semicolon_ziet_reasonunit)
    casa_plan = zia_belief.get_plan_obj(semicolon_casa_rope)
    assert casa_plan.reasonunits.get(semicolon_ziet_rope) is not None
    gen_ziet_reasonunit = casa_plan.reasonunits.get(semicolon_ziet_rope)
    assert gen_ziet_reasonunit.cases.get(semicolon_8am_rope) is not None

    # WHEN
    zia_belief.set_knot(exx.slash)

    # THEN
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_8am_rope = zia_belief.make_rope(slash_ziet_rope, _8am_str)
    slash_casa_rope = zia_belief.make_l1_rope(exx.casa)
    casa_plan = zia_belief.get_plan_obj(slash_casa_rope)
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_8am_rope = zia_belief.make_rope(slash_ziet_rope, _8am_str)
    assert casa_plan.reasonunits.get(slash_ziet_rope) is not None
    gen_ziet_reasonunit = casa_plan.reasonunits.get(slash_ziet_rope)
    assert gen_ziet_reasonunit.cases.get(slash_8am_rope) is not None

    assert casa_plan.reasonunits.get(semicolon_ziet_rope) is None
    assert gen_ziet_reasonunit.cases.get(semicolon_8am_rope) is None


def test_belief_set_knot_ModifiesFactUnit():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia", "Texas")
    zia_belief.set_l1_plan(planunit_shop(exx.casa))
    ziet_str = "ziet"
    semicolon_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    _8am_str = "8am"
    semicolon_8am_rope = zia_belief.make_rope(semicolon_ziet_rope, _8am_str)
    semicolon_ziet_factunit = factunit_shop(semicolon_ziet_rope, semicolon_8am_rope)

    semicolon_casa_rope = zia_belief.make_l1_rope(exx.casa)
    zia_belief.edit_plan_attr(semicolon_casa_rope, factunit=semicolon_ziet_factunit)
    casa_plan = zia_belief.get_plan_obj(semicolon_casa_rope)
    print(f"{casa_plan.factunits=} {semicolon_ziet_rope=}")
    assert casa_plan.factunits.get(semicolon_ziet_rope) is not None
    gen_ziet_factunit = casa_plan.factunits.get(semicolon_ziet_rope)

    # WHEN
    zia_belief.set_knot(exx.slash)

    # THEN
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_casa_rope = zia_belief.make_l1_rope(exx.casa)
    casa_plan = zia_belief.get_plan_obj(slash_casa_rope)
    slash_ziet_rope = zia_belief.make_l1_rope(ziet_str)
    slash_8am_rope = zia_belief.make_rope(slash_ziet_rope, _8am_str)
    assert casa_plan.factunits.get(slash_ziet_rope) is not None
    gen_ziet_factunit = casa_plan.factunits.get(slash_ziet_rope)
    assert gen_ziet_factunit.fact_context is not None
    assert gen_ziet_factunit.fact_context == slash_ziet_rope
    assert gen_ziet_factunit.fact_state is not None
    assert gen_ziet_factunit.fact_state == slash_8am_rope

    assert casa_plan.factunits.get(semicolon_ziet_rope) is None


def test_BeliefUnit_set_knot_SetsAttr():
    # ESTABLISH
    a45_str = "amy45"
    slash_knot = "/"
    sue_belief = beliefunit_shop(exx.sue, a45_str, knot=slash_knot)
    assert sue_belief.knot == slash_knot

    # WHEN
    at_label_knot = "@"
    sue_belief.set_knot(new_knot=at_label_knot)

    # THEN
    assert sue_belief.knot == at_label_knot
