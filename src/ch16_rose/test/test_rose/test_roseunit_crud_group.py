from pytest import raises as pytest_raises
from src.ch16_rose.map import titlemap_shop
from src.ch16_rose.rose_main import roseunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_RoseUnit_set_titlemap_SetsAttr():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    x_titlemap = titlemap_shop(face_name=exx.sue)
    x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_roseunit.titlemap != x_titlemap

    # WHEN
    sue_roseunit.set_titlemap(x_titlemap)

    # THEN
    assert sue_roseunit.titlemap == x_titlemap


def test_RoseUnit_set_titlemap_RaisesErrorIf_titlemap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_titlemap = titlemap_shop(otx_knot=slash_otx_knot, face_name=exx.sue)
    assert sue_roseunit.otx_knot != x_titlemap.otx_knot
    assert sue_roseunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: RoseUnit otx_knot is '{sue_roseunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_titlemap_RaisesErrorIf_titlemap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_titlemap = titlemap_shop(inx_knot=slash_inx_knot, face_name=exx.sue)
    assert sue_roseunit.inx_knot != x_titlemap.inx_knot
    assert sue_roseunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: RoseUnit inx_knot is '{sue_roseunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_titlemap_RaisesErrorIf_titlemap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_titlemap = titlemap_shop(unknown_str=casa_unknown_str, face_name=exx.sue)
    assert sue_roseunit.unknown_str != x_titlemap.unknown_str
    assert sue_roseunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: RoseUnit unknown_str is '{sue_roseunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_titlemap_RaisesErrorIf_titlemap_face_name_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    x_titlemap = titlemap_shop(face_name=exx.yao)
    assert sue_roseunit.face_name != x_titlemap.face_name
    assert sue_roseunit.titlemap != x_titlemap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_titlemap(x_titlemap)
    exception_str = f"set_mapcore Error: RoseUnit face_name is '{sue_roseunit.face_name}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_get_titlemap_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    static_x_titlemap = titlemap_shop(face_name=exx.sue)
    static_x_titlemap.set_otx2inx("Bob", "Bob of Portland")
    sue_roseunit.set_titlemap(static_x_titlemap)

    # WHEN
    gen_x_titlemap = sue_roseunit.get_titlemap()

    # THEN
    assert gen_x_titlemap == static_x_titlemap


def test_RoseUnit_set_titleterm_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    voice_name_titlemap = zia_roseunit.get_titlemap()
    assert voice_name_titlemap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert voice_name_titlemap.otx2inx_exists(sue_otx, sue_inx)


def test_RoseUnit_titleterm_exists_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)

    assert zia_roseunit.titleterm_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_roseunit.titleterm_exists(sue_otx, sue_inx)


def test_RoseUnit_get_inx_title_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    assert zia_roseunit._get_inx_title(sue_otx) != sue_inx

    # WHEN
    zia_roseunit.set_titleterm(sue_otx, sue_inx)

    # THEN
    assert zia_roseunit._get_inx_title(sue_otx) == sue_inx


def test_RoseUnit_del_titleterm_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)

    zia_roseunit.set_titleterm(sue_otx, sue_inx)
    zia_roseunit.set_titleterm(exx.zia, exx.zia)
    assert zia_roseunit.titleterm_exists(sue_otx, sue_inx)
    assert zia_roseunit.titleterm_exists(exx.zia, exx.zia)

    # WHEN
    zia_roseunit.del_titleterm(sue_otx)

    # THEN
    assert zia_roseunit.titleterm_exists(sue_otx, sue_inx) is False
    assert zia_roseunit.titleterm_exists(exx.zia, exx.zia)
