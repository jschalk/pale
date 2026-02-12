from src.ch04_rope.rope import to_rope
from src.ch06_keg.keg import kegunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_with_4_levels_and_2reasons,
)
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_UnitDoesNotErrorWithEmptyPersonUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    assert not root_keg.begin
    assert not root_keg.close
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not root_keg.begin
    assert not root_keg.close
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_DoesNotErrorWhenThereAreNoRangeKegs():
    # ESTABLISH
    yao_person = get_personunit_with_4_levels_and_2reasons()
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    assert not root_keg.gogo_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not root_keg.gogo_calc


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_SimpleLabel():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_begin = 7
    ziet0_close = 31
    yao_person.edit_keg_attr(root_rope, begin=ziet0_begin, close=ziet0_close)
    yao_person._set_keg_dict()
    root_keg = yao_person.get_keg_obj(root_rope)
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.gogo_calc == ziet0_begin
    assert root_keg.stop_calc == ziet0_close


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_begin = 6
    ziet0_close = 21
    ziet0_denom = 3
    yao_person.edit_keg_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        denom=ziet0_denom,
    )
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.denom == ziet0_denom
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.gogo_calc == ziet0_begin / ziet0_denom
    assert root_keg.stop_calc == ziet0_close / ziet0_denom
    assert root_keg.gogo_calc == 2
    assert root_keg.stop_calc == 7


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_begin = 6
    ziet0_close = 18
    ziet0_numor = 7
    ziet0_denom = 3
    yao_person.edit_keg_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        numor=ziet0_numor,
        denom=ziet0_denom,
    )
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.numor == ziet0_numor
    assert root_keg.denom == ziet0_denom
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.gogo_calc == (ziet0_begin * ziet0_numor) / ziet0_denom
    assert root_keg.stop_calc == (ziet0_close * ziet0_numor) / ziet0_denom
    assert root_keg.gogo_calc == 14
    assert root_keg.stop_calc == 42


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_begin = 6
    ziet0_close = 18
    ziet0_addin = 7
    yao_person.edit_keg_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        addin=ziet0_addin,
    )
    yao_person._set_keg_dict()
    root_keg = yao_person.get_keg_obj(root_rope)
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.addin == ziet0_addin
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.gogo_calc == ziet0_begin + ziet0_addin
    assert root_keg.stop_calc == ziet0_close + ziet0_addin
    assert root_keg.gogo_calc == 13
    assert root_keg.stop_calc == 25


def test_PersonUnit_set_kegtree_range_attrs_SetsInitialKeg_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_begin = 6
    ziet0_close = 18
    ziet0_denom = 3
    ziet0_addin = 60
    yao_person.edit_keg_attr(
        root_rope,
        begin=ziet0_begin,
        close=ziet0_close,
        denom=ziet0_denom,
        addin=ziet0_addin,
    )
    yao_person._set_keg_dict()
    root_keg = yao_person.get_keg_obj(root_rope)
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.denom == ziet0_denom
    assert root_keg.addin == ziet0_addin
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert root_keg.begin == ziet0_begin
    assert root_keg.close == ziet0_close
    assert root_keg.gogo_calc == (ziet0_begin + ziet0_addin) / ziet0_denom
    assert root_keg.stop_calc == (ziet0_close + ziet0_addin) / ziet0_denom
    assert root_keg.gogo_calc == 22
    assert root_keg.stop_calc == 26


def test_PersonUnit_set_kegtree_range_attrs_SetsDescendentKeg_gogo_calc_stop_calc_Simple0():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 7
    ziet0_close = 31
    ziet0_keg = kegunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    yao_person.set_keg_obj(kegunit_shop(ziet1_str), ziet0_rope)
    ziet1_keg = yao_person.get_keg_obj(ziet1_rope)
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert not ziet1_keg.gogo_calc
    assert not ziet1_keg.stop_calc
    assert yao_person.range_inheritors == {}

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert not ziet1_keg.begin
    assert not ziet1_keg.close
    assert ziet1_keg.gogo_calc == ziet0_begin
    assert ziet1_keg.stop_calc == ziet0_close
    assert yao_person.range_inheritors == {ziet1_rope: ziet0_rope}


def test_PersonUnit_set_kegtree_range_attrs_SetsDescendentKeg_gogo_calc_stop_calc_LabelWith_denom():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 14
    ziet0_close = 35
    ziet0_keg = kegunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_denom = 7
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    yao_person.set_keg_obj(kegunit_shop(ziet1_str, denom=ziet1_denom), ziet0_rope)
    ziet1_keg = yao_person.get_keg_obj(ziet1_rope)
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert not ziet1_keg.gogo_calc
    assert not ziet1_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not ziet1_keg.begin
    assert not ziet1_keg.close
    assert ziet1_keg.gogo_calc == ziet0_begin / ziet1_denom
    assert ziet1_keg.stop_calc == ziet0_close / ziet1_denom
    assert ziet1_keg.gogo_calc == 2
    assert ziet1_keg.stop_calc == 5


def test_PersonUnit_set_kegtree_range_attrs_SetsDescendentKeg_gogo_calc_stop_calc_LabelWith_denom_numor():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 14
    ziet0_close = 35
    ziet0_keg = kegunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_denom = 7
    ziet1_numor = 3
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    temp_keg = kegunit_shop(ziet1_str, numor=ziet1_numor, denom=ziet1_denom)
    yao_person.set_keg_obj(temp_keg, ziet0_rope)
    ziet1_keg = yao_person.get_keg_obj(ziet1_rope)
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert not ziet1_keg.gogo_calc
    assert not ziet1_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not ziet1_keg.begin
    assert not ziet1_keg.close
    assert ziet1_keg.gogo_calc == (ziet0_begin * ziet1_numor) / ziet1_denom
    assert ziet1_keg.stop_calc == (ziet0_close * ziet1_numor) / ziet1_denom
    assert ziet1_keg.gogo_calc == 6
    assert ziet1_keg.stop_calc == 15


def test_PersonUnit_set_kegtree_range_attrs_SetsDescendentKeg_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 3
    ziet0_close = 7
    ziet0_keg = kegunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_addin = 5
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    temp_keg = kegunit_shop(ziet1_str, addin=ziet1_addin)
    yao_person.set_keg_obj(temp_keg, ziet0_rope)
    ziet1_keg = yao_person.get_keg_obj(ziet1_rope)
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert ziet1_keg.addin == ziet1_addin
    assert not ziet1_keg.gogo_calc
    assert not ziet1_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not ziet1_keg.begin
    assert not ziet1_keg.close
    assert ziet1_keg.gogo_calc == ziet0_keg.gogo_calc + ziet1_addin
    assert ziet1_keg.stop_calc == ziet0_keg.stop_calc + ziet1_addin
    assert ziet1_keg.gogo_calc == 8
    assert ziet1_keg.stop_calc == 12


def test_PersonUnit_set_kegtree_range_attrs_Sets2LevelsDescendentKeg_gogo_calc_stop_calc_LabelWith_addin():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 3
    ziet0_close = 7
    ziet0_keg = kegunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    yao_person.add_keg(ziet1_rope)
    ziet2_str = "ziet2"
    ziet2_rope = yao_person.make_rope(ziet1_rope, ziet2_str)
    ziet2_addin = 5
    x_ziet2_keg = kegunit_shop(ziet2_str, addin=ziet2_addin)
    yao_person.set_keg_obj(x_ziet2_keg, ziet1_rope)
    ziet2_keg = yao_person.get_keg_obj(ziet2_rope)
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet2_keg.begin != ziet0_begin
    assert ziet2_keg.close != ziet0_close
    assert ziet2_keg.addin == ziet2_addin
    assert not ziet2_keg.gogo_calc
    assert not ziet2_keg.stop_calc
    assert yao_person.range_inheritors == {}

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not ziet2_keg.begin
    assert not ziet2_keg.close
    assert ziet2_keg.gogo_calc == ziet0_keg.gogo_calc + ziet2_addin
    assert ziet2_keg.stop_calc == ziet0_keg.stop_calc + ziet2_addin
    assert ziet2_keg.gogo_calc == 8
    assert ziet2_keg.stop_calc == 12
    assert yao_person.range_inheritors == {
        ziet1_rope: ziet0_rope,
        ziet2_rope: ziet0_rope,
    }


def test_PersonUnit_set_kegtree_range_attrs_SetsDescendentKeg_gogo_calc_stop_calc_LabelWith_denom_addin():
    # ESTABLISH
    yao_person = personunit_shop("Yao")
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 21
    ziet0_close = 35
    ziet0_keg = kegunit_shop(ziet0_str, begin=ziet0_begin, close=ziet0_close)
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_addin = 70
    ziet1_denom = 7
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    temp_keg = kegunit_shop(ziet1_str, denom=ziet1_denom, addin=ziet1_addin)
    yao_person.set_keg_obj(temp_keg, ziet0_rope)
    ziet1_keg = yao_person.get_keg_obj(ziet1_rope)
    root_rope = yao_person.kegroot.get_keg_rope()
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert ziet1_keg.addin == ziet1_addin
    assert not ziet1_keg.gogo_calc
    assert not ziet1_keg.stop_calc

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert not ziet1_keg.begin
    assert not ziet1_keg.close
    assert ziet1_keg.gogo_calc == (ziet0_keg.gogo_calc + ziet1_addin) / ziet1_denom
    assert ziet1_keg.stop_calc == (ziet0_keg.stop_calc + ziet1_addin) / ziet1_denom
    assert ziet1_keg.gogo_calc == 13
    assert ziet1_keg.stop_calc == 15


def test_PersonUnit_set_kegtree_range_attrs_SetsDescendentKeg_When_knot_IsNonDefault():
    # ESTABLISH
    yao_person = personunit_shop("Yao", knot=exx.slash)
    root_rope = yao_person.kegroot.get_keg_rope()
    ziet0_str = "ziet0"
    ziet0_rope = yao_person.make_l1_rope(ziet0_str)
    ziet0_begin = 7
    ziet0_close = 31
    ziet0_keg = kegunit_shop(
        ziet0_str, begin=ziet0_begin, close=ziet0_close, knot=exx.slash
    )
    yao_person.set_l1_keg(ziet0_keg)

    ziet1_str = "ziet1"
    ziet1_rope = yao_person.make_rope(ziet0_rope, ziet1_str)
    yao_person.set_keg_obj(kegunit_shop(ziet1_str), ziet0_rope)
    ziet1_keg = yao_person.get_keg_obj(ziet1_rope)
    root_keg = yao_person.get_keg_obj(root_rope)
    yao_person._set_keg_dict()
    assert not root_keg.gogo_calc
    assert not root_keg.stop_calc
    assert ziet0_keg.begin == ziet0_begin
    assert ziet0_keg.close == ziet0_close
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert not ziet1_keg.gogo_calc
    assert not ziet1_keg.stop_calc
    assert yao_person.range_inheritors == {}

    # WHEN
    yao_person._set_kegtree_range_attrs()

    # THEN
    assert ziet1_keg.begin != ziet0_begin
    assert ziet1_keg.close != ziet0_close
    assert not ziet1_keg.begin
    assert not ziet1_keg.close
    assert ziet1_keg.gogo_calc == ziet0_begin
    assert ziet1_keg.stop_calc == ziet0_close
    assert yao_person.range_inheritors == {ziet1_rope: ziet0_rope}
