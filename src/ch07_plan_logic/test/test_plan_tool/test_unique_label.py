from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch07_plan_logic.plan_tool import get_plan_unique_short_ropes
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_get_plan_unique_short_ropes_ReturnsObj_Scenario0_RootOnly():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)

    # WHEN
    unique_short_ropes = get_plan_unique_short_ropes(sue_plan)

    # THEN
    assert unique_short_ropes == {sue_plan.kegroot.get_keg_rope(): exx.a23}


def test_get_plan_unique_short_ropess_ReturnsObj_Scenario1_KegsWithUniqueLabels():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    mop_rope = sue_plan.make_rope(casa_rope, exx.mop)
    sue_plan.add_keg(mop_rope)

    # WHEN
    unique_short_ropes = get_plan_unique_short_ropes(sue_plan)

    # THEN
    root_rope = sue_plan.kegroot.get_keg_rope()
    assert unique_short_ropes == {
        root_rope: exx.a23,
        casa_rope: exx.casa,
        mop_rope: exx.mop,
    }


def test_get_plan_unique_short_ropess_ReturnsObj_Scenario2_KegsWithCommonLabels():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", exx.a23)
    casa_rope = sue_plan.make_l1_rope(exx.casa)
    casa_mop_rope = sue_plan.make_rope(casa_rope, exx.mop)
    sports_str = "sports"
    sports_rope = sue_plan.make_l1_rope(sports_str)
    sports_mop_rope = sue_plan.make_rope(sports_rope, exx.mop)
    sue_plan.add_keg(casa_mop_rope)
    sue_plan.add_keg(sports_mop_rope)

    # WHEN
    unique_short_ropes = get_plan_unique_short_ropes(sue_plan)

    # THEN
    root_rope = sue_plan.kegroot.get_keg_rope()
    knot = sue_plan.knot
    expected_short_casa_mop = f"{exx.casa}{knot}{exx.mop}"
    assert unique_short_ropes.get(casa_mop_rope) == expected_short_casa_mop
    assert unique_short_ropes == {
        root_rope: exx.a23,
        casa_rope: exx.casa,
        casa_mop_rope: expected_short_casa_mop,
        sports_rope: sports_str,
        sports_mop_rope: f"{sports_str}{knot}{exx.mop}",
    }
