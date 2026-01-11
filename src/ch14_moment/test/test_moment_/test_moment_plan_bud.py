from pytest import raises as pytest_raises
from src.ch11_bud.bud_main import planbudhistory_shop
from src.ch14_moment.moment_main import momentunit_shop
from src.ch14_moment.test._util.ch14_env import get_temp_dir
from src.ref.keywords import ExampleStrs as exx


def test_MomentUnit_set_planbudhistory_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    assert amy_moment.planbudhistorys == {}

    # WHEN
    sue_planbudhistory = planbudhistory_shop(exx.sue)
    amy_moment.set_planbudhistory(sue_planbudhistory)

    # THEN
    assert amy_moment.planbudhistorys != {}
    assert amy_moment.planbudhistorys.get(exx.sue) == sue_planbudhistory


def test_MomentUnit_planbudhistory_exists_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    assert amy_moment.planbudhistory_exists(exx.sue) is False

    # WHEN
    sue_planbudhistory = planbudhistory_shop(exx.sue)
    amy_moment.set_planbudhistory(sue_planbudhistory)

    # THEN
    assert amy_moment.planbudhistory_exists(exx.sue)


def test_MomentUnit_get_planbudhistory_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    sue_planbudhistory = planbudhistory_shop(exx.sue)
    amy_moment.set_planbudhistory(sue_planbudhistory)
    assert amy_moment.planbudhistory_exists(exx.sue)

    # WHEN
    sue_gen_planbudhistory = amy_moment.get_planbudhistory(exx.sue)

    # THEN
    assert sue_planbudhistory
    assert sue_planbudhistory == sue_gen_planbudhistory


def test_MomentUnit_del_planbudhistory_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    sue_planbudhistory = planbudhistory_shop(exx.sue)
    amy_moment.set_planbudhistory(sue_planbudhistory)
    assert amy_moment.planbudhistory_exists(exx.sue)

    # WHEN
    amy_moment.del_planbudhistory(exx.sue)

    # THEN
    assert amy_moment.planbudhistory_exists(exx.sue) is False


def test_MomentUnit_add_budunit_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    assert amy_moment.planbudhistorys == {}

    # WHEN
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)

    # THEN
    assert amy_moment.planbudhistorys != {}
    sue_planbudhistory = planbudhistory_shop(exx.sue)
    sue_planbudhistory.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_planbudhistory.add_bud(sue_x7_bud_time, sue_x7_quota)
    bob_planbudhistory = planbudhistory_shop(exx.bob)
    bob_planbudhistory.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert amy_moment.get_planbudhistory(exx.sue) == sue_planbudhistory
    assert amy_moment.get_planbudhistory(exx.bob) == bob_planbudhistory


def test_MomentUnit_bud_quota_exists_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    assert amy_moment.planbudhistorys == {}
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    assert not amy_moment.bud_quota_exists(exx.bob, bob_x0_bud_time, bob_x0_quota)
    assert not amy_moment.bud_quota_exists(exx.sue, sue_x4_bud_time, sue_x4_quota)
    assert not amy_moment.bud_quota_exists(exx.sue, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)

    # THEN
    assert amy_moment.bud_quota_exists(exx.bob, bob_x0_bud_time, bob_x0_quota)
    assert not amy_moment.bud_quota_exists(exx.sue, sue_x4_bud_time, sue_x4_quota)
    assert not amy_moment.bud_quota_exists(exx.sue, sue_x7_bud_time, sue_x7_quota)


def test_MomentUnit_get_budunit_ReturnsObj_Scenario0_BrokerDoesNotExist():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    sue_x7_bud_time = 7

    # WHEN
    gen_sue_x7_budunit = amy_moment.get_budunit(exx.sue, sue_x7_bud_time)

    # THEN
    assert amy_moment.planbudhistorys == {}
    assert not gen_sue_x7_budunit


def test_MomentUnit_get_budunit_ReturnsObj_Scenario1_BudDoesNotExist():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    sue_x4_bud_time = 4
    sue_x4_quota = 66
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)

    # WHEN
    sue_x7_bud_time = 7
    gen_sue_x7_budunit = amy_moment.get_budunit(exx.sue, sue_x7_bud_time)

    # THEN
    assert amy_moment.planbudhistorys != {}
    assert not gen_sue_x7_budunit


def test_MomentUnit_get_budunit_ReturnsObj_Scenario2_BudExists():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    gen_sue_x7_budunit = amy_moment.get_budunit(exx.sue, sue_x7_bud_time)

    # THEN
    assert amy_moment.planbudhistorys != {}
    sue_broker = amy_moment.planbudhistorys.get(exx.sue)
    assert gen_sue_x7_budunit == sue_broker.get_bud(sue_x7_bud_time)


def test_MomentUnit_get_planbudhistorys_bud_times_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    assert amy_moment.get_planbudhistorys_bud_times() == set()

    # WHEN
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)

    # THEN
    all_bud_times = {bob_x0_bud_time, sue_x4_bud_time, sue_x7_bud_time}
    assert amy_moment.get_planbudhistorys_bud_times() == all_bud_times


def test_MomentUnit_add_budunit_RaisesErrorWhen_bud_time_IsLessThan_offi_time_max():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    amy_offi_time_max = 606
    amy_moment.offi_time_max = amy_offi_time_max
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert amy_moment.get_planbudhistorys_bud_times() == set()
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    exception_str = f"Cannot set budunit because bud_time {sue_x4_bud_time} is less than MomentUnit.offi_time_max {amy_offi_time_max}."
    assert str(excinfo.value) == exception_str


def test_MomentUnit_add_budunit_DoesNotRaiseError_allow_prev_to_offi_time_max_entry_IsTrue():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    amy_offi_time_max = 606
    amy_moment.offi_time_max = amy_offi_time_max
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert amy_moment.get_planbudhistorys_bud_times() == set()
    amy_moment.add_budunit(exx.bob, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(exx.sue, sue_x7_bud_time, sue_x7_quota)

    sue_planbudhistory = planbudhistory_shop(exx.sue)
    sue_planbudhistory.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_planbudhistory.add_bud(sue_x7_bud_time, sue_x7_quota)
    assert amy_moment.get_planbudhistory(exx.sue) != sue_planbudhistory

    # WHEN
    amy_moment.add_budunit(
        plan_name=exx.sue,
        bud_time=sue_x4_bud_time,
        quota=sue_x4_quota,
        allow_prev_to_offi_time_max_entry=True,
    )

    # THEN
    assert amy_moment.planbudhistorys != {}
    assert amy_moment.get_planbudhistory(exx.sue) == sue_planbudhistory
    bob_planbudhistory = planbudhistory_shop(exx.bob)
    bob_planbudhistory.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert amy_moment.get_planbudhistory(exx.bob) == bob_planbudhistory


def test_MomentUnit_add_budunit_SetsAttr_celldepth():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_temp_dir())
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    sue_x7_celldepth = 5
    assert amy_moment.planbudhistorys == {}

    # WHEN
    amy_moment.add_budunit(exx.sue, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(
        exx.sue, sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )

    # THEN
    assert amy_moment.planbudhistorys != {}
    expected_sue_planbudhistory = planbudhistory_shop(exx.sue)
    expected_sue_planbudhistory.add_bud(sue_x4_bud_time, sue_x4_quota)
    expected_sue_planbudhistory.add_bud(
        sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )
    # print(f"{expected_sue_planbudhistory=}")
    gen_sue_planbudhistory = amy_moment.get_planbudhistory(exx.sue)
    gen_sue_x7_bud = gen_sue_planbudhistory.get_bud(sue_x7_bud_time)
    print(f"{gen_sue_planbudhistory=}")
    assert gen_sue_x7_bud == expected_sue_planbudhistory.get_bud(sue_x7_bud_time)
    assert gen_sue_planbudhistory.buds == expected_sue_planbudhistory.buds
    assert gen_sue_planbudhistory == expected_sue_planbudhistory
    assert amy_moment.get_planbudhistory(exx.sue) == expected_sue_planbudhistory
