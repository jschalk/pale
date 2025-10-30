from pytest import raises as pytest_raises
from src.ch16_rose.map import labelmap_shop
from src.ch16_rose.rose_main import roseunit_shop
from src.ref.keywords import ExampleStrs as exx


def test_RoseUnit_set_labelmap_SetsAttr():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    x_labelmap = labelmap_shop(face_name=exx.sue)
    x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    assert sue_roseunit.labelmap != x_labelmap

    # WHEN
    sue_roseunit.set_labelmap(x_labelmap)

    # THEN
    assert sue_roseunit.labelmap == x_labelmap


def test_RoseUnit_set_labelmap_RaisesErrorIf_labelmap_otx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_otx_knot = "/"
    x_labelmap = labelmap_shop(otx_knot=slash_otx_knot, face_name=exx.sue)
    assert sue_roseunit.otx_knot != x_labelmap.otx_knot
    assert sue_roseunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: RoseUnit otx_knot is '{sue_roseunit.otx_knot}', MapCore is '{slash_otx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_labelmap_RaisesErrorIf_labelmap_inx_knot_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    slash_inx_knot = "/"
    x_labelmap = labelmap_shop(inx_knot=slash_inx_knot, face_name=exx.sue)
    assert sue_roseunit.inx_knot != x_labelmap.inx_knot
    assert sue_roseunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: RoseUnit inx_knot is '{sue_roseunit.inx_knot}', MapCore is '{slash_inx_knot}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_labelmap_RaisesErrorIf_labelmap_unknown_str_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    casa_unknown_str = "Unknown_casa"
    x_labelmap = labelmap_shop(unknown_str=casa_unknown_str, face_name=exx.sue)
    assert sue_roseunit.unknown_str != x_labelmap.unknown_str
    assert sue_roseunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: RoseUnit unknown_str is '{sue_roseunit.unknown_str}', MapCore is '{casa_unknown_str}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_set_labelmap_RaisesErrorIf_labelmap_face_name_IsNotSame():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    x_labelmap = labelmap_shop(face_name=exx.yao)
    assert sue_roseunit.face_name != x_labelmap.face_name
    assert sue_roseunit.labelmap != x_labelmap

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_roseunit.set_labelmap(x_labelmap)
    exception_str = f"set_mapcore Error: RoseUnit face_name is '{sue_roseunit.face_name}', MapCore is '{exx.yao}'."
    assert str(excinfo.value) == exception_str


def test_RoseUnit_get_labelmap_ReturnsObj():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)
    static_x_labelmap = labelmap_shop(face_name=exx.sue)
    static_x_labelmap.set_otx2inx("Bob", "Bob of Portland")
    sue_roseunit.set_labelmap(static_x_labelmap)

    # WHEN
    gen_x_labelmap = sue_roseunit.get_labelmap()

    # THEN
    assert gen_x_labelmap == static_x_labelmap


def test_RoseUnit_set_label_SetsAttr_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)
    labelid_labelmap = zia_roseunit.get_labelmap()
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx) is False

    # WHEN
    zia_roseunit.set_roadmap_label(sue_otx, sue_inx)

    # THEN
    assert labelid_labelmap.otx2inx_exists(sue_otx, sue_inx)


def test_RoseUnit_del_roadmap_label_ReturnsObj():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suita"
    zia_roseunit = roseunit_shop(exx.zia)

    zia_roseunit.set_roadmap_label(sue_otx, sue_inx)
    zia_roseunit.set_roadmap_label(exx.zia, exx.zia)
    assert zia_roseunit.roadmap_label_exists(sue_otx, sue_inx)
    assert zia_roseunit.roadmap_label_exists(exx.zia, exx.zia)

    # WHEN
    zia_roseunit.del_roadmap_label(sue_otx)

    # THEN
    assert zia_roseunit.roadmap_label_exists(sue_otx, sue_inx) is False
    assert zia_roseunit.roadmap_label_exists(exx.zia, exx.zia)
