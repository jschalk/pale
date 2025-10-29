from numpy import int64 as numpy_int64
from pytest import raises as pytest_raises
from src.ch14_epoch.epoch_main import DEFAULT_EPOCH_LENGTH
from src.ch16_translate.map import (
    EpochMap,
    epochmap_shop,
    get_epochmap_from_dict,
    inherit_epochmap,
)
from src.ref.keywords import Ch16Keywords as kw, ExampleStrs as exx


def test_EpochMap_Exists():
    # ESTABLISH
    x_epochmap = EpochMap()

    # WHEN / THEN
    assert not x_epochmap.face_name
    assert not x_epochmap.spark_num
    assert not x_epochmap.otx2inx
    assert set(x_epochmap.__dict__.keys()) == {
        kw.face_name,
        kw.spark_num,
        kw.otx2inx,
    }


def test_EpochMap_set_all_otx2inx_SetsAttr_Scenario0():
    # ESTABLISH
    sue_epochmap = EpochMap(face_name=exx.sue)
    sue_inx_epoch_diff = 19
    sue_epoch_length = 100
    sue_otx2inx = {sue_epoch_length: sue_inx_epoch_diff}
    assert sue_epochmap.otx2inx != sue_otx2inx

    # WHEN
    sue_epochmap.set_all_otx2inx(sue_otx2inx)

    # THEN
    assert sue_epochmap.otx2inx == sue_otx2inx


def test_EpochMap_set_all_otx2inx_SetsAttr_Scenario1_WithParametersGreaterThan_epoch_length():
    # ESTABLISH
    sue_epochmap = EpochMap(face_name=exx.sue)
    sue_epoch_length = 500
    sue_inx_epoch_diff = 719
    static_sue_otx2inx = {sue_epoch_length: sue_inx_epoch_diff}
    assert sue_epochmap.otx2inx != static_sue_otx2inx

    # WHEN
    sue_epochmap.set_all_otx2inx(static_sue_otx2inx)

    # THEN
    expected_sue_otx2inx = {sue_epoch_length: sue_inx_epoch_diff % sue_epoch_length}
    assert sue_epochmap.otx2inx == expected_sue_otx2inx
    assert sue_epochmap.otx2inx == {500: 219}


def test_epochmap_shop_ReturnsObj_Scenario0():
    # ESTABLISH

    # WHEN
    sue_epochmap = epochmap_shop(exx.sue)

    # THEN
    assert sue_epochmap.face_name == exx.sue
    assert sue_epochmap.spark_num == 0
    assert sue_epochmap.otx2inx == {}


def test_epochmap_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    sue_epoch_length = 500
    sue_inx_epoch_diff = 11
    spark2 = 2
    x_otx2inx = {sue_epoch_length: sue_inx_epoch_diff}

    # WHEN
    sue_epochmap = epochmap_shop(exx.sue, spark2, otx2inx=x_otx2inx)

    # THEN
    assert sue_epochmap.face_name == exx.sue
    assert sue_epochmap.spark_num == spark2
    assert sue_epochmap.otx2inx == x_otx2inx
    assert sue_epochmap.otx2inx == {500: 11}


def test_epochmap_shop_ReturnsObj_Scenario2_WithParametersGreaterThan_epoch_length():
    # ESTABLISH
    sue_epoch_length = 500
    sue_inx_epoch_diff = 719
    spark2 = 2
    static_sue_otx2inx = {sue_epoch_length: sue_inx_epoch_diff}

    # WHEN
    sue_epochmap = epochmap_shop(exx.sue, spark2, static_sue_otx2inx)

    # THEN
    assert sue_epochmap.face_name == exx.sue
    assert sue_epochmap.spark_num == spark2
    assert sue_epochmap.otx2inx != static_sue_otx2inx
    expected_sue_otx2inx = {sue_epoch_length: sue_inx_epoch_diff % sue_epoch_length}
    assert sue_epochmap.otx2inx == expected_sue_otx2inx
    assert sue_epochmap.otx2inx == {500: 219}


def test_epochmap_shop_ReturnsObj_Scenario3_TranslateCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    spark7 = numpy_int64(7)
    sue_epoch_length = 123
    sue_inx_epoch_diff = 19
    x_otx2inx = {numpy_int64(sue_epoch_length): numpy_int64(sue_inx_epoch_diff)}

    # WHEN
    sue_epochmap = epochmap_shop(exx.sue, numpy_int64(spark7), otx2inx=x_otx2inx)

    # THEN
    assert sue_epochmap.face_name == exx.sue
    assert sue_epochmap.spark_num == spark7
    assert str(type(sue_epochmap.spark_num)) != "<class 'numpy.int64'>"
    assert str(type(sue_epochmap.spark_num)) == "<class 'int'>"
    assert sue_epochmap.otx2inx == x_otx2inx
    assert sue_epochmap.otx2inx == {sue_epoch_length: sue_inx_epoch_diff}


def test_epochmap_shop_ReturnsObj_Scenario4_otx2inx_HasNoneKey():
    # ESTABLISH
    sue_epoch_length = 123
    sue_inx_epoch_diff = 19
    sue_otx2inx = {sue_epoch_length: sue_inx_epoch_diff, None: sue_inx_epoch_diff}

    # WHEN
    sue_epochmap = epochmap_shop(exx.sue, None, sue_otx2inx)

    # THEN
    assert sue_epochmap.otx2inx == sue_otx2inx


def test_EpochMap_set_otx2inx_SetsAttr_Scenario0_key_Exists():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    assert sue_epochmap.otx2inx == {}

    # WHEN
    sue_epoch_length = 123
    sue_inx_epoch_diff = 19
    sue_epochmap.set_otx2inx(sue_epoch_length, sue_inx_epoch_diff)

    # THEN
    assert sue_epochmap.otx2inx == {sue_epoch_length: sue_inx_epoch_diff}


def test_EpochMap_set_otx2inx_SetsAttr_Scenario1_key_IsNone():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    assert sue_epochmap.otx2inx == {}

    # WHEN
    sue_inx_epoch_diff = 19
    sue_epochmap.set_otx2inx(None, sue_inx_epoch_diff)

    # THEN
    assert sue_epochmap.otx2inx == {None: sue_inx_epoch_diff}


def test_EpochMap_set_otx2inx_SetsAttr_Scenario2_ValueIsLargerThanKey():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    sue_inx_epoch_diff = 333
    sue_epochmap.set_otx2inx(None, sue_inx_epoch_diff)
    assert sue_epochmap.otx2inx == {None: sue_inx_epoch_diff}

    # WHEN
    sue_otx_epoch_length = 200
    sue_epochmap.set_otx2inx(sue_otx_epoch_length, sue_inx_epoch_diff)

    # THEN
    assert sue_epochmap.otx2inx != {sue_otx_epoch_length: sue_inx_epoch_diff}
    assert sue_epochmap.otx2inx == {None: 333, 200: 133}


def test_EpochMap_get_inx_value_ReturnsObj():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    sue_epoch_length = 123
    sue_inx_epoch_diff = 19
    assert sue_epochmap._get_inx_value(sue_epoch_length) != sue_inx_epoch_diff

    # WHEN
    sue_epochmap.set_otx2inx(sue_epoch_length, sue_inx_epoch_diff)

    # THEN
    assert sue_epochmap._get_inx_value(sue_epoch_length) == sue_inx_epoch_diff


def test_EpochMap_otx2inx_exists_ReturnsObj():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    x0_epoch_length = 660
    x1_epoch_length = 770
    x3_epoch_length = 880
    x0_epoch_diff = 6
    x1_epoch_diff = 7
    x3_epoch_diff = 8
    assert not sue_epochmap.otx2inx_exists(x0_epoch_length, x0_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x0_epoch_length, x1_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x1_epoch_length, x1_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x3_epoch_length, x3_epoch_diff)

    # WHEN
    sue_epochmap.set_otx2inx(x0_epoch_length, x0_epoch_diff)

    # THEN
    assert sue_epochmap.otx2inx_exists(x0_epoch_length, x0_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x0_epoch_length, x1_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x1_epoch_length, x1_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x3_epoch_length, x3_epoch_diff)

    # WHEN
    sue_epochmap.set_otx2inx(x3_epoch_length, x3_epoch_diff)

    # THEN
    assert sue_epochmap.otx2inx_exists(x0_epoch_length, x0_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x0_epoch_length, x1_epoch_diff)
    assert not sue_epochmap.otx2inx_exists(x1_epoch_length, x1_epoch_diff)
    assert sue_epochmap.otx2inx_exists(x3_epoch_length, x3_epoch_diff)


def test_EpochMap_otx_exists_ReturnsObj():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    x0_epoch_length = 660
    x3_epoch_length = 880
    x0_epoch_diff = 6
    x3_epoch_diff = 8
    assert not sue_epochmap.otx_exists(x0_epoch_length)
    assert not sue_epochmap.otx_exists(None)
    assert not sue_epochmap.otx_exists(x3_epoch_length)

    # WHEN
    sue_epochmap.set_otx2inx(x0_epoch_length, x0_epoch_diff)

    # THEN
    assert sue_epochmap.otx_exists(x0_epoch_length)
    assert not sue_epochmap.otx_exists(None)
    assert not sue_epochmap.otx_exists(x3_epoch_length)

    # WHEN
    sue_epochmap.set_otx2inx(None, x3_epoch_diff)

    # THEN
    assert sue_epochmap.otx_exists(x0_epoch_length)
    assert sue_epochmap.otx_exists(None)
    assert not sue_epochmap.otx_exists(x3_epoch_length)


def test_EpochMap_del_otx2inx_SetsAttr():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    x0_epoch_length = 660
    x3_epoch_length = 880
    x0_epoch_diff = 6
    assert not sue_epochmap.otx_exists(x0_epoch_length)
    assert not sue_epochmap.otx_exists(None)
    assert not sue_epochmap.otx_exists(x3_epoch_length)
    sue_epochmap.set_otx2inx(x0_epoch_length, x0_epoch_diff)
    assert sue_epochmap.otx2inx_exists(x0_epoch_length, x0_epoch_diff)

    # WHEN
    sue_epochmap.del_otx2inx(x0_epoch_length)

    # THEN
    assert not sue_epochmap.otx2inx_exists(x0_epoch_length, x0_epoch_diff)


def test_EpochMap_reveal_inx_ReturnsObjAndSetsAttr_voice_name():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    x0_epoch_length = 660
    x3_epoch_length = 880
    x0_epoch_diff = 6
    sue_epochmap.set_otx2inx(x0_epoch_length, x0_epoch_diff)
    assert sue_epochmap.otx_exists(x0_epoch_length)
    assert not sue_epochmap.otx_exists(x3_epoch_length)

    # WHEN / THEN
    x_otx_value = 22
    assert sue_epochmap.reveal_inx(x3_epoch_length, x_otx_value) == x_otx_value

    # WHEN / THEN
    x_otx_value = 22
    expected_x0_inx = x_otx_value + x0_epoch_diff
    assert sue_epochmap.reveal_inx(x0_epoch_length, x_otx_value) == expected_x0_inx
    assert sue_epochmap.reveal_inx(x0_epoch_length, x_otx_value) == 28

    # WHEN / THEN
    x_otx_value = 1000
    expected_x0_inx = x_otx_value + x0_epoch_diff
    expected_x0_inx = expected_x0_inx % x0_epoch_length
    assert sue_epochmap.reveal_inx(x0_epoch_length, x_otx_value) == expected_x0_inx
    assert sue_epochmap.reveal_inx(x0_epoch_length, x_otx_value) == 346


def test_EpochMap_to_dict_ReturnsObj():
    # ESTABLISH
    sue_epochmap = epochmap_shop(exx.sue)
    x0_epoch_length = 660
    x0_epoch_diff = 6
    sue_epochmap.set_otx2inx(x0_epoch_length, x0_epoch_diff)
    expected_dict = {
        kw.face_name: sue_epochmap.face_name,
        kw.spark_num: sue_epochmap.spark_num,
        kw.otx2inx: sue_epochmap.otx2inx,
    }

    # WHEN / THEN
    assert sue_epochmap.to_dict() == expected_dict


def test_get_epochmap_from_dict_ReturnsObj():
    # ESTABLISH
    spark7 = 7
    sue_epochmap = epochmap_shop(exx.sue, spark7)
    x0_epoch_length = 660
    x0_epoch_diff = 6
    sue_epochmap.set_otx2inx(x0_epoch_length, x0_epoch_diff)

    # WHEN
    gen_epochmap = get_epochmap_from_dict(sue_epochmap.to_dict())

    # THEN
    assert gen_epochmap.face_name == sue_epochmap.face_name
    assert gen_epochmap.spark_num == sue_epochmap.spark_num
    assert gen_epochmap.spark_num == spark7
    assert gen_epochmap.otx2inx == {x0_epoch_length: x0_epoch_diff}
    assert gen_epochmap == sue_epochmap


def test_inherit_epochmap_ReturnsObj_Scenario0():
    # ESTABLISH
    old_epochmap = epochmap_shop(exx.sue, 3)
    new_epochmap = epochmap_shop(exx.sue, 5)
    # WHEN
    inherit_epochmap(new_epochmap, old_epochmap)

    # THEN
    assert new_epochmap
    assert new_epochmap == epochmap_shop(exx.sue, 5)


def test_inherit_epochmap_ReturnsObj_Scenario1_Inherit_otx2inx_FromOld_epochmap():
    # ESTABLISH
    sue_otx_time = 45
    sue_inx_time = 55
    sue_epoch_diff = sue_otx_time - sue_inx_time
    old_epochmap = epochmap_shop(exx.sue, 3)
    old_epochmap.set_otx2inx(None, sue_epoch_diff)
    assert old_epochmap.otx2inx == {None: sue_epoch_diff}

    new_epochmap = epochmap_shop(exx.sue, 5)
    # WHEN
    inherit_epochmap(new_epochmap, old_epochmap)

    # THEN
    assert new_epochmap
    assert new_epochmap.otx2inx == {None: sue_epoch_diff}
    assert new_epochmap == epochmap_shop(exx.sue, 5, {None: sue_epoch_diff})


def test_inherit_epochmap_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_face_name():
    # ESTABLISH
    sue0_epoch_min = 555
    sue1_epoch_min = 655
    old_epochmap = epochmap_shop(exx.sue, 0, {sue0_epoch_min: 0})
    new_epochmap = epochmap_shop(exx.bob, 1, {sue1_epoch_min: 7})

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_epochmap(new_epochmap, old_epochmap)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_epochmap_ReturnsObj_Scenario3_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    old_epochmap = epochmap_shop(exx.sue, 5)
    new_epochmap = epochmap_shop(exx.sue, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_epochmap(new_epochmap, old_epochmap)

    # THEN
    assert str(excinfo.value) == f"older {kw.EpochMap} is not older"
