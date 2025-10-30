from pytest import raises as pytest_raises
from src.ch16_rose.map import ropemap_shop
from src.ch16_rose.rose_main import roseunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_RoseUnit_set_ropemap_SetsAttr():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    x_ropemap = ropemap_shop(face_name=exx.sue)
    x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_roseunit.ropemap != x_ropemap

    # WHEN
    sue_roseunit.set_ropemap(x_ropemap)

    # THEN
    assert sue_roseunit.ropemap == x_ropemap


def test_RoseUnit_set_ropemap_RaisesErrorIf_ropemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_ropemap = ropemap_shop(otx_knot=slash_otx_knot, face_name=exx.sue)
    assert sue_roseunit.otx_knot != x_ropemap.otx_knot
    assert sue_roseunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: RoseUnit otx_knot is '{sue_roseunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_ropemap_RaisesErrorIf_ropemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_ropemap = ropemap_shop(inx_knot=slash_inx_knot, face_name=exx.sue)
    assert sue_roseunit.inx_knot != x_ropemap.inx_knot
    assert sue_roseunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: RoseUnit inx_knot is '{sue_roseunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_ropemap_RaisesErrorIf_ropemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_ropemap = ropemap_shop(unknown_str=casa_unknown_str, face_name=exx.sue)
    assert sue_roseunit.unknown_str != x_ropemap.unknown_str
    assert sue_roseunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: RoseUnit unknown_str is '{sue_roseunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_ropemap_RaisesErrorIf_ropemap_face_name_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    x_ropemap = ropemap_shop(face_name=exx.yao)
    assert sue_roseunit.face_name != x_ropemap.face_name
    assert sue_roseunit.ropemap != x_ropemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_ropemap(x_ropemap)
    exception_str = f"set_mapcore Error: RoseUnit face_name is '{sue_roseunit.face_name}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_get_ropemap_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    static_x_ropemap = ropemap_shop(face_name=exx.sue)
    static_x_ropemap.set_otx2inx("Bob", "Bob of Portland")
    sue_roseunit.set_ropemap(static_x_ropemap)

    # WHEN
    gen_x_ropemap = sue_roseunit.get_ropemap()

    # THEN
    assert gen_x_ropemap == static_x_ropemap


def test_RoseUnit_set_rope_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    ropeid_ropemap = zia_roseunit.get_ropemap()
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert ropeid_ropemap.otx2inx_exists(sue_otx, sue_inx)


def test_RoseUnit_rope_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)

    assert zia_roseunit.rope_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_roseunit.rope_exists(sue_otx, sue_inx)


def test_RoseUnit_get_inx_rope_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    assert zia_roseunit._get_inx_rope(sue_otx) != sue_inx

    # WHEN
    zia_roseunit.set_rope(sue_otx, sue_inx)

    # THEN
    assert zia_roseunit._get_inx_rope(sue_otx) == sue_inx


def test_RoseUnit_del_rope_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)

    zia_roseunit.set_rope(sue_otx, sue_inx)
    zia_roseunit.set_rope(exx.zia, exx.zia)
    assert zia_roseunit.rope_exists(sue_otx, sue_inx)
    assert zia_roseunit.rope_exists(exx.zia, exx.zia)

    # WHEN
    zia_roseunit.del_rope(sue_otx)

    # THEN
    assert zia_roseunit.rope_exists(sue_otx, sue_inx) is False
    assert zia_roseunit.rope_exists(exx.zia, exx.zia)
