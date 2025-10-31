from src.ch04_rope.rope import default_knot_if_None
from src.ch16_rose.rose_config import default_unknown_str_if_None
from src.ch16_rose.rose_term import (
    _get_rid_of_rose_core_keys,
    get_roseunit_from_dict,
    roseunit_shop,
)
from src.ch16_rose.test._util.ch16_examples import (
    get_slash_labelmap,
    get_slash_namemap,
    get_slash_ropemap,
    get_slash_titlemap,
)
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_RoseUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_roseunit = roseunit_shop(exx.sue)

    # WHEN
    sue_dict = sue_roseunit.to_dict()

    # THEN
    print(sue_dict)
    assert sue_dict
    assert sue_dict.get(kw.face_name) == exx.sue
    assert sue_dict.get(kw.spark_num) == sue_roseunit.spark_num
    assert sue_dict.get(kw.otx_knot) == default_knot_if_None()
    assert sue_dict.get(kw.inx_knot) == default_knot_if_None()
    assert sue_dict.get(kw.unknown_str) == default_unknown_str_if_None()
    sue_namemap = sue_roseunit.namemap.to_dict()
    sue_titlemap = sue_roseunit.titlemap.to_dict()
    sue_labelmap = sue_roseunit.labelmap.to_dict()
    sue_ropemap = sue_roseunit.ropemap.to_dict()
    assert sue_dict.get(kw.namemap) == _get_rid_of_rose_core_keys(sue_namemap)
    assert sue_dict.get(kw.titlemap) == _get_rid_of_rose_core_keys(sue_titlemap)
    assert sue_dict.get(kw.labelmap) == _get_rid_of_rose_core_keys(sue_labelmap)
    assert sue_dict.get(kw.ropemap) == _get_rid_of_rose_core_keys(sue_ropemap)
    assert sue_dict.keys() == sue_roseunit.__dict__.keys()


def test_RoseUnit_to_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_roseunit = roseunit_shop(
        exx.sue, 0, slash_otx_knot, colon_inx_knot, x_unknown_str
    )
    sue_roseunit.set_namemap(get_slash_namemap())
    sue_roseunit.set_titlemap(get_slash_titlemap())
    sue_roseunit.set_labelmap(get_slash_labelmap())
    sue_roseunit.set_ropemap(get_slash_ropemap())

    # WHEN
    sue_dict = sue_roseunit.to_dict()

    # THEN
    assert sue_dict.get(kw.face_name) == exx.sue
    assert sue_dict.get(kw.otx_knot) == slash_otx_knot
    assert sue_dict.get(kw.inx_knot) == colon_inx_knot
    assert sue_dict.get(kw.unknown_str) == x_unknown_str
    sue_namemap = sue_roseunit.namemap.to_dict()
    sue_titlemap = sue_roseunit.titlemap.to_dict()
    sue_labelmap = sue_roseunit.labelmap.to_dict()
    sue_ropemap = sue_roseunit.ropemap.to_dict()
    assert sue_dict.get(kw.namemap) == _get_rid_of_rose_core_keys(sue_namemap)
    assert sue_dict.get(kw.titlemap) == _get_rid_of_rose_core_keys(sue_titlemap)
    assert sue_dict.get(kw.labelmap) == _get_rid_of_rose_core_keys(sue_labelmap)
    assert sue_dict.get(kw.ropemap) == _get_rid_of_rose_core_keys(sue_ropemap)


def test_get_roseunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_spark_num = 7
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_roseunit = roseunit_shop(
        exx.sue,
        sue_spark_num,
        slash_otx_knot,
        colon_inx_knot,
        x_unknown_str,
    )
    sue_roseunit.set_namemap(get_slash_namemap())
    sue_roseunit.set_labelmap(get_slash_labelmap())
    sue_roseunit.set_ropemap(get_slash_ropemap())
    sue_roseunit.set_titlemap(get_slash_titlemap())

    # WHEN
    gen_roseunit = get_roseunit_from_dict(sue_roseunit.to_dict())

    # THEN
    assert gen_roseunit
    assert gen_roseunit.face_name == exx.sue
    assert gen_roseunit.spark_num == sue_spark_num
    assert gen_roseunit.otx_knot == slash_otx_knot
    assert gen_roseunit.inx_knot == colon_inx_knot
    assert gen_roseunit.unknown_str == x_unknown_str
    assert gen_roseunit.namemap == get_slash_namemap()
    assert gen_roseunit.ropemap == get_slash_ropemap()
    assert gen_roseunit.titlemap == get_slash_titlemap()
