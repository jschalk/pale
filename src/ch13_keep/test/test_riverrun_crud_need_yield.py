from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_keep.rivercycle import get_doctorledger
from src.ch13_keep.riverrun import riverrun_shop
from src.ch13_keep.test._util.ch13_env import get_temp_dir, temp_moment_label
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_set_voice_need_yield_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_riverrun = riverrun_shop(mstr_dir, a23_str, exx.bob)
    assert bob_riverrun.need_yields.get(exx.yao) is None

    # WHEN
    yao_need_yield = 7
    bob_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)

    # THEN
    assert bob_riverrun.need_yields.get(exx.yao) == yao_need_yield


def test_RiverRun_need_yields_is_empty_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    x_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao)
    assert x_riverrun.need_yields_is_empty()

    # WHEN
    yao_need_yield = 500
    x_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)
    # THEN
    assert x_riverrun.need_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_need_yield(exx.yao)
    # THEN
    assert x_riverrun.need_yields_is_empty()

    # WHEN
    bob_need_yield = 300
    x_riverrun.set_voice_need_yield(exx.yao, bob_need_yield)
    x_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)
    # THEN
    assert x_riverrun.need_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_need_yield(exx.yao)
    # THEN
    assert x_riverrun.need_yields_is_empty()


def test_RiverRun_reset_need_yields_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        a23_str,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_riverrun.set_voice_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_voice_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.need_yields_is_empty() is False

    # WHEN
    bob_riverrun.reset_need_yields()

    # THEN
    assert bob_riverrun.need_yields_is_empty()


def test_RiverRun_voice_has_need_yield_ReturnsBool():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        a23_str,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    zia_str = "Zia"
    yao_need_yield = 6
    bob_need_yield = 38
    sue_need_yield = 56
    bob_riverrun.set_voice_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_voice_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.voice_has_need_yield(exx.bob)
    assert bob_riverrun.voice_has_need_yield(exx.sue)
    assert bob_riverrun.voice_has_need_yield(exx.yao)
    assert bob_riverrun.voice_has_need_yield(zia_str) is False

    # WHEN
    bob_riverrun.reset_need_yields()

    # THEN
    assert bob_riverrun.voice_has_need_yield(exx.bob) is False
    assert bob_riverrun.voice_has_need_yield(exx.sue) is False
    assert bob_riverrun.voice_has_need_yield(exx.yao) is False
    assert bob_riverrun.voice_has_need_yield(zia_str) is False


def test_RiverRun_delete_need_yield_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_mana_amount = 88
    bob_mana_grain = 11

    bob_riverrun = riverrun_shop(
        mstr_dir,
        a23_str,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_riverrun.set_voice_need_yield(exx.yao, 5)
    assert bob_riverrun.voice_has_need_yield(exx.yao)

    # WHEN
    bob_riverrun.delete_need_yield(exx.yao)

    # THEN
    assert bob_riverrun.voice_has_need_yield(exx.yao) is False


def test_RiverRun_get_voice_need_yield_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_mana_amount = 1000
    bob_mana_grain = 1

    bob_riverrun = riverrun_shop(
        mstr_dir,
        a23_str,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    zia_str = "Zia"
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_riverrun.set_voice_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_voice_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.voice_has_need_yield(exx.bob)
    assert bob_riverrun.get_voice_need_yield(exx.bob) == bob_need_yield
    assert bob_riverrun.voice_has_need_yield(zia_str) is False
    assert bob_riverrun.get_voice_need_yield(zia_str) == 0

    # WHEN
    bob_riverrun.reset_need_yields()

    # THEN
    assert bob_riverrun.voice_has_need_yield(exx.bob) is False
    assert bob_riverrun.get_voice_need_yield(exx.bob) == 0
    assert bob_riverrun.voice_has_need_yield(zia_str) is False
    assert bob_riverrun.get_voice_need_yield(zia_str) == 0


def test_RiverRun_add_voice_need_yield_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        a23_str,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    zia_str = "Zia"
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_riverrun.set_voice_need_yield(exx.bob, bob_need_yield)
    bob_riverrun.set_voice_need_yield(exx.sue, sue_need_yield)
    bob_riverrun.set_voice_need_yield(exx.yao, yao_need_yield)
    assert bob_riverrun.get_voice_need_yield(exx.bob) == bob_need_yield
    assert bob_riverrun.get_voice_need_yield(exx.sue) == sue_need_yield
    assert bob_riverrun.get_voice_need_yield(zia_str) == 0

    # WHEN
    bob_riverrun.add_voice_need_yield(exx.sue, 5)
    bob_riverrun.add_voice_need_yield(zia_str, 10)

    # THEN
    assert bob_riverrun.get_voice_need_yield(exx.bob) == bob_need_yield
    assert bob_riverrun.get_voice_need_yield(exx.sue) == sue_need_yield + 5
    assert bob_riverrun.get_voice_need_yield(zia_str) == 10


def test_RiverRun_levy_need_due_SetsAttr_ScenarioY():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        mstr_dir,
        a23_str,
        exx.bob,
        mana_grain=bob_mana_grain,
        keep_point_magnitude=bob_mana_amount,
    )
    bob_need_yield = 38
    sue_need_yield = 56
    yao_need_yield = 6
    bob_belief = beliefunit_shop(exx.bob)
    bob_belief.add_voiceunit(exx.bob, 2, bob_need_yield)
    bob_belief.add_voiceunit(exx.sue, 2, sue_need_yield)
    bob_belief.add_voiceunit(exx.yao, 2, yao_need_yield)
    bob_doctorledger = get_doctorledger(bob_belief)
    bob_riverrun.set_need_dues(bob_doctorledger)
    assert bob_riverrun.get_voice_need_due(exx.bob) == 380
    assert bob_riverrun.get_voice_need_yield(exx.bob) == 0

    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.bob, 5)
    # THEN
    assert excess_carer_points == 0
    assert bob_riverrun.get_voice_need_due(exx.bob) == 375
    assert bob_riverrun.get_voice_need_yield(exx.bob) == 5

    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.bob, 375)
    # THEN
    assert excess_carer_points == 0
    assert bob_riverrun.get_voice_need_due(exx.bob) == 0
    assert bob_riverrun.get_voice_need_yield(exx.bob) == 380

    # ESTABLISH
    assert bob_riverrun.get_voice_need_due(exx.sue) == 560
    assert bob_riverrun.get_voice_need_yield(exx.sue) == 0
    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.sue, 1000)
    # THEN
    assert excess_carer_points == 440
    assert bob_riverrun.get_voice_need_due(exx.sue) == 0
    assert bob_riverrun.get_voice_need_yield(exx.sue) == 560

    # ESTABLISH
    zia_str = "Zia"
    assert bob_riverrun.get_voice_need_due(zia_str) == 0
    assert bob_riverrun.get_voice_need_yield(zia_str) == 0
    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(zia_str, 1000)
    # THEN
    assert excess_carer_points == 1000
    assert bob_riverrun.get_voice_need_due(zia_str) == 0
    assert bob_riverrun.get_voice_need_yield(zia_str) == 0

    # ESTABLISH
    assert bob_riverrun.get_voice_need_due(exx.yao) == 60
    assert bob_riverrun.get_voice_need_yield(exx.yao) == 0
    # WHEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(exx.yao, 81)
    # THEN
    assert excess_carer_points == 21
    assert bob_riverrun.get_voice_need_due(exx.yao) == 0
    assert bob_riverrun.get_voice_need_yield(exx.yao) == 60


def test_RiverRun_set_need_got_attrs_SetsAttrs():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    six_need_got = 6
    ten_need_got = 10
    x_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao)
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun.need_got_prev == 0

    # WHEN
    x_riverrun._set_need_got_attrs(six_need_got)
    # THEN
    assert x_riverrun.need_got_curr == six_need_got
    assert x_riverrun.need_got_prev == 0

    # WHEN
    x_riverrun._set_need_got_attrs(ten_need_got)
    # THEN
    assert x_riverrun.need_got_curr == ten_need_got
    assert x_riverrun.need_got_prev == six_need_got


def test_RiverRun_need_gotten_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    six_need_got = 6
    ten_need_got = 10
    x_riverrun = riverrun_shop(mstr_dir, a23_str, exx.yao)
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun._need_gotten() is False

    # WHEN
    x_riverrun._set_need_got_attrs(six_need_got)
    # THEN
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == six_need_got
    assert x_riverrun._need_gotten()

    # ESTABLISH
    x_riverrun._set_need_got_attrs(six_need_got)
    # THEN
    assert x_riverrun.need_got_prev == six_need_got
    assert x_riverrun.need_got_curr == six_need_got
    assert x_riverrun._need_gotten()

    # WHEN
    x_riverrun._set_need_got_attrs(0)
    # THEN
    assert x_riverrun.need_got_prev == six_need_got
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun._need_gotten()

    # WHEN
    x_riverrun._set_need_got_attrs(0)
    # THEN
    assert x_riverrun.need_got_prev == 0
    assert x_riverrun.need_got_curr == 0
    assert x_riverrun._need_gotten() is False
