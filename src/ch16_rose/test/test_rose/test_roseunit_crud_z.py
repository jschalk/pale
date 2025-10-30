from pytest import raises as pytest_raises
from src.ch16_rose.map import namemap_shop, ropemap_shop
from src.ch16_rose.rose_term import roseunit_shop
from src.ch16_rose.test._util.ch16_examples import (
    get_clean_ropemap,
    get_invalid_namemap,
    get_invalid_ropemap,
    get_invalid_titlemap,
    get_suita_namemap,
    get_swim_titlemap,
)
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_RoseUnit_set_mapunit_SetsAttr():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    namemap = namemap_shop(face_name=exx.sue)
    namemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_roseunit.namemap != namemap

    # WHEN
    sue_roseunit.set_namemap(namemap)

    # THEN
    assert sue_roseunit.namemap == namemap


def test_RoseUnit_set_mapunit_SetsAttr_SpecialSituation_RopeTerm():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    ropemap = ropemap_shop(face_name=exx.sue)
    ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_roseunit.ropemap != ropemap

    # WHEN
    sue_roseunit.set_ropemap(ropemap)

    # THEN
    assert sue_roseunit.ropemap == ropemap


def test_RoseUnit_set_mapunit_RaisesErrorIf_mapunit_otx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_otx_knot = "/"
    namemap = namemap_shop(otx_knot=slash_otx_knot, face_name=exx.sue)
    assert sue_roseunit.otx_knot != namemap.otx_knot
    assert sue_roseunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: RoseUnit otx_knot is '{sue_roseunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_mapunit_RaisesErrorIf_mapunit_inx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_inx_knot = "/"
    namemap = namemap_shop(inx_knot=slash_inx_knot, face_name=exx.sue)
    assert sue_roseunit.inx_knot != namemap.inx_knot
    assert sue_roseunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: RoseUnit inx_knot is '{sue_roseunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_mapunit_RaisesErrorIf_mapunit_unknown_str_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    namemap = namemap_shop(unknown_str=casa_unknown_str, face_name=exx.sue)
    assert sue_roseunit.unknown_str != namemap.unknown_str
    assert sue_roseunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: RoseUnit unknown_str is '{sue_roseunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_mapunit_RaisesErrorIf_mapunit_face_name_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    namemap = namemap_shop(face_name=exx.yao)
    assert sue_roseunit.face_name != namemap.face_name
    assert sue_roseunit.namemap != namemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_namemap(namemap)
    exception_str = f"set_mapcore Error: RoseUnit face_name is '{sue_roseunit.face_name}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_get_mapunit_ReturnsObj():
    # ESTABLISH
    sue_pu = roseunit_shop(exx.sue)
    static_namemap = namemap_shop(face_name=exx.sue)
    static_namemap.set_otx2inx("Bob", "Bob of Portland")
    sue_pu.set_namemap(static_namemap)

    # WHEN / THEN
    assert sue_pu.get_mapunit(kw.NameTerm) == sue_pu.namemap
    assert sue_pu.get_mapunit(kw.TitleTerm) == sue_pu.titlemap
    assert sue_pu.get_mapunit(kw.LabelTerm) == sue_pu.labelmap
    assert sue_pu.get_mapunit(kw.RopeTerm) == sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.EpochTime) == sue_pu.epochmap
    assert not sue_pu.get_mapunit("testing")

    assert sue_pu.get_mapunit(kw.NameTerm) != sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.TitleTerm) != sue_pu.ropemap
    assert sue_pu.get_mapunit(kw.LabelTerm) != sue_pu.ropemap


def test_RoseUnit_is_valid_ReturnsObj():
    # ESTABLISH
    invalid_namemap = get_invalid_namemap()
    invalid_titlemap = get_invalid_titlemap()
    invalid_labelmap = get_invalid_ropemap()
    valid_namemap = get_suita_namemap()
    valid_titlemap = get_swim_titlemap()
    valid_labelmap = get_clean_ropemap()
    assert valid_namemap.is_valid()
    assert valid_titlemap.is_valid()
    assert valid_labelmap.is_valid()
    assert invalid_labelmap.is_valid() is False
    assert invalid_titlemap.is_valid() is False
    assert invalid_namemap.is_valid() is False

    # WHEN / THEN
    sue_roseunit = roseunit_shop("Sue")
    assert sue_roseunit.is_valid()
    sue_roseunit.set_namemap(valid_namemap)
    sue_roseunit.set_titlemap(valid_titlemap)
    sue_roseunit.set_ropemap(valid_labelmap)
    assert sue_roseunit.is_valid()

    # WHEN / THEN
    sue_roseunit.set_namemap(invalid_namemap)
    assert sue_roseunit.is_valid() is False
    sue_roseunit.set_namemap(valid_namemap)
    assert sue_roseunit.is_valid()

    # WHEN / THEN
    sue_roseunit.set_titlemap(invalid_titlemap)
    assert sue_roseunit.is_valid() is False
    sue_roseunit.set_titlemap(valid_titlemap)
    assert sue_roseunit.is_valid()

    # WHEN / THEN
    sue_roseunit.set_ropemap(invalid_labelmap)
    assert sue_roseunit.is_valid() is False
    sue_roseunit.set_ropemap(valid_labelmap)
    assert sue_roseunit.is_valid()


def test_RoseUnit_set_otx2inx_SetsAttr_Scenario0_NameTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    namemap = zia_roseunit.get_namemap()
    assert namemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert namemap.otx2inx_exists(sue_otx, sue_inx)


def test_RoseUnit_set_otx2inx_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    ropemap = zia_roseunit.get_ropemap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_otx2inx(kw.RopeTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_RoseUnit_set_otx2inx_SetsAttr_Scenario2_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    ropemap = zia_roseunit.get_labelmap()
    assert ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_RoseUnit_set_otx2inx_SetsAttr_Scenario3_EpochTime():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epoch_diff = 10
    assert sue_roseunit._get_otx_epoch_diff(None) is None

    # WHEN
    sue_roseunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

    # THEN
    assert sue_roseunit._get_otx_epoch_diff(None) == sue_epoch_diff


def test_RoseUnit_otx2inx_exists_ReturnsObj_Scenario0_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    rope_type = kw.LabelTerm
    assert zia_roseunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)

    # THEN
    assert zia_roseunit.otx2inx_exists(rope_type, sue_otx, sue_inx)


def test_RoseUnit_otx2inx_exists_ReturnsObj_Scenario1_EpochTime():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epoch0_diff = 10
    sue_epoch1_diff = 11
    assert not sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
    assert not sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

    # WHEN
    sue_roseunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)

    # THEN
    assert sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
    assert not sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)


def test_RoseUnit_get_inx_value_ReturnsObj_Scenario0_NameTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    assert zia_roseunit._get_inx_value(kw.NameTerm, sue_otx) != sue_inx

    # WHEN
    zia_roseunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)

    # THEN
    assert zia_roseunit._get_inx_value(kw.NameTerm, sue_otx) == sue_inx


def test_RoseUnit_get_inx_value_ReturnsObj_Scenario1_EpochTerm():
    # ESTABLISH
    sue_epoch_diff = 10
    sue_roseunit = roseunit_shop(exx.sue)
    assert sue_roseunit._get_inx_value(kw.EpochTime, None) != sue_epoch_diff

    # WHEN
    sue_roseunit.set_otx2inx(kw.EpochTime, None, sue_epoch_diff)

    # THEN
    assert sue_roseunit._get_inx_value(kw.EpochTime, None) == sue_epoch_diff


def test_RoseUnit_del_otx2inx_ReturnsObj_Scenario0_LabelTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    rope_type = kw.LabelTerm
    zia_roseunit.set_otx2inx(kw.LabelTerm, sue_otx, sue_inx)
    zia_roseunit.set_otx2inx(kw.LabelTerm, exx.zia, exx.zia)
    assert zia_roseunit.otx2inx_exists(rope_type, sue_otx, sue_inx)
    assert zia_roseunit.otx2inx_exists(rope_type, exx.zia, exx.zia)

    # WHEN
    zia_roseunit.del_otx2inx(rope_type, sue_otx)

    # THEN
    assert zia_roseunit.otx2inx_exists(rope_type, sue_otx, sue_inx) is False
    assert zia_roseunit.otx2inx_exists(rope_type, exx.zia, exx.zia)


def test_RoseUnit_del_otx2inx_ReturnsObj_Scenario1_EpochTime():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    sue_epoch0_diff = 10
    sue_epoch1_diff = 11
    sue_roseunit.set_otx2inx(kw.EpochTime, None, sue_epoch0_diff)
    assert sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
    assert not sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)

    # WHEN
    sue_roseunit.del_otx2inx(kw.EpochTime, None)

    # THEN
    assert not sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch0_diff)
    assert not sue_roseunit.otx2inx_exists(kw.EpochTime, None, sue_epoch1_diff)


def test_RoseUnit_set_roadmap_label_SetsAttr_Scenario1_RopeTerm():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    ropemap = zia_roseunit.get_ropemap()
    assert ropemap.label_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert ropemap.label_exists(sue_otx, sue_inx)


def test_RoseUnit_roadmap_label_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    sue_exists = zia_roseunit.roadmap_label_exists(sue_otx, sue_inx)
    assert sue_exists is False

    # WHEN
    zia_roseunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert zia_roseunit.roadmap_label_exists(sue_otx, sue_inx)
