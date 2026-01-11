from pytest import raises as pytest_raises
from src.ch04_rope.rope import create_rope
from src.ch06_keg.keg import kegunit_shop
from src.ref.keywords import Ch06Keywords as kw, ExampleStrs as exx


def test_get_kids_in_range_GetsCorrectKegs():
    # ESTABLISH
    mon_str = "months"
    mon_keg = kegunit_shop(mon_str, begin=0, close=366)
    jan_str = "Jan"
    feb_str = "Feb"
    mar_str = "Mar"
    mon_keg.add_kid(kegunit_shop(jan_str))
    mon_keg.add_kid(kegunit_shop(feb_str))
    mon_keg.add_kid(kegunit_shop(mar_str))
    jan_keg = mon_keg.get_kid(jan_str)
    feb_keg = mon_keg.get_kid(feb_str)
    mar_keg = mon_keg.get_kid(mar_str)
    jan_keg.gogo_calc = 0
    jan_keg.stop_calc = 31
    feb_keg.gogo_calc = 31
    feb_keg.stop_calc = 60
    mar_keg.gogo_calc = 60
    mar_keg.stop_calc = 91

    # WHEN / THEN
    assert len(mon_keg.get_kids_in_range(x_gogo=100, x_stop=120)) == 0
    assert len(mon_keg.get_kids_in_range(x_gogo=0, x_stop=31)) == 1
    assert len(mon_keg.get_kids_in_range(x_gogo=5, x_stop=5)) == 1
    assert len(mon_keg.get_kids_in_range(x_gogo=0, x_stop=61)) == 3
    assert len(mon_keg.get_kids_in_range(x_gogo=31, x_stop=31)) == 1
    assert set(mon_keg.get_kids_in_range(x_gogo=31, x_stop=31).keys()) == {feb_str}
    assert list(mon_keg.get_kids_in_range(x_gogo=31, x_stop=31).values()) == [feb_keg]


def test_get_kids_in_range_EmptyParametersReturnsAll_kids():
    # ESTABLISH
    mon_str = "366months"
    mon_keg = kegunit_shop(mon_str)
    jan_str = "Jan"
    feb29_str = "Feb29"
    mar_str = "Mar"
    mon_keg.add_kid(kegunit_shop(jan_str))
    mon_keg.add_kid(kegunit_shop(feb29_str))
    mon_keg.add_kid(kegunit_shop(mar_str))

    # WHEN / THEN
    assert len(mon_keg.get_kids_in_range()) == 3


def test_KegUnit_get_descendants_ReturnsNoRopeTerms():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)

    # WHEN
    nation_descendants = nation_keg.get_descendant_ropes_from_kids()

    # THEN
    assert nation_descendants == {}


def test_KegUnit_get_descendants_Returns3DescendantsRopeTerms():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)

    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    usa_keg = kegunit_shop(usa_str, parent_rope=nation_rope)
    nation_keg.add_kid(usa_keg)

    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    texas_keg = kegunit_shop(texas_str, parent_rope=usa_rope)
    usa_keg.add_kid(texas_keg)

    iowa_str = "Iowa"
    iowa_rope = create_rope(usa_rope, iowa_str)
    iowa_keg = kegunit_shop(iowa_str, parent_rope=usa_rope)
    usa_keg.add_kid(iowa_keg)

    # WHEN
    nation_descendants = nation_keg.get_descendant_ropes_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_rope) is not None
    assert nation_descendants.get(texas_rope) is not None
    assert nation_descendants.get(iowa_rope) is not None


def test_KegUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)
    nation_keg.add_kid(nation_keg)
    max_count = 1000

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        nation_keg.get_descendant_ropes_from_kids()
    assert (
        str(excinfo.value)
        == f"Keg '{nation_keg.get_keg_rope()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_KegUnit_clear_kids_SetsAttr():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)
    nation_keg.add_kid(kegunit_shop("USA", parent_rope=nation_rope))
    nation_keg.add_kid(kegunit_shop("France", parent_rope=nation_rope))
    assert len(nation_keg.kids) == 2

    # WHEN
    nation_keg.clear_kids()

    # THEN
    assert len(nation_keg.kids) == 0


def test_KegUnit_get_kid_ReturnsObj():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)

    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    nation_keg.add_kid(kegunit_shop(usa_str, parent_rope=nation_rope))

    france_str = "France"
    france_rope = create_rope(nation_rope, france_str)
    nation_keg.add_kid(kegunit_shop(france_str, parent_rope=nation_rope))
    assert len(nation_keg.kids) == 2

    # WHEN
    france_keg = nation_keg.get_kid(france_str)

    # THEN
    assert france_keg.keg_label == france_str


def test_KegUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)

    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    nation_keg.add_kid(kegunit_shop(usa_str, parent_rope=nation_rope))

    france_str = "France"
    france_rope = create_rope(nation_rope, france_str)
    nation_keg.add_kid(kegunit_shop(france_str, parent_rope=nation_rope))
    assert len(nation_keg.kids) == 2

    # WHEN
    nation_keg.del_kid(france_str)

    # THEN
    assert len(nation_keg.kids) == 1


def test_KegUnit_get_kids_star_sum_ReturnsObj_Scenario0():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)
    usa_str = "USA"
    usa_keg = kegunit_shop(usa_str, parent_rope=nation_rope)
    nation_keg.add_kid(usa_keg)
    france_str = "France"
    france_keg = kegunit_shop(france_str, parent_rope=nation_rope)
    nation_keg.add_kid(france_keg)

    # WHEN / THEN
    assert nation_keg.get_kids_star_sum() == 2


def test_KegUnit_get_kids_star_sum_ReturnsObj_Scenario1():
    # ESTABLISH
    amy_str = exx.a23
    nation_str = "nation"
    nation_rope = create_rope(amy_str, nation_str)
    nation_keg = kegunit_shop(nation_str, parent_rope=amy_str)
    usa_str = "USA"
    usa_keg = kegunit_shop(usa_str, star=0, parent_rope=nation_rope)
    nation_keg.add_kid(usa_keg)
    france_str = "France"
    france_keg = kegunit_shop(france_str, star=0, parent_rope=nation_rope)
    nation_keg.add_kid(france_keg)

    # WHEN / THEN
    assert nation_keg.get_kids_star_sum() == 0

    # WHEN
    france_str = "France"
    france_keg = kegunit_shop(france_str, star=3, parent_rope=nation_rope)
    nation_keg.add_kid(france_keg)

    # WHEN / THEN
    assert nation_keg.get_kids_star_sum() == 3
