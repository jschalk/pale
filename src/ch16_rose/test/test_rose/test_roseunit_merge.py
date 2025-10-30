from pytest import raises as pytest_raises
from src.ch16_rose.rose_main import inherit_roseunit, roseunit_shop
from src.ch16_rose.test._util.ch16_examples import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_suita_namemap,
    get_swim_titlemap,
)
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario0_EmptyRoseUnits():
    # ESTABLISH
    old_roseunit = roseunit_shop(exx.sue, 0)
    new_roseunit = roseunit_shop(exx.sue, 1)

    # WHEN
    merged_roseunit = inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert merged_roseunit
    assert merged_roseunit == new_roseunit


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_roseunit = roseunit_shop(exx.sue, 0, otx_knot=slash_otx_knot)
    new_roseunit = roseunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    slash_otx_knot = "/"
    old_roseunit = roseunit_shop(exx.sue, 0, inx_knot=slash_otx_knot)
    new_roseunit = roseunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    old_roseunit = roseunit_shop(exx.sue, 0, unknown_str=x_unknown_str)
    new_roseunit = roseunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    old_roseunit = roseunit_shop(exx.sue, 0)
    new_roseunit = roseunit_shop(exx.bob, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_roseunit = roseunit_shop(exx.sue, 5)
    new_roseunit = roseunit_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert str(excinfo.value) == "older roseunit is not older"


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario6_namemap_Inherited():
    # ESTABLISH
    spark1 = 1
    old_roseunit = roseunit_shop(exx.sue, 0)
    old_roseunit.set_namemap(get_suita_namemap())
    old_roseunit.set_titlemap(get_swim_titlemap())
    old_roseunit.set_labelmap(get_clean_labelmap())
    old_roseunit.set_ropemap(get_clean_ropemap())
    new_roseunit = roseunit_shop(exx.sue, spark1)
    assert new_roseunit.namemap != get_suita_namemap()

    # WHEN
    merged_roseunit = inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert merged_roseunit
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.spark_num = spark1
    assert merged_roseunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.spark_num = spark1
    assert merged_roseunit.titlemap == merged_groupbrigde
    merged_labelbrigde = get_clean_labelmap()
    merged_labelbrigde.spark_num = spark1
    assert merged_roseunit.labelmap == merged_labelbrigde
    merged_ropebrigde = get_clean_ropemap()
    merged_ropebrigde.spark_num = spark1
    merged_ropebrigde.labelmap = merged_labelbrigde
    assert merged_roseunit.ropemap == merged_ropebrigde


def test_RoseUnit_inherit_roseunit_ReturnsObj_Scenario7_namemap_Inherited():
    # ESTABLISH
    spark1 = 1
    old_roseunit = roseunit_shop(exx.sue, 0)
    old_roseunit.set_namemap(get_suita_namemap())
    old_roseunit.set_titlemap(get_swim_titlemap())
    new_roseunit = roseunit_shop(exx.sue, spark1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_roseunit.set_otx2inx(kw.NameTerm, bob_otx, bob_inx)
    assert new_roseunit.namemap != get_suita_namemap()
    assert new_roseunit.nameterm_exists(bob_otx, bob_inx)

    # WHEN
    merged_roseunit = inherit_roseunit(old_roseunit, new_roseunit)

    # THEN
    assert merged_roseunit
    assert new_roseunit.nameterm_exists(bob_otx, bob_inx)
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.spark_num = spark1
    merged_voicebrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_roseunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.spark_num = spark1
    assert merged_roseunit.titlemap == merged_groupbrigde
