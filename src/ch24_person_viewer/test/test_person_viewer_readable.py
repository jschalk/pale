from src.ch07_person_logic.person_main import personunit_shop
from src.ch24_person_viewer.person_viewer_tool import (
    get_keg_view_dict,
    get_person_view_dict,
)
from src.ref.keywords import Ch24Keywords as kw, ExampleStrs as exx


def test_get_person_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_believer = personunit_shop(exx.sue)
    sue_believer.cashout()

    # WHEN
    sue_person_view_dict = get_person_view_dict(sue_believer)

    # THEN
    assert set(sue_person_view_dict.keys()) == {
        # kw.groupunits,
        kw.partners,
        kw.kegroot,
    }
    sue_keg_view_dict = sue_person_view_dict.get(kw.kegroot)
    expected_sue_keg_view_dict = get_keg_view_dict(sue_believer.kegroot)
    assert sue_keg_view_dict == expected_sue_keg_view_dict
