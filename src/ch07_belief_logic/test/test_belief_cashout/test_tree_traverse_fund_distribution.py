from dataclasses import dataclass
from pytest import raises as pytest_raises
from src.ch02_allot.allot import default_pool_num
from src.ch03_voice.group import awardline_shop, awardunit_shop
from src.ch03_voice.voice import voiceunit_shop
from src.ch04_rope.rope import RopeTerm, to_rope
from src.ch06_keg.keg import KegUnit, kegunit_shop
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import (
    beliefunit_v001,
    beliefunit_v001_with_large_agenda,
    get_beliefunit_with7am_clean_table_reason,
    get_beliefunit_with_4_levels,
)
from src.ref.keywords import ExampleStrs as exx


def test_BeliefUnit_cashout_Sets_kegunit_fund_onset_fund_cease_Scenario0():
    # ESTABLISH
    x_beliefunit = get_beliefunit_with7am_clean_table_reason()
    casa_rope = x_beliefunit.make_l1_rope("casa")
    catt_rope = x_beliefunit.make_l1_rope("cat have dinner")
    wk_rope = x_beliefunit.make_l1_rope("sem_jours")
    x_beliefunit.kegroot.fund_onset = 13
    x_beliefunit.kegroot.fund_cease = 13
    x_beliefunit.get_keg_obj(casa_rope).fund_onset = 13
    x_beliefunit.get_keg_obj(casa_rope).fund_cease = 13
    x_beliefunit.get_keg_obj(catt_rope).fund_onset = 13
    x_beliefunit.get_keg_obj(catt_rope).fund_cease = 13
    x_beliefunit.get_keg_obj(wk_rope).fund_onset = 13
    x_beliefunit.get_keg_obj(wk_rope).fund_cease = 13

    assert x_beliefunit.kegroot.fund_onset == 13
    assert x_beliefunit.kegroot.fund_cease == 13
    assert x_beliefunit.get_keg_obj(casa_rope).fund_onset == 13
    assert x_beliefunit.get_keg_obj(casa_rope).fund_cease == 13
    assert x_beliefunit.get_keg_obj(catt_rope).fund_onset == 13
    assert x_beliefunit.get_keg_obj(catt_rope).fund_cease == 13
    assert x_beliefunit.get_keg_obj(wk_rope).fund_onset == 13
    assert x_beliefunit.get_keg_obj(wk_rope).fund_cease == 13

    # WHEN
    x_beliefunit.cashout()

    # THEN
    assert x_beliefunit.kegroot.fund_onset != 13
    assert x_beliefunit.kegroot.fund_cease != 13
    assert x_beliefunit.get_keg_obj(casa_rope).fund_onset != 13
    assert x_beliefunit.get_keg_obj(casa_rope).fund_cease != 13
    assert x_beliefunit.get_keg_obj(catt_rope).fund_onset != 13
    assert x_beliefunit.get_keg_obj(catt_rope).fund_cease != 13
    assert x_beliefunit.get_keg_obj(wk_rope).fund_onset != 13
    assert x_beliefunit.get_keg_obj(wk_rope).fund_cease != 13


def test_BeliefUnit_cashout_Sets_kegunit_fund_onset_fund_cease_Scenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_beliefunit = beliefunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_rope = yao_beliefunit.make_l1_rope(auto_str)
    auto_keg = kegunit_shop(auto_str, star=10)
    yao_beliefunit.set_l1_keg(auto_keg)

    carn_str = "carn"
    carn_rope = yao_beliefunit.make_l1_rope(carn_str)
    carn_keg = kegunit_shop(carn_str, star=60)
    yao_beliefunit.set_l1_keg(carn_keg)
    lamb_str = "lambs"
    lamb_rope = yao_beliefunit.make_rope(carn_rope, lamb_str)
    lamb_keg = kegunit_shop(lamb_str, star=1)
    yao_beliefunit.set_keg_obj(lamb_keg, parent_rope=carn_rope)
    duck_str = "ducks"
    duck_rope = yao_beliefunit.make_rope(carn_rope, duck_str)
    duck_keg = kegunit_shop(duck_str, star=2)
    yao_beliefunit.set_keg_obj(duck_keg, parent_rope=carn_rope)

    coal_str = "coal"
    coal_rope = yao_beliefunit.make_l1_rope(coal_str)
    coal_keg = kegunit_shop(coal_str, star=30)
    yao_beliefunit.set_l1_keg(coal_keg)

    assert yao_beliefunit.kegroot.fund_onset is None
    assert yao_beliefunit.kegroot.fund_cease is None
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_onset is None
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_cease is None
    assert yao_beliefunit.get_keg_obj(carn_rope).fund_onset is None
    assert yao_beliefunit.get_keg_obj(carn_rope).fund_cease is None
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_onset is None
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_cease is None
    lamb_before = yao_beliefunit.get_keg_obj(rope=lamb_rope)
    assert lamb_before.fund_onset is None
    assert lamb_before.fund_cease is None
    duck_before = yao_beliefunit.get_keg_obj(rope=duck_rope)
    assert duck_before.fund_onset is None
    assert duck_before.fund_cease is None

    # WHEN
    yao_beliefunit.cashout()

    # THEN
    assert yao_beliefunit.kegroot.fund_onset == 0.0
    assert yao_beliefunit.kegroot.fund_cease == default_pool_num()
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_onset == 0.0
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_cease == default_pool_num() * 0.1
    assert yao_beliefunit.get_keg_obj(carn_rope).fund_onset == default_pool_num() * 0.1
    assert yao_beliefunit.get_keg_obj(carn_rope).fund_cease == default_pool_num() * 0.7
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_onset == default_pool_num() * 0.7
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_cease == default_pool_num() * 1.0

    duck_after = yao_beliefunit.get_keg_obj(rope=duck_rope)
    assert duck_after.fund_onset == default_pool_num() * 0.1
    assert duck_after.fund_cease == default_pool_num() * 0.5
    lamb_after = yao_beliefunit.get_keg_obj(rope=lamb_rope)
    assert lamb_after.fund_onset == default_pool_num() * 0.5
    assert lamb_after.fund_cease == default_pool_num() * 0.7


def test_BeliefUnit_cashout_Sets_kegunit_fund_onset_fund_cease_Scenario2_DifferentOrderOfKegs():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_beliefunit = beliefunit_shop("Yao", tally=10)

    auto_str = "auto"
    auto_rope = yao_beliefunit.make_l1_rope(auto_str)
    auto_keg = kegunit_shop(auto_str, star=10)
    yao_beliefunit.set_l1_keg(auto_keg)

    yarn_str = "yarn"
    yarn_rope = yao_beliefunit.make_l1_rope(yarn_str)
    yarn_keg = kegunit_shop(yarn_str, star=60)
    yao_beliefunit.set_l1_keg(yarn_keg)
    lamb_str = "lambs"
    lamb_rope = yao_beliefunit.make_rope(yarn_rope, lamb_str)
    lamb_keg = kegunit_shop(lamb_str, star=1)
    yao_beliefunit.set_keg_obj(lamb_keg, parent_rope=yarn_rope)
    duck_str = "ducks"
    duck_rope = yao_beliefunit.make_rope(yarn_rope, duck_str)
    duck_keg = kegunit_shop(duck_str, star=2)
    yao_beliefunit.set_keg_obj(duck_keg, parent_rope=yarn_rope)

    coal_str = "coal"
    coal_rope = yao_beliefunit.make_l1_rope(coal_str)
    coal_keg = kegunit_shop(coal_str, star=30)
    yao_beliefunit.set_l1_keg(coal_keg)

    assert yao_beliefunit.kegroot.fund_onset is None
    assert yao_beliefunit.kegroot.fund_cease is None
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_onset is None
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_cease is None
    assert yao_beliefunit.get_keg_obj(yarn_rope).fund_onset is None
    assert yao_beliefunit.get_keg_obj(yarn_rope).fund_cease is None
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_onset is None
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_cease is None
    lamb_before = yao_beliefunit.get_keg_obj(rope=lamb_rope)
    assert lamb_before.fund_onset is None
    assert lamb_before.fund_cease is None
    duck_before = yao_beliefunit.get_keg_obj(rope=duck_rope)
    assert duck_before.fund_onset is None
    assert duck_before.fund_cease is None

    # WHEN
    yao_beliefunit.cashout()

    # THEN
    assert yao_beliefunit.kegroot.fund_onset == 0.0
    assert yao_beliefunit.kegroot.fund_cease == default_pool_num()
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_onset == 0.0
    assert yao_beliefunit.get_keg_obj(auto_rope).fund_cease == default_pool_num() * 0.1
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_onset == default_pool_num() * 0.1
    assert yao_beliefunit.get_keg_obj(coal_rope).fund_cease == default_pool_num() * 0.4
    assert yao_beliefunit.get_keg_obj(yarn_rope).fund_onset == default_pool_num() * 0.4
    assert yao_beliefunit.get_keg_obj(yarn_rope).fund_cease == default_pool_num() * 1.0

    duck_after = yao_beliefunit.get_keg_obj(rope=duck_rope)
    assert duck_after.fund_onset == default_pool_num() * 0.4
    assert duck_after.fund_cease == default_pool_num() * 0.8
    lamb_after = yao_beliefunit.get_keg_obj(rope=lamb_rope)
    assert lamb_after.fund_onset == default_pool_num() * 0.8
    assert lamb_after.fund_cease == default_pool_num() * 1.0


def test_BeliefUnit_cashout_Sets_fund_ratio_WithSomeKegsOfZero_starScenario0():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_belief.make_rope(casa_rope, floor_str)
    floor_keg = kegunit_shop(floor_str, pledge=True)
    sue_belief.set_keg_obj(floor_keg, casa_rope)
    sue_belief.set_l1_keg(kegunit_shop("unimportant"))

    situation_str = "cleaniness situation"
    situation_rope = sue_belief.make_rope(casa_rope, situation_str)
    sue_belief.set_keg_obj(kegunit_shop(situation_str, star=0), casa_rope)

    non_str = "not clean"
    yes_str = "yes clean"
    non_rope = sue_belief.make_rope(situation_rope, non_str)
    yes_rope = sue_belief.make_rope(situation_rope, yes_str)
    sue_belief.set_keg_obj(kegunit_shop(non_str), situation_rope)
    sue_belief.set_keg_obj(kegunit_shop(yes_str, star=2), situation_rope)

    assert sue_belief.kegroot.fund_ratio is None
    assert sue_belief.get_keg_obj(casa_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(floor_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(situation_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(non_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(yes_rope).fund_ratio is None

    # WHEN
    sue_belief.cashout()

    # THEN
    print(f"{sue_belief.fund_pool=}")
    assert sue_belief.kegroot.fund_ratio == 1
    assert sue_belief.get_keg_obj(casa_rope).fund_ratio == 0.5
    assert sue_belief.get_keg_obj(floor_rope).fund_ratio == 0.5
    assert sue_belief.get_keg_obj(situation_rope).fund_ratio == 0.0
    assert sue_belief.get_keg_obj(non_rope).fund_ratio == 0.0
    assert sue_belief.get_keg_obj(yes_rope).fund_ratio == 0.0


def test_BeliefUnit_cashout_Sets_fund_ratio_WithSomeKegsOfZero_starScenario1():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_belief.make_rope(casa_rope, floor_str)
    floor_keg = kegunit_shop(floor_str, pledge=True)
    sue_belief.set_keg_obj(floor_keg, casa_rope)
    sue_belief.set_l1_keg(kegunit_shop("unimportant"))

    situation_str = "cleaniness situation"
    situation_rope = sue_belief.make_rope(casa_rope, situation_str)
    sue_belief.set_keg_obj(kegunit_shop(situation_str), casa_rope)

    situation_keg = sue_belief.get_keg_obj(situation_rope)
    print(f"{situation_keg.star=}")
    print("This should raise error: 'Kegunit._'")

    clean_rope = sue_belief.make_rope(situation_rope, exx.clean)
    very_str = "very_much"
    mod_str = "moderately"
    dirty_str = "dirty"

    sue_belief.set_keg_obj(kegunit_shop(exx.clean, star=0), situation_rope)
    sue_belief.set_keg_obj(kegunit_shop(very_str), clean_rope)
    sue_belief.set_keg_obj(kegunit_shop(mod_str, star=2), clean_rope)
    sue_belief.set_keg_obj(kegunit_shop(dirty_str), clean_rope)

    very_rope = sue_belief.make_rope(clean_rope, very_str)
    mod_rope = sue_belief.make_rope(clean_rope, mod_str)
    dirty_rope = sue_belief.make_rope(clean_rope, dirty_str)
    assert sue_belief.get_keg_obj(casa_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(floor_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(situation_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(clean_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(very_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(mod_rope).fund_ratio is None
    assert sue_belief.get_keg_obj(dirty_rope).fund_ratio is None

    # WHEN
    sue_belief.cashout()

    # THEN
    print(f"{sue_belief.fund_pool=}")
    assert sue_belief.get_keg_obj(casa_rope).fund_ratio == 0.5
    assert sue_belief.get_keg_obj(floor_rope).fund_ratio == 0.25
    assert sue_belief.get_keg_obj(situation_rope).fund_ratio == 0.25
    assert sue_belief.get_keg_obj(clean_rope).fund_ratio == 0
    assert sue_belief.get_keg_obj(very_rope).fund_ratio == 0
    assert sue_belief.get_keg_obj(mod_rope).fund_ratio == 0
    assert sue_belief.get_keg_obj(dirty_rope).fund_ratio == 0


def test_BeliefUnit_cashout_WhenKegUnitHasFundsBut_kidsHaveNostarDistributeFundsToVoiceUnits_Scenario0():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    sue_beliefunit.add_voiceunit(exx.yao)
    casa_rope = sue_beliefunit.make_l1_rope(exx.casa)
    casa_keg = kegunit_shop(exx.casa, star=1)

    swim_rope = sue_beliefunit.make_rope(casa_rope, exx.swim)
    swim_keg = kegunit_shop(exx.swim, star=8)

    clean_str = "cleaning"
    clean_rope = sue_beliefunit.make_rope(casa_rope, clean_str)
    clean_keg = kegunit_shop(clean_str, star=2)
    sue_beliefunit.set_keg_obj(kegunit_shop(clean_str), casa_rope)

    sweep_str = "sweep"
    sweep_rope = sue_beliefunit.make_rope(clean_rope, sweep_str)
    sweep_keg = kegunit_shop(sweep_str, star=0)
    vacuum_str = "vacuum"
    vacuum_rope = sue_beliefunit.make_rope(clean_rope, vacuum_str)
    vacuum_keg = kegunit_shop(vacuum_str, star=0)

    sue_beliefunit.set_l1_keg(casa_keg)
    sue_beliefunit.set_keg_obj(swim_keg, casa_rope)
    sue_beliefunit.set_keg_obj(clean_keg, casa_rope)
    sue_beliefunit.set_keg_obj(sweep_keg, clean_rope)  # _star=0
    sue_beliefunit.set_keg_obj(vacuum_keg, clean_rope)  # _star=0

    assert sue_beliefunit.get_keg_obj(casa_rope).fund_ratio is None
    assert sue_beliefunit.get_keg_obj(swim_rope).fund_ratio is None
    assert sue_beliefunit.get_keg_obj(clean_rope).fund_ratio is None
    assert sue_beliefunit.get_keg_obj(sweep_rope).fund_ratio is None
    assert sue_beliefunit.get_keg_obj(vacuum_rope).fund_ratio is None
    assert sue_beliefunit.get_groupunit(exx.yao) is None

    assert not sue_beliefunit.offtrack_fund
    assert sue_beliefunit.get_voice(exx.yao).fund_give == 0
    assert sue_beliefunit.get_voice(exx.yao).fund_take == 0

    # WHEN
    sue_beliefunit.cashout()

    # THEN
    print(f"{sue_beliefunit.fund_pool=}")
    clean_fund_ratio = 0.2
    assert sue_beliefunit.get_keg_obj(casa_rope).fund_ratio == 1
    assert sue_beliefunit.get_keg_obj(swim_rope).fund_ratio == 0.8
    assert sue_beliefunit.get_keg_obj(clean_rope).fund_ratio == clean_fund_ratio
    assert sue_beliefunit.get_keg_obj(sweep_rope).fund_ratio == 0
    assert sue_beliefunit.get_keg_obj(vacuum_rope).fund_ratio == 0
    assert sue_beliefunit.get_groupunit(exx.yao).fund_give == 0
    assert sue_beliefunit.get_groupunit(exx.yao).fund_take == 0

    assert sue_beliefunit.offtrack_fund == clean_fund_ratio * default_pool_num()
    assert sue_beliefunit.get_voice(exx.yao).fund_give == default_pool_num()
    assert sue_beliefunit.get_voice(exx.yao).fund_take == default_pool_num()


def test_BeliefUnit_cashout_TreeTraverseSetsAwardLine_fundFromRoot():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.cashout()
    # keg tree has no awardunits
    assert sue_belief.kegroot.awardlines == {}
    wk_str = "sem_jours"
    nation_str = "nation"
    sue_awardunit = awardunit_shop(awardee_title=exx.sue)
    sue_belief.add_voiceunit(voice_name=exx.sue)
    sue_belief.kegroot.set_awardunit(awardunit=sue_awardunit)
    # keg tree has awardlines
    assert sue_belief.kegroot.awardheirs.get(exx.sue) is None

    # WHEN
    sue_belief.cashout()

    # THEN
    assert sue_belief.kegroot.awardheirs.get(exx.sue) is not None
    assert sue_belief.kegroot.awardheirs.get(exx.sue).awardee_title == exx.sue
    assert sue_belief.kegroot.awardlines != {}
    root_rope = to_rope(sue_belief.kegroot.keg_label)
    root_keg = sue_belief.get_keg_obj(rope=root_rope)
    sue_awardline = sue_belief.kegroot.awardlines.get(exx.sue)
    print(f"{sue_awardline.fund_give=} {root_keg.fund_ratio=} ")
    print(f"  {sue_awardline.fund_take=} {root_keg.fund_ratio=} ")
    sum_x = 0
    cat_rope = sue_belief.make_l1_rope("cat have dinner")
    cat_keg = sue_belief.get_keg_obj(cat_rope)
    wk_rope = sue_belief.make_l1_rope(wk_str)
    wk_keg = sue_belief.get_keg_obj(wk_rope)
    casa_rope = sue_belief.make_l1_rope(exx.casa)
    casa_keg = sue_belief.get_keg_obj(casa_rope)
    nation_rope = sue_belief.make_l1_rope(nation_str)
    nation_keg = sue_belief.get_keg_obj(nation_rope)
    sum_x = cat_keg.fund_ratio
    print(f"{cat_keg.fund_ratio=} {sum_x} ")
    sum_x += wk_keg.fund_ratio
    print(f"{wk_keg.fund_ratio=} {sum_x} ")
    sum_x += casa_keg.fund_ratio
    print(f"{casa_keg.fund_ratio=} {sum_x} ")
    sum_x += nation_keg.fund_ratio
    print(f"{nation_keg.fund_ratio=} {sum_x} ")
    tolerance = 1e-10
    assert sum_x < 1.0 + tolerance

    # for kid_keg in root_keg.kids.values():
    #     sum_x += kid_keg.fund_ratio
    #     print(f"  {kid_keg.fund_ratio=} {sum_x=} {kid_keg.get_keg_rope()=}")
    assert round(sue_awardline.fund_give, 15) == default_pool_num()
    assert round(sue_awardline.fund_take, 15) == default_pool_num()
    x_awardline = awardline_shop(exx.sue, default_pool_num(), default_pool_num())
    assert sue_belief.kegroot.awardlines == {x_awardline.awardee_title: x_awardline}


def test_BeliefUnit_cashout_TreeTraverseSets_awardlines_ToRootKegUnitFromNon_RootKegUnit():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sue_belief.cashout()
    sue_belief.add_voiceunit(exx.sue)
    casa_rope = sue_belief.make_l1_rope("casa")
    sue_belief.get_keg_obj(casa_rope).set_awardunit(
        awardunit_shop(awardee_title=exx.sue)
    )
    assert sue_belief.kegroot.awardlines == {}

    # WHEN
    sue_belief.cashout()

    # THEN
    assert sue_belief.kegroot.awardlines != {}
    print(f"{sue_belief.kegroot.awardlines=}")
    x_awardline = awardline_shop(
        awardee_title=exx.sue,
        fund_give=0.230769231 * default_pool_num(),
        fund_take=0.230769231 * default_pool_num(),
    )
    assert sue_belief.kegroot.awardlines == {x_awardline.awardee_title: x_awardline}
    casa_kegunit = sue_belief.get_keg_obj(casa_rope)
    assert casa_kegunit.awardlines != {}
    assert casa_kegunit.awardlines == {x_awardline.awardee_title: x_awardline}


def test_BeliefUnit_cashout_WithRootLevelAwardUnitSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    sue_belief = beliefunit_shop(exx.sue)
    sue_belief.set_voiceunit(voiceunit_shop(exx.yao))
    sue_belief.set_voiceunit(voiceunit_shop(exx.zia))
    sue_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    root_rope = to_rope(sue_belief.kegroot.keg_label)
    x_kegroot = sue_belief.get_keg_obj(root_rope)
    x_kegroot.set_awardunit(awardunit=yao_awardunit)
    x_kegroot.set_awardunit(awardunit=zia_awardunit)
    x_kegroot.set_awardunit(awardunit=xio_awardunit)
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 3

    # WHEN
    sue_belief.cashout()

    # THEN
    yao_groupunit = sue_belief.get_groupunit(exx.yao)
    zia_groupunit = sue_belief.get_groupunit(exx.zia)
    xio_groupunit = sue_belief.get_groupunit(exx.xio)
    assert yao_groupunit.fund_give == 0.5 * default_pool_num()
    assert yao_groupunit.fund_take == 0.75 * default_pool_num()
    assert zia_groupunit.fund_give == 0.25 * default_pool_num()
    assert zia_groupunit.fund_take == 0.125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.25 * default_pool_num()
    assert xio_groupunit.fund_take == 0.125 * default_pool_num()
    cred_sum1 = yao_groupunit.fund_give
    cred_sum1 += zia_groupunit.fund_give + xio_groupunit.fund_give
    assert cred_sum1 == 1 * default_pool_num()
    debt_sum1 = yao_groupunit.fund_take
    debt_sum1 += zia_groupunit.fund_take + xio_groupunit.fund_take
    assert debt_sum1 == 1 * default_pool_num()

    # ESTABLISH
    sue_belief.set_voiceunit(voiceunit_shop(exx.sue))
    sue_awardunit = awardunit_shop(exx.sue, give_force=37)
    x_kegroot.set_awardunit(sue_awardunit)
    assert len(x_kegroot.awardunits) == 4
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 4

    # WHEN
    sue_belief.cashout()

    # THEN
    yao_groupunit = sue_belief.get_groupunit(exx.yao)
    zia_groupunit = sue_belief.get_groupunit(exx.zia)
    xio_groupunit = sue_belief.get_groupunit(exx.xio)
    sue_groupunit = sue_belief.get_groupunit(exx.sue)
    assert yao_groupunit.fund_give != 0.5 * default_pool_num()
    assert yao_groupunit.fund_take != 0.75 * default_pool_num()
    assert zia_groupunit.fund_give != 0.25 * default_pool_num()
    assert zia_groupunit.fund_take != 0.125 * default_pool_num()
    assert xio_groupunit.fund_give != 0.25 * default_pool_num()
    assert xio_groupunit.fund_take != 0.125 * default_pool_num()
    assert sue_groupunit.fund_give is not None
    assert sue_groupunit.fund_take is not None
    cred_sum1 = yao_groupunit.fund_give + zia_groupunit.fund_give
    cred_sum1 += xio_groupunit.fund_give + sue_groupunit.fund_give
    assert cred_sum1 == 1 * default_pool_num()
    debt_sum1 = yao_groupunit.fund_take + zia_groupunit.fund_take
    debt_sum1 += xio_groupunit.fund_take + sue_groupunit.fund_take
    assert round(debt_sum1) == 1 * default_pool_num()


def test_BeliefUnit_cashout_WithLevel3AwardUnitSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    x_belief = beliefunit_shop(exx.bob)
    swim_rope = x_belief.make_l1_rope(exx.swim)
    x_belief.set_l1_keg(kegunit_shop(exx.swim))

    x_belief.set_voiceunit(voiceunit_shop(exx.yao))
    x_belief.set_voiceunit(voiceunit_shop(exx.zia))
    x_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    swim_keg = x_belief.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(yao_awardunit)
    swim_keg.set_awardunit(zia_awardunit)
    swim_keg.set_awardunit(xio_awardunit)
    assert len(x_belief.get_voiceunit_group_titles_dict()) == 3

    # WHEN
    x_belief.cashout()

    # THEN
    yao_groupunit = x_belief.get_groupunit(exx.yao)
    zia_groupunit = x_belief.get_groupunit(exx.zia)
    xio_groupunit = x_belief.get_groupunit(exx.xio)
    assert yao_groupunit.fund_give == 0.5 * default_pool_num()
    assert yao_groupunit.fund_take == 0.75 * default_pool_num()
    assert zia_groupunit.fund_give == 0.25 * default_pool_num()
    assert zia_groupunit.fund_take == 0.125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.25 * default_pool_num()
    assert xio_groupunit.fund_take == 0.125 * default_pool_num()
    groupunit_fund_give_sum = (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_pool_num()
    assert groupunit_fund_take_sum == 1 * default_pool_num()


def test_BeliefUnit_cashout_CreatesNewGroupUnitAndSetsGroup_fund_give_fund_take():
    # ESTABLISH
    x_belief = beliefunit_shop(exx.yao)
    swim_rope = x_belief.make_l1_rope(exx.swim)
    x_belief.set_l1_keg(kegunit_shop(exx.swim))

    x_belief.set_voiceunit(voiceunit_shop(exx.yao))
    x_belief.set_voiceunit(voiceunit_shop(exx.zia))
    # x_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    swim_keg = x_belief.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(yao_awardunit)
    swim_keg.set_awardunit(zia_awardunit)
    swim_keg.set_awardunit(xio_awardunit)
    assert len(x_belief.get_voiceunit_group_titles_dict()) == 2

    # WHEN
    x_belief.cashout()

    # THEN
    yao_groupunit = x_belief.get_groupunit(exx.yao)
    zia_groupunit = x_belief.get_groupunit(exx.zia)
    xio_groupunit = x_belief.get_groupunit(exx.xio)
    assert len(x_belief.get_voiceunit_group_titles_dict()) != len(x_belief.groupunits)
    assert yao_groupunit.fund_give == 0.5 * default_pool_num()
    assert yao_groupunit.fund_take == 0.75 * default_pool_num()
    assert zia_groupunit.fund_give == 0.25 * default_pool_num()
    assert zia_groupunit.fund_take == 0.125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.25 * default_pool_num()
    assert xio_groupunit.fund_take == 0.125 * default_pool_num()
    groupunit_fund_give_sum = (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
    )
    groupunit_fund_take_sum = (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
    )
    assert groupunit_fund_give_sum == 1 * default_pool_num()
    assert groupunit_fund_take_sum == 1 * default_pool_num()


def test_BeliefUnit_cashout_WithLevel3AwardUnitAndEmptyAncestorsSetsGroupUnit_fund_give_fund_take():
    # ESTABLISH
    x_belief = beliefunit_shop(exx.yao)
    swim_rope = x_belief.make_l1_rope(exx.swim)
    x_belief.set_l1_keg(kegunit_shop(exx.swim))

    x_belief.set_voiceunit(voiceunit_shop(exx.yao))
    x_belief.set_voiceunit(voiceunit_shop(exx.zia))
    x_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    swim_keg = x_belief.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(yao_awardunit)
    swim_keg.set_awardunit(zia_awardunit)
    swim_keg.set_awardunit(xio_awardunit)

    # no awardunits attached to this one
    x_belief.set_l1_keg(kegunit_shop("hunt", star=3))

    # WHEN
    x_belief.cashout()

    # THEN
    x_kegroot = x_belief.get_keg_obj(x_belief.kegroot.get_keg_rope())
    with pytest_raises(Exception) as excinfo:
        x_kegroot.awardunits[str(exx.yao)]
    print(f"{excinfo.value=}")
    assert str(excinfo.value) == f"'{exx.yao}'"
    with pytest_raises(Exception) as excinfo:
        x_kegroot.awardunits[str(exx.zia)]
    assert str(excinfo.value) == f"'{exx.zia}'"
    with pytest_raises(Exception) as excinfo:
        x_kegroot.awardunits[str(exx.xio)]
    assert str(excinfo.value) == f"'{exx.xio}'"
    with pytest_raises(Exception) as excinfo:
        x_kegroot.kids["hunt"].awardheirs[str(exx.yao)]
    assert str(excinfo.value) == f"'{exx.yao}'"
    with pytest_raises(Exception) as excinfo:
        x_kegroot.kids["hunt"].awardheirs[str(exx.zia)]
    assert str(excinfo.value) == f"'{exx.zia}'"
    with pytest_raises(Exception) as excinfo:
        x_kegroot.kids["hunt"].awardheirs[str(exx.xio)]
    assert str(excinfo.value) == f"'{exx.xio}'"

    # THEN
    yao_groupunit = x_belief.get_groupunit(exx.yao)
    zia_groupunit = x_belief.get_groupunit(exx.zia)
    xio_groupunit = x_belief.get_groupunit(exx.xio)
    assert yao_groupunit.fund_give == 0.125 * default_pool_num()
    assert yao_groupunit.fund_take == 0.1875 * default_pool_num()
    assert zia_groupunit.fund_give == 0.0625 * default_pool_num()
    assert zia_groupunit.fund_take == 0.03125 * default_pool_num()
    assert xio_groupunit.fund_give == 0.0625 * default_pool_num()
    assert xio_groupunit.fund_take == 0.03125 * default_pool_num()
    assert (
        yao_groupunit.fund_give + zia_groupunit.fund_give + xio_groupunit.fund_give
        == 0.25 * default_pool_num()
    )
    assert (
        yao_groupunit.fund_take + zia_groupunit.fund_take + xio_groupunit.fund_take
        == 0.25 * default_pool_num()
    )


def test_BeliefUnit_set_awardunit_CalculatesInheritedAwardUnitBeliefFund():
    # ESTABLISH
    sue_belief = beliefunit_shop(exx.sue)
    sue_belief.set_voiceunit(voiceunit_shop(exx.yao))
    sue_belief.set_voiceunit(voiceunit_shop(exx.zia))
    sue_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    Xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    sue_belief.kegroot.set_awardunit(yao_awardunit)
    sue_belief.kegroot.set_awardunit(zia_awardunit)
    sue_belief.kegroot.set_awardunit(Xio_awardunit)
    assert len(sue_belief.kegroot.awardunits) == 3

    # WHEN
    keg_dict = sue_belief.get_keg_dict()

    # THEN
    print(f"{keg_dict.keys()=}")
    keg_bob = keg_dict.get(sue_belief.kegroot.get_keg_rope())
    assert len(keg_bob.awardheirs) == 3

    bheir_yao = keg_bob.awardheirs.get(exx.yao)
    bheir_zia = keg_bob.awardheirs.get(exx.zia)
    bheir_Xio = keg_bob.awardheirs.get(exx.xio)
    assert bheir_yao.fund_give == 0.5 * default_pool_num()
    assert bheir_yao.fund_take == 0.75 * default_pool_num()
    assert bheir_zia.fund_give == 0.25 * default_pool_num()
    assert bheir_zia.fund_take == 0.125 * default_pool_num()
    assert bheir_Xio.fund_give == 0.25 * default_pool_num()
    assert bheir_Xio.fund_take == 0.125 * default_pool_num()
    assert (
        bheir_yao.fund_give + bheir_zia.fund_give + bheir_Xio.fund_give
        == 1 * default_pool_num()
    )
    assert (
        bheir_yao.fund_take + bheir_zia.fund_take + bheir_Xio.fund_take
        == 1 * default_pool_num()
    )

    # fund_give_sum = 0
    # fund_take_sum = 0
    # for group in x_belief.kegroot.awardheirs.values():
    #     print(f"{group=}")
    #     assert group.fund_give is not None
    #     assert group.fund_give in [0.25, 0.5]
    #     assert group.fund_take is not None
    #     assert group.fund_take in [0.75, 0.125]
    #     fund_give_sum += group.fund_give
    #     fund_take_sum += group.fund_take

    # assert fund_give_sum == 1
    # assert fund_take_sum == 1


def test_BeliefUnit_cashout_SetsGroupLinkBeliefCredAndDebt():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    yao_belief.set_voiceunit(voiceunit_shop(exx.sue))
    yao_belief.set_voiceunit(voiceunit_shop(exx.bob))
    yao_belief.set_voiceunit(voiceunit_shop(exx.zia))
    sue_awardunit = awardunit_shop(exx.sue, 20, take_force=40)
    bob_awardunit = awardunit_shop(exx.bob, 10, take_force=5)
    zia_awardunit = awardunit_shop(exx.zia, 10, take_force=5)
    root_rope = yao_belief.kegroot.get_keg_rope()
    yao_belief.edit_keg_attr(root_rope, awardunit=sue_awardunit)
    yao_belief.edit_keg_attr(root_rope, awardunit=bob_awardunit)
    yao_belief.edit_keg_attr(root_rope, awardunit=zia_awardunit)

    sue_voiceunit = yao_belief.get_voice(exx.sue)
    bob_voiceunit = yao_belief.get_voice(exx.bob)
    zia_voiceunit = yao_belief.get_voice(exx.zia)
    sue_sue_membership = sue_voiceunit.get_membership(exx.sue)
    bob_bob_membership = bob_voiceunit.get_membership(exx.bob)
    zia_zia_membership = zia_voiceunit.get_membership(exx.zia)
    assert sue_sue_membership.fund_give is None
    assert sue_sue_membership.fund_take is None
    assert bob_bob_membership.fund_give is None
    assert bob_bob_membership.fund_take is None
    assert zia_zia_membership.fund_give is None
    assert zia_zia_membership.fund_take is None

    # WHEN
    yao_belief.cashout()

    # THEN
    assert sue_sue_membership.fund_give == 0.5 * default_pool_num()
    assert sue_sue_membership.fund_take == 0.8 * default_pool_num()
    assert bob_bob_membership.fund_give == 0.25 * default_pool_num()
    assert bob_bob_membership.fund_take == 0.1 * default_pool_num()
    assert zia_zia_membership.fund_give == 0.25 * default_pool_num()
    assert zia_zia_membership.fund_take == 0.1 * default_pool_num()

    membership_cred_sum = (
        sue_sue_membership.fund_give
        + bob_bob_membership.fund_give
        + zia_zia_membership.fund_give
    )
    assert membership_cred_sum == 1.0 * default_pool_num()
    membership_debt_sum = (
        sue_sue_membership.fund_take
        + bob_bob_membership.fund_take
        + zia_zia_membership.fund_take
    )
    assert membership_debt_sum == 1.0 * default_pool_num()

    # ESTABLISH another pledge, check metrics are as expected
    yao_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_belief.kegroot.set_awardunit(awardunit_shop(exx.xio, 20, take_force=13))

    # WHEN
    yao_belief.cashout()

    # THEN
    xio_groupunit = yao_belief.get_groupunit(exx.xio)
    xio_xio_membership = xio_groupunit.get_voice_membership(exx.xio)
    sue_voiceunit = yao_belief.get_voice(exx.sue)
    bob_voiceunit = yao_belief.get_voice(exx.bob)
    zia_voiceunit = yao_belief.get_voice(exx.zia)
    sue_sue_membership = sue_voiceunit.get_membership(exx.sue)
    bob_bob_membership = bob_voiceunit.get_membership(exx.bob)
    zia_zia_membership = zia_voiceunit.get_membership(exx.zia)
    assert sue_sue_membership.fund_give != 0.25 * default_pool_num()
    assert sue_sue_membership.fund_take != 0.8 * default_pool_num()
    assert bob_bob_membership.fund_give != 0.25 * default_pool_num()
    assert bob_bob_membership.fund_take != 0.1 * default_pool_num()
    assert zia_zia_membership.fund_give != 0.5 * default_pool_num()
    assert zia_zia_membership.fund_take != 0.1 * default_pool_num()
    assert xio_xio_membership.fund_give is not None
    assert xio_xio_membership.fund_take is not None

    x_fund_give_sum = (
        sue_sue_membership.fund_give
        + bob_bob_membership.fund_give
        + zia_zia_membership.fund_give
        + xio_xio_membership.fund_give
    )
    print(f"{x_fund_give_sum=}")
    assert x_fund_give_sum == 1.0 * default_pool_num()
    x_fund_take_sum = (
        sue_sue_membership.fund_take
        + bob_bob_membership.fund_take
        + zia_zia_membership.fund_take
        + xio_xio_membership.fund_take
    )
    assert x_fund_take_sum == 1.0 * default_pool_num()


def test_BeliefUnit_cashout_SetsVoiceUnitBelief_fund():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    swim_rope = yao_belief.make_l1_rope(exx.swim)
    yao_belief.set_l1_keg(kegunit_shop(exx.swim))
    yao_belief.set_voiceunit(voiceunit_shop(exx.sue))
    yao_belief.set_voiceunit(voiceunit_shop(exx.bob))
    yao_belief.set_voiceunit(voiceunit_shop(exx.zia))
    bl_sue = awardunit_shop(exx.sue, 20, take_force=40)
    bl_bob = awardunit_shop(exx.bob, 10, take_force=5)
    bl_zia = awardunit_shop(exx.zia, 10, take_force=5)
    yao_belief.get_keg_obj(swim_rope).set_awardunit(bl_sue)
    yao_belief.get_keg_obj(swim_rope).set_awardunit(bl_bob)
    yao_belief.get_keg_obj(swim_rope).set_awardunit(bl_zia)

    sue_voiceunit = yao_belief.get_voice(exx.sue)
    bob_voiceunit = yao_belief.get_voice(exx.bob)
    zia_voiceunit = yao_belief.get_voice(exx.zia)

    assert sue_voiceunit.fund_give == 0
    assert sue_voiceunit.fund_take == 0
    assert bob_voiceunit.fund_give == 0
    assert bob_voiceunit.fund_take == 0
    assert zia_voiceunit.fund_give == 0
    assert zia_voiceunit.fund_take == 0

    # WHEN
    yao_belief.cashout()

    # THEN
    assert sue_voiceunit.fund_give == 0.5 * default_pool_num()
    assert sue_voiceunit.fund_take == 0.8 * default_pool_num()
    assert bob_voiceunit.fund_give == 0.25 * default_pool_num()
    assert bob_voiceunit.fund_take == 0.1 * default_pool_num()
    assert zia_voiceunit.fund_give == 0.25 * default_pool_num()
    assert zia_voiceunit.fund_take == 0.1 * default_pool_num()

    assert (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
        == 1.0 * default_pool_num()
    )
    assert (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
        == 1.0 * default_pool_num()
    )

    # WHEN another pledge, check metrics are as expected
    yao_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_belief.kegroot.set_awardunit(awardunit_shop(exx.xio, 20, take_force=10))
    yao_belief.cashout()

    # THEN
    xio_voiceunit = yao_belief.get_voice(exx.xio)

    assert sue_voiceunit.fund_give != 0.5 * default_pool_num()
    assert sue_voiceunit.fund_take != 0.8 * default_pool_num()
    assert bob_voiceunit.fund_give != 0.25 * default_pool_num()
    assert bob_voiceunit.fund_take != 0.1 * default_pool_num()
    assert zia_voiceunit.fund_give != 0.25 * default_pool_num()
    assert zia_voiceunit.fund_take != 0.1 * default_pool_num()
    assert xio_voiceunit.fund_give is not None
    assert xio_voiceunit.fund_take is not None

    sum_voiceunit_fund_give = (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
    )
    assert sum_voiceunit_fund_give < 1.0 * default_pool_num()
    assert (
        sue_voiceunit.fund_give
        + bob_voiceunit.fund_give
        + zia_voiceunit.fund_give
        + xio_voiceunit.fund_give
        == 1.0 * default_pool_num()
    )
    assert (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
        < 1.0 * default_pool_num()
    )
    assert (
        sue_voiceunit.fund_take
        + bob_voiceunit.fund_take
        + zia_voiceunit.fund_take
        + xio_voiceunit.fund_take
        == 1.0 * default_pool_num()
    )


def test_BeliefUnit_cashout_SetsPartGroupedLWVoiceUnitBelief_fund():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    swim_rope = yao_belief.make_l1_rope(exx.swim)
    yao_belief.set_l1_keg(kegunit_shop(exx.swim))
    yao_belief.set_voiceunit(voiceunit_shop(exx.sue))
    yao_belief.set_voiceunit(voiceunit_shop(exx.bob))
    yao_belief.set_voiceunit(voiceunit_shop(exx.zia))
    sue_awardunit = awardunit_shop(exx.sue, 20, take_force=40)
    bob_awardunit = awardunit_shop(exx.bob, 10, take_force=5)
    zia_awardunit = awardunit_shop(exx.zia, 10, take_force=5)
    swim_keg = yao_belief.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(sue_awardunit)
    swim_keg.set_awardunit(bob_awardunit)
    swim_keg.set_awardunit(zia_awardunit)

    # no awardunits attached to this one
    hunt_str = "hunt"
    yao_belief.set_l1_keg(kegunit_shop(hunt_str, star=3))

    # WHEN
    yao_belief.cashout()

    # THEN
    sue_groupunit = yao_belief.get_groupunit(exx.sue)
    bob_groupunit = yao_belief.get_groupunit(exx.bob)
    zia_groupunit = yao_belief.get_groupunit(exx.zia)
    assert sue_groupunit.fund_give != 0.5 * default_pool_num()
    assert sue_groupunit.fund_take != 0.8 * default_pool_num()
    assert bob_groupunit.fund_give != 0.25 * default_pool_num()
    assert bob_groupunit.fund_take != 0.1 * default_pool_num()
    assert zia_groupunit.fund_give != 0.25 * default_pool_num()
    assert zia_groupunit.fund_take != 0.1 * default_pool_num()
    assert (
        sue_groupunit.fund_give + bob_groupunit.fund_give + zia_groupunit.fund_give
        == 0.25 * default_pool_num()
    )
    assert (
        sue_groupunit.fund_take + bob_groupunit.fund_take + zia_groupunit.fund_take
        == 0.25 * default_pool_num()
    )

    sue_voiceunit = yao_belief.get_voice(exx.sue)
    bob_voiceunit = yao_belief.get_voice(exx.bob)
    zia_voiceunit = yao_belief.get_voice(exx.zia)

    assert sue_voiceunit.fund_give == 0.375 * default_pool_num()
    assert sue_voiceunit.fund_take == 0.45 * default_pool_num()
    assert bob_voiceunit.fund_give == 0.3125 * default_pool_num()
    assert bob_voiceunit.fund_take == 0.275 * default_pool_num()
    assert zia_voiceunit.fund_give == 0.3125 * default_pool_num()
    assert zia_voiceunit.fund_take == 0.275 * default_pool_num()

    assert (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
        == 1.0 * default_pool_num()
    )
    assert (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
        == 1.0 * default_pool_num()
    )


def test_BeliefUnit_cashout_CreatesNewGroupUnitAndSetsVoice_fund_give_fund_take():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.bob)
    swim_rope = bob_belief.make_l1_rope(exx.swim)
    bob_belief.set_l1_keg(kegunit_shop(exx.swim))

    bob_belief.set_voiceunit(voiceunit_shop(exx.yao))
    bob_belief.set_voiceunit(voiceunit_shop(exx.zia))
    # bob_belief.set_voiceunit(voiceunit_shop(exx.xio))
    yao_awardunit = awardunit_shop(exx.yao, give_force=20, take_force=6)
    zia_awardunit = awardunit_shop(exx.zia, give_force=10, take_force=1)
    xio_awardunit = awardunit_shop(exx.xio, give_force=10)
    swim_keg = bob_belief.get_keg_obj(swim_rope)
    swim_keg.set_awardunit(yao_awardunit)
    swim_keg.set_awardunit(zia_awardunit)
    swim_keg.set_awardunit(xio_awardunit)
    assert len(bob_belief.get_voiceunit_group_titles_dict()) == 2

    # WHEN
    bob_belief.cashout()

    # THEN
    assert len(bob_belief.get_voiceunit_group_titles_dict()) != len(
        bob_belief.groupunits
    )
    assert not bob_belief.voice_exists(exx.xio)
    yao_voiceunit = bob_belief.get_voice(exx.yao)
    zia_voiceunit = bob_belief.get_voice(exx.zia)
    voiceunit_fund_give_sum = yao_voiceunit.fund_give + zia_voiceunit.fund_give
    voiceunit_fund_take_sum = yao_voiceunit.fund_take + zia_voiceunit.fund_take
    assert voiceunit_fund_give_sum == default_pool_num()
    assert voiceunit_fund_take_sum == default_pool_num()


def test_BeliefUnit_cashout_SetsVoiceUnit_fund_give_fund_take():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    yao_belief.set_l1_keg(kegunit_shop("swim"))
    yao_belief.set_voiceunit(voiceunit_shop(exx.sue, 8))
    yao_belief.set_voiceunit(voiceunit_shop(exx.bob))
    yao_belief.set_voiceunit(voiceunit_shop(exx.zia))
    sue_voiceunit = yao_belief.get_voice(exx.sue)
    bob_voiceunit = yao_belief.get_voice(exx.bob)
    zia_voiceunit = yao_belief.get_voice(exx.zia)
    assert sue_voiceunit.fund_give == 0
    assert sue_voiceunit.fund_take == 0
    assert bob_voiceunit.fund_give == 0
    assert bob_voiceunit.fund_take == 0
    assert zia_voiceunit.fund_give == 0
    assert zia_voiceunit.fund_take == 0

    # WHEN
    yao_belief.cashout()

    # THEN
    fund_give_sum = (
        sue_voiceunit.fund_give + bob_voiceunit.fund_give + zia_voiceunit.fund_give
    )
    assert fund_give_sum == 1.0 * default_pool_num()
    fund_take_sum = (
        sue_voiceunit.fund_take + bob_voiceunit.fund_take + zia_voiceunit.fund_take
    )
    assert fund_take_sum == 1.0 * default_pool_num()


def clear_all_voiceunits_groupunits_fund_agenda_give_take(x_belief: BeliefUnit):
    # delete belief_agenda_debt and belief_agenda_cred
    for x_groupunit in x_belief.groupunits.values():
        x_groupunit.clear_group_fund_give_take()
        # for membership_x in groupunit_x._voices.values():
        #     print(f"{groupunit_x.} {membership_x.}  {membership_x.fund_give:.6f} {membership_x.voice_debt_lumen=} {membership_fund_take:t:.6f} {membership_x.} ")

    # delete belief_agenda_debt and belief_agenda_cred
    for x_voiceunit in x_belief.voices.values():
        x_voiceunit.clear_fund_give_take()


@dataclass
class GroupAgendaMetrics:
    sum_groupunit_give: float = 0
    sum_groupunit_take: float = 0
    sum_membership_cred: float = 0
    sum_membership_debt: float = 0
    membership_count: int = 0

    def set_groupagendametrics_sums(self, x_belief: BeliefUnit):
        for x_groupunit in x_belief.groupunits.values():
            self.sum_groupunit_give += x_groupunit.fund_agenda_give
            self.sum_groupunit_take += x_groupunit.fund_agenda_take
            for membership_x in x_groupunit.memberships.values():
                self.sum_membership_cred += membership_x.fund_agenda_give
                self.sum_membership_debt += membership_x.fund_agenda_take
                self.membership_count += 1


@dataclass
class VoiceAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_voiceagendametrics_sums(self, x_belief: BeliefUnit):
        for voiceunit in x_belief.voices.values():
            self.sum_agenda_cred += voiceunit.fund_agenda_give
            self.sum_agenda_debt += voiceunit.fund_agenda_take
            self.sum_agenda_ratio_cred += voiceunit.fund_agenda_ratio_give
            self.sum_agenda_ratio_debt += voiceunit.fund_agenda_ratio_take


@dataclass
class AwardAgendaMetrics:
    sum_belief_agenda_kegs_fund_total = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_belief_i_sum = 0
    agenda_yes_belief_i_sum = 0

    def set_awardagendametrics_sums(self, agenda_dict: dict[RopeTerm, KegUnit]):
        for agenda_keg in agenda_dict.values():
            self.sum_belief_agenda_kegs_fund_total += agenda_keg.get_keg_fund_total()
            if agenda_keg.awardlines == {}:
                self.agenda_no_count += 1
                self.agenda_no_belief_i_sum += agenda_keg.get_keg_fund_total()
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_belief_i_sum += agenda_keg.get_keg_fund_total()


def test_BeliefUnit_agenda_cred_debt_SetAttrs():
    # ESTABLISH
    yao_belief = beliefunit_v001_with_large_agenda()
    clear_all_voiceunits_groupunits_fund_agenda_give_take(yao_belief)

    # TEST belief_agenda_debt and belief_agenda_cred are empty
    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_groupagendametrics_sums(yao_belief)
    assert x_groupagendametrics.sum_groupunit_give == 0
    assert x_groupagendametrics.sum_groupunit_take == 0
    assert x_groupagendametrics.sum_membership_cred == 0
    assert x_groupagendametrics.sum_membership_debt == 0

    # TEST belief_agenda_debt and belief_agenda_cred are empty
    x_voiceagendametrics = VoiceAgendaMetrics()
    x_voiceagendametrics.set_voiceagendametrics_sums(yao_belief)
    assert x_voiceagendametrics.sum_agenda_cred == 0
    assert x_voiceagendametrics.sum_agenda_debt == 0
    assert x_voiceagendametrics.sum_agenda_ratio_cred == 0
    assert x_voiceagendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = yao_belief.get_agenda_dict()
    # for keg_rope in yao_belief._keg_dict.keys():
    #     print(f"{keg_rope=}")
    # for x_voice in yao_belief.voices.values():
    #     for x_membership in x_voice.memberships.values():
    #         print(f"{x_membership.group_title=}")

    # THEN
    print(f"{yao_belief.get_reason_contexts()=}")
    assert len(agenda_dict) == 69
    x_awardagendametrics = AwardAgendaMetrics()
    x_awardagendametrics.set_awardagendametrics_sums(agenda_dict=agenda_dict)
    # print(f"{sum_belief_agenda_kegs_fund_total=}")
    # assert x_awardagendametrics.agenda_no_count == 14
    assert x_awardagendametrics.agenda_yes_count == 49
    predicted_agenda_no_belief_i_sum = int(0.004908864 * default_pool_num())
    assert (
        x_awardagendametrics.agenda_no_belief_i_sum == predicted_agenda_no_belief_i_sum
    )
    predicted_agenda_yes_belief_i_sum = int(0.003065400 * default_pool_num())
    assert (
        x_awardagendametrics.agenda_yes_belief_i_sum
        == predicted_agenda_yes_belief_i_sum
    )
    assert are_equal(
        x_awardagendametrics.agenda_no_belief_i_sum
        + x_awardagendametrics.agenda_yes_belief_i_sum,
        x_awardagendametrics.sum_belief_agenda_kegs_fund_total,
    )
    predicted_sum_belief_agenda_kegs_fund_total = 0.007974264 * default_pool_num()
    assert (
        x_awardagendametrics.sum_belief_agenda_kegs_fund_total
        == predicted_sum_belief_agenda_kegs_fund_total
    )

    x_groupagendametrics = GroupAgendaMetrics()
    x_groupagendametrics.set_groupagendametrics_sums(yao_belief)
    assert x_groupagendametrics.membership_count == 81
    x_sum = 3065400
    print(f"{x_groupagendametrics.sum_groupunit_give=}")
    assert are_equal(x_groupagendametrics.sum_groupunit_give, x_sum)
    assert are_equal(x_groupagendametrics.sum_groupunit_take, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_cred, x_sum)
    assert are_equal(x_groupagendametrics.sum_membership_debt, x_sum)
    assert are_equal(
        x_awardagendametrics.agenda_yes_belief_i_sum,
        x_groupagendametrics.sum_groupunit_give,
    )

    assert all_voiceunits_have_legitimate_values(yao_belief)

    x_voiceagendametrics = VoiceAgendaMetrics()
    x_voiceagendametrics.set_voiceagendametrics_sums(yao_belief)
    assert are_equal(
        x_voiceagendametrics.sum_agenda_cred,
        x_awardagendametrics.sum_belief_agenda_kegs_fund_total,
    )
    assert are_equal(
        x_voiceagendametrics.sum_agenda_debt,
        x_awardagendametrics.sum_belief_agenda_kegs_fund_total,
    )
    assert are_equal(x_voiceagendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_voiceagendametrics.sum_agenda_ratio_debt, 1)

    # voiceunit_fund_give_sum = 0.0
    # voiceunit_fund_take_sum = 0.0

    # assert voiceunit_fund_give_sum == 1.0
    # assert voiceunit_fund_take_sum > 0.9999999
    # assert voiceunit_fund_take_sum < 1.00000001


def all_voiceunits_have_legitimate_values(x_belief: BeliefUnit):
    return not any(
        (
            voiceunit.fund_give is None
            or voiceunit.fund_give in [0.25, 0.5]
            or voiceunit.fund_take is None
            or voiceunit.fund_take in [0.8, 0.1]
        )
        for voiceunit in x_belief.voices.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000001
    return abs(x1 - x2) < e10


def test_BeliefUnit_cashout_SetsAttrsWhenNoFactUnitsNoReasonUnitsEmpty_agenda_ratio_cred_debt():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    sue_voiceunit = voiceunit_shop(exx.sue, 0.5, voice_debt_lumen=2)
    bob_voiceunit = voiceunit_shop(exx.bob, 1.5, voice_debt_lumen=3)
    zia_voiceunit = voiceunit_shop(exx.zia, 8, voice_debt_lumen=5)
    yao_belief.set_voiceunit(sue_voiceunit)
    yao_belief.set_voiceunit(bob_voiceunit)
    yao_belief.set_voiceunit(zia_voiceunit)
    sue_voice = yao_belief.get_voice(exx.sue)
    bob_voice = yao_belief.get_voice(exx.bob)
    zia_voice = yao_belief.get_voice(exx.zia)

    assert not sue_voice.fund_give
    assert not sue_voice.fund_take
    assert not bob_voice.fund_give
    assert not bob_voice.fund_take
    assert not zia_voice.fund_give
    assert not zia_voice.fund_take
    assert not sue_voice.fund_agenda_give
    assert not sue_voice.fund_agenda_take
    assert not bob_voice.fund_agenda_give
    assert not bob_voice.fund_agenda_take
    assert not zia_voice.fund_agenda_give
    assert not zia_voice.fund_agenda_take
    assert not sue_voice.fund_agenda_ratio_give
    assert not sue_voice.fund_agenda_ratio_take
    assert not bob_voice.fund_agenda_ratio_give
    assert not bob_voice.fund_agenda_ratio_take
    assert not zia_voice.fund_agenda_ratio_give
    assert not zia_voice.fund_agenda_ratio_take

    # WHEN
    yao_belief.cashout()

    # THEN
    assert yao_belief.reason_contexts == set()
    assert sue_voice.fund_give == 50000000
    assert sue_voice.fund_take == 200000000
    assert bob_voice.fund_give == 150000000
    assert bob_voice.fund_take == 300000000
    assert zia_voice.fund_give == 800000000
    assert zia_voice.fund_take == 500000000
    assert sue_voice.fund_agenda_give == 50000000
    assert sue_voice.fund_agenda_take == 200000000
    assert bob_voice.fund_agenda_give == 150000000
    assert bob_voice.fund_agenda_take == 300000000
    assert zia_voice.fund_agenda_give == 800000000
    assert zia_voice.fund_agenda_take == 500000000
    assert sue_voice.fund_agenda_give == sue_voice.fund_give
    assert sue_voice.fund_agenda_take == sue_voice.fund_take
    assert bob_voice.fund_agenda_give == bob_voice.fund_give
    assert bob_voice.fund_agenda_take == bob_voice.fund_take
    assert zia_voice.fund_agenda_give == zia_voice.fund_give
    assert zia_voice.fund_agenda_take == zia_voice.fund_take
    assert sue_voice.fund_agenda_ratio_give == 0.05
    assert sue_voice.fund_agenda_ratio_take == 0.2
    assert bob_voice.fund_agenda_ratio_give == 0.15
    assert bob_voice.fund_agenda_ratio_take == 0.3
    assert zia_voice.fund_agenda_ratio_give == 0.8
    assert zia_voice.fund_agenda_ratio_take == 0.5


def test_BeliefUnit_cashout_CreatesGroupUnitWith_beliefunit_v001():
    # ESTABLISH / WHEN
    yao_belief = beliefunit_v001()
    yao_belief.cashout()

    # THEN
    assert yao_belief.groupunits is not None
    assert len(yao_belief.groupunits) == 34
    everyone_voices_len = None
    everyone_group = yao_belief.get_groupunit(";Everyone")
    everyone_voices_len = len(everyone_group.memberships)
    assert everyone_voices_len == 22

    # WHEN
    yao_belief.cashout()
    keg_dict = yao_belief._keg_dict

    # THEN
    # print(f"{len(keg_dict)=}")
    db_keg = keg_dict.get(yao_belief.make_l1_rope("D&B"))
    assert len(db_keg.awardunits) == 3
    # for keg_key in keg_dict:
    #     print(f"{keg_key=}")
    #     if keg.keg_label == "D&B":
    #         print(f"{keg.keg_label=} {keg.awardunits=}")
    #         db_awardunit_len = len(keg.awardunits)
    # assert db_awardunit_len == 3
