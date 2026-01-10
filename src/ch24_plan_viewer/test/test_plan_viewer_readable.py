from src.ch07_plan_logic.plan_main import planunit_shop
from src.ch24_plan_viewer.plan_viewer_tool import get_keg_view_dict, get_plan_view_dict
from src.ref.keywords import Ch24Keywords as kw, ExampleStrs as exx


def test_get_plan_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_believer = planunit_shop(exx.sue)
    sue_believer.cashout()

    # WHEN
    sue_plan_view_dict = get_plan_view_dict(sue_believer)

    # THEN
    assert set(sue_plan_view_dict.keys()) == {
        # kw.groupunits,
        kw.persons,
        kw.kegroot,
    }
    sue_keg_view_dict = sue_plan_view_dict.get(kw.kegroot)
    expected_sue_keg_view_dict = get_keg_view_dict(sue_believer.kegroot)
    assert sue_keg_view_dict == expected_sue_keg_view_dict
