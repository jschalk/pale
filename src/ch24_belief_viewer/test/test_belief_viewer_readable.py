from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch24_belief_viewer.belief_viewer_tool import (
    get_belief_view_dict,
    get_keg_view_dict,
)
from src.ref.keywords import Ch24Keywords as kw, ExampleStrs as exx


def test_get_belief_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_believer = beliefunit_shop(exx.sue)
    sue_believer.cashout()

    # WHEN
    sue_belief_view_dict = get_belief_view_dict(sue_believer)

    # THEN
    assert set(sue_belief_view_dict.keys()) == {
        # kw.groupunits,
        kw.voices,
        kw.kegroot,
    }
    sue_keg_view_dict = sue_belief_view_dict.get(kw.kegroot)
    expected_sue_keg_view_dict = get_keg_view_dict(sue_believer.kegroot)
    assert sue_keg_view_dict == expected_sue_keg_view_dict
