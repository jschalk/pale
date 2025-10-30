from src.ch13_keep.rivercycle import rivergrade_shop
from src.ch13_keep.riverrun import riverrun_shop
from src.ch13_keep.test._util.ch13_env import get_temp_dir, temp_moment_label
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_set_initial_rivergrade_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao, number=yao_number)
    x_doctor_count = 5
    x_patient_count = 8
    yao_riverrun.doctor_count = x_doctor_count
    yao_riverrun.patient_count = x_patient_count
    assert yao_riverrun.rivergrades.get(exx.bob) is None

    # WHEN
    yao_riverrun.set_initial_rivergrade(exx.bob)

    # THEN
    bob_rivergrade = rivergrade_shop(
        a23_str,
        exx.yao,
        None,
        exx.bob,
        yao_number,
        x_doctor_count,
        x_patient_count,
    )
    bob_rivergrade.care_amount = 0
    assert yao_riverrun.rivergrades.get(exx.bob) is not None
    gen_rivergrade = yao_riverrun.rivergrades.get(exx.bob)
    assert gen_rivergrade.doctor_count == x_doctor_count
    assert gen_rivergrade.patient_count == x_patient_count
    assert gen_rivergrade == bob_rivergrade


def test_RiverRun_rivergrades_is_empty_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao, number=yao_number)

    assert yao_riverrun.rivergrades_is_empty()

    # WHEN
    yao_riverrun.set_initial_rivergrade(exx.bob)

    # THEN
    assert yao_riverrun.rivergrades_is_empty() is False


def test_RiverRun_rivergrade_exists_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao, yao_number)
    yao_riverrun.set_initial_rivergrade("Yao")

    assert yao_riverrun.rivergrade_exists(exx.bob) is False
    assert yao_riverrun.rivergrades_is_empty() is False

    # WHEN
    yao_riverrun.set_initial_rivergrade(exx.bob)

    # THEN
    assert yao_riverrun.rivergrade_exists(exx.bob)
    assert yao_riverrun.rivergrades_is_empty() is False


def test_RiverRun_set_all_initial_rivergrades_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    zia_str = "Zia"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_keep_patientledger(exx.yao, exx.bob, 1)
    x_riverrun.set_keep_patientledger(zia_str, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.xio, exx.sue, 1)
    all_voices_ids = x_riverrun.get_all_keep_patientledger_voice_names()
    assert all_voices_ids == {exx.yao, exx.bob, zia_str, exx.xio, exx.sue}
    assert x_riverrun.rivergrades_is_empty()
    assert x_riverrun.rivergrade_exists(exx.yao) is False
    assert x_riverrun.rivergrade_exists(exx.bob) is False
    assert x_riverrun.rivergrade_exists(zia_str) is False

    # WHEN
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrades_is_empty() is False
    assert x_riverrun.rivergrade_exists(exx.yao)
    assert x_riverrun.rivergrade_exists(exx.bob)
    assert x_riverrun.rivergrade_exists(zia_str)


def test_RiverRun_set_all_initial_rivergrades_OverWritesPrevious():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    zia_str = "Zia"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, 1)
    x_riverrun.set_keep_patientledger(exx.yao, exx.bob, 1)
    x_riverrun.set_keep_patientledger(zia_str, exx.bob, 1)
    x_riverrun.set_keep_patientledger(exx.xio, exx.sue, 1)
    x_riverrun.set_all_initial_rivergrades()
    assert x_riverrun.rivergrade_exists(exx.yao)
    assert x_riverrun.rivergrade_exists(exx.bob)
    assert x_riverrun.rivergrade_exists(zia_str)
    assert x_riverrun.rivergrade_exists(exx.xio)
    assert x_riverrun.rivergrade_exists(exx.sue)

    # WHEN
    x_riverrun.delete_keep_patientledgers_belief(exx.xio)
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrade_exists(exx.yao)
    assert x_riverrun.rivergrade_exists(exx.bob)
    assert x_riverrun.rivergrade_exists(zia_str)
    assert x_riverrun.rivergrade_exists(exx.xio) is False
    assert x_riverrun.rivergrade_exists(exx.sue) is False
