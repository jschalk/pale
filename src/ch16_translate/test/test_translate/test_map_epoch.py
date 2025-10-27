from numpy import int64 as numpy_int64
from pytest import raises as pytest_raises
from src.ch14_epoch.epoch_main import get_c400_constants, get_default_epoch_config_dict
from src.ch16_translate.formula import (
    EpochFormula,
    epochformula_shop,
    get_epochformula_from_dict,
    inherit_epochformula,
)
from src.ch16_translate.translate_config import default_unknown_str_if_None
from src.ref.keywords import Ch16Keywords as kw


def test_EpochFormula_Exists():
    # ESTABLISH
    x_epochformula = EpochFormula()

    # WHEN / THEN
    assert not x_epochformula.face_name
    assert not x_epochformula.spark_num
    assert not x_epochformula.otx_time
    assert not x_epochformula.inx_time
    assert not x_epochformula.inx_time
    assert not x_epochformula.epoch_length_min
    assert set(x_epochformula.__dict__.keys()) == {
        kw.face_name,
        kw.spark_num,
        kw.otx_time,
        kw.inx_time,
        kw.epoch_length_min,
    }


def test_epochformula_shop_ReturnsObj_Scenario0():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    x_epochformula = epochformula_shop(bob_str)

    # THEN
    assert x_epochformula.face_name == bob_str
    assert x_epochformula.spark_num == 0
    assert x_epochformula.otx_time is None
    assert x_epochformula.inx_time is None

    default_epoch_config = get_default_epoch_config_dict()
    default_c400_number = default_epoch_config.get(kw.c400_number)
    c400_length_constant = get_c400_constants().c400_leap_length
    default_epoch_length_min = default_c400_number * c400_length_constant
    assert x_epochformula.epoch_length_min == default_epoch_length_min


def test_epochformula_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    bob_str = "Bob"
    bob_otx_time = 11
    bob_inx_time = 19
    bob_epoch_length_min = 500
    spark2 = 2

    # WHEN
    x_epochformula = epochformula_shop(
        face_name=bob_str,
        spark_num=spark2,
        otx_time=bob_otx_time,
        inx_time=bob_inx_time,
        epoch_length_min=bob_epoch_length_min,
    )

    # THEN
    assert x_epochformula.face_name == bob_str
    assert x_epochformula.spark_num == spark2
    assert x_epochformula.otx_time == bob_otx_time
    assert x_epochformula.inx_time == bob_inx_time
    assert x_epochformula.epoch_length_min == bob_epoch_length_min


def test_epochformula_shop_ReturnsObj_Scenario2_WithParametersModolarMath():
    # ESTABLISH
    bob_str = "Bob"
    bob_otx_time = 611
    bob_inx_time = 619
    bob_epoch_length_min = 500
    spark2 = 2

    # WHEN
    x_epochformula = epochformula_shop(
        face_name=bob_str,
        spark_num=spark2,
        otx_time=bob_otx_time,
        inx_time=bob_inx_time,
        epoch_length_min=bob_epoch_length_min,
    )

    # THEN
    assert x_epochformula.face_name == bob_str
    assert x_epochformula.spark_num == spark2
    assert x_epochformula.otx_time != bob_otx_time
    assert x_epochformula.otx_time == bob_otx_time % bob_epoch_length_min
    assert x_epochformula.inx_time != bob_inx_time
    assert x_epochformula.inx_time == bob_inx_time % bob_epoch_length_min
    assert x_epochformula.epoch_length_min == bob_epoch_length_min


def test_epochformula_shop_ReturnsObj_Scenario3_WithParametersGreaterThan_epoch_length_min():
    # ESTABLISH
    bob_str = "Bob"
    bob_otx_time = 11
    bob_inx_time = 19
    spark2 = 2

    # WHEN
    x_epochformula = epochformula_shop(
        face_name=bob_str,
        spark_num=spark2,
        otx_time=bob_otx_time,
        inx_time=bob_inx_time,
    )

    # THEN
    assert x_epochformula.face_name == bob_str
    assert x_epochformula.spark_num == spark2
    assert x_epochformula.otx_time == bob_otx_time
    assert x_epochformula.inx_time == bob_inx_time


def test_epochformula_shop_ReturnsObj_Scenario4_TranslateCoreAttrAreDefaultWhenGiven_float_nan():
    # ESTABLISH
    bob_str = "Bob"
    spark7 = numpy_int64(7)
    bob_otx_time = 11
    bob_inx_time = 19
    x_nan = float("nan")

    # WHEN
    x_epochformula = epochformula_shop(
        face_name=bob_str,
        spark_num=numpy_int64(spark7),
        otx_time=numpy_int64(bob_otx_time),
        inx_time=numpy_int64(bob_inx_time),
    )

    # THEN
    assert x_epochformula.face_name == bob_str
    assert x_epochformula.spark_num == spark7
    assert str(type(x_epochformula.spark_num)) != "<class 'numpy.int64'>"
    assert str(type(x_epochformula.spark_num)) == "<class 'int'>"
    assert x_epochformula.otx_time == bob_otx_time
    assert x_epochformula.inx_time == bob_inx_time


def test_EpochFormula_get_inx_value_ReturnsObj_Scenario0_NoParametersGiven():
    # ESTABLISH
    bob_str = "Bob"
    bob_epochformula = epochformula_shop(bob_str)

    # WHEN
    six_int = 6
    inx_value = bob_epochformula.get_inx_value(otx_value=six_int)

    # THEN
    assert inx_value
    assert inx_value == six_int


def test_EpochFormula_get_inx_value_ReturnsObj_Scenario1_ParametersGiven():
    # ESTABLISH
    bob_str = "Bob"
    six_int = 6
    bob_otx_time = 11
    bob_inx_time = 18
    bob_epochformula = epochformula_shop(bob_str, None, bob_otx_time, bob_inx_time)

    # WHEN
    six_int = 6
    inx_value = bob_epochformula.get_inx_value(otx_value=six_int)

    # THEN
    assert inx_value
    assert inx_value == six_int + (bob_inx_time - bob_otx_time)
    assert inx_value == 13


def test_EpochFormula_get_inx_value_ReturnsObj_Scenario2_GreaterThan_epoch_length_min():
    # ESTABLISH
    bob_str = "Bob"
    six_int = 6
    bob_otx_time = 11
    bob_inx_time = 18
    bob_epoch_length_min = 500
    bob_epochformula = epochformula_shop(
        bob_str, None, bob_otx_time, bob_inx_time, bob_epoch_length_min
    )

    # WHEN
    x_int = 498
    inx_value = bob_epochformula.get_inx_value(x_int)

    # THEN
    assert inx_value
    assert inx_value != x_int + (bob_inx_time - bob_otx_time)
    assert inx_value == (x_int + (bob_inx_time - bob_otx_time)) % bob_epoch_length_min
    assert inx_value == 5


def test_EpochFormula_to_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_otx_time = 11
    sue_inx_time = 18
    spark7 = 7
    sue_epochformula = epochformula_shop(
        face_name=sue_str,
        spark_num=spark7,
        otx_time=sue_otx_time,
        inx_time=sue_inx_time,
    )
    expected_dict = {
        kw.face_name: sue_epochformula.face_name,
        kw.spark_num: sue_epochformula.spark_num,
        kw.otx_time: sue_epochformula.otx_time,
        kw.inx_time: sue_epochformula.inx_time,
    }

    # WHEN / THEN
    assert sue_epochformula.to_dict() == expected_dict


def test_get_epochformula_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_otx_time = 11
    sue_inx_time = 18
    spark7 = 7
    sue_epochformula = epochformula_shop(
        face_name=sue_str,
        spark_num=spark7,
        otx_time=sue_otx_time,
        inx_time=sue_inx_time,
    )

    # WHEN
    gen_epochformula = get_epochformula_from_dict(sue_epochformula.to_dict())

    # THEN
    assert gen_epochformula.face_name == sue_epochformula.face_name
    assert gen_epochformula.spark_num == sue_epochformula.spark_num
    assert gen_epochformula.spark_num == spark7
    assert gen_epochformula.otx_time == sue_otx_time
    assert gen_epochformula.inx_time == sue_inx_time
    assert gen_epochformula == sue_epochformula


def test_inherit_epochformula_ReturnsObj_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    old_epochformula = epochformula_shop(zia_str, 3)
    new_epochformula = epochformula_shop(zia_str, 5)
    # WHEN
    inherit_epochformula(new_epochformula, old_epochformula)

    # THEN
    assert new_epochformula
    assert new_epochformula == epochformula_shop(zia_str, 5)


def test_inherit_epochformula_ReturnsObj_Scenario1_OldHasParameters():
    # ESTABLISH
    zia_str = "Zia"
    zia_otx_time = 45
    zia_inx_time = 55
    old_epochformula = epochformula_shop(zia_str, 3, zia_otx_time, zia_inx_time)
    new_epochformula = epochformula_shop(zia_str, 5)
    # WHEN
    inherit_epochformula(new_epochformula, old_epochformula)

    # THEN
    assert new_epochformula
    assert new_epochformula == epochformula_shop(zia_str, 5, zia_otx_time, zia_inx_time)


def test_inherit_epochformula_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    sue_str = "Sue"
    sue0_epoch_min = 555
    sue1_epoch_min = 655
    old_epochformula = epochformula_shop(sue_str, 0, epoch_length_min=sue0_epoch_min)
    new_epochformula = epochformula_shop(sue_str, 1, epoch_length_min=sue1_epoch_min)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_epochformula(new_epochformula, old_epochformula)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_epochformula_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_epochformula = epochformula_shop(sue_str, 0)
    new_epochformula = epochformula_shop(bob_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_epochformula(new_epochformula, old_epochformula)

    # THEN
    assert str(excinfo.value) == "Core attrs in conflict"


def test_inherit_epochformula_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_epochformula = epochformula_shop(sue_str, 5)
    new_epochformula = epochformula_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_epochformula(new_epochformula, old_epochformula)

    # THEN
    assert str(excinfo.value) == f"older {kw.EpochFormula} is not older"
